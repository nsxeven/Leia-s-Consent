"""Day Four: pure-Python Day pack data (see lc_days/__init__.py for the names).

Ren'Py side: game/chapters/ch01/day4/. Guide: docs/DAY_PACK.md.
"""

# Chapter registry entry (lc_chapters.CHAPTERS["day4"]).
CHAPTER = {
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
}

# "Likes watching" key: an exhibition ending shows the NTS title when it is set (lc_chapters).
NTS_VARIANT_KEY = "ch01_d4_exhib_variant"
