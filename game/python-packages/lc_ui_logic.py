"""Pure helpers for the scrapbook UI.

Imported by Ren'Py (game/python-packages is on the path) and by unittest.
No Ren'Py dependency.
"""

from __future__ import annotations

import re

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

# Image attributes that contain a night token but are daytime scenes (each Day pack adds its
# own: UI_DAY_EXCEPTIONS in game/python-packages/lc_days/<day>.py).
DAY_EXCEPTIONS = frozenset()

# Night or late-evening images whose names carry no night token.
# Add new night CGs to the Day pack (UI_NIGHT_EXCEPTIONS) when their name does not say so.
NIGHT_EXCEPTIONS = frozenset()  # each Day's UI_NIGHT_EXCEPTIONS in lc_days/<day>.py (added at import)

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

DAY_FLAGS = ()  # each Day's UI_DAY_FLAG in lc_days/<day>.py (added at import, latest Day first)

# Flag that means the story has begun (the first Day's UI_STORY_START_FLAG).
STORY_START_FLAG = None


def _install_day_packs():
    """Add every Day's journal flags and paper exceptions (game/python-packages/lc_days/<day>.py).
    DAY_FLAGS ends up latest Day first. Runs once, at import."""
    global DAY_FLAGS, STORY_START_FLAG, NIGHT_EXCEPTIONS, DAY_EXCEPTIONS
    import lc_days
    flags = list(DAY_FLAGS)
    for day in lc_days.modules():
        if hasattr(day, "UI_DAY_FLAG"):
            flags.append(tuple(day.UI_DAY_FLAG))
        if hasattr(day, "UI_STORY_START_FLAG") and STORY_START_FLAG is None:
            STORY_START_FLAG = day.UI_STORY_START_FLAG
        NIGHT_EXCEPTIONS = NIGHT_EXCEPTIONS | frozenset(getattr(day, "UI_NIGHT_EXCEPTIONS", ()))
        DAY_EXCEPTIONS = DAY_EXCEPTIONS | frozenset(getattr(day, "UI_DAY_EXCEPTIONS", ()))
    DAY_FLAGS = tuple(sorted(flags, key=lambda row: row[0], reverse=True))


_install_day_packs()


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
    if STORY_START_FLAG and flags.get(STORY_START_FLAG):
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


CHOICE_MARK_RE = re.compile(r"\{#lcpath=(\w+)\}")


def choice_mark(choice_id):
    """Invisible marker (a Ren'Py {#...} comment tag) carrying a choice id in its caption."""
    return "{#lcpath=" + choice_id + "}"


def split_choice_mark(caption):
    """(choice_id or None, caption without the marker)."""
    text = caption or ""
    found = CHOICE_MARK_RE.search(text)
    if not found:
        return None, text
    return found.group(1), CHOICE_MARK_RE.sub("", text)


def _chips_from_body(body):
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
    return chips


def parse_choice_caption(caption):
    """Split a formatted choice into (line, chips).

    Chips are (name, amount, exact). Developer captions that include an ID
    or tags stay as a single raw line with no chips. Immersive captions have
    no bracket suffix. Gate captions put a label group before the stats
    ("[MAJOR RELATIONSHIP CONSEQUENCE] [Love -1 • Temptation +3]"): the first
    bracket group that holds stats is used. The {#lcpath=...} marker is dropped.
    """
    _choice_id, text = split_choice_mark(caption)
    if "\n[" not in text:
        return text, []
    head, tail = text.split("\n[", 1)
    if "[ID:" in text or "Tags:" in tail:
        return text, []
    chips = []
    for body in re.findall(r"\[([^\[\]]*)\]", "[" + tail):
        chips = _chips_from_body(body)
        if chips:
            break
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
