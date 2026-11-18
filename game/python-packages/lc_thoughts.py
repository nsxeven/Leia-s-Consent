"""Ryan's thoughts: keep one thought at the end of a day review (pure Python, no Ren'Py import).

At the end of a day's review the game offers one *thought* per part of the day (OFFER_PARTS:
Day One = daytime, evening, night; Day Two = morning, afternoon, night), drawn only from beats the
player actually saw, plus "keep nothing". The kept thought is a save-local value that a later day reads (lc_thought_kept /
lc_thought_line in game/systems/thoughts.rpy) to tint a few `think` lines or add one reply
option. It never changes stats by itself.

Each thought has a base text and variants by lane or stat. A variant is resolved whenever the
thought is shown, so a kept thought evolves with the save: the lane variant comes first; then,
in a lane, the first of that lane's stats (LANE_STATS) over its tint bar (TINT); with no lane,
the stat furthest over its bar; else the base text.

Every text is checked against its day's script: the comment above each thought names the
label(s) it was checked against (`Source:`, tested), so an edit to either side re-checks both. A
Day Two text must hold on every path where its beat is seen (who was there differs by lane).

Texts are Ryan's inner voice (docs/characters/ryan.md, LC-Brain Characters/Ryan.md: a bit timid,
self-deprecating, plain words). They use [player_name] / [girlfriend_name] / [friend_name] and
never name a stat or route, so Immersive mode can show them as they are.

Ren'Py side: game/systems/thoughts.rpy, game/screens/thoughts_screen.rpy.
Tests: tests/test_thoughts.py. Doc: docs/THOUGHTS.md.
"""

# Lane keys a variant may use. Mapped from the stats model's lean (lane_from_lean).
LANES = ("love_lane", "exhib_lane", "ntr_lane")

_LEAN_TO_LANE = {"love": "love_lane", "love_exhib": "exhib_lane", "ntr": "ntr_lane"}

# Tint bars: a stat at or over its bar can tint a thought. Day One scale (defaults are
# Love/Trust 50, Exhibitionism/Temptation 10, Sharing 0): a few warm choices pass Love/Trust 58,
# Exhibitionism 19 is the Day One "shared glance" line (lc_stat_model d1_pool_shared_glance),
# Temptation 12 is two slips (one short of the Day One NTR seed at 13). Love and Sharing have no
# Day One variant yet (Sharing never moves on Day One): their bars are for Day Two onward.
TINT = {
    "love": 58,
    "trust": 58,
    "exhibitionism": 19,
    "sharing": 3,
    "temptation": 12,
}

# Tie-break when two stats sit equally far over their bars (saves with no lane).
STAT_PRIORITY = ("temptation", "exhibitionism", "sharing", "trust", "love")

# A lane limits which stat variants may tint it, in order of preference: the first listed stat
# over its bar wins. Love keeps its warmth (never an Exhibitionism or Temptation pull), NTR never
# reads as Love and prefers Temptation over Exhibitionism, Love + Exhibitionism never lets
# Temptation outrank Exhibitionism.
LANE_STATS = {
    "love_lane": ("love", "trust"),
    "exhib_lane": ("exhibitionism", "trust", "love", "temptation"),
    "ntr_lane": ("temptation", "exhibitionism", "trust"),
}

# Labels for the small tint stamp in Insight/Full (never shown in Immersive).
TINT_LABELS = {
    "love": "Love", "trust": "Trust", "exhibitionism": "Exhibitionism",
    "sharing": "Sharing", "temptation": "Temptation",
    "love_lane": "Love", "exhib_lane": "Love + Exhibitionism", "ntr_lane": "NTR",
}

# Beats a thought can require. test is one of:
#   ("flag", flag_id)            the story flag is set
#   ("value_set", key)           the story value exists (any value but None)
#   ("value_min", key, n)        the story value is a number >= n
BEATS = {}  # each Day's THOUGHT_BEATS in lc_days/<day>.py (added at import)

# The pool, in day order. Ids are save data once shipped: never rename one.
THOUGHT_ORDER = ()  # each Day's THOUGHT_ORDER in lc_days/<day>.py (added at import)

THOUGHTS = {}  # each Day's THOUGHTS in lc_days/<day>.py (added at import)

# One card per part of the day, in day order. Within a part the offer takes the seen thought
# this save colours most (colour_count), else the first in day order.
OFFER_PARTS = {}  # each Day's THOUGHT_OFFER_PARTS in lc_days/<day>.py (added at import)


def _install_day_packs():
    """Put every Day's beats, thoughts and offer parts (game/python-packages/lc_days/<day>.py)
    in front of the tables above, in play order. Runs once, at import."""
    global BEATS, THOUGHT_ORDER, THOUGHTS, OFFER_PARTS
    import lc_days
    beats, order, thoughts, parts = {}, (), {}, {}
    for day in lc_days.modules():
        beats.update(getattr(day, "THOUGHT_BEATS", {}))
        order += tuple(getattr(day, "THOUGHT_ORDER", ()))
        thoughts.update(getattr(day, "THOUGHTS", {}))
        parts.update(getattr(day, "THOUGHT_OFFER_PARTS", {}))
    beats.update(BEATS)
    thoughts.update(THOUGHTS)
    parts.update(OFFER_PARTS)
    BEATS, THOUGHT_ORDER, THOUGHTS, OFFER_PARTS = beats, order + THOUGHT_ORDER, thoughts, parts


_install_day_packs()

_DEFAULT_NAMES = {"player_name": "Ryan", "girlfriend_name": "Leia", "friend_name": "Julian"}


