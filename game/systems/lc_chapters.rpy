# Chapter registry bridge - chapter titles and cards for Ren'Py script
#
# Purpose: Exposes python-packages/lc_chapters.py (the ONE place chapter titles live; one chapter
#   per in-game day, display only) to scripts and screens, names new saves after the chapter, and
#   defines the title-card variables. Internal ids (ch01_* labels, story keys, review day ids) never
#   change.
#
# Public API (call these from scenes/screens):
#   lc_chapter_title(chapter_id, family=None)
#       display title for (chapter, route family or None = neutral)
#   lc_chapter_heading(chapter_id)            'Chapter N' heading
#   lc_chapter_for_review_day(day_id)         chapter id for a review day id
#   lc_route_family(route_key)                route family of a route key
#   lc_chapter_set_save_name(chapter_id) -> None
#       name new saves after a chapter
#   lc_chapter_start_save_name() -> None      start callback: saves start as the Prologue
#   define lc_chapter_card_day1               opening card text (same for day2 .. day5)
#   define lc_chapter_card_day2               Day 2 opening card
#   define lc_chapter_complete_card_day4      Day 4 completion card (also day5)
#
# Example:
#   centered "[lc_chapter_card_day2]"
#
# Notes: A new day needs one CHAPTERS entry in lc_chapters.py plus its define line(s) here.
#   Title cards use the say statement with a plain variable name, so interpolation works with
#   config.interpolate_exprs on or off.
#
# Depends on: python-packages/lc_chapters.py
# Hooks: none (adds lc_chapter_start_save_name to config.start_callbacks)
# Load order: init -10: before anything (day review, gallery, Chapter Select) asks for titles
# Docs: docs/ARCHITECTURE.md   Tests: tests/test_lc_chapters.py

init -10 python:
    import lc_chapters

    def lc_chapter_title(chapter_id, family=None):
        """Display title for (chapter, route family or None = neutral)."""
        return lc_chapters.chapter_title(chapter_id, family)

    def lc_chapter_heading(chapter_id):
        return lc_chapters.chapter_heading(chapter_id)

    def lc_chapter_for_review_day(day_id):
        return lc_chapters.chapter_for_review_day(day_id)

    def lc_route_family(route_key):
        return lc_chapters.route_family(route_key)

    def lc_chapter_set_save_name(chapter_id):
        """Name new saves after the chapter being played (save slots + Continue card)."""
        store.save_name = lc_chapters.save_name(chapter_id)

    def lc_chapter_start_save_name():
        lc_chapter_set_save_name("prologue")

    if lc_chapter_start_save_name not in config.start_callbacks:
        config.start_callbacks.append(lc_chapter_start_save_name)

# Opening title cards (neutral title for everyone).
define lc_chapter_card_day1 = lc_chapters.card_text("day1")
define lc_chapter_card_day2 = lc_chapters.card_text("day2")
define lc_chapter_card_day3 = lc_chapters.card_text("day3")
define lc_chapter_card_day4 = lc_chapters.card_text("day4")
define lc_chapter_card_day5 = lc_chapters.card_text("day5")

# "CHAPTER N COMPLETE" headings (temporary end-of-build cards).
define lc_chapter_complete_card_day4 = lc_chapters.complete_card_text("day4")
define lc_chapter_complete_card_day5 = lc_chapters.complete_card_text("day5")
