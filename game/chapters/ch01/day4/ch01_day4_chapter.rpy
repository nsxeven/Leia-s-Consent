# Day Four pack - chapter: title-card text, review row and Chapter Select preset. The chapter registry entry (titles) is CHAPTER in
#   game/python-packages/lc_days/day4.py.
#
# Where every kind of content goes: docs/DAY_PACK.md.

# Opening title card (neutral title for everyone), shown by the Day's start label.
define lc_chapter_card_day4 = lc_chapters.card_text("day4")
# Title-card accent (screens/lc_title_cards.rpy), matching this Day's gallery tab.
define lc_title_card_accent_day4 = "#556b78"

# "CHAPTER 4 COMPLETE" heading (temporary end-of-build card).
define lc_chapter_complete_card_day4 = lc_chapters.complete_card_text("day4")

# End-of-day review: this Day's row (systems/day_review.rpy). route_key = the end-route story key.
init 1 python:
    import lc_chapters
    LC_REVIEW_DAYS["ch01_d4"] = {"label": lc_chapters.review_label("day4"), "chapter": "day4", "route_key": "ch01_d4_end_route"}
    LC_REVIEW_NIGHT["ch01_d4"] = ("DAY 4", lc_chapters.chapter_title("day4").upper(), "the town folds up its awnings…")  # night card: day, neutral title, caption
    LC_REVIEW_TICKET["ch01_d4"] = ("MARKET DAY", "ONE STUB")  # ticket stub: title, detail

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
        ch01_d4_select_phone(route, d5p, d3_lane_value)

    # Ryan's answer to Leia's morning text (a scored story menu) for each stored Day Four end route:
    # warm on Love, the flirt on Exhibitionism; on the NTR lane the join for the repaired night, the
    # "twenty minutes" for the unresolved one and "I'm fine" for confirmed NTR (its ntr_fine_count).
    CH01_SELECT_D4_MORNING_REPLY = {
        "love": "warm", "exhibitionism": "flirt", "love_repaired": "join",
        "ntr_unresolved": "later", "ntr_confirmed": "fine",
    }

    def ch01_d4_select_phone(route, d5p, lane):
        """Chapter Select: Day Four's phone as a player who read every chat has it at Day Five's start,
        following the preset's stored Day Four values (lane, photo style, boat reply)."""
        chapter_select_phone("group", "julian", "ch01_d4_group_breakfast_julian",
                             "Breakfast is at ten. I have personally supervised the pancakes. Do not make me regret it.")
        chapter_select_phone("group", "maya", "ch01_d4_group_breakfast_maya",
                             (friend_name + ' does not cook. ' + friend_name + ' supervised a chef named Teodoro.'))
        chapter_select_phone("group", "maya", "ch01_d4_group_maya_police_growth", "Day one it was 11 or he called the police. Growth.")
        chapter_select_phone("group", "julian", "ch01_d4_group_julian_energy", "I contributed energy.")
        chapter_select_phone("group", "maya", "ch01_d4_group_maya_shoes",
                             "Comfortable shoes today. We are walking. Outfit advice after that is billable. I charge by the hour.")
        morning = CH01_SELECT_D4_MORNING_REPLY.get(route, "warm")
        if lane == "love":
            chapter_select_phone("leia", "leia", "ch01_d4_leia_morning_text",
                                 "I'm three feet away and I'm texting you. Please note how romantic this is.")
        elif lane == "exhibitionism":
            chapter_select_phone("leia", "leia", "ch01_d4_leia_morning_text",
                                 "I'm at the window. The sheet is doing its best. You should come and supervise.")
        if lane != "ntr":
            if morning == "flirt":
                chapter_select_phone("leia", "player", "ch01_d4_player_text_flirt", "Come closer and I'll make it better.")
            else:
                chapter_select_phone("leia", "player", "ch01_d4_player_text_warm", "Best three feet of my whole week.")
        else:
            chapter_select_phone("leia", "leia", "ch01_d4_leia_morning_ntr_1", "Morning.")
            chapter_select_phone("leia", "leia", "ch01_d4_leia_morning_ntr_2", "Coffee's on the terrace if you want some. No pressure.")
            if morning == "join":
                chapter_select_phone("leia", "player", "ch01_d4_player_ntr_join", "Be right down. Save me the good chair.")
                chapter_select_phone("leia", "leia", "ch01_d4_leia_morning_ntr_3",
                                     "The good chair is the one that wobbles. I'm keeping it warm.")
            elif morning == "later":
                chapter_select_phone("leia", "player", "ch01_d4_player_ntr_later", "Give me twenty minutes.")
                chapter_select_phone("leia", "leia", "ch01_d4_leia_morning_ntr_3", "Okay.")
            else:
                chapter_select_phone("leia", "player", "ch01_d4_player_ntr_fine", "I'm fine. Go ahead without me.")
                chapter_select_phone("leia", "leia", "ch01_d4_leia_morning_ntr_3", "Okay.")
        style = d5p["d4"]["photo_style"]
        if style == "candid":
            chapter_select_phone("leia", "player", "ch01_d4_leia_photo_candid",
                                 "Maya's prompt one. Your person, looking like themselves.",
                                 attachment_id="ch01_d4_photo_candid", attachment_label=(girlfriend_name + ', market, candid'))
            chapter_select_phone("leia", "leia", "ch01_d4_leia_photo_candid_reply",
                                 "Okay that's actually good. Send it to me. Do not send it to Maya.")
        elif style == "posed":
            chapter_select_phone("leia", "player", "ch01_d4_leia_photo_pose",
                                 "Maya's prompt one. Your person, looking like themselves.",
                                 attachment_id="ch01_d4_photo_pose", attachment_label=(girlfriend_name + ', sunglasses stall, posed'))
            chapter_select_phone("leia", "leia", "ch01_d4_leia_photo_pose_reply",
                                 "That is a very good picture of a woman who is pretending not to like it.")
        elif style == "swap":
            chapter_select_phone("leia", "leia", "ch01_d4_leia_photo_swap_reply",
                                 "Saving the one I took of you. You look terrified. For the box.")
        chapter_select_phone("maya", "maya", "ch01_d4_maya_dress_code",
                             "Dinner terrace, eight. Dress code: look like you're being photographed by someone who loves you. Advice is billable. I charge by the hour.")
        if style in ("candid", "posed", "swap"):
            chapter_select_phone("leia", "leia", "ch01_d4_leia_dinner_toast", "Your toast was good. Do not tell Maya I said so.")
        chapter_select_phone("group", "julian", "ch01_d4_group_day5_announce",
                             "Announcement. Pack for the water. Two nights. My family's boat is hungry for guests. Everyone. Yes, you two.")
        chapter_select_phone("group", "maya", "ch01_d4_group_day5_maya", "He says 'hungry for guests' like it's a haunted house.")
        chapter_select_phone("group", "julian", "ch01_d4_group_day5_julian_boat", "It's a boat.")
        chapter_select_phone("group", "maya", "ch01_d4_group_day5_maya_haunted", "It's a haunted boat.")
        if lane == "love":
            chapter_select_phone("leia", "leia", "ch01_d4_leia_day5_love",
                                 "I have a plan for the boat. You'll like it. It involves very little rope.")
        elif lane == "exhibitionism":
            chapter_select_phone("maya", "maya", "ch01_d4_maya_day5_exhib", "Dress code for the boat: brave. Billing: pending.")
            chapter_select_phone("leia", "leia", "ch01_d4_leia_day5_exhib", (player_name + '. I have an idea. Tell you tomorrow. Say yes now.'))
        elif route == "love_repaired":
            chapter_select_phone("leia", "leia", "ch01_d4_leia_day5_ntr_repaired",
                                 "Thank you for tonight. Tomorrow I'll tell you the rest. All of it.")
        elif route == "ntr_unresolved":
            chapter_select_phone("leia", "leia", "ch01_d4_leia_day5_ntr_unresolved", "Sorry.")
        else:
            chapter_select_phone("maya", "maya", "ch01_d4_maya_day5_ntr_confirmed",
                                 "I'm not taking sides. I'm taking both of you to breakfast. Be there.")
            chapter_select_phone("julian", "julian", "ch01_d4_julian_day5_ntr_confirmed",
                                 "Hey. Whatever it is, I'm here. Not as a referee. As your friend.")
        hook = d5p["d4"]["hook_reply"]
        if hook == "in":
            chapter_select_phone("group", "player", "ch01_d4_player_hook_in", "We're in.")
            chapter_select_phone("group", "maya", "ch01_d4_group_hook_reply_in", "Say it with more enthusiasm.")
        elif hook == "ask_leia":
            chapter_select_phone("group", "player", "ch01_d4_player_hook_ask", ('Let me check with ' + girlfriend_name + ' first.'))
            chapter_select_phone("group", "julian", "ch01_d4_group_hook_reply_ask", "That's the right answer. Annoying, but right.")
        else:
            chapter_select_phone("group", "player", "ch01_d4_player_hook_maybe", "Depends on tomorrow morning.")
            chapter_select_phone("group", "maya", "ch01_d4_group_hook_reply_maybe",
                                 "Tomorrow morning is a very long time. See you on the dock.")

    CHAPTER_SELECT_PRESETS["day4"] = dict(
        label=lc_chapters.select_label("day4"),
        note="Starts at Day Four with Day Two and Day Three marked complete and their end state stored.",
        heading=_("Stored Day Two ending"), routes=CH01_SELECT_END_ROUTES, seed=ch01_d4_select_seed,
    )
