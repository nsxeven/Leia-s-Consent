"""Day Three: pure-Python Day pack data (see lc_days/__init__.py for the names).

Ren'Py side: game/chapters/ch01/day3/. Guide: docs/DAY_PACK.md.
"""

# Chapter registry entry (lc_chapters.CHAPTERS["day3"]).
CHAPTER = {
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
}


# ---------------------------------------------------------------- stat model (lc_stat_model)
# Repair beats (lc_stat_model.REPAIR_CHOICES): the only choices allowed to pair Temptation down
# with Love/Trust up.
STAT_REPAIR_CHOICES = frozenset((
    "ch01_d3_ntr_enjoy",
    "ch01_d3_ntr_talk",
))


# ---------------------------------------------------------------- UI (lc_ui_logic)
# Journal day number and its started / complete flags (lc_ui_logic.DAY_FLAGS).
UI_DAY_FLAG = (3, "ch01_day_03_started", "ch01_day_03_complete")
