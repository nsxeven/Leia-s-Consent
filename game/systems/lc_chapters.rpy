# Chapter registry bridge: one chapter per in-game day (display only).
#
# The titles live in ONE place: game/python-packages/lc_chapters.py (CHAPTERS,
# all PLACEHOLDER until darryn names them). This file only exposes them to
# Ren'Py script and screens. Internal ids (ch01_* labels, story keys, review
# day ids) are unchanged.
#
# Title cards use the say statement so seen/skip/history keep working, and a
# plain variable name so interpolation works with config.interpolate_exprs
# on or off:
#     centered "[lc_chapter_card_day2]"
#     centered "[lc_chapter_complete_card_day4]\n\n{size=25}...{/size}"
# A new day needs one CHAPTERS entry plus its define lines below.

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
