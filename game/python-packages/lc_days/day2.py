"""Day Two: pure-Python Day pack data (see lc_days/__init__.py for the names).

Ren'Py side: game/chapters/ch01/day2/. Guide: docs/DAY_PACK.md.
"""

# Chapter registry entry (lc_chapters.CHAPTERS["day2"]).
CHAPTER = {
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
}
