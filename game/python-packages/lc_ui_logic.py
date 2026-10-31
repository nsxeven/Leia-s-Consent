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
