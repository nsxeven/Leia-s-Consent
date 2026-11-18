# Day Three pack - registrations: choice effects (the effective, stat-model-v2 scoring) and
#   tags, and the story-key ledger.
#
# Where every kind of content goes: docs/DAY_PACK.md. Scoring rules: docs/STAT_MODEL.md.
# Load order: init 1 (the engine tables exist at init <= 0).

init 1 python:
    # Day Three's two menus. Ordinary scale (+/-1..2), same as Day Two's
    # mid-day choices and Day Four's non-gate choices. Not a route lock:
    # the lane is already set, and Day Four still reads that lane.
    CHOICE_EFFECTS.update({
        "ch01_d3_ntr_enjoy": [
            ("relationship", "love", 1),
            ("relationship", "temptation", -1),
        ],
        "ch01_d3_ntr_talk": [
            ("relationship", "love", 2),
            ("relationship", "temptation", -3),
        ],
        "ch01_d3_ntr_withdraw": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 2),
        ],
        "ch01_d3_dessert_chocolate": [
            ("relationship", "trust", 1),
        ],
        "ch01_d3_dessert_recommended": [],  # Neutral: no stats
        "ch01_d3_dessert_surprise": [
            ("relationship", "love", 1),
        ],
    })

    CHOICE_TAGS.update({
        "ch01_d3_ntr_enjoy": ("supportive", "attentive", "repair"),
        "ch01_d3_ntr_talk": ("supportive", "attentive", "honest", "repair"),
        "ch01_d3_ntr_withdraw": ("neutral", "nonchalant", "dismissive", "withdrawal"),
        "ch01_d3_dessert_chocolate": ("supportive", "attentive"),
        "ch01_d3_dessert_recommended": ("neutral", "trusting"),
        "ch01_d3_dessert_surprise": ("encouraging", "playful", "lighthearted"),
    })

# Full "Current lean" (systems/stats.rpy lc_current_lean): Day Three's reader.
init 1 python:
    def ch01_d3_current_lean(lean, flat):
        """current_lean hook: the Day Three / Four lane once Day Three has started."""
        if has_story_flag("ch01_day_03_started"):
            lane = get_story_value("ch01_d4_lane", None) or get_story_value("ch01_d3_lane", None)
            if (lane == "love" and get_story_value("ch01_d3_strained_love", False)
                    and not has_story_flag("ch01_day_03_complete")):
                return "strained"
            if lane:
                return lc_stat_model.lean_from_route_value(lane)
        return lean

    lc_hook_add("current_lean", ch01_d3_current_lean)


# ------------------------------------------------------------------ story-key ledger
# Every story flag / value this Day sets, one line each (tests/test_day_packs.py checks it):
#   # key <name>: read-by <who reads it>     or     # key <name>: pending <why nothing reads it yet>
# Patterns with * cover dynamic keys. Keys are save data: never rename one.
# key ch01_d3_complete: read-by chapter_select.rpy
# key ch01_d3_cutout_consent_established: pending set by ch01_day3_scenes.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d3_cutout_secret: read-by ch01_day4_registrations.rpy, ch01_day4_scenes_01_08.rpy
# key ch01_d3_cutout_stranger_choice: pending set by ch01_day3_scenes.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d3_end_variant: read-by ch01_day4_registrations.rpy, ch01_day4_scenes_01_08.rpy
# key ch01_d3_lane: read-by ch01_day3_chapter.rpy, ch01_day4_scenes_01_08.rpy, ch01_day5_scenes_01_08.rpy +1 more
# key ch01_d3_maya_dessert: read-by ch01_day4_scenes_01_08.rpy
# key ch01_d3_ntr_repair_effort: read-by ch01_day3_scenes.rpy, ch01_day4_registrations.rpy, day_review.rpy
# key ch01_d3_strained_love: read-by ch01_day3_scenes.rpy, day_review.rpy, stats.rpy
# key ch01_day_03_complete: read-by chapter_select.rpy, lc_ui_logic.py, stats.rpy
# key ch01_day_03_started: read-by chapter_select.rpy, lc_ui_logic.py, stats.rpy
