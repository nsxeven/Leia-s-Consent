"""Title-screen Leia: touch reactions (pure logic, unit-tested; darryn 2026-11-09).

Clicking the title-screen Leia plays a voice clip, a small motion and a brief
expression, then she settles back to the face picked in Customize. Chest and
private-area clicks escalate (shy -> flustered -> Ahegao at the peak) and only
turn lewd (moans, wet sounds, chest jiggle) when 18+ options are shown. Spamming
gets a "Hey~ hands off!" pout and a short cooldown.

Coordinates are on the 941 x 1672 Leia canvas. The Ren'Py side
(systems/lc_title_touch.rpy) converts the mouse position, plays the audio and
drives the transforms from the live dict this module fills in.
"""

import math

CANVAS = (941, 1672)

# Must match `transform lc_title_leia` in screens/title_screen.rpy:
# zoom 0.74, xcenter 1470, feet (yanchor 1.0) at y 1277.
TITLE_ZOOM = 0.74
TITLE_XCENTER = 1470
TITLE_BOTTOM = 1277
TITLE_LEFT = TITLE_XCENTER - CANVAS[0] * TITLE_ZOOM / 2.0
TITLE_TOP = TITLE_BOTTOM - CANVAS[1] * TITLE_ZOOM

# Canvas rectangles (x0, y0, x1, y1), first match wins. Every outfit shares the
# same pose, so one set fits all (chest layers span ~372-704 x 407-665).
REGIONS = (
    ("chest", (360, 400, 715, 615)),
    ("private", (425, 815, 610, 965)),
    ("head", (290, 50, 630, 360)),
)
LEWD_REGIONS = ("chest", "private")

MIN_GAP = 0.25        # ignore clicks closer together than this (no audio spam)
STREAK_GAP = 2.5      # lewd clicks within this many seconds build the streak
QUICK_GAP = 0.45      # clicks this close together count as spamming
QUICK_LIMIT = 6       # this many rapid lewd clicks in a row (mashing) -> pout
COOLDOWN = 4.0        # after a pout, lewd clicks only get a silent pout
HOLD = 1.6            # seconds a reaction face stays before settling back
HOLD_PEAK = 2.6
HOLD_POUT = 2.2

POUT_LINE = "Hey~ hands off!"

WET_SOUNDS = tuple("wet%02d" % i for i in range(1, 13))


def screen_to_canvas(x, y):
    return ((x - TITLE_LEFT) / TITLE_ZOOM, (y - TITLE_TOP) / TITLE_ZOOM)


def region_at(cx, cy):
    for name, (x0, y0, x1, y1) in REGIONS:
        if x0 <= cx <= x1 and y0 <= cy <= y1:
            return name
    return "body"


def new_state():
    return {"streak": 0, "last": -99.0, "last_any": -99.0, "cool_until": -99.0, "quick": 0}


def new_live():
    return {"kind": None, "start": -99.0, "face": None, "until": -99.0, "jiggle": False,
            "bubble": None, "bubble_start": -99.0, "bubble_until": -99.0}


def _reaction(kind, face, hold, voice=None, lewd=None, lewd_vol=0.0, jiggle=False, bubble=None):
    return {"kind": kind, "face": face, "hold": hold, "voice": voice, "lewd": lewd,
            "lewd_vol": lewd_vol, "jiggle": jiggle, "bubble": bubble}


def _pout(state, now):
    state["streak"] = 0
    state["quick"] = 0
    state["cool_until"] = now + COOLDOWN
    return _reaction("shake", "pout", HOLD_POUT, voice=("sfx", "leia_grunt"), bubble=POUT_LINE)


