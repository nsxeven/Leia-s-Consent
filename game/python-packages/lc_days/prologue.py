"""Prologue: pure-Python Day pack data (see lc_days/__init__.py for the names).

Ren'Py side: game/chapters/prologue/. Guide: docs/DAY_PACK.md.
"""

# Chapter registry entry (lc_chapters.CHAPTERS["prologue"]).
CHAPTER = {
    "number": 0, "number_word": "", "day": None, "day_word": "",
    "review_day": None,
    "title": 'Truth or Dare',
    # The Prologue happens before any route exists.
    "routes": {"love": None, "love_exhib": None, "nts": None, "ntr": None, "repair": None},
}

# The journal shows "PROLOGUE" once this flag is set (lc_ui_logic.story_day_number).
UI_STORY_START_FLAG = "prologue_started"
