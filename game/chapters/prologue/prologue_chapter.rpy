# Prologue pack - chapter: the Prologue's chapter registry entry is CHAPTER in
#   game/python-packages/lc_days/prologue.py. The Prologue has no end-of-day review, no
#   title-card variable and no Chapter Select preset of its own; this file holds its phone
#   history for the later Days' presets.
#
# Where every kind of content goes: docs/DAY_PACK.md.

# Chapter Select (systems/chapter_select.rpy): the Prologue's phone history, delivered by Day One's
#   "finished" seed. Same ids, threads and texts as prologue.rpy (tests/test_chapter_select_phone.py).
init 1 python:
    def prologue_select_phone():
        """Chapter Select: the Prologue's Trip Group messages, read."""
        chapter_select_phone("group", "julian", "prologue_julian_downstairs_01", "I'm downstairs.")
        chapter_select_phone("group", "julian", "prologue_julian_downstairs_02",
                             "If either of you makes us miss this flight I am leaving without you.")
