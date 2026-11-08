"""Pure helpers for the scrapbook UI.

Imported by Ren'Py (game/python-packages is on the path) and by unittest.
No Ren'Py dependency.
"""

from __future__ import annotations

# Tokens that mean the current scene is night for the dialogue paper.
# "dinner" is included because evening meals use night paper; the daytime
# drive to dinner is listed in DAY_EXCEPTIONS.
NIGHT_PARTS = frozenset({
    "night",
    "evening",
    "dusk",
    "sunset",
    "bar",
    "party",
    "club",
    "dinner",
    "dream",
    "movie",
    "galley",
    "cabin",
    "kiss",
    "truthordare",
    "invitation",
})

# Image attributes that contain a night token but are daytime scenes.
DAY_EXCEPTIONS = frozenset({
    "ch01_drive_to_dinner",
})

# Night or late-evening images whose names carry no night token.
# Add new night CGs here when their name does not say so.
NIGHT_EXCEPTIONS = frozenset({
    # Day 1: walk to the shop, drive back, carry, lounge
    "ch01_walk_back_01",
    "ch01_walk_back_call",
    "ch01_trip_catch",
    "ch01_trip_catch_followup",
    "ch01_trip_catch_aftermath",
    "ch01_drive_back_seating",
    "ch01_julian_carry",
    "ch01_carry_walk",
    "ch01_carry_dress_shift",
    "ch01_lounge_micro_test",
    # Day 2: sunset pool, game night, bedroom finales
    "ch01_d2_love_pool_oral_01",
    "ch01_d2_love_pool_oral_02",
    "ch01_d2_julian_underwear_reveal",
    "ch01_d2_love_bedroom_01",
    "ch01_d2_love_bedroom_02",
    "ch01_d2_exhib_bed_open_01",
    "ch01_d2_exhib_bed_open_02",
    "ch01_d2_exhib_bed_open_03",
    "ch01_d2_exhib_bed_open_04",
    # Day 4: terrace at night
    "ch01_d4_exhib_watching",
    "ch01_d4_exhib_terrace_01",
    "ch01_d4_exhib_terrace_02",
    "ch01_d4_ntr_terrace_talk",
    # Day 5: sunset deck
    "ch01_d5_ntr_deck_alone",
})

# Cues from the style-guide motion sheet. Playback is a no-op until audio exists.
UI_CUES = {
    "polaroid": 0.35,
    "rustle": 0.40,
    "tape": 0.08,
    "bar": 0.60,
    "tick": 0.0,
    "thud": 0.12,
}

SPEAKER_COLORS = {
    "leia": "#cc0066",
    "ryan": "#3f6470",
    "maya": "#8a6420",
    "julian": "#5f8a32",
}

DAY_FLAGS = (
    (5, "ch01_day_05_started", "ch01_day_05_complete"),
    (4, "ch01_day_04_started", "ch01_day_04_complete"),
    (3, "ch01_day_03_started", "ch01_day_03_complete"),
    (2, "ch01_day_02_started", "ch01_day_02_complete"),
    (1, "ch01_started", "ch01_day_01_complete"),
)


def _attribute_key(image_name):
    parts = image_name.replace("-", "_").split()
    return parts[-1].lower() if parts else ""


def infer_dialogue_theme(image_names, manual=None, fallback="day"):
    """Return 'day' or 'night' for the dialogue paper.

    ``manual`` wins when it is 'day' or 'night'. With no scene images, the
    previous theme is kept via ``fallback`` so a black screen does not flash
    the other paper.
    """
    if manual in ("day", "night"):
        return manual
    if fallback not in ("day", "night"):
        fallback = "day"
    names = [name for name in (image_names or []) if name]
    if not names:
        return fallback

    for name in names:
        key = _attribute_key(name)
        if key in DAY_EXCEPTIONS:
            continue
        if key in NIGHT_EXCEPTIONS:
            return "night"
        parts = set(key.split("_"))
        if parts & NIGHT_PARTS:
            return "night"
    return "day"


