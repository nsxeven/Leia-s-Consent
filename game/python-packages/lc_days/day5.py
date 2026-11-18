"""Day Five: pure-Python Day pack data (see lc_days/__init__.py for the names).

Ren'Py side: game/chapters/ch01/day5/. Guide: docs/DAY_PACK.md.
"""

# Chapter registry entry (lc_chapters.CHAPTERS["day5"]).
CHAPTER = {
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
}

# "Likes watching" key: an exhibition ending shows the NTS title when it is set (lc_chapters).
NTS_VARIANT_KEY = "ch01_d5_exhib_variant"
