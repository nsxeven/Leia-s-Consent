"""Chapter registry: one chapter per in-game day (display only).

Prologue stays the Prologue; Chapter 1 = Day One ... Chapter 5 = Day Five.
Internal ids (ch01_* labels, story keys, review day ids, file names) do NOT
change: this module only decides what the player reads.

    * Title cards at the start of each chapter show the NEUTRAL title.
    * The end-of-day review reveals the ROUTE-FLAVOURED title of the chapter
      just played (route family from ROUTE_FAMILY below). Mixed, undecided and
      unresolved endings keep the neutral title.

Titles chosen by darryn 2026-11-09 (options doc: chapter_title_options.md).
Each Day's entry lives in its Day pack (CHAPTER in game/python-packages/lc_days/<day>.py);
this module assembles CHAPTERS from them. Edit titles THERE ONLY: every title card, the day
review, Chapter Select, save names and the gallery read from this table.

Pure Python (no Ren'Py import) so tests/ can load it directly.
"""

# The four route families (see leias-consent-flow-review route-model.md).
FAMILIES = ("love", "love_exhib", "nts", "ntr")

# Repair endings (made up after a rough day) get their own fifth title on the
# days that have one (darryn 2026-11-09); other days fall back to the Love title.
REPAIR = "repair"
TITLE_FAMILIES = FAMILIES + (REPAIR,)

FAMILY_LABELS = {
    "love": "Love",
    "love_exhib": "Love + Exhibitionism",
    "nts": "NTS",
    "ntr": "NTR",
    "repair": "Repair",
}

PLACEHOLDER_TITLES = False  # darryn picked the titles 2026-11-09

import lc_days  # noqa: E402  (Day packs; lazy, no import cycle)

CHAPTER_ORDER = tuple(lc_days.DAY_MODULES)  # play order (lc_days/__init__.py)

# ---------------------------------------------------------------- REGISTRY
# number       : chapter number shown as "Chapter N" (0 = Prologue)
# number_word  : "One", "Two"... used in "Chapter One" headings
# day          : in-game day this chapter covers (None for the Prologue)
# day_word     : "One", "Two"... used in "Day Two"
# review_day   : the internal end-of-day review id (LC_REVIEW_DAYS key)
# title        : NEUTRAL title (title cards, undecided reviews)
# routes       : route-flavoured titles revealed by the day review (+ repair)
#                (None = no route variant; the neutral title is used)
CHAPTERS = {  # each Day's entry: CHAPTER in its lc_days/<day>.py (added at import)
}

# ------------------------------------------------- ROUTE KEY -> FAMILY TABLE
# Every route id the end-of-day review can store (LC_REVIEW_ROUTES keys in
# game/systems/day_review.rpy). None = mixed / undecided / unresolved: the
# review keeps the NEUTRAL title. tests/test_lc_chapters.py checks that every
# LC_REVIEW_ROUTES key is listed here.
#
# Where the stored key comes from (LC_REVIEW_DAYS route_key, plus the
# lc_review_route() overrides):
#   Day 1 ch01_day1_route_pressure: nts_seeded / ntr_seeded / mixed (love via ch01_day1_love_ending)
#   Day 2 ch01_d2_end_route: love / exhibitionism / ntr_confirmed / mixed_unresolved / ...
#   Day 3 ch01_d3_lane: love / exhibitionism / ntr (+ ntr_talked / ntr_withdrew / love_repaired)
#   Day 4 ch01_d4_end_route, Day 5 ch01_d5_end_route:
#         love / exhibitionism / love_repaired / ntr_unresolved / ntr_confirmed
ROUTE_FAMILY = {
    "mixed": None,                    # undecided
    "mixed_unresolved": None,         # unresolved
    "love": "love",
    "love_repaired": REPAIR,          # own title where the day has one, else Love (darryn)
    # Exhibition lane. Shows NTS instead when Ryan chose "likes watching"
    # that day (review_family / NTS_VARIANT_KEYS, darryn 2026-11-09).
    "exhibitionism": "love_exhib",
    # Day One "nts_seeded" = the exhibition family was seeded (day_review.rpy).
    "nts_seeded": "love_exhib",
    "ntr_seeded": "ntr",
    "ntr": "ntr",
    "ntr_confirmed": "ntr",
    "ntr_talked": "ntr",              # Day 3 NTR lane, recap wording only; lane stays NTR
    "ntr_withdrew": "ntr",            # Day 3 NTR lane, recap wording only; lane stays NTR
    "ntr_unresolved": "ntr",          # on the NTR lane, so the NTR title (darryn)
}

UNSURE_ROUTE_KEYS = ()  # all settled by darryn 2026-11-09

# NTS vs Love + Exhibitionism (darryn 2026-11-09): an exhibition ending shows
# the NTS title when Ryan chose "likes watching" that day. Only Days 4 and 5
# have that beat so far, so Days 1-3 always show the Love + Exhib title.
NTS_VARIANT_KEYS = {}  # each Day's NTS_VARIANT_KEY in its lc_days/<day>.py (added at import)
NTS_VARIANT = "ryan_likes_watching"

