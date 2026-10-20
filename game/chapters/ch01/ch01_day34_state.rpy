# Save-local narrative data only. No device, network, account or filesystem access.
define adrian = Character("Adrian")

init 3 python:
    def ch01_club_betrayal():
        return get_story_value("ch01_d3_club_event", "unknown") == "affair"

    def ch01_covert_trajectory():
        return ch01_club_betrayal() and not get_story_value("ch01_d4_betrayal_disclosed", False)

    def ch01_disclosure_eligible():
        return (ch01_club_betrayal()
                and get_story_value("ch01_d3_ntr_repair_effort") == "talk"
                and get_story_value("ch01_d4_morning_reply") == "joined"
                and not get_story_value("ch01_d4_monitoring_active", False))

    def ch01_nts_agreed():
        return (ch01_club_betrayal()
                and get_story_value("ch01_d4_betrayal_disclosed", False)
                and get_story_value("ch01_d4_discovery_source") == "voluntary_disclosure"
                and get_story_value("ch01_d4_ryan_sharing_curiosity", False)
                and get_story_value("ch01_d4_leia_future_interest", False)
                and get_story_value("ch01_d4_nts_boundaries_discussed", False)
                and get_story_value("ch01_d4_nts_future_agreed", False)
                and not get_story_value("ch01_d4_monitoring_active", False))

    def ch01_d3_record_club_event():
        # Called while Ryan is occupied. Facts are deliberately not Ryan's knowledge.
        confirmed = get_story_value("ch01_d2_end_route") == "ntr_confirmed"
        set_story_value("ch01_d3_club_event", "affair" if confirmed else "unresolved")
        set_story_value("ch01_d3_club_contact_id", "adrian_vale" if confirmed else "none")
        set_story_value("ch01_d3_club_contact_active", confirmed)
        set_story_value("ch01_d3_club_private_photos", confirmed)
        set_story_value("ch01_d3_leia_knows_club_event", confirmed)
        set_story_value("ch01_d4_ryan_knows_club_event", False)
        set_story_value("ch01_d4_leia_knows_discovery", False)
        set_story_value("ch01_d4_monitoring_active", False)

    def ch01_d4_discover_club():
        if not ch01_covert_trajectory():
            return False
        set_story_value("ch01_d4_discovery_source", "covert_phone_access")
        set_story_value("ch01_d4_ryan_knows_club_event", True)
        set_story_value("ch01_d4_ryan_knows_contact", True)
        set_story_value("ch01_d4_ryan_knows_private_photos", True)
        set_story_flag("ch01_d4_phone_access_without_permission")
        return True

    def ch01_d4_enable_monitoring(reason):
        if not ch01_covert_trajectory() or not get_story_value("ch01_d4_ryan_knows_club_event", False):
            return False
        # This sets story state. It does not enable any real capability.
        set_story_value("ch01_d4_monitoring_reason", reason)
        set_story_value("ch01_d4_monitoring_active", True)
        return True

    def ch01_d4_record_second_meeting():
        if not ch01_covert_trajectory() or not get_story_value("ch01_d4_monitoring_active", False):
            return False
        set_story_value("ch01_d4_second_meeting", True)
        set_story_value("ch01_d4_ryan_knows_second_meeting", True)
        set_story_value("ch01_d4_second_meeting_photos", True)
        set_story_value("ch01_d4_leia_knows_discovery", False)
        set_story_value("ch01_d4_leia_knows_monitoring", False)
        set_story_value("ch01_d4_julian_suspicion", "unconfirmed")
        set_story_value("ch01_d4_end_route_pending", "ntr_confirmed")
        set_story_value("ch01_d4_ntr_outcome", "ntr_confirmed")
        set_story_value("ch01_d4_ntr_confirmed", True)
        return True

    def ch01_d4_resolved_ending():
        if ch01_covert_trajectory():
            return "ntr_confirmed"
        pending = get_story_value("ch01_d4_end_route_pending", "love")
        if pending == "nts_discovery":
            return "nts_discovery" if ch01_nts_agreed() else "ntr_unresolved"
        return pending if pending in ("love", "exhibitionism", "love_repaired", "ntr_unresolved", "ntr_confirmed") else "love"

    def ch01_evidence_rows(kind):
        # Static fictional records. No secret thread is inserted into Ryan's phone.
        if kind == "hike":
            if not has_story_flag("ch01_d4_maya_photos_shown"):
                return ()
            return (("Maya", "He agreed you could see these. Just you two, please."),
                    ("Photo 1 · art pending", "Maya and Julian together at the cliff lookout, away from the group."),
                    ("Photo 2 · art pending", "A candid kiss; Julian has forgotten about the camera."),
                    ("Leia", "You actually got him to stop posing."))
        if not get_story_value("ch01_d4_ryan_knows_club_event", False):
            return ()
        if kind == "club":
            return (("Adrian · last night", "I liked the time we had upstairs. I'd like to see you again."),
                    ("Leia · last night", "We slept together. I chose that. I can't pretend it was just a kiss because I feel guilty now."),
                    ("Adrian", "You told me about your boyfriend. I know this isn't simple."),
                    ("Leia", "He doesn't know. Don't message me where he can see."),
                    ("Adrian", "The photos we took are here. I haven't shared them."),
                    ("Private photographs · art pending", "Their kiss in the upstairs lounge. The same hairclip, the same night."),
                    ("Leia · today", "I keep thinking about it. Are you still on the island?"),
                    ("Adrian", "Until Friday. I'll be near the old ferry steps tonight."))
        if kind == "meeting" and get_story_value("ch01_d4_ryan_knows_second_meeting", False):
            return (("Story event · evening", "Leia leaves the villa. Later: a conversation resumes."),
                    ("Leia", "I'm at the old ferry steps."),
                    ("Adrian", "I can see you. Blue jacket, by the closed kiosk."),
                    ("Later · Adrian", "You left your hairclip on the bench. I caught you just in time."),
                    ("Leia", "I shouldn't have stayed that long. I need to get back."),
                    ("Adrian", "Sending the pictures you asked for. They're only for us."),
                    ("Private photographs · art pending", "Leia and Adrian together at the ferry steps; a kiss beneath the kiosk light."),
                    ("Leia", "Got them. Goodnight."))
        return ()

    CHOICE_EFFECTS.update({
        "ch01_d4_wall_name_fear": [("relationship", "trust", -1)],
        "ch01_d4_wall_demand_timeline": [("relationship", "trust", -2)],
        "ch01_d4_monitor_need_truth": [("player", "jealousy", 1)],
        "ch01_d4_monitor_fear_loss": [("player", "jealousy", 1)],
        "ch01_d4_roleplay_play": [],
        "ch01_d4_roleplay_watch": [],
        "ch01_d4_disclosure_listen": [],
        "ch01_d4_disclosure_crosscheck": [("relationship", "trust", -1)],
        "ch01_d4_disclosed_exclusive": [],
        "ch01_d4_disclosed_curious": [],
        "ch01_d4_disclosed_unresolved": [],
        "ch01_d4_nts_talk_only": [],
        "ch01_d4_nts_not_ready": [],
        "ch01_d4_back_love": [],
        "ch01_d4_back_exhibition": [],
    })
    CHOICE_TAGS.update({
        "ch01_d4_wall_name_fear": ["suspicion"],
        "ch01_d4_wall_demand_timeline": ["accusation"],
        "ch01_d4_monitor_need_truth": ["covert_monitoring"],
        "ch01_d4_monitor_fear_loss": ["covert_monitoring"],
        "ch01_d4_roleplay_play": ["shared_roleplay"],
        "ch01_d4_roleplay_watch": ["shared_roleplay"],
    })