def day_thoughts(day_id, thoughts=None, order=None):
    """Thought ids for day_id, in day order."""
    thoughts = THOUGHTS if thoughts is None else thoughts
    order = THOUGHT_ORDER if order is None else order
    return [tid for tid in order if thoughts[tid]["day"] == day_id]


def lane_from_lean(lean):
    """Lane key for a stats-model lean ('love' / 'love_exhib' / 'ntr'); None otherwise."""
    return _LEAN_TO_LANE.get(lean)


def _number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _over_bar(stat, stats):
    """How far the stat sits over its tint bar, or None when it is under it or unreadable."""
    value = _number(stats.get(stat))
    if value is None or value < TINT[stat]:
        return None
    return value - TINT[stat]


def variant_key(thought_id, stats, lane, thoughts=None):
    """The variant key that applies now, or None for the base text.

    The lane variant comes first (when the thought has one for that lane). In a lane, the first
    of LANE_STATS[lane] that the thought has a variant for and that sits over its TINT bar wins;
    a lane never shows a stat it does not list. With no lane, the stat furthest over its bar
    (ties follow STAT_PRIORITY). Missing or non-numeric stats never tint.
    """
    thoughts = THOUGHTS if thoughts is None else thoughts
    variants = thoughts[thought_id]["variants"]
    if lane in LANES and lane in variants:
        return lane
    stats = stats or {}
    if lane in LANE_STATS:
        for stat in LANE_STATS[lane]:
            if stat in variants and _over_bar(stat, stats) is not None:
                return stat
        return None
    best, best_margin = None, None
    for stat in STAT_PRIORITY:
        if stat not in variants:
            continue
        margin = _over_bar(stat, stats)
        if margin is None:
            continue
        if best_margin is None or margin > best_margin:
            best, best_margin = stat, margin
    return best


def colour_count(thought_id, stats, lane, thoughts=None):
    """How many of this save's colours the thought has words for: its lane variant, plus each
    stat the lane allows (every stat with no lane) that is over its bar. 0 = it reads as base."""
    thoughts = THOUGHTS if thoughts is None else thoughts
    variants = thoughts[thought_id]["variants"]
    stats = stats or {}
    count = 1 if (lane in LANES and lane in variants) else 0
    allowed = LANE_STATS.get(lane, STAT_PRIORITY)
    return count + sum(1 for stat in allowed
                       if stat in variants and _over_bar(stat, stats) is not None)


def thought_text(thought_id, stats, lane, thoughts=None):
    """The thought's text for these stats and lane (unknown id -> KeyError)."""
    thoughts = THOUGHTS if thoughts is None else thoughts
    entry = thoughts[thought_id]
    key = variant_key(thought_id, stats, lane, thoughts=thoughts)
    return entry["variants"][key] if key else entry["base"]


def fill_names(text, names):
    """Replace the three name tokens with the player's names (defaults when missing)."""
    for token, default in _DEFAULT_NAMES.items():
        text = text.replace("[" + token + "]", (names or {}).get(token) or default)
    return text


def _beat_seen(test, has_flag, get_value):
    kind = test[0]
    if kind == "flag":
        return bool(has_flag(test[1]))
    if kind == "value_set":
        return get_value(test[1]) is not None
    if kind == "value_min":
        value = _number(get_value(test[1]))
        return value is not None and value >= test[2]
    raise ValueError("unknown beat test %r" % (test,))


def seen_beats(day_id, has_flag, get_value, beats=None):
    """Ids of day_id's beats this save has seen. has_flag(flag) and get_value(key) read the save
    (get_value returns None when the value is missing)."""
    beats = BEATS if beats is None else beats
    return {beat for beat, spec in beats.items()
            if spec["day"] == day_id and _beat_seen(spec["test"], has_flag, get_value)}


def offer(day_id, stats, lane, seen, demo=False, thoughts=None, parts=None):
    """The thought ids for the end of day_id's review: one per part of the day, in day order.

    Only thoughts whose required beat is in `seen`; a part with none seen gives no card. Within
    a part, the thought this save colours most (colour_count: it reflects how this save played
    the day) wins; equal counts (including none) go to the earlier beat. A demo build offers
    nothing.
    """
    if demo:
        return []
    seen = seen or ()
    thoughts = THOUGHTS if thoughts is None else thoughts
    parts = OFFER_PARTS if parts is None else parts
    out = []
    for part in parts.get(day_id, ()):
        ids = [tid for tid in part if thoughts[tid]["requires"] in seen]
        if not ids:
            continue
        ranked = sorted(enumerate(ids),
                        key=lambda pair: (-colour_count(pair[1], stats, lane, thoughts), pair[0]))
        out.append(ranked[0][1])
    return out


def keep(kept, day_id, thought_id, thoughts=None):
    """A new {day_id: thought id or None} dict with day_id's choice recorded.

    thought_id None means "keep nothing" and is stored as None. An unknown id, or one from
    another day, raises ValueError.
    """
    thoughts = THOUGHTS if thoughts is None else thoughts
    if thought_id is not None:
        entry = thoughts.get(thought_id)
        if entry is None or entry["day"] != day_id:
            raise ValueError("not a %s thought: %r" % (day_id, thought_id))
    out = dict(kept or {})
    out[day_id] = thought_id
    return out


def kept_id(kept, day_id, thoughts=None):
    """The thought id kept for day_id, or None (nothing kept, never offered, old save, or an id
    that no longer exists)."""
    thoughts = THOUGHTS if thoughts is None else thoughts
    tid = (kept or {}).get(day_id)
    return tid if tid in thoughts else None


def tint_label(key):
    """Display label for a variant key (Insight/Full stamp), '' for the base text."""
    return TINT_LABELS.get(key, "") if key else ""
