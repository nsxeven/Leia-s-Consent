# Leia's Consent: Chapter One, Day Five choice registration + helpers.
#
# DROP-IN FILE. Same pattern as Day Two / Day Four:
#   init 1 python:
#       CHOICE_EFFECTS.update({...})
#       CHOICE_TAGS.update({...})
# Stable ids use the "ch01_d5_" prefix so chapter_nonchalant_count("ch01") and
# choice_ids_with_prefix("ch01_d5_") pick them up.
#
# Effect rows are (group, stat, amount) with group in relationship / partner / player.
# Verified stats: relationship love trust boredom momentum; partner curiosity temptation
# exhibitionism boundary_looseness secrecy; player jealousy acceptance (see defaults.rpy).
#
# Scale note: ordinary Day Five choices are +/-1..2 (slow burn), with +3 only for the two
# trust-trade / honesty beats that Leia explicitly earns. Gate choices follow the Day Two /
# Day Four gate scale (soft -1..2, hard up to -5). Nothing here moves a stat by more than 5.

init 1 python:

    CHOICE_EFFECTS.update({

            # 01 packing (Love)
            "ch01_d5_pack_ryan_picks": [
                ("relationship", "love", 1),
                ("player", "acceptance", 1),
                ("relationship", "momentum", 1),
            ],
            "ch01_d5_pack_leia_decides": [
                ("relationship", "trust", 2),
                ("relationship", "love", 1),
            ],

            # 01 packing (Exhibition)
            "ch01_d5_pack_bolder": [
                ("partner", "curiosity", 1),
                ("partner", "exhibitionism", 2),
                ("player", "acceptance", 1),
                ("relationship", "momentum", 1),
            ],
            "ch01_d5_pack_classic": [
                ("relationship", "love", 1),
                ("relationship", "trust", 1),
            ],
            "ch01_d5_pack_her_call": [
                ("relationship", "trust", 1),
                ("partner", "exhibitionism", 1),
                ("player", "acceptance", 1),
            ],

            # 01 packing (NTR)
            "ch01_d5_ntr_pack_help": [
                ("relationship", "love", 1),
                ("relationship", "trust", 1),
                ("relationship", "boredom", -1),
            ],
            "ch01_d5_ntr_pack_joke": [
                ("relationship", "boredom", -1),
                ("relationship", "trust", 1),
            ],
            "ch01_d5_ntr_pack_nothing": [
                ("relationship", "boredom", 1),
                ("relationship", "love", -1),
            ],

            # 02 Julian seasick
            "ch01_d5_julian_stay": [
                ("relationship", "trust", 1),
                ("player", "acceptance", 1),
            ],
            "ch01_d5_julian_joke": [
                ("player", "acceptance", 1),
            ],
            "ch01_d5_julian_leave": [
                ("relationship", "boredom", 1),
            ],

            # 03 no bars
            "ch01_d5_bars_bag": [
                ("relationship", "love", 1),
                ("relationship", "trust", 1),
                ("relationship", "boredom", -1),
            ],
            "ch01_d5_bars_check": [
                ("relationship", "boredom", 1),
            ],

            # 04 snorkel pairs
            "ch01_d5_snorkel_leia_first": [
                ("relationship", "love", 1),
                ("relationship", "trust", 1),
            ],
            "ch01_d5_snorkel_maya_first": [
                ("player", "acceptance", 1),
            ],
            "ch01_d5_snorkel_julian_first": [
                ("relationship", "boredom", 1),
            ],
            "ch01_d5_ntr_snorkel_stay": [
                ("relationship", "love", -1),
                ("relationship", "trust", -1),
                ("relationship", "boredom", 2),
                ("partner", "secrecy", 1),
            ],

            # 05 cove lunch
            "ch01_d5_bee_calm": [
                ("relationship", "trust", 1),
                ("player", "acceptance", 1),
            ],
            "ch01_d5_bee_film": [
                ("relationship", "boredom", -1),
                ("player", "acceptance", 1),
            ],
            "ch01_d5_photo_share_group": [
                ("player", "acceptance", 1),
            ],
            "ch01_d5_photo_keep_album": [
                ("relationship", "love", 1),
            ],

            # 06 foredeck
            "ch01_d5_eaves_announce": [
                ("relationship", "trust", 1),
            ],
            "ch01_d5_eaves_listen": [
                ("relationship", "trust", -1),
                ("partner", "secrecy", 1),
                ("player", "jealousy", 1),
            ],

            # 07 stern
            "ch01_d5_stern_thanks": [
                ("relationship", "trust", 1),
            ],
            "ch01_d5_stern_joke": [
                ("player", "acceptance", 1),
            ],
            "ch01_d5_stern_push": [
                ("player", "jealousy", 1),
                ("relationship", "trust", -1),
            ],

            # 08 Love cove
            "ch01_d5_love_swim_close": [
                ("relationship", "love", 2),
                ("relationship", "trust", 1),
                ("relationship", "boredom", -1),
            ],
            "ch01_d5_love_swim_race": [
                ("relationship", "love", 1),
                ("relationship", "boredom", -2),
            ],
            "ch01_d5_love_secret_dream": [
                ("relationship", "love", 1),
                ("relationship", "trust", 3),
                ("relationship", "boredom", -2),
            ],
            "ch01_d5_love_secret_mirror": [
                ("relationship", "love", 2),
                ("relationship", "trust", 2),
                ("relationship", "boredom", -1),
            ],
            "ch01_d5_love_secret_owe": [
                ("relationship", "trust", 1),
                ("relationship", "boredom", 1),
            ],

            # 08 Exhibition cove
            "ch01_d5_exhib_stay": [
                ("relationship", "love", 1),
                ("partner", "curiosity", 1),
                ("partner", "exhibitionism", 2),
                ("player", "acceptance", 1),
                ("relationship", "momentum", 1),
            ],
            "ch01_d5_exhib_watching": [
                ("partner", "exhibitionism", 2),
                ("player", "acceptance", 2),
                ("relationship", "momentum", 1),
            ],
            "ch01_d5_exhib_private": [
                ("relationship", "love", 2),
                ("relationship", "trust", 1),
            ],
            "ch01_d5_exhib_her_call": [
                ("partner", "exhibitionism", 1),
                ("relationship", "trust", 1),
                ("player", "acceptance", 1),
            ],
            "ch01_d5_exhib_tease_then_me": [
                ("partner", "exhibitionism", 1),
                ("relationship", "love", 1),
                ("player", "jealousy", 1),
            ],
            "ch01_d5_photo_private_face": [
                ("relationship", "love", 1),
                ("relationship", "trust", 2),
            ],
            "ch01_d5_photo_private_moment": [
                ("relationship", "love", 1),
                ("relationship", "trust", 1),
                ("partner", "exhibitionism", 1),
                ("player", "acceptance", 1),
            ],
            "ch01_d5_photo_private_none": [
                ("relationship", "love", 2),
                ("relationship", "trust", 2),
            ],

            # 08/09 NTR disclosure reactions
            "ch01_d5_ntr_react_thanks": [
                ("relationship", "trust", 2),
                ("relationship", "love", 1),
            ],
            "ch01_d5_ntr_react_boundary": [
                ("relationship", "trust", 1),
                ("relationship", "love", 1),
                ("partner", "boundary_looseness", -1),
            ],
            "ch01_d5_ntr_react_curious": [
                ("partner", "curiosity", 1),
                ("partner", "exhibitionism", 1),
                ("player", "acceptance", 2),
                ("relationship", "trust", 1),
            ],
            "ch01_d5_ntr_gate_fine_hard": [
                ("relationship", "love", -3),
                ("relationship", "trust", -3),
                ("relationship", "boredom", 3),
                ("player", "jealousy", 1),
                ("partner", "secrecy", 3),
                ("partner", "boundary_looseness", 2),
            ],

            # 09 sunset gates (NTR unresolved)
            "ch01_d5_ntr_u_ask_gently": [
                ("relationship", "love", 2),
                ("relationship", "trust", 3),
                ("relationship", "boredom", -3),
                ("partner", "secrecy", -3),
                ("partner", "temptation", -1),
            ],
            "ch01_d5_ntr_u_press_hard": [
                ("relationship", "love", -3),
                ("relationship", "trust", -3),
                ("relationship", "boredom", 3),
                ("player", "jealousy", 3),
                ("partner", "secrecy", 3),
                ("partner", "boundary_looseness", 2),
            ],
            "ch01_d5_ntr_u_fine_hard": [
                ("relationship", "love", -4),
                ("relationship", "trust", -3),
                ("relationship", "boredom", 4),
                ("partner", "temptation", 3),
                ("partner", "secrecy", 3),
                ("partner", "boundary_looseness", 2),
            ],

            # 09 sunset gates (NTR confirmed)
            "ch01_d5_ntr_c_go_to_her": [
                ("relationship", "love", 2),
                ("relationship", "trust", 2),
                ("relationship", "boredom", -3),
                ("partner", "secrecy", -2),
            ],
            "ch01_d5_ntr_c_accuse_hard": [
                ("relationship", "love", -2),
                ("relationship", "trust", -2),
                ("relationship", "boredom", 2),
                ("player", "jealousy", 3),
                ("partner", "secrecy", 2),
            ],
            "ch01_d5_ntr_c_fine_hard": [
                ("relationship", "love", -4),
                ("relationship", "trust", -3),
                ("relationship", "boredom", 4),
                ("partner", "temptation", 3),
                ("partner", "secrecy", 3),
                ("partner", "boundary_looseness", 2),
            ],

            # 09 evening wardrobe (Love)
            "ch01_d5_evening_ryan_picks": [
                ("relationship", "love", 1),
                ("player", "acceptance", 1),
                ("relationship", "momentum", 1),
            ],
            "ch01_d5_evening_leia_decides": [
                ("relationship", "trust", 2),
                ("relationship", "love", 1),
            ],

            # 10 dinner truth round
            "ch01_d5_truth_honest": [
                ("relationship", "love", 1),
                ("relationship", "trust", 2),
                ("relationship", "boredom", -1),
            ],
            "ch01_d5_truth_funny": [
                ("relationship", "boredom", -1),
            ],
            "ch01_d5_truth_dodge": [
                ("relationship", "boredom", 1),
                ("relationship", "trust", -1),
            ],
            "ch01_d5_ask_sweet": [
                ("relationship", "love", 1),
                ("relationship", "trust", 1),
            ],
            "ch01_d5_ask_brave": [
                ("relationship", "trust", 1),
                ("player", "acceptance", 1),
            ],
            "ch01_d5_ask_silly": [
                ("relationship", "boredom", -1),
            ],

            # 11 bunk split
            "ch01_d5_bunk_cabin": [
                ("relationship", "love", 1),
                ("relationship", "trust", 1),
            ],
            "ch01_d5_bunk_deck": [
                ("relationship", "love", 1),
                ("player", "acceptance", 1),
                ("relationship", "momentum", 1),
            ],
            "ch01_d5_bunk_apart": [
                ("relationship", "trust", 1),
            ],
            "ch01_d5_ntr_bunk_apart": [
                ("relationship", "love", -1),
                ("relationship", "trust", -1),
                ("relationship", "boredom", 2),
                ("partner", "secrecy", 1),
            ],

            # 12 Love night
            "ch01_d5_love_bracelet_hers": [
                ("relationship", "love", 2),
                ("relationship", "trust", 2),
            ],
            "ch01_d5_love_bracelet_his": [
                ("relationship", "love", 2),
                ("relationship", "trust", 2),
            ],

            # 12 Exhibition night
            "ch01_d5_exhib_rule_wrist": [
                ("relationship", "trust", 3),
                ("partner", "exhibitionism", 1),
                ("player", "acceptance", 1),
            ],
            "ch01_d5_exhib_rule_dare": [
                ("partner", "exhibitionism", 1),
                ("partner", "curiosity", 1),
                ("player", "acceptance", 1),
                ("relationship", "momentum", 1),
            ],
            "ch01_d5_exhib_rule_skip": [
                ("relationship", "love", 1),
                ("relationship", "trust", 1),
            ],

            # 15 pier invitation
            "ch01_d5_invite_in": [
                ("player", "acceptance", 1),
                ("relationship", "momentum", 1),
            ],
            "ch01_d5_invite_ask_leia": [
                ("relationship", "trust", 1),
                ("relationship", "love", 1),
            ],
            "ch01_d5_invite_maybe": [
                ("relationship", "boredom", 1),
            ],
            "ch01_d5_invite_read_aloud": [
                ("relationship", "trust", 1),
                ("relationship", "love", 1),
                ("relationship", "boredom", -1),
            ],
            "ch01_d5_invite_keep_quiet": [
                ("relationship", "boredom", 1),
            ],
    })

    CHOICE_TAGS.update({

            "ch01_d5_pack_ryan_picks": ("supportive", "attentive", "participating", "love-route"),
            "ch01_d5_pack_leia_decides": ("supportive", "respectful", "comfort-first"),

            "ch01_d5_pack_bolder": ("encouraging", "open", "participating", "playful"),
            "ch01_d5_pack_classic": ("supportive", "comfort-first", "attentive"),
            "ch01_d5_pack_her_call": ("supportive", "open", "her-pace"),

            "ch01_d5_ntr_pack_help": ("supportive", "attentive", "repair"),
            "ch01_d5_ntr_pack_joke": ("lighthearted", "attentive"),
            "ch01_d5_ntr_pack_nothing": ("neutral", "nonchalant", "distracted"),

            "ch01_d5_julian_stay": ("supportive", "attentive", "loyal"),
            "ch01_d5_julian_joke": ("encouraging", "lighthearted"),
            "ch01_d5_julian_leave": ("neutral", "nonchalant", "distracted"),

            "ch01_d5_bars_bag": ("supportive", "attentive", "present"),
            "ch01_d5_bars_check": ("neutral", "nonchalant", "distracted"),

            "ch01_d5_snorkel_leia_first": ("supportive", "attentive", "love-route"),
            "ch01_d5_snorkel_maya_first": ("neutral", "trusting", "lighthearted"),
            "ch01_d5_snorkel_julian_first": ("neutral", "lighthearted", "distracted"),
            "ch01_d5_ntr_snorkel_stay": ("neutral", "nonchalant", "dismissive", "distracted", "ntr-gate"),

            "ch01_d5_bee_calm": ("supportive", "lighthearted", "attentive"),
            "ch01_d5_bee_film": ("playful", "lighthearted"),
            "ch01_d5_photo_share_group": ("open", "trusting", "lighthearted"),
            "ch01_d5_photo_keep_album": ("attentive", "private"),

            "ch01_d5_eaves_announce": ("honest", "respectful"),
            "ch01_d5_eaves_listen": ("neutral", "secretive", "curious"),

            "ch01_d5_stern_thanks": ("supportive", "honest", "trusting"),
            "ch01_d5_stern_joke": ("encouraging", "lighthearted"),
            "ch01_d5_stern_push": ("protective", "pressing"),

            "ch01_d5_love_swim_close": ("attentive", "supportive", "love-route"),
            "ch01_d5_love_swim_race": ("playful", "lighthearted", "attentive"),
            "ch01_d5_love_secret_dream": ("supportive", "honest", "attentive", "love-route", "trust-trade"),
            "ch01_d5_love_secret_mirror": ("supportive", "honest", "playful", "love-route", "trust-trade"),
            "ch01_d5_love_secret_owe": ("neutral", "playful", "deferring"),

            "ch01_d5_exhib_stay": ("encouraging", "open", "participating", "attentive"),
            "ch01_d5_exhib_watching": ("encouraging", "open", "honest", "participating", "watching"),
            "ch01_d5_exhib_private": ("protective", "attentive", "supportive", "boundary-setting"),
            "ch01_d5_exhib_her_call": ("supportive", "open", "attentive", "her-pace"),
            "ch01_d5_exhib_tease_then_me": ("encouraging", "playful", "possessive", "attentive"),
            "ch01_d5_photo_private_face": ("supportive", "attentive", "private"),
            "ch01_d5_photo_private_moment": ("encouraging", "open", "private", "her-pace"),
            "ch01_d5_photo_private_none": ("supportive", "respectful", "private"),

            "ch01_d5_ntr_react_thanks": ("supportive", "honest", "repair"),
            "ch01_d5_ntr_react_boundary": ("protective", "boundary-setting", "honest", "repair"),
            "ch01_d5_ntr_react_curious": ("open", "honest", "attentive", "repair", "exhibitionism-seed"),
            "ch01_d5_ntr_gate_fine_hard": ("neutral", "nonchalant", "dismissive", "ntr-confirm"),

            "ch01_d5_ntr_u_ask_gently": ("supportive", "attentive", "honest", "repair"),
            "ch01_d5_ntr_u_press_hard": ("protective", "jealous", "accusatory", "ntr-confirm"),
            "ch01_d5_ntr_u_fine_hard": ("neutral", "nonchalant", "dismissive", "ntr-confirm"),

            "ch01_d5_ntr_c_go_to_her": ("supportive", "attentive", "honest", "repair"),
            "ch01_d5_ntr_c_accuse_hard": ("protective", "jealous", "accusatory", "ntr-confirm"),
            "ch01_d5_ntr_c_fine_hard": ("neutral", "nonchalant", "dismissive", "ntr-confirm"),

            "ch01_d5_evening_ryan_picks": ("supportive", "attentive", "participating", "love-route"),
            "ch01_d5_evening_leia_decides": ("supportive", "respectful", "comfort-first"),

            "ch01_d5_truth_honest": ("supportive", "honest", "attentive"),
            "ch01_d5_truth_funny": ("lighthearted", "playful"),
            "ch01_d5_truth_dodge": ("neutral", "nonchalant", "distracted"),
            "ch01_d5_ask_sweet": ("supportive", "attentive", "love-route"),
            "ch01_d5_ask_brave": ("supportive", "attentive", "honest"),
            "ch01_d5_ask_silly": ("playful", "lighthearted"),

            "ch01_d5_bunk_cabin": ("attentive", "supportive"),
            "ch01_d5_bunk_deck": ("encouraging", "playful", "attentive"),
            "ch01_d5_bunk_apart": ("respectful", "neutral", "comfort-first"),
            "ch01_d5_ntr_bunk_apart": ("neutral", "nonchalant", "dismissive", "distracted", "ntr-gate"),

            "ch01_d5_love_bracelet_hers": ("attentive", "supportive", "love-route"),
            "ch01_d5_love_bracelet_his": ("attentive", "supportive", "trusting", "love-route"),

            "ch01_d5_exhib_rule_wrist": ("supportive", "open", "attentive", "boundary-setting", "her-pace", "pass-signal"),
            "ch01_d5_exhib_rule_dare": ("encouraging", "open", "playful", "her-pace"),
            "ch01_d5_exhib_rule_skip": ("supportive", "attentive"),

            "ch01_d5_invite_in": ("encouraging", "open"),
            "ch01_d5_invite_ask_leia": ("supportive", "attentive", "respectful"),
            "ch01_d5_invite_maybe": ("neutral", "unresolved"),
            "ch01_d5_invite_read_aloud": ("supportive", "honest", "attentive", "repair"),
            "ch01_d5_invite_keep_quiet": ("neutral", "unresolved", "distracted"),
    })


