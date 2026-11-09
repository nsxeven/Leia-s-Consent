"""Chapter registry: one chapter per in-game day (display only).

Prologue stays the Prologue; Chapter 1 = Day One ... Chapter 5 = Day Five.
Internal ids (ch01_* labels, story keys, review day ids, file names) do NOT
change: this module only decides what the player reads.

    * Title cards at the start of each chapter show the NEUTRAL title.
    * The end-of-day review reveals the ROUTE-FLAVOURED title of the chapter
      just played (route family from ROUTE_FAMILY below). Mixed, undecided and
      unresolved endings keep the neutral title.

Titles chosen by darryn 2026-11-09 (options doc: chapter_title_options.md).
Edit them HERE ONLY: every title card, the day review, Chapter Select, save
names and the gallery read from this table.

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

CHAPTER_ORDER = ("prologue", "day1", "day2", "day3", "day4", "day5")

# ---------------------------------------------------------------- REGISTRY
# number       : chapter number shown as "Chapter N" (0 = Prologue)
# number_word  : "One", "Two"... used in "Chapter One" headings
# day          : in-game day this chapter covers (None for the Prologue)
# day_word     : "One", "Two"... used in "Day Two"
# review_day   : the internal end-of-day review id (LC_REVIEW_DAYS key)
# title        : NEUTRAL title (title cards, undecided reviews)
# routes       : route-flavoured titles revealed by the day review (+ repair)
#                (None = no route variant; the neutral title is used)
CHAPTERS = {
    "prologue": {
        "number": 0, "number_word": "", "day": None, "day_word": "",
        "review_day": None,
        "title": 'Truth or Dare',
        # The Prologue happens before any route exists.
        "routes": {"love": None, "love_exhib": None, "nts": None, "ntr": None, "repair": None},
    },
    "day1": {
        "number": 1, "number_word": "One", "day": 1, "day_word": "One",
        "review_day": "ch01_d1",
        "title": 'Sheer Curtains',
        "routes": {
            "love": 'Today Was Good',
            "love_exhib": 'Can He Tell?',
            "nts": 'A Third Person',  # not reachable yet: no NTS beat this day (see NTS_VARIANT_KEYS)
            "ntr": 'Spaces Left Open',
            "repair": None,  # no repair ending this day; falls back to the Love title
        },
    },
    "day2": {
        "number": 2, "number_word": "Two", "day": 2, "day_word": "Two",
        "review_day": "ch01_d2",
        "title": 'Plus One',
        "routes": {
            "love": 'They Hide Enough',
            "love_exhib": 'Leave Them Open',
            "nts": 'Terrible Influence',  # not reachable yet: no NTS beat this day (see NTS_VARIANT_KEYS)
            "ntr": 'Are We Okay?',
            "repair": 'Tell Her the Truth',
        },
    },
    "day3": {
        "number": 3, "number_word": "Three", "day": 3, "day_word": "Three",
        "review_day": "ch01_d3",
        "title": 'The Glass Wall',
        "routes": {
            "love": 'Curtains Drawn',
            "love_exhib": 'Getting Braver',
            "nts": 'Causing a Scene',  # not reachable yet: no NTS beat this day (see NTS_VARIANT_KEYS)
            "ntr": 'Typing…',
            "repair": None,  # no repair ending this day; falls back to the Love title
        },
    },
    "day4": {
        "number": 4, "number_word": "Four", "day": 4, "day_word": "Four",
        "review_day": "ch01_d4",
        "title": 'Blue Hour',
        "routes": {
            "love": 'Badly, Slowly',
            "love_exhib": 'One Slow Heartbeat',
            "nts": 'Watching Her Decide',
            "ntr": 'The Hairclip',
            "repair": 'Back in Her Hair',
        },
    },
    "day5": {
        "number": 5, "number_word": "Five", "day": 5, "day_word": "Five",
        "review_day": "ch01_d5",
        "title": 'The Water',
        "routes": {
            "love": "Nobody's Cove",
            "love_exhib": 'Still Me',
            "nts": 'Her Biggest Fan',
            "ntr": 'Reasonable Doubt',
            "repair": 'The Second Try',
        },
    },
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
NTS_VARIANT_KEYS = {
    "day4": "ch01_d4_exhib_variant",
    "day5": "ch01_d5_exhib_variant",
}
NTS_VARIANT = "ryan_likes_watching"

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
