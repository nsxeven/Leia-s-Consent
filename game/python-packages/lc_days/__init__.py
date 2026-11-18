"""Day packs, pure-Python side: one module per Day (game/python-packages/lc_days/<day>.py).

Each module holds that Day's data for the pure-Python engine modules, which read it here
instead of naming any Day themselves (tests/test_day_packs.py keeps them Day-free):

    CHAPTER                 chapter registry entry (lc_chapters.CHAPTERS[<day>])
    NTS_VARIANT_KEY         story key of the Day's "likes watching" variant (lc_chapters)
    STAT_THRESHOLDS         route / her-own-call thresholds (lc_stat_model.THRESHOLDS)
    STAT_CHOICE_GATES       gate choices: "soft" / "hard" (lc_stat_model.CHOICE_GATES)
    STAT_ROUTE_FLAGS        route value a branch writes (lc_stat_model.CHOICE_ROUTE_FLAGS)
    STAT_REPAIR_CHOICES     repair beats (lc_stat_model.REPAIR_CHOICES)
    STAT_MODEL_EXPORTS      names of the Day's route resolvers, published on lc_stat_model
    THOUGHT_BEATS, THOUGHT_ORDER, THOUGHTS, THOUGHT_OFFER_PARTS   Ryan's thoughts (lc_thoughts)
    UI_DAY_FLAG             (day number, started flag, complete flag) (lc_ui_logic.DAY_FLAGS)
    UI_STORY_START_FLAG     flag that means the story has begun (lc_ui_logic.story_day_number)
    UI_NIGHT_EXCEPTIONS     night images whose names carry no night token (lc_ui_logic)
    UI_DAY_EXCEPTIONS       day images whose names carry a night token (lc_ui_logic)

Every name is optional. A new Day adds its module name to DAY_MODULES (in play order) and
copies the module skeleton that tools/new_day.py writes. Guide: docs/DAY_PACK.md.

Pure Python (no Ren'Py import). Modules are imported lazily, so a Day module may import
lc_stat_model at its end (it does, for THRESHOLDS) without an import cycle.
"""
import importlib

# Play order. Engine tables are filled in this order.
DAY_MODULES = ("prologue", "day1", "day2", "day3", "day4", "day5")


def modules():
    """The Day modules in play order."""
    return [importlib.import_module(__name__ + "." + name) for name in DAY_MODULES]


def collect(attr):
    """[(module, value)] for every Day module that defines `attr`, in play order."""
    return [(mod, getattr(mod, attr)) for mod in modules() if hasattr(mod, attr)]
