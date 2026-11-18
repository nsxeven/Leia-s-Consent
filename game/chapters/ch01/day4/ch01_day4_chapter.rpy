# Day Four pack - chapter: title-card text, review row and Chapter Select preset. The chapter registry entry (titles) is CHAPTER in
#   game/python-packages/lc_days/day4.py.
#
# Where every kind of content goes: docs/DAY_PACK.md.

# Opening title card (neutral title for everyone), shown by the Day's start label.
define lc_chapter_card_day4 = lc_chapters.card_text("day4")

# End-of-day review: this Day's row (systems/day_review.rpy). route_key = the end-route story key.
init 1 python:
    import lc_chapters
    LC_REVIEW_DAYS["ch01_d4"] = {"label": lc_chapters.review_label("day4"), "chapter": "day4", "route_key": "ch01_d4_end_route"}

# Chapter Select (systems/chapter_select.rpy): the Day Four preset (keyed by the stored Day Two
#   end state) and the seed for "Day Four finished" (its values: CH01_SELECT_DAY5_PRESETS).
init 1 python:
    import lc_chapters

    def ch01_d4_select_seed(route):
        """Chapter Select "Day Four" preset: Days Two and Three finished after Day Two end state `route`."""
        ch01_d2_select_finished(route)
        ch01_d3_select_finished(route)
        return "ch01_day4_start"

    def ch01_d4_select_finished(route, d5p, d3_lane_value):
        """Chapter Select: Day Four finished on end route `route`; `d5p` is its CH01_SELECT_DAY5_PRESETS row."""
        # Day Four finished: seed what ch01_day5_start reads (stored Day Four values and flags).
        set_story_value("ch01_d2_pool_outfit", "pool_conservative")
        for flag in ("ch01_day_04_started", "ch01_day_04_complete", "ch01_d4_scene_16_complete"):
            set_story_flag(flag)
        set_story_value("ch01_d4_lane", d3_lane_value)
        set_story_value("ch01_d4_d3_variant", d5p["d3_variant"])
        set_story_value("ch01_d4_end_route", route)
        set_story_value("ch01_d4_end_route_pending", route)
        for key, value in d5p["d4"].items():
            set_story_value("ch01_d4_" + key, value)
        set_story_value("ch01_d4_ntr_confirmed", route in ("ntr_unresolved", "ntr_confirmed"))
        set_story_value("ch01_d4_ntr_repaired", route == "love_repaired")
        for flag in d5p["flags"]:
            set_story_flag(flag)
        store.equipped_outfit = d5p["d4"]["dusk_outfit_id"] if owns_outfit(d5p["d4"]["dusk_outfit_id"]) else "resort_dinner_dress"

    CHAPTER_SELECT_PRESETS["day4"] = dict(
        label=lc_chapters.select_label("day4"),
        note="Starts at Day Four with Day Two and Day Three marked complete and their end state stored.",
        heading=_("Stored Day Two ending"), routes=CH01_SELECT_END_ROUTES, seed=ch01_d4_select_seed,
    )