def story_day_number(flags):
    """Return 0 for the prologue, 1-5 for chapter days, or None before the story."""
    flags = flags or {}
    for day, started, complete in DAY_FLAGS:
        if flags.get(started) and not flags.get(complete):
            return day
    for day, _started, complete in DAY_FLAGS:
        if flags.get(complete):
            return day
    if flags.get("prologue_started"):
        return 0
    return None


def day_period_label(flags, theme):
    """Quick-menu caption such as 'DAY 3  NIGHT'."""
    day = story_day_number(flags)
    period = "NIGHT" if theme == "night" else "DAY"
    if day is None:
        return period
    if day == 0:
        return "PROLOGUE  " + period
    return "DAY {}  {}".format(day, period)


def parse_choice_caption(caption):
    """Split a formatted choice into (line, chips).

    Chips are (name, amount, exact). Developer captions that include an ID
    or tags stay as a single raw line with no chips. Immersive captions have
    no bracket suffix.
    """
    text = caption or ""
    if "\n[" not in text:
        return text, []
    head, tail = text.split("\n[", 1)
    if "[ID:" in text or "Tags:" in tail:
        return text, []
    body = tail.split("]")[0]
    chips = []
    for part in body.split("•"):
        piece = " ".join(part.split())
        if not piece:
            continue
        bits = piece.split()
        if len(bits) < 2:
            continue
        mark = bits[-1]
        name = " ".join(bits[:-1])
        if mark == "↑":
            chips.append((name, 1, False))
        elif mark == "↓":
            chips.append((name, -1, False))
        elif mark == "→":
            chips.append((name, 0, False))
        else:
            try:
                amount = int(mark)
            except ValueError:
                continue
            chips.append((name, amount, True))
    return head.strip(), chips


def effect_markup(chips, up="#5aa874", down="#d4636e", neutral=None, arrow_font="DejaVuSans.ttf", colour_for=None):
    """Ren'Py markup for a choice's stat line: "[Love +1 • Trust -1]".

    `colour_for(name, amount)` picks each chip's colour by meaning (stat model v2:
    Temptation up is a warning, Exhibitionism/Sharing keep a route colour); when
    it is missing or returns None, gains are `up` and losses `down`. Brackets and
    separators keep the card's normal ink. Insight-mode chips (exact=False) show arrows instead of
    numbers, drawn in `arrow_font` because the handwriting fonts have no arrow
    glyphs. Brackets are plain text, so render with `substitute False`.
    """
    parts = []
    for name, amount, exact in chips:
        amount = int(amount)
        label = (name or "").replace("{", "{{")
        if exact:
            shown = "{} {:+d}".format(label, amount)
        else:
            arrow = "\u2191" if amount > 0 else ("\u2193" if amount < 0 else "\u2192")
            shown = "{} {{font={}}}{}{{/font}}".format(label, arrow_font, arrow)
        colour = colour_for(name, amount) if colour_for else None
        if colour is None:
            colour = up if amount > 0 else (down if amount < 0 else neutral)
        parts.append("{{color={}}}{}{{/color}}".format(colour, shown) if colour else shown)
    return "[" + " \u2022 ".join(parts) + "]"


def speaker_color(who, aliases=None):
    """Ink color for a history name. Unknown speakers use warm plum."""
    if not who:
        return "#7a6266"
    if who.strip().upper() == "I SAID":
        return "#cc0066"
    key = who.strip().lower()
    aliases = aliases or {}
    for canonical, names in aliases.items():
        for name in names:
            if name and name.strip().lower() == key:
                key = canonical
                break
    return SPEAKER_COLORS.get(key, "#3b2a30")


def chip_label(name, amount, exact):
    shown = (name or "").upper()
    if not exact:
        return shown
    return "{} {:+d}".format(shown, int(amount))
