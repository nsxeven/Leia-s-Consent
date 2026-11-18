# Day One pack - chapter: title-card text, review row and Chapter Select preset. The chapter registry entry (titles) is CHAPTER in
#   game/python-packages/lc_days/day1.py.
#
# Where every kind of content goes: docs/DAY_PACK.md.

# Opening title card (neutral title for everyone), shown by the Day's start label.
define lc_chapter_card_day1 = lc_chapters.card_text("day1")

# End-of-day review: this Day's row (systems/day_review.rpy). route_key = the end-route story key.
init 1 python:
    import lc_chapters
    LC_REVIEW_DAYS["ch01_d1"] = {"label": lc_chapters.review_label("day1"), "chapter": "day1", "route_key": "ch01_day1_route_pressure"}
    LC_REVIEW_NIGHT["ch01_d1"] = ("DAY 1", lc_chapters.chapter_title("day1").upper(), "night falls over the villa…")  # night card: day, neutral title, caption
    LC_REVIEW_TICKET["ch01_d1"] = ("VILLA NIGHT", "QUIET HOURS")  # ticket stub: title, detail

    # Day One's night reads Love when its love ending played (review_route hook).
    def ch01_d1_review_route(route, day_id, value):
        """review_route hook: the Day One love ending reads as Love."""
        if day_id == "ch01_d1" and getattr(store, "ch01_day1_love_ending", False):
            return "love"
        return route

    lc_hook_add("review_route", ch01_d1_review_route)

# Chapter Select (systems/chapter_select.rpy): every later Day's preset starts from Day One done.
init 1 python:
    def ch01_d1_select_finished(pressure):
        """Chapter Select: mark the Prologue and Day One finished, with Day One's end route."""
        # Day One is treated as finished.
        for flag in ("prologue_started", "ch01_started", "ch01_scene_30_complete", "ch01_day_01_complete", "ch01_scenes_14_30_complete"):
            set_story_flag(flag)
        set_story_value("ch01_day1_route_pressure", pressure)
        set_story_value("ch01_dream_response", "grounded")
