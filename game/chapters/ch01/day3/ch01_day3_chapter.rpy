# Day Three pack - chapter: title-card text. The chapter registry entry (titles) is CHAPTER in
#   game/python-packages/lc_days/day3.py.
#
# Where every kind of content goes: docs/DAY_PACK.md.

# Opening title card (neutral title for everyone), shown by the Day's start label.
define lc_chapter_card_day3 = lc_chapters.card_text("day3")

# End-of-day review: this Day's row (systems/day_review.rpy). route_key = the end-route story key.
init 1 python:
    import lc_chapters
    LC_REVIEW_DAYS["ch01_d3"] = {"label": lc_chapters.review_label("day3"), "chapter": "day3", "route_key": "ch01_d3_lane"}
