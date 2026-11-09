"""Chapter registry: one chapter per in-game day (display only).

Prologue stays the Prologue; Chapter 1 = Day One ... Chapter 5 = Day Five.
Internal ids (ch01_* labels, story keys, review day ids, file names) do NOT
change: this module only decides what the player reads.

    * Title cards at the start of each chapter show the NEUTRAL title.
    * The end-of-day review reveals the ROUTE-FLAVOURED title of the chapter
      just played (route family from ROUTE_FAMILY below). Mixed, undecided and
      unresolved endings keep the neutral title.

=========================================================================
PLACEHOLDER TITLES: darryn has not named the chapters yet. Every title in
CHAPTERS below ("title" and the four "routes" entries) is a placeholder.
Replace them HERE ONLY; every title card, the day review, Chapter Select,
save names and the gallery read from this table.
=========================================================================

Pure Python (no Ren'Py import) so tests/ can load it directly.
"""

# The four route families (see leias-consent-flow-review route-model.md).
FAMILIES = ("love", "love_exhib", "nts", "ntr")

FAMILY_LABELS = {
    "love": "Love",
    "love_exhib": "Love + Exhibitionism",
    "nts": "NTS",
    "ntr": "NTR",
}

PLACEHOLDER_TITLES = True  # flip to False once darryn's real titles are in

CHAPTER_ORDER = ("prologue", "day1", "day2", "day3", "day4", "day5")

# ---------------------------------------------------------------- REGISTRY
# number       : chapter number shown as "Chapter N" (0 = Prologue)
# number_word  : "One", "Two"... used in "Chapter One" headings
# day          : in-game day this chapter covers (None for the Prologue)
# day_word     : "One", "Two"... used in "Day Two"
# review_day   : the internal end-of-day review id (LC_REVIEW_DAYS key)
# title        : NEUTRAL title (title cards, undecided reviews)       PLACEHOLDER
# routes       : route-flavoured titles revealed by the day review      PLACEHOLDER
#                (None = no route variant; the neutral title is used)
CHAPTERS = {
    "prologue": {
        "number": 0, "number_word": "", "day": None, "day_word": "",
        "review_day": None,
        "title": "Every Boundary Starts Somewhere",  # PLACEHOLDER (current Prologue tagline)
        # The Prologue happens before any route exists.
        "routes": {"love": None, "love_exhib": None, "nts": None, "ntr": None},
    },
    "day1": {
        "number": 1, "number_word": "One", "day": 1, "day_word": "One",
        "review_day": "ch01_d1",
        "title": "Arrival",  # PLACEHOLDER (current day-review name)
        "routes": {
            "love": "Arrival (Love)",              # PLACEHOLDER
            "love_exhib": "Arrival (Love+Exhib)",  # PLACEHOLDER
            "nts": "Arrival (NTS)",                # PLACEHOLDER
            "ntr": "Arrival (NTR)",                # PLACEHOLDER
        },
    },
    "day2": {
        "number": 2, "number_word": "Two", "day": 2, "day_word": "Two",
        "review_day": "ch01_d2",
        "title": "The Shore",  # PLACEHOLDER (current day-review name)
        "routes": {
            "love": "The Shore (Love)",              # PLACEHOLDER
            "love_exhib": "The Shore (Love+Exhib)",  # PLACEHOLDER
            "nts": "The Shore (NTS)",                # PLACEHOLDER
            "ntr": "The Shore (NTR)",                # PLACEHOLDER
        },
    },
    "day3": {
        "number": 3, "number_word": "Three", "day": 3, "day_word": "Three",
        "review_day": "ch01_d3",
        "title": "The Club",  # PLACEHOLDER (current day-review name)
        "routes": {
            "love": "The Club (Love)",              # PLACEHOLDER
            "love_exhib": "The Club (Love+Exhib)",  # PLACEHOLDER
            "nts": "The Club (NTS)",                # PLACEHOLDER
            "ntr": "The Club (NTR)",                # PLACEHOLDER
        },
    },
    "day4": {
        "number": 4, "number_word": "Four", "day": 4, "day_word": "Four",
        "review_day": "ch01_d4",
        "title": "The Market",  # PLACEHOLDER (current day-review name; script calls Day Four "Recalibration")
        "routes": {
            "love": "The Market (Love)",              # PLACEHOLDER
            "love_exhib": "The Market (Love+Exhib)",  # PLACEHOLDER
            "nts": "The Market (NTS)",                # PLACEHOLDER
            "ntr": "The Market (NTR)",                # PLACEHOLDER
        },
    },
    "day5": {
        "number": 5, "number_word": "Five", "day": 5, "day_word": "Five",
        "review_day": "ch01_d5",
        "title": "The Water",  # PLACEHOLDER (current day-review name)
        "routes": {
            "love": "The Water (Love)",              # PLACEHOLDER
            "love_exhib": "The Water (Love+Exhib)",  # PLACEHOLDER
            "nts": "The Water (NTS)",                # PLACEHOLDER
            "ntr": "The Water (NTR)",                # PLACEHOLDER
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
    "love_repaired": "love",          # route model: "Love repaired = way back from NTR to Love"
    # UNSURE: Days 2-4 'exhibitionism' is the shared Love+Exhib / NTS family
    # (NTS only splits from Love+Exhib at Day 5's Maya moment, and no NTS key
    # exists yet). Review already labels it "Love + Exhibitionism".
    "exhibitionism": "love_exhib",
    # UNSURE: Day One "nts_seeded" means the exhibition family was SEEDED
    # (comment in day_review.rpy); could equally stay neutral ("Nothing is
    # settled yet") or count as NTS.
    "nts_seeded": "love_exhib",
    # UNSURE: Day One "ntr_seeded" is only pressure/distance, could stay neutral.
    "ntr_seeded": "ntr",
    "ntr": "ntr",
    "ntr_confirmed": "ntr",
    "ntr_talked": "ntr",              # Day 3 NTR lane, recap wording only; lane stays NTR
    "ntr_withdrew": "ntr",            # Day 3 NTR lane, recap wording only; lane stays NTR
    # UNSURE: "unresolved" -> neutral per the rule, though it sits in the NTR lane.
    "ntr_unresolved": None,
}

UNSURE_ROUTE_KEYS = ("exhibitionism", "nts_seeded", "ntr_seeded", "ntr_unresolved")

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


def chapter_title(chapter_id, family=None):
    """Display title: route-flavoured for a known family, otherwise neutral."""
    c = CHAPTERS[chapter_id]
    if family:
        variant = c["routes"].get(family)
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
