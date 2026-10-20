# Chapter Select (developer / QA / unlockable skip-to-day).
#
# Starts a NEW game at Chapter 1 Day 2, Day 3, Day 4 or Day 5 with a consistent
# preset of the state those days read. It never edits story scenes: it seeds the
# same story values/flags/stats/outfits the real script would have produced and
# then jumps to the normal day entry label (ch01_day2_start / ch01_day3_start /
# ch01_day4_start / ch01_day5_start).
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
        ("day5", "Day Five", "Starts at Day Five with Days Two to Four marked complete and a typical Day Four end state stored."),
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

    CH01_SELECT_DAY4_ROUTES = CH01_SELECT_END_ROUTES + (
        ("disclosure_ready", "Voluntary disclosure / NTS decision"),
    )

    # Day Five presets: the six stored Day Four end routes (ch01_d4_end_route).
    CH01_SELECT_DAY5_ROUTES = (
        ("love", "Love"),
        ("exhibitionism", "Exhibitionism"),
        ("love_repaired", "Love (repaired)"),
        ("nts_discovery", "NTS Discovery"),
        ("ntr_unresolved", "NTR unresolved"),
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

    # Day Four end state seeded for the Day Five presets (a typical playthrough of each route; the choices
    # made are recorded in the values below). "d2" is the Day Two end state that leads to that Day Four lane.
    CH01_SELECT_DAY5_PRESETS = {
        "love": dict(
            d2="love", lane="love", d3_variant="love_private",
            stats=dict(love=57, trust=56, boredom=9, exh=10, cur=20, acc=14, sec=5, bnd=10, tem=10, jea=20),
            d4=dict(end_variant="love_slow_dance", exposure_step="none", exhib_variant="none", photo_style="candid",
                    dusk_outfit_id="resort_dinner_dress", dusk_outfit_source="leia", hook_reply="in", ntr_react=None,
                    ntr_outcome="ntr_confirmed", ntr_fine_count=0, disclosure_when=None, leia_call=None,
                    day_outfit_id="casual_default", day_outfit_source="leia"),
            flags=["ch01_d4_market_honey_bee_callback", "ch01_d4_photo_candid_taken"],
        ),
        "exhibitionism": dict(
            d2="exhibitionism", lane="exhibitionism", d3_variant="exhibition_window",
            stats=dict(love=53, trust=50, boredom=10, exh=38, cur=33, acc=24, sec=5, bnd=10, tem=10, jea=20),
            d4=dict(end_variant="exhib_shared_step", exposure_step="brief_reveal", exhib_variant="shared_step", photo_style="posed",
                    dusk_outfit_id="boutique_cutout_mini", dusk_outfit_source="leia", hook_reply="in", ntr_react=None,
                    ntr_outcome="ntr_confirmed", ntr_fine_count=0, disclosure_when=None, leia_call="brief_reveal",
                    day_outfit_id="casual_default", day_outfit_source="leia"),
            flags=["ch01_d4_market_honey_bee_callback", "ch01_d4_photo_pose_taken", "ch01_d4_exhib_brief_done"],
        ),
        "love_repaired": dict(
            d2="ntr_confirmed", lane="ntr", d3_variant="ntr_restroom_nightmare",
            stats=dict(love=50, trust=60, boredom=16, exh=10, cur=20, acc=12, sec=3, bnd=10, tem=10, jea=20),
            d4=dict(end_variant="ntr_repaired_thanks", exposure_step="none", exhib_variant="none", photo_style="candid",
                    dusk_outfit_id="resort_dinner_dress", dusk_outfit_source="leia", hook_reply="in", ntr_react="thanks",
                    ntr_outcome="love_repaired", ntr_fine_count=0, disclosure_when="harbor_wall", leia_call=None,
                    day_outfit_id="casual_default", day_outfit_source="leia", betrayal_disclosed=True,
                    discovery_source="voluntary_disclosure", ryan_sharing_curiosity=False, leia_future_interest=False,
                    nts_boundaries_discussed=False, nts_future_agreed=False, nts_discovery=False, monitoring_active=False),
            flags=["ch01_d4_market_honey_bee_callback", "ch01_d4_photo_candid_taken", "ch01_d4_cutout_disclosed", "ch01_d4_club_story_deferred"],
        ),
        "nts_discovery": dict(
            d2="ntr_confirmed", lane="ntr", d3_variant="ntr_restroom_nightmare",
            stats=dict(love=49, trust=53, boredom=15, exh=18, cur=32, acc=28, sec=3, bnd=20, tem=10, jea=24),
            d4=dict(end_variant="nts_discovery_conversation", exposure_step="none", exhib_variant="none", photo_style="candid",
                    dusk_outfit_id="resort_dinner_dress", dusk_outfit_source="leia", hook_reply="ask_leia", ntr_react="curious",
                    ntr_outcome="nts_discovery", ntr_fine_count=0, disclosure_when="harbor_wall", leia_call=None,
                    day_outfit_id="casual_default", day_outfit_source="leia", betrayal_disclosed=True,
                    discovery_source="voluntary_disclosure", ryan_sharing_curiosity=True, leia_future_interest=True,
                    nts_boundaries_discussed=True, nts_future_agreed=True, nts_discovery=True, monitoring_active=False,
                    ryan_knows_club_event=True, second_meeting=False),
            flags=["ch01_d4_market_honey_bee_callback", "ch01_d4_photo_candid_taken", "ch01_d4_cutout_disclosed", "ch01_d4_club_story_deferred"],
        ),
        "ntr_unresolved": dict(
            d2="mixed_unresolved", lane="ntr", d3_variant="ntr_restroom_nightmare",
            stats=dict(love=43, trust=50, boredom=25, exh=10, cur=20, acc=11, sec=9, bnd=12, tem=10, jea=25),
            d4=dict(end_variant="ntr_unresolved", exposure_step="none", exhib_variant="none", photo_style="candid",
                    dusk_outfit_id="resort_dinner_dress", dusk_outfit_source="leia", hook_reply="maybe", ntr_react=None,
                    ntr_outcome="ntr_unresolved", ntr_fine_count=0, disclosure_when=None, leia_call=None,
                    day_outfit_id="casual_default", day_outfit_source="leia"),
            flags=["ch01_d4_market_honey_bee_callback", "ch01_d4_photo_candid_taken", "ch01_d4_cutout_partial"],
        ),
        "ntr_confirmed": dict(
            d2="ntr_confirmed", lane="ntr", d3_variant="ntr_restroom_nightmare",
            stats=dict(love=35, trust=45, boredom=33, exh=10, cur=20, acc=12, sec=10, bnd=12, tem=15, jea=20),
            d4=dict(end_variant="ntr_confirmed", exposure_step="none", exhib_variant="none", photo_style="skipped",
                    dusk_outfit_id="resort_dinner_dress", dusk_outfit_source="leia", hook_reply="maybe", ntr_react=None,
                    ntr_outcome="ntr_confirmed", ntr_fine_count=3, disclosure_when=None, leia_call=None,
                    day_outfit_id="casual_default", day_outfit_source="leia"),
            flags=["ch01_d4_market_honey_bee_callback", "ch01_d4_ntr_soft_gate", "ch01_d4_photo_skipped", "ch01_d4_cutout_partial"],
        ),
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
        # Optional extra stats (Day Five presets only).
        for _k, _stat in (("sec", "secrecy"), ("bnd", "boundary_looseness"), ("tem", "temptation")):
            if _k in stats:
                store.partner_stats[_stat] = stats[_k]
        if "jea" in stats:
            store.player_stats["jealousy"] = stats["jea"]
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
        preset_route = route
        disclosure_ready = day == "day4" and route == "disclosure_ready"
        if disclosure_ready:
            route = "ntr_confirmed"
        if day == "day2":
            p = CH01_SELECT_DAY2_PRESETS[route]
            _chapter_select_reset(p["stats"], p["hist"], p["pressure"])
            entry = "ch01_day2_start"
        else:
            # Day Five presets are keyed by the Day Four end route; "base" is the Day Two end state behind it.
            d5p = CH01_SELECT_DAY5_PRESETS[route] if day == "day5" else None
            base = d5p["d2"] if d5p else route
            p = CH01_SELECT_END_PRESETS[base]
            _chapter_select_reset(d5p["stats"] if d5p else p["stats"], p["hist"], p["pressure"])
            lane = p["lane"]
            set_story_value("ch01_d2_end_route", base)
            set_story_value("ch01_d2_bedroom_variant", p["bedroom"])
            for part in ("pre_split", "post_pool", "post_sunset", "dinner"):
                set_story_value("ch01_d2_route_lane_" + part, lane)
            set_story_value("ch01_d2_ntr_soft_gate", p["soft_gate"])
            set_story_value("ch01_d2_dinner_wink", p["wink"])
            set_story_value("ch01_d2_ntr_confirmed", p["confirmed"])
            if base == "love_repaired":
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
                d3_lane_value = "ntr" if base in ("ntr_confirmed", "mixed_unresolved") else ("exhibitionism" if base == "exhibitionism" else "love")
                set_story_value("ch01_d3_lane", d3_lane_value)
                set_story_value("ch01_d3_end_variant", {"love": "love_private", "exhibitionism": "exhibition_window", "ntr": "ntr_restroom_nightmare"}[d3_lane_value])
                # Day Four also reads these Day Three values (same values Day Three writes).
                if d3_lane_value == "ntr":
                    set_story_value("ch01_d3_ntr_repair_effort", "enjoy")  # Day Three's own default when unset
                    set_story_value("ch01_d3_maya_dessert", "chocolate")
                    set_story_flag("ch01_d3_cutout_secret")
                else:
                    set_story_value("ch01_d3_ntr_repair_effort", "none")
                if day == "day4" and d3_lane_value == "ntr":
                    ch01_d3_record_club_event()
                    if disclosure_ready:
                        set_story_value("ch01_d3_ntr_repair_effort", "talk")
                entry = "ch01_day4_start"
                if day == "day5":
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
                    if route == "nts_discovery":
                        set_story_value("ch01_d3_club_event", "affair")
                        set_story_value("ch01_d3_club_contact_id", "adrian_vale")
                        set_story_value("ch01_d3_club_contact_active", True)
                        set_story_value("ch01_d3_club_private_photos", True)
                        set_story_value("ch01_d3_leia_knows_club_event", True)
                        set_story_value("ch01_d4_leia_knows_discovery", False)
                    set_story_value("ch01_d4_ntr_confirmed", route in ("ntr_unresolved", "ntr_confirmed"))
                    set_story_value("ch01_d4_ntr_repaired", route == "love_repaired")
                    for flag in d5p["flags"]:
                        set_story_flag(flag)
                    if route in ("love_repaired", "nts_discovery", "ntr_confirmed"):
                        ch01_d3_record_club_event()
                    if route in ("love_repaired", "nts_discovery"):
                        set_story_value("ch01_d3_club_contact_active", False)
                        set_story_value("ch01_d4_betrayal_disclosed", True)
                        set_story_value("ch01_d4_discovery_source", "voluntary_disclosure")
                        set_story_value("ch01_d4_ryan_knows_club_event", True)
                        set_story_value("ch01_d4_leia_knows_discovery", False)
                    if route == "ntr_confirmed":
                        ch01_d4_discover_club()
                        ch01_d4_enable_monitoring("chapter_select_confirmed_ntr")
                        ch01_d4_record_second_meeting()
                    store.equipped_outfit = d5p["d4"]["dusk_outfit_id"] if owns_outfit(d5p["d4"]["dusk_outfit_id"]) else "resort_dinner_dress"
                    entry = "ch01_day5_start"
        set_story_flag("chapter_select_used")
        if disclosure_ready:
            set_story_value("chapter_select_disclosure_hint", True)
        set_story_value("chapter_select_preset", "{}:{}".format(day, preset_route))
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
    elif _cs_entry == "ch01_day5_start":
        jump ch01_day5_start
    else:
        jump ch01_day4_start