init 2 python:

    D5_BOLDER_SWIM_MIN = 24                 # Leia's own Exhibitionism needed to wear the bolder swimsuit by choice
    D5_COMFORTABLE_MIN = 34                 # Exhibitionism needed for the 'comfortable' cove step
    D5_COMFORTABLE_MIN_AFTER_BRIEF = 30     # lower bar if Day Four's step was already 'brief_reveal'
    D5_NO_PACK_OUTFITS = ("boutique_cutout_mini", "after_hours_dress")
    D5_NO_EVENING_OUTFITS = ("casual_default",)


    def ch01_d5_choice_ids():
        return choice_ids_with_prefix("ch01_d5_")


    def ch01_d5_nonchalant_count():
        return choice_tag_count("nonchalant", ch01_d5_choice_ids())


    def ch01_d5_is_ntr():
        return str(get_story_value("ch01_d5_track", "love")).startswith("ntr")


    def ch01_d5_bolder_swim_ok():
        """Leia's own comfort with the bolder swimsuit: she already wore it on Day Two, or her
        Exhibitionism has grown enough. Reads stored Day Two history and her stat; never forces."""
        if get_story_value("ch01_d2_pool_outfit", None) == "pool_bolder":
            return True
        return partner_stats["exhibitionism"] >= D5_BOLDER_SWIM_MIN


    def ch01_d5_leia_call_for(exhibitionism, prev_step):
        """Leia's own call for the cove step. Both results are positive.

        'comfortable' (cropped, implied) needs her Exhibitionism at D5_COMFORTABLE_MIN, or the lower
        D5_COMFORTABLE_MIN_AFTER_BRIEF if Day Four's step was already a brief reveal. Otherwise she
        chooses 'ties_loosened' (covered, implied). Never a recompute of the route."""
        needed = D5_COMFORTABLE_MIN_AFTER_BRIEF if prev_step == "brief_reveal" else D5_COMFORTABLE_MIN
        return "comfortable" if exhibitionism >= needed else "ties_loosened"


    def ch01_d5_track_text():
        """Track card for Insight / Full / Developer modes. None in Normal mode.

        Reads stored state only. It never recomputes a track."""
        mode = current_choice_mode()
        if mode == "normal":
            return None

        track = get_story_value("ch01_d5_track", "love")
        if track == "love":
            head = "TRACK: LOVE (pure couple track)"
            line = "A private cove and a trust trade. No outside-attention beats today."
        elif track == "exhibitionism":
            head = "TRACK: SHARED EXHIBITION (NTS)"
            line = (girlfriend_name + " sets how far she goes among the four. 'Just us' is always available.")
        elif track == "ntr_repaired":
            head = "TRACK: DISTANCE, REPAIRED (NTR pressure)"
            line = (girlfriend_name + ' tells the club story slowly. How ' + player_name + ' reacts decides what it repairs.')
        elif track == "ntr_unresolved":
            head = "TRACK: DISTANCE, UNRESOLVED (NTR pressure)"
            line = "Repair is still possible. Gate choices carry a red diamond."
        else:
            head = "TRACK: DISTANCE, CONFIRMED (NTR pressure)"
            line = ('A door is open if ' + player_name + ' walks through it. Gate choices carry a red diamond.')

        if mode == "insight":
            return "{}\n\n{}".format(head, line)

        detail = "Day 4 end: {}  |  Day 4 variant: {}".format(
            get_story_value("ch01_d4_end_route", "?"),
            get_story_value("ch01_d4_end_variant", "?"),
        )
        if mode == "full":
            return "{}\n\n{}\n{}".format(head, line, detail)

        return "{}\n\n{}\n{}\nlane={}  d4_fine_count={}  cutout_disclosed={}  club_deferred={}".format(
            head, line, detail,
            get_story_value("ch01_d5_lane", "?"),
            get_story_value("ch01_d4_ntr_fine_count", "?"),
            has_story_flag("ch01_d4_cutout_disclosed"),
            has_story_flag("ch01_d4_club_story_deferred"),
        )


    def format_day5_gate_choice(choice_id, base_text, severity="soft", gate_label="D5-1"):
        """Risk-aware label for Day Five NTR gates (mirrors format_day4_gate_choice)."""
        mode = current_choice_mode()
        if mode == "normal":
            return base_text

        if severity == "hard":
            marker = "{color=#ff4242}\u25c6\u25c6{/color}"
            if mode == "insight":
                return "{} {}\n[Critical relationship choice]".format(marker, base_text)
            if mode == "full":
                return "{} {}\n[CRITICAL ROUTE CHOICE] [{}]".format(
                    marker, base_text, _choice_effect_text(choice_id, exact=True)
                )
            return "{} {}\n[CONFIRM NTR ROUTE {}] [{}]  [ID: {}]".format(
                marker, base_text, gate_label, _choice_effect_text(choice_id, exact=True), choice_id
            )

        marker = "{color=#d85a5a}\u25c6{/color}"
        if mode == "insight":
            return "{} {}\n[Major relationship consequence]".format(marker, base_text)
        if mode == "full":
            return "{} {}\n[MAJOR RELATIONSHIP CONSEQUENCE] [{}]".format(
                marker, base_text, _choice_effect_text(choice_id, exact=True)
            )
        return "{} {}\n[NTR GATE {}] [{}]  [ID: {}]".format(
            marker, base_text, gate_label, _choice_effect_text(choice_id, exact=True), choice_id
        )


    def ch01_d5_wear(outfit_id):
        """Ask Leia to wear a story outfit through the NORMAL wear-path rules.

        grant_story_outfit(..., equip=True) grants the outfit and equips it only if a wear path
        passes. Returns True when she is wearing it. Only for story_grant outfits."""
        return bool(grant_story_outfit(outfit_id, equip=True))


    def ch01_d5_pack_options():
        """Love picker for the boat day: outdoor daywear, plus owned swimwear (visible but LOCKED
        below the Love swimwear Exhibitionism threshold, so the player can see control expand)."""
        options = []
        for outfit_id in love_outfit_candidates(
            story_ids=("casual_default", "d2_loose_low_cut", "resort_dinner_dress"),
        ):
            if outfit_id in D5_NO_PACK_OUTFITS:
                continue
            options.append(outfit_id)
        return options


    def ch01_d5_evening_options():
        """Love picker for the boat dinner: evening-capable, no swimwear, no plain casual."""
        options = []
        for outfit_id in love_outfit_candidates(
            story_ids=("resort_dinner_dress", "d2_loose_low_cut", "boutique_cutout_mini"),
        ):
            if outfit_id in D5_NO_EVENING_OUTFITS or love_outfit_is_swimwear(outfit_id):
                continue
            options.append(outfit_id)
        return options
