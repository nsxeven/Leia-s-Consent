# Day Three pack - chapter: title-card text, review row and Chapter Select preset. The chapter registry entry (titles) is CHAPTER in
#   game/python-packages/lc_days/day3.py.
#
# Where every kind of content goes: docs/DAY_PACK.md.

# Opening title card (neutral title for everyone), shown by the Day's start label.
define lc_chapter_card_day3 = lc_chapters.card_text("day3")

# End-of-day review: this Day's row (systems/day_review.rpy). route_key = the end-route story key.
init 1 python:
    import lc_chapters
    LC_REVIEW_DAYS["ch01_d3"] = {"label": lc_chapters.review_label("day3"), "chapter": "day3", "route_key": "ch01_d3_lane"}
    LC_REVIEW_NIGHT["ch01_d3"] = ("DAY 3", lc_chapters.chapter_title("day3").upper(), "night falls over the villa…")  # night card: day, neutral title, caption
    LC_REVIEW_TICKET["ch01_d3"] = ("CLUB NIGHT", "ADMIT ONE")  # ticket stub: title, detail

    # Day Three's lane is fixed by Day Two. The two NTR choices still change how the recap
    # describes the night, without relabeling the lane Day Four reads (review_route hook).
    def ch01_d3_review_route(route, day_id, value):
        """review_route hook: Day Three's NTR talk / withdraw nights and the strained-Love repair."""
        if day_id == "ch01_d3" and value == "ntr":
            effort = get_story_value("ch01_d3_ntr_repair_effort", "none")
            if effort == "talk":
                return "ntr_talked"
            if effort == "withdraw":
                return "ntr_withdrew"
        # mixed_unresolved starts Day Three as strained Love; talking it out at the club is a repair.
        if (day_id == "ch01_d3" and value == "love" and get_story_value("ch01_d3_strained_love", False)
                and get_story_value("ch01_d3_ntr_repair_effort", "none") == "talk"):
            return "love_repaired"
        return route

    lc_hook_add("review_route", ch01_d3_review_route)

# Chapter Select (systems/chapter_select.rpy): the Day Three preset (keyed by the stored Day Two
#   end state, CH01_SELECT_END_ROUTES in ch01_day2_chapter.rpy) and the seed for "Day Three finished".
init 1 python:
    import lc_chapters

    def ch01_d3_select_seed(route):
        """Chapter Select "Day Three" preset: Day Two finished on end state `route`; returns the entry label."""
        ch01_d2_select_finished(route)
        return "ch01_day3_start"

    def ch01_d3_select_finished(base, lane=None):
        """Chapter Select: Day Three finished after Day Two end state `base`. `lane` names the
        Day Three lane outright (the Day Five presets do). Returns the Day Three lane."""
        for flag in ("ch01_day_03_started", "ch01_d3_complete", "ch01_day_03_complete"):
            set_story_flag(flag)
        # Same mapping ch01_day3_start uses: mixed_unresolved starts Day Three as a
        # strained Love track and only becomes NTR if Ryan walks away at the club.
        # The Day Five presets name the Day Four lane they need explicitly.
        d3_lane_value = "ntr" if base == "ntr_confirmed" else ("exhibitionism" if base == "exhibitionism" else "love")
        if lane is not None:
            d3_lane_value = lane
        if base == "mixed_unresolved":
            set_story_value("ch01_d3_strained_love", True)
        set_story_value("ch01_d3_lane", d3_lane_value)
        set_story_value("ch01_d3_end_variant", {"love": "love_private", "exhibitionism": "exhibition_window", "ntr": "ntr_restroom_nightmare"}[d3_lane_value])
        # Day Four also reads these Day Three values (same values Day Three writes).
        if d3_lane_value == "ntr":
            set_story_value("ch01_d3_ntr_repair_effort", "enjoy")  # Day Three's own default when unset
            set_story_value("ch01_d3_maya_dessert", "chocolate")
            set_story_flag("ch01_d3_cutout_secret")
        else:
            set_story_value("ch01_d3_ntr_repair_effort", "none")
        return d3_lane_value

    CHAPTER_SELECT_PRESETS["day3"] = dict(
        label=lc_chapters.select_label("day3"),
        note="Starts at Day Three with the chosen Day Two ending stored.",
        heading=_("Stored Day Two ending"), routes=CH01_SELECT_END_ROUTES, seed=ch01_d3_select_seed,
        default=True,
    )