def _install_day_packs():
    """Put every Day's chapter entry (CHAPTER) and "likes watching" key (NTS_VARIANT_KEY) from
    game/python-packages/lc_days/<day>.py in front, in play order, keyed by the module name.
    Runs once, at import."""
    rest, keys = dict(CHAPTERS), dict(NTS_VARIANT_KEYS)
    CHAPTERS.clear()
    NTS_VARIANT_KEYS.clear()
    for day in lc_days.modules():
        day_id = day.__name__.rsplit(".", 1)[-1]
        if hasattr(day, "CHAPTER"):
            CHAPTERS[day_id] = day.CHAPTER
        if hasattr(day, "NTS_VARIANT_KEY"):
            NTS_VARIANT_KEYS[day_id] = day.NTS_VARIANT_KEY
    CHAPTERS.update(rest)
    NTS_VARIANT_KEYS.update(keys)


_install_day_packs()

_REVIEW_DAY_CHAPTER = dict((c["review_day"], cid) for cid, c in CHAPTERS.items() if c["review_day"])


# ------------------------------------------------------------------ lookups
def chapter(chapter_id):
    return CHAPTERS[chapter_id]


def chapter_for_review_day(day_id):
    """'ch01_d2' -> 'day2'; None for unknown/future review days."""
    return _REVIEW_DAY_CHAPTER.get(day_id)


def route_family(route_key):
    """Route id -> 'love' / 'love_exhib' / 'nts' / 'ntr', or None (neutral)."""
    return ROUTE_FAMILY.get(route_key)


def chapter_heading(chapter_id):
    """'Prologue' or 'Chapter Two'."""
    c = CHAPTERS[chapter_id]
    if not c["number"]:
        return "Prologue"
    return "Chapter " + c["number_word"]


def chapter_short(chapter_id):
    """'Prologue' or 'Chapter 2'."""
    c = CHAPTERS[chapter_id]
    if not c["number"]:
        return "Prologue"
    return "Chapter {}".format(c["number"])


def day_label(chapter_id):
    """'Day Two', or '' for the Prologue."""
    c = CHAPTERS[chapter_id]
    return ("Day " + c["day_word"]) if c["day"] else ""


def review_family(chapter_id, route_key, get_value=None):
    """Title family for a finished day: route_family(), plus the NTS rule.

    get_value(key, default) reads story values (get_story_value in game)."""
    family = route_family(route_key)
    key = NTS_VARIANT_KEYS.get(chapter_id)
    if family == "love_exhib" and key and get_value and get_value(key, None) == NTS_VARIANT:
        return "nts"
    return family


def chapter_title(chapter_id, family=None):
    """Display title: route-flavoured for a known family, otherwise neutral.
    A repair ending without its own title shows the Love title."""
    c = CHAPTERS[chapter_id]
    if family:
        variant = c["routes"].get(family)
        if not variant and family == REPAIR:
            variant = c["routes"].get("love")
        if variant:
            return variant
    return c["title"]


def chapter_title_for_route(chapter_id, route_key):
    return chapter_title(chapter_id, route_family(route_key))


def card_text(chapter_id):
    """Opening title card (neutral for everyone). Ren'Py text tags included."""
    text = "{size=58}" + chapter_heading(chapter_id).upper() + "{/size}\n"
    text += "{size=40}" + chapter_title(chapter_id).upper() + "{/size}"
    day = day_label(chapter_id)
    if day:
        text += "\n{size=28}" + day + "{/size}"
    return text


def complete_card_text(chapter_id):
    """'CHAPTER FOUR COMPLETE' card heading."""
    return "{size=46}" + chapter_heading(chapter_id).upper() + " COMPLETE{/size}"


def review_label(chapter_id):
    """End-of-day review label: 'Chapter Two · Day Two'."""
    day = day_label(chapter_id)
    head = chapter_heading(chapter_id)
    return head + " \u00b7 " + day if day else head


def select_label(chapter_id):
    """Chapter Select button: 'Chapter 2 · Day Two'."""
    day = day_label(chapter_id)
    head = chapter_short(chapter_id)
    return head + " \u00b7 " + day if day else head


def save_name(chapter_id):
    """Save slot / Continue card name: 'Chapter 2 · Day Two' or 'Prologue'."""
    return select_label(chapter_id)


_PART_WORDS = ("", "One", "Two", "Three", "Four", "Five", "Six")


def part_card_text(chapter_id, number, title):
    """Part card inside a day (darryn 2026-11-19): 'DAY TWO / PART TWO / THE POOL'. Display only."""
    text = ""
    day = day_label(chapter_id)
    if day:
        text += "{size=28}" + day.upper() + "{/size}\n"
    text += "{size=50}PART " + _PART_WORDS[number].upper() + "{/size}\n"
    text += "{size=40}" + title.upper() + "{/size}"
    return text


def part_save_name(chapter_id, title):
    """Save slot name inside a part: 'Chapter 2 · Day Two · The Pool'."""
    return save_name(chapter_id) + " \u00b7 " + title
