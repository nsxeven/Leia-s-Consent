# Chapter Select (developer / QA / unlockable skip-to-day).
#
# Starts a NEW game at Chapter 1 Day 2, Day 3 or Day 4 with a consistent
# preset of the state those days read. It never edits story scenes: it seeds the
# same story values/flags/stats/outfits the real script would have produced and
# then jumps to the normal day entry label (ch01_day2_start / ch01_day3_start /
# ch01_day4_start).
#
# UNLOCK RULE (one line to flip):
#   CHAPTER_SELECT_RULE = "developer_or_unlocked"   # default
#     "always"                -> always shown on the main menu
#     "developer"             -> only when config.developer is true
#     "unlocked"              -> only after persistent.ch01_chapter_select_unlocked
#                                (set automatically the first time Day 2 is finished)
#     "developer_or_unlocked" -> either of the above
#     "never"                 -> hidden
# persistent.ch01_chapter_select_unlocked is set by a wrapper around set_story_flag
# when "ch01_day_02_complete" is set, so no story scene had to change.

define CHAPTER_SELECT_RULE = "developer_or_unlocked"

init 10 python:

    CH01_SELECT_DAYS = (
        ("day2", "Day Two", "Starts at the Day Two title card; the Day Two lane still depends on your choices."),
        ("day3", "Day Three", "Starts at Day Three with the chosen Day Two ending stored."),
        ("day4", "Day Four", "Starts at Day Four with Day Two and Day Three marked complete and their end state stored."),
    )

    # Day Two entry presets: seeds only. The real end state is decided by play.
    CH01_SELECT_DAY2_ROUTES = (
        ("love", "Love lane"),
        ("exhibitionism", "Exhibitionism lane"),
        ("ntr_risk", "NTR-risk lane"),
    )

    # Day Three / Four presets: the five stored Day Two end states.
    CH01_SELECT_END_ROUTES = (
        ("love", "Love"),
        ("exhibitionism", "Exhibitionism"),
        ("love_repaired", "Love (repaired)"),
        ("mixed_unresolved", "Mixed / unresolved"),
        ("ntr_confirmed", "NTR confirmed"),
    )

    # Per end-state values. "lane" is the Day Two lane vocabulary (love / exhibitionism / ntr_risk).
    CH01_SELECT_END_PRESETS = {
        "love": dict(
            lane="love", bedroom="love_private", soft_gate=False, wink=False, confirmed=False,
            pool_suspicion=False, pressure="mixed", stats=dict(love=60, trust=58, boredom=5, exh=10, cur=20, acc=10), hist=[],
        ),
        "exhibitionism": dict(
            lane="exhibitionism", bedroom="exhibition_open_curtains", soft_gate=False, wink=False, confirmed=False,
            pool_suspicion=False, pressure="nts_seeded", stats=dict(love=55, trust=55, boredom=8, exh=25, cur=26, acc=16), hist=["ch01_d2_morning_tease"],
        ),
        "love_repaired": dict(
            lane="ntr_risk", bedroom="ntr_gate_repaired", soft_gate=True, wink=True, confirmed=False,
            pool_suspicion=True, pressure="ntr_seeded", stats=dict(love=48, trust=48, boredom=15, exh=10, cur=20, acc=10), hist=["ch01_d2_morning_dismiss"],
        ),
        "mixed_unresolved": dict(
            lane="ntr_risk", bedroom="pool_suspicion_unresolved", soft_gate=False, wink=False, confirmed=False,
            pool_suspicion=True, pressure="ntr_seeded", stats=dict(love=44, trust=44, boredom=20, exh=10, cur=20, acc=10), hist=["ch01_d2_morning_dismiss"],
        ),
        "ntr_confirmed": dict(
            lane="ntr_risk", bedroom="ntr_gate_accusation", soft_gate=True, wink=True, confirmed=True,
            pool_suspicion=True, pressure="ntr_seeded", stats=dict(love=40, trust=40, boredom=24, exh=10, cur=20, acc=10), hist=["ch01_d2_morning_dismiss"],
        ),
    }

    # Day Two lane seeds (state at ch01_day2_start, not at the end of Day Two).
    CH01_SELECT_DAY2_PRESETS = {
        "love": dict(pressure="mixed", stats=dict(love=50, trust=50, boredom=10, exh=10, cur=20, acc=10), hist=[]),
        "exhibitionism": dict(pressure="nts_seeded", stats=dict(love=50, trust=50, boredom=10, exh=25, cur=26, acc=16), hist=["ch01_d2_morning_tease"]),
        "ntr_risk": dict(pressure="ntr_seeded", stats=dict(love=44, trust=50, boredom=20, exh=10, cur=20, acc=10), hist=["ch01_d2_morning_dismiss"]),
    }

    def chapter_select_unlocked():
        """True when the main-menu Chapter Select entry should be offered."""
        rule = store.CHAPTER_SELECT_RULE
        dev = bool(config.developer)
        unlocked = bool(getattr(persistent, "ch01_chapter_select_unlocked", False))
        if rule == "always":
            return True
        if rule == "developer":
            return dev
        if rule == "unlocked":
            return unlocked
        if rule == "developer_or_unlocked":
            return dev or unlocked
        return False

    def _chapter_select_reset(stats, hist, pressure):
        store.story_flags = {}
        store.story_values = {}
        store.relationship_stats.update({"love": stats["love"], "trust": stats["trust"], "boredom": stats["boredom"], "momentum": 0})
        store.partner_stats.update({"curiosity": stats["cur"], "exhibitionism": stats["exh"]})
        store.player_stats.update({"acceptance": stats["acc"]})
        store.choice_history = list(hist)
        store.last_choice_id = None
        store.owned_outfits = ["casual_default"]
        store.equipped_outfit = "casual_default"
        store.money = 500
        set_phone_unlocked(True)
        set_phone_hud_enabled(True)
        # Day One is treated as finished.
        for flag in ("prologue_started", "ch01_started", "ch01_scene_30_complete", "ch01_day_01_complete", "ch01_scenes_14_30_complete"):
            set_story_flag(flag)
        set_story_value("ch01_day1_route_pressure", pressure)
        set_story_value("ch01_dream_response", "grounded")

    def chapter_select_apply(day, route):
        """Seed a new game for the chosen day and route preset. Returns the entry label."""
        if day == "day2":
            p = CH01_SELECT_DAY2_PRESETS[route]
            _chapter_select_reset(p["stats"], p["hist"], p["pressure"])
            entry = "ch01_day2_start"
        else:
            p = CH01_SELECT_END_PRESETS[route]
            _chapter_select_reset(p["stats"], p["hist"], p["pressure"])
            lane = p["lane"]
            set_story_value("ch01_d2_end_route", route)
            set_story_value("ch01_d2_bedroom_variant", p["bedroom"])
            for part in ("pre_split", "post_pool", "post_sunset", "dinner"):
                set_story_value("ch01_d2_route_lane_" + part, lane)
            set_story_value("ch01_d2_ntr_soft_gate", p["soft_gate"])
            set_story_value("ch01_d2_dinner_wink", p["wink"])
            set_story_value("ch01_d2_ntr_confirmed", p["confirmed"])
            if route == "love_repaired":
                set_story_value("ch01_d2_ntr_soft_gate_repaired", True)
            if p["pool_suspicion"]:
                set_story_flag("ch01_d2_pool_suspicion")
            # Boutique: Black Cutout Mini owned, bought by Leia (Day Three text assumes she owns it).
            set_story_value("ch01_d2_mall_outfit_source", "leia")
            set_story_flag("ch01_d2_boutique_shop_open")
            set_story_flag("ch01_d2_boutique_outfit_owned")
            set_story_flag("ch01_d2_boutique_black_mini_reserved_day3")
            for outfit_id in ("boutique_cutout_mini", "resort_dinner_dress"):
                grant_story_outfit(outfit_id, equip=False)
            set_story_value("ch01_d2_dinner_outfit", "secure_date")
            set_story_value("ch01_d2_dinner_outfit_id", "resort_dinner_dress")
            set_story_value("ch01_d2_dinner_outfit_source", "leia")
            store.equipped_outfit = "resort_dinner_dress"
            for flag in ("ch01_day_02_started", "ch01_d2_scene_30_complete", "ch01_day_02_complete"):
                set_story_flag(flag)
            if day == "day3":
                entry = "ch01_day3_start"
            else:
                for flag in ("ch01_day_03_started", "ch01_d3_complete", "ch01_day_03_complete"):
                    set_story_flag(flag)
                # Same mapping ch01_day3_start uses.
                d3_lane_value = "ntr" if route in ("ntr_confirmed", "mixed_unresolved") else ("exhibitionism" if route == "exhibitionism" else "love")
                set_story_value("ch01_d3_lane", d3_lane_value)
                set_story_value("ch01_d3_end_variant", {"love": "love_private", "exhibitionism": "exhibition_window", "ntr": "ntr_restroom_nightmare"}[d3_lane_value])
                # Day Four also reads these Day Three values (same values Day Three writes).
                if d3_lane_value == "ntr":
                    set_story_value("ch01_d3_ntr_repair_effort", "enjoy")  # Day Three's own default when unset
                    set_story_value("ch01_d3_maya_dessert", "chocolate")
                    set_story_flag("ch01_d3_cutout_secret")
                else:
                    set_story_value("ch01_d3_ntr_repair_effort", "none")
                entry = "ch01_day4_start"
        set_story_flag("chapter_select_used")
        set_story_value("chapter_select_preset", "{}:{}".format(day, route))
        return entry

    # Unlock after the first completed Day Two, without editing any story scene.
    _chapter_select_orig_set_story_flag = set_story_flag

    def set_story_flag(flag_id, value=True):
        result = _chapter_select_orig_set_story_flag(flag_id, value)
        if flag_id == "ch01_day_02_complete" and value:
            if not getattr(persistent, "ch01_chapter_select_unlocked", False):
                persistent.ch01_chapter_select_unlocked = True
        return result


label ch01_chapter_select_entry:
    # Entered from the Chapter Select screen (Start) with the choice stored in
    # persistent.ch01_chapter_select_pending = (day, route).
    $ _cs_pending = persistent.ch01_chapter_select_pending or ("day3", "love")
    $ _cs_entry = chapter_select_apply(_cs_pending[0], _cs_pending[1])
    $ persistent.ch01_chapter_select_pending = None
    if _cs_entry == "ch01_day2_start":
        jump ch01_day2_start
    elif _cs_entry == "ch01_day3_start":
        jump ch01_day3_start
    else:
        jump ch01_day4_start