def plan(state, region, now, mature, rnd):
    """Pick the reaction for a click on `region` at time `now`; None = ignore.

    `state` (from new_state) is updated in place. `rnd` is a random.Random-like
    object (choice/random), so tests can make it deterministic.
    """
    if now - state["last_any"] < MIN_GAP:
        return None
    state["last_any"] = now

    if region not in LEWD_REGIONS:
        if region == "head":
            r = rnd.random()
            voice = "leia_giggle" if r < 0.5 else ("leia_laugh" if r < 0.8 else "leia_kiss")
            return _reaction("tilt", rnd.choice(("smile", "shy")), HOLD, voice=("sfx", voice))
        return _reaction("hop", "smile", HOLD, voice=("sfx", "leia_giggle"))

    if now < state["cool_until"]:
        return _reaction("shake", "pout", 1.2)

    state["quick"] = state["quick"] + 1 if now - state["last"] < QUICK_GAP else 1
    state["streak"] = state["streak"] + 1 if now - state["last"] < STREAK_GAP else 1
    state["last"] = now
    level = state["streak"]

    # The ladder always reaches its peak; the click after the peak, or mashing
    # (QUICK_LIMIT rapid clicks in a row), gets the pout and the cooldown.
    peak = 4 if mature else 3
    if level > peak or state["quick"] >= QUICK_LIMIT:
        return _pout(state, now)

    if not mature:
        face = "flustered" if level >= 3 else "shy"
        voice = "leia_gasp" if level == 1 else "leia_giggle"
        return _reaction("flinch", face, HOLD, voice=("sfx", voice))

    face = {1: "shy", 2: "flustered", 3: "flustered", 4: "ahegao"}[level]
    hold = HOLD_PEAK if level == 4 else HOLD
    if region == "chest":
        voice = ("sfx", "leia_gasp") if level == 1 else ("moan", level - 1)
        return _reaction("chest", face, hold, voice=voice, jiggle=True)
    vol = (0.35, 0.5, 0.65, 0.8)[level - 1]
    return _reaction("squirm", face, hold, voice=("moan", level), lewd=rnd.choice(WET_SOUNDS),
                     lewd_vol=vol)


def apply(live, reaction, now):
    """Copy a planned reaction into the live dict the transforms read."""
    live["kind"] = reaction["kind"]
    live["start"] = now
    live["face"] = reaction["face"]
    live["until"] = now + reaction["hold"]
    live["jiggle"] = bool(reaction["jiggle"])
    if reaction["bubble"]:
        live["bubble"] = reaction["bubble"]
        live["bubble_start"] = now
        live["bubble_until"] = now + reaction["hold"]


def current_face(live, now):
    return live["face"] if live["face"] and now < live["until"] else None


def _decay(t, rate):
    return math.exp(-rate * t)


def body_offset(kind, t):
    """(xoffset, yoffset) in canvas pixels for the whole sprite, `t` s after the click."""
    if t < 0:
        return (0.0, 0.0)
    if kind == "hop":
        if t < 0.34:
            return (0.0, -22.0 * math.sin(math.pi * t / 0.34))
        if t < 0.56:
            return (0.0, 5.0 * math.sin(math.pi * (t - 0.34) / 0.22))
    elif kind == "tilt":
        if t < 1.1:
            return (9.0 * math.sin(2 * math.pi * 2.2 * t) * _decay(t, 3.0), 0.0)
    elif kind == "flinch":
        if t < 0.26:
            return (0.0, -9.0 * math.sin(math.pi * t / 0.26))
    elif kind == "chest":
        if t < 0.28:
            return (0.0, 6.0 * math.sin(math.pi * t / 0.28))
    elif kind == "squirm":
        if t < 1.3:
            y = 5.0 * math.sin(math.pi * t / 0.3) if t < 0.3 else 0.0
            return (8.0 * math.sin(2 * math.pi * 3.0 * t) * _decay(t, 2.5), y)
    elif kind == "shake":
        if t < 0.7:
            return (11.0 * math.sin(2 * math.pi * 6.0 * t) * _decay(t, 5.0), 0.0)
    return (0.0, 0.0)


def chest_offset(jiggle, t):
    """yoffset in canvas pixels for the chest layer (a damped bounce)."""
    if not jiggle or t < 0 or t > 1.4:
        return 0.0
    return 14.0 * math.sin(2 * math.pi * 4.5 * t) * _decay(t, 3.2)


def bubble_alpha(live, now):
    if not live["bubble"]:
        return 0.0
    t = now - live["bubble_start"]
    left = live["bubble_until"] - now
    if t < 0 or left <= -0.3:
        return 0.0
    if t < 0.15:
        return t / 0.15
    if left < 0:
        return max(0.0, 1.0 + left / 0.3)
    return 1.0
