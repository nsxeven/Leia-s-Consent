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
#   lc_part_begin(chapter_id, number, title)  part card text + save name inside a day
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

default lc_part_card = ""

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

    def lc_part_begin(chapter_id, number, title):
        """Start a part inside a day (display only): sets the card text for
        `centered "[lc_part_card]"` and names new saves 'Chapter 2 · Day Two · The Pool'."""
        store.lc_part_card = lc_chapters.part_card_text(chapter_id, number, title)
        store.save_name = lc_chapters.part_save_name(chapter_id, title)

    def lc_chapter_start_save_name():
        lc_chapter_set_save_name("prologue")

    if lc_chapter_start_save_name not in config.start_callbacks:
        config.start_callbacks.append(lc_chapter_start_save_name)

# Opening title cards and "CHAPTER N COMPLETE" headings: each Day pack's *_chapter.rpy.
