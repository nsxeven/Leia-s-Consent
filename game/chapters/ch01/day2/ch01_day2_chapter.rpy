# Day Two pack - chapter: title-card text, review row and Chapter Select preset. The chapter registry entry (titles) is CHAPTER in
#   game/python-packages/lc_days/day2.py.
#
# Where every kind of content goes: docs/DAY_PACK.md.

# Opening title card (neutral title for everyone), shown by the Day's start label.
define lc_chapter_card_day2 = lc_chapters.card_text("day2")
# Title-card accent (screens/lc_title_cards.rpy), matching this Day's gallery tab.
define lc_title_card_accent_day2 = "#70566f"

# End-of-day review: this Day's row (systems/day_review.rpy). route_key = the end-route story key.
init 1 python:
    import lc_chapters
    LC_REVIEW_DAYS["ch01_d2"] = {"label": lc_chapters.review_label("day2"), "chapter": "day2", "route_key": "ch01_d2_end_route"}
    LC_REVIEW_NIGHT["ch01_d2"] = ("DAY 2", lc_chapters.chapter_title("day2").upper(), "the lights along the water go low…")  # night card: day, neutral title, caption
    LC_REVIEW_TICKET["ch01_d2"] = ("SHORE PASS", "DAY TWO")  # ticket stub: title, detail

# Chapter Select (systems/chapter_select.rpy): the Day Two preset, the five stored Day Two end
#   states the Day Three / Four presets use, and the seed for "Day Two finished".
init 1 python:
    import lc_chapters

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
            pool_suspicion=False, pressure="mixed", stats=dict(love=60, trust=58, exh=10, tem=5), hist=[],
        ),
        "exhibitionism": dict(
            lane="exhibitionism", bedroom="exhibition_open_curtains", soft_gate=False, wink=False, confirmed=False,
            pool_suspicion=False, pressure="nts_seeded", stats=dict(love=55, trust=55, exh=43, tem=8), hist=["ch01_d2_morning_tease"],
        ),
        "love_repaired": dict(
            lane="ntr_risk", bedroom="ntr_gate_repaired", soft_gate=True, wink=True, confirmed=False,
            pool_suspicion=True, pressure="ntr_seeded", stats=dict(love=48, trust=48, exh=10, tem=15), hist=["ch01_d2_morning_dismiss"],
        ),
        "mixed_unresolved": dict(
            lane="ntr_risk", bedroom="pool_suspicion_unresolved", soft_gate=False, wink=False, confirmed=False,
            pool_suspicion=True, pressure="ntr_seeded", stats=dict(love=44, trust=44, exh=10, tem=20), hist=["ch01_d2_morning_dismiss"],
        ),
        "ntr_confirmed": dict(
            lane="ntr_risk", bedroom="ntr_gate_accusation", soft_gate=True, wink=True, confirmed=True,
            pool_suspicion=True, pressure="ntr_seeded", stats=dict(love=40, trust=40, exh=10, tem=24), hist=["ch01_d2_morning_dismiss"],
        ),
    }

    # Day Two lane seeds (state at ch01_day2_start, not at the end of Day Two).
    CH01_SELECT_DAY2_PRESETS = {
        "love": dict(pressure="mixed", stats=dict(love=50, trust=50, exh=10, tem=10), hist=[]),
        "exhibitionism": dict(pressure="nts_seeded", stats=dict(love=50, trust=50, exh=40, tem=10), hist=["ch01_d2_morning_tease"]),
        "ntr_risk": dict(pressure="ntr_seeded", stats=dict(love=44, trust=50, exh=10, tem=20), hist=["ch01_d2_morning_dismiss"]),
    }

    # The first finished Day Two unlocks Chapter Select (chapter_select_unlock_after_day_two).
    def ch01_d2_select_seed(route):
        """Chapter Select "Day Two" preset: Day One done, the Day Two lane seeds; returns the entry label."""
        p = CH01_SELECT_DAY2_PRESETS[route]
        _chapter_select_reset(p["stats"], p["hist"])
        ch01_d1_select_finished(p["pressure"])
        return "ch01_day2_start"

    def ch01_d2_select_finished(base, stats=None):
        """Chapter Select: Days One and Two finished on Day Two end state `base` (CH01_SELECT_END_PRESETS);
        `stats` replaces the end state's stats. Returns the end-state preset."""
        p = CH01_SELECT_END_PRESETS[base]
        _chapter_select_reset(p["stats"] if stats is None else stats, p["hist"])
        ch01_d1_select_finished(p["pressure"])
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
        # Every Day Two path installs the feed app on the photo walk (systems/feed.rpy).
        lc_feed_install()
        ch01_d2_select_phone(base)
        return p

    # Ryan's answer to the changing-room selfie (a scored story menu) for each stored end state:
    # the route-consistent pick (warm for Love, open for Exhibitionism, playful for the mixed night,
    # flat for confirmed NTR). The preset's stats already include it, so nothing is scored here.
    CH01_SELECT_D2_SELFIE_REPLY = {
        "love": "affection", "love_repaired": "affection", "exhibitionism": "open",
        "mixed_unresolved": "tease", "ntr_confirmed": "flat",
    }

    def ch01_d2_select_phone(base):
        """Chapter Select: Day Two's phone as a player who read every chat has it at Day Three's start.
        Reply cards take their defaults: Maya's lunch check-in "alive", her late DM left on read."""
        chapter_select_phone("group", "julian", "ch01_d2_julian_wake_up", "Bro wake up", display_time="11:00")
        chapter_select_phone("maya", "maya", "ch01_d2_maya_lunch_checkin",
                             "You people alive? I'm near the resort around lunch. Still meeting?")
        chapter_select_phone("maya", "player", "ch01_d2_maya_lunch_reply_ryan",
                             "Alive. Barely. Lunch works, I'll send you where we are.")
        chapter_select_phone("maya", "maya", "ch01_d2_maya_lunch_reply_followup_01", "Look at you, being organized 👍")
        chapter_select_phone_reply("ch01_d2_maya_lunch_reply", "alive")
        chapter_select_phone("group", "system", "ch01_trip_group_maya_added", friend_name + " added Maya to the group.")
        chapter_select_phone("group", "system", "ch01_trip_group_four_photo", friend_name + " changed the group picture.")
        chapter_select_phone_group("four", maya_member=True)
        chapter_select_phone("group", "maya", "ch01_trip_group_maya_first_post", "First post as an official member. You're welcome.",
                             attachment_id="ch01_d2_leia_maya_selfie", attachment_label=girlfriend_name + " and Maya")
        chapter_select_phone("leia", "leia", "ch01_d2_boutique_selfie", "", attachment_id="ch01_d2_changing_room_selfie",
                             attachment_label=girlfriend_name + " in the changing room")
        chapter_select_phone("leia", "leia", "ch01_d2_boutique_selfie_ask", "Be honest. Is this too much?? Maya picked it. Obviously.")
        reply = CH01_SELECT_D2_SELFIE_REPLY.get(base, "affection")
        if reply == "affection":
            chapter_select_phone("leia", "player", "ch01_d2_boutique_selfie_reply", "You look incredible.")
            chapter_select_phone("leia", "leia", "ch01_d2_boutique_selfie_followup", "You have to say that. You're biased.")
        elif reply == "open":
            chapter_select_phone("leia", "player", "ch01_d2_boutique_selfie_reply", "Didn't know you had that in you.")
            chapter_select_phone("leia", "leia", "ch01_d2_boutique_selfie_followup", "I DON'T. This is all Maya. I'm just standing in it.")
        elif reply == "tease":
            chapter_select_phone("leia", "player", "ch01_d2_boutique_selfie_reply", "Maya really did this to you?")
            chapter_select_phone("leia", "leia", "ch01_d2_boutique_selfie_followup", "Against my better judgment. VERY much against it.")
        else:
            chapter_select_phone("leia", "player", "ch01_d2_boutique_selfie_reply", "It's... nice.")
            chapter_select_phone("leia", "leia", "ch01_d2_boutique_selfie_followup", "Nice.")
        chapter_select_phone("leia", "leia", "ch01_d2_boutique_selfie_stay",
                             "Don't come over here. I'm not coming out in this. Changing room only.")
        chapter_select_phone("maya", "maya", "ch01_d2_maya_dm_01", "you two okay in there? 👀", display_time="23:52")
        chapter_select_phone("maya", "maya", "ch01_d2_maya_dm_02",
                             "asking because it's very quiet through this wall and [friend_name] is pretending to be asleep. badly.",
                             display_time="23:52")
        chapter_select_phone_reply("ch01_d2_maya_dm", "read", left_on_read="maya", time="23:52")

    CHAPTER_SELECT_PRESETS["day2"] = dict(
        label=lc_chapters.select_label("day2"),
        note="Starts at the Day Two title card; the Day Two lane still depends on your choices.",
        heading=_("Day Two lane preset"), routes=CH01_SELECT_DAY2_ROUTES, seed=ch01_d2_select_seed,
        unlock_flag="ch01_day_02_complete",
    )
