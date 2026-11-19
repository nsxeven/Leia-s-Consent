# Day Two pack - registrations: every Day Two choice row (CHOICE_EFFECTS / CHOICE_TAGS), the
#   Leia's-errand rows and map places, the lane / end-route helpers and their exempt choice
#   lists, the Maya DM phone moment, the pool-outfit names, and the story-key ledger. The
#   scene files (ch01_day2_scenes_*.rpy, ch01_day2_leia_errand.rpy) hold only labels.
#
# Where every kind of content goes: docs/DAY_PACK.md. Scoring rules: docs/STAT_MODEL.md.
# Load order: init 1 (the engine tables exist at init <= 0), except the pool-outfit block at
#   init 998 (see its comment). Blocks run in the order they ran from their old files
#   (errand, mall, scenes 1-15, scenes 16-30), so every table keeps its insertion order.

# Leia's errand (was ch01_day2_leia_errand.rpy): her choices, scored like any choice.
init 1 python:
    CHOICE_EFFECTS.update({
        # Café (Love lane): thank him and tell him about Ryan / brush him off.
        "ch01_d2_errand_cafe_love_thank": [
            ("relationship", "love", 1),
        ],
        "ch01_d2_errand_cafe_love_brush": [],  # Neutral: no stats
        # Café (Exhibitionism lane): let the chat run / mention Ryan now.
        "ch01_d2_errand_cafe_exhib_linger": [
            ("partner", "exhibitionism", 1),
        ],
        "ch01_d2_errand_cafe_exhib_mention": [],  # Neutral: no stats
        # Café (NTR-risk lane): how long she hesitates. The ending is the same either way.
        "ch01_d2_errand_cafe_ntr_linger": [
            ("relationship", "temptation", 1),
        ],
        "ch01_d2_errand_cafe_ntr_shut": [],  # Neutral: no stats
        # Resort shop (shop first on Love/Exhib; after the café on Love).
        "ch01_d2_errand_shop_tell": [
            ("relationship", "love", 1),
        ],
        "ch01_d2_errand_shop_keep": [],  # Neutral: no stats
        # Resort shop after the café (Exhibitionism lane): the fridge-door reflection.
        "ch01_d2_errand_shop_mirror_leave": [
            ("partner", "exhibitionism", 1),
        ],
        "ch01_d2_errand_shop_mirror_fix": [],  # Neutral: no stats
        # Walk back (NTR-risk lane, her inner voice). Stores ch01_d2_leia_told.
        "ch01_d2_errand_walk_tell": [
            ("relationship", "sharing", 1),
        ],
        # Stamps "NTR" in Full mode (canon call K4: lc_stat_model.CHOICE_ROUTE_FLAGS "lean").
        "ch01_d2_errand_walk_keep": [
            ("relationship", "temptation", 1),
        ],
        # Ryan's reply to her confession (19c, told path). His own pick: never capped.
        "ch01_d2_confession_ask": [
            ("relationship", "sharing", 1),
        ],
        "ch01_d2_confession_protect": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d2_confession_brush": [],  # Neutral: no stats
        # Scene 30 "saw a post" bring-up (canon call K5). Ryan's picks: never capped.
        "ch01_d2_feed_love_tease": [
            ("relationship", "love", 1),
        ],
        "ch01_d2_feed_exhib_show": [
            ("partner", "exhibitionism", 1),
        ],
        "ch01_d2_feed_told_aside": [
            ("relationship", "trust", 1),
        ],
        "ch01_d2_feed_kept_ask": [
            ("relationship", "trust", 1),
        ],
        "ch01_d2_feed_kept_silent": [
            ("relationship", "temptation", 1),
        ],
        "ch01_d2_feed_let_go": [],  # Neutral: no stats
    })

    CHOICE_TAGS.update({
        "ch01_d2_errand_cafe_love_thank": ("honest", "attentive", "love-route"),
        "ch01_d2_errand_cafe_love_brush": ("neutral",),
        "ch01_d2_errand_cafe_exhib_linger": ("playful", "open", "curious"),
        "ch01_d2_errand_cafe_exhib_mention": ("neutral", "honest"),
        "ch01_d2_errand_cafe_ntr_linger": ("curious", "ntr-seed"),
        "ch01_d2_errand_cafe_ntr_shut": ("boundary-setting",),
        "ch01_d2_errand_shop_tell": ("honest", "supportive", "love-route"),
        "ch01_d2_errand_shop_keep": ("neutral",),
        "ch01_d2_errand_shop_mirror_leave": ("playful", "open"),
        "ch01_d2_errand_shop_mirror_fix": ("neutral",),
        "ch01_d2_errand_walk_tell": ("honest", "open", "trusting"),
        "ch01_d2_errand_walk_keep": ("withdrawal", "ntr-seed"),
        "ch01_d2_confession_ask": ("curious", "open", "honest"),
        "ch01_d2_confession_protect": ("protective", "supportive", "attentive"),
        "ch01_d2_confession_brush": ("neutral", "nonchalant", "dismissive"),
        "ch01_d2_feed_love_tease": ("playful", "attentive"),
        "ch01_d2_feed_exhib_show": ("encouraging", "open", "playful"),
        "ch01_d2_feed_told_aside": ("supportive", "trusting", "honest"),
        "ch01_d2_feed_kept_ask": ("attentive", "honest"),
        "ch01_d2_feed_kept_silent": ("nonchalant", "withdrawal"),
        "ch01_d2_feed_let_go": ("neutral", "trusting"),
    })

    # Her own choices: their gains share the day's +2 cap (docs/LEIA_SIDE.md). Ryan's confession
    # reply and his scene 30 bring-up are his, so they are never registered here.
    lc_leia_register_choices(
        "ch01_d2",
        "ch01_d2_errand_cafe_love_thank", "ch01_d2_errand_cafe_love_brush",
        "ch01_d2_errand_cafe_exhib_linger", "ch01_d2_errand_cafe_exhib_mention",
        "ch01_d2_errand_cafe_ntr_linger", "ch01_d2_errand_cafe_ntr_shut",
        "ch01_d2_errand_shop_tell", "ch01_d2_errand_shop_keep",
        "ch01_d2_errand_shop_mirror_leave", "ch01_d2_errand_shop_mirror_fix",
        "ch01_d2_errand_walk_tell", "ch01_d2_errand_walk_keep",
    )

# Map cards (lc_leia_map). Text fields are player-visible. Place ids are save data: never rename.
# Each open place is also a Moments strip moment on the Day Two review (leia_ch01_d2_cafe/_shop).
define CH01_D2_ERRAND_PLACES = [
    {"id": "cafe", "label": "Café", "bg": "bg ch01_d2_cafe",
     "hint": "The café from lunch. They do his caramel frappuccino.",
     "done": "Frappuccino: got it."},
    {"id": "shop", "label": "Resort shop", "bg": "bg ch01_shop_day",
     "hint": "Snacks, sunscreen, inflatable everything. Hopefully chocolate muffins.",
     "done": "Muffins: got them."},
    {"id": "bar", "label": "Resort bar", "bg": "bg ch01_restaurant_bar", "locked": True,
     "locked_reason": "A bar, on my own, at four in the afternoon? Not on day two. Maybe if Maya comes next time."},
    {"id": "boutique", "label": "Boutique", "bg": "bg ch01_d2_boutique", "locked": True,
     "locked_reason": "I've had enough of that boutique for one day, thank you."},
]

init 1 python:
    lc_leia_register_places("ch01_d2", CH01_D2_ERRAND_PLACES)


# Mall rows (were in systems/choice_engine.rpy).
init 1 python:

    CHOICE_EFFECTS.update({
        "ch01_d2_mall_go_to_leia": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d2_mall_leave_to_maya": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_d2_mall_reveal_affection": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d2_mall_reveal_open": [
            ("partner", "exhibitionism", 2),
        ],
        "ch01_d2_mall_reveal_tease": [
            ("relationship", "love", 1),
        ],
        "ch01_d2_mall_reveal_flat": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
    })

    CHOICE_TAGS.update({
        "ch01_d2_mall_go_to_leia": ("supportive", "attentive", "love-route"),
        "ch01_d2_mall_leave_to_maya": ("neutral", "nonchalant", "dismissive", "withdrawal", "ntr-seed"),
        "ch01_d2_mall_reveal_affection": ("supportive", "attentive", "love-route"),
        "ch01_d2_mall_reveal_open": ("encouraging", "participating", "open", "exhibitionism-seed"),
        "ch01_d2_mall_reveal_tease": ("encouraging", "playful", "attentive"),
        "ch01_d2_mall_reveal_flat": ("neutral", "nonchalant", "distracted"),
    })


# Scenes 1-15 (was ch01_day2_scenes_01_15.rpy): choice rows, lane helpers, the gate formatter.
init 1 python:

    # Register Day Two choices with the existing central Choice Engine after it
    # has created CHOICE_EFFECTS / CHOICE_TAGS.
    CHOICE_EFFECTS.update({
        "ch01_dream_ground": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_dream_curiosity": [
            ("partner", "exhibitionism", 2),
        ],
        "ch01_dream_withdraw": [
            ("relationship", "temptation", 1),
        ],
        "ch01_d2_morning_reassure": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d2_morning_tease": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 2),
        ],
        "ch01_d2_morning_dismiss": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        # Post-shop check-in menu: the warm answers stay flavor (their repair tags pick which cafe
        # talk Ryan overhears). darryn 2026-11-19: with the pair-photo choice cut, "I'm fine." counts
        # again and "act like you didn't hear" counts double, so the NTR slide takes three steps here.
        "ch01_d2_postshop_sleep": [],  # Flavor: no stats
        "ch01_d2_postshop_head": [],  # Flavor: no stats
        "ch01_d2_postshop_shut_down": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        # Day Two incident (v0.2.0): Ryan overhears Leia and Maya at the cafe.
        "ch01_d2_overheard_own": [
            ("relationship", "trust", 1),
            ("relationship", "temptation", -1),
        ],
        "ch01_d2_overheard_joke": [],  # Flavor: no stats
        "ch01_d2_overheard_pretend": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 2),
        ],
        "ch01_d2_maya_reassure": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d2_maya_tease_jealousy": [
            ("relationship", "love", 1),
        ],
        "ch01_d2_maya_open_honest": [
            ("relationship", "trust", 1),
        ],
        "ch01_d2_maya_include": [
            ("relationship", "love", 1),
            ("relationship", "trust", 2),
        ],
        "ch01_d2_maya_catchup": [],  # Neutral: no stats
        "ch01_d2_maya_dismiss_leia": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_d2_photo_pair_encourage": [
            ("partner", "exhibitionism", 2),
        ],
        "ch01_d2_photo_pair_redirect": [
            ("relationship", "trust", 1),
        ],
        "ch01_d2_photo_pair_shrug": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_d2_pool_reassure": [
            ("relationship", "love", 1),
            ("relationship", "trust", 2),
        ],
        "ch01_d2_pool_honest_jealous": [
            ("relationship", "trust", 1),
        ],
        "ch01_d2_pool_accuse": [
            ("relationship", "trust", -2),
            ("relationship", "temptation", 1),
        ],
        "ch01_d2_sunset_connect": [
            ("relationship", "love", 2),
            ("relationship", "trust", 1),
        ],
        "ch01_d2_sunset_partial": [
            ("relationship", "trust", 1),
            ("relationship", "temptation", -1),
        ],
        "ch01_d2_sunset_ignore_gate": [
            ("relationship", "love", -3),
            ("relationship", "temptation", 5),
        ],
        "ch01_d2_bed_pool_love": [
            ("relationship", "love", 3),
            ("relationship", "temptation", -3),
        ],
        "ch01_d2_bed_pool_exhibition": [
            ("relationship", "love", 2),
            ("partner", "exhibitionism", 3),
        ],
        "ch01_d2_bed_pool_accuse": [
            ("relationship", "trust", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_d2_wink_repair": [
            ("relationship", "love", 3),
            ("relationship", "temptation", -3),
        ],
        "ch01_d2_wink_accuse_hard": [
            ("relationship", "love", -4),
            ("relationship", "trust", -5),
            ("relationship", "temptation", 5),
        ],
        "ch01_d2_wink_reject_hard": [
            ("relationship", "love", -5),
            ("relationship", "trust", -4),
            ("relationship", "temptation", 5),
        ],
        # Door B (sc 27 dare signal). Ryan only signals; Leia's decision and the scene 27-29 branch stay as they were.
        "ch01_d2_dare_nod": [
            ("partner", "exhibitionism", 1),
        ],
        "ch01_d2_dare_shrug": [],  # Neutral: no stats (plays today's text)
        "ch01_d2_dare_lap": [
            ("relationship", "love", 1),
        ],
        # Door A (sc 15 knot): Love / Neutral / Love+Exhib, after the lane record.
        "ch01_d2_knot_fix": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d2_knot_tell": [],  # Neutral: plays only the noticing beat
        "ch01_d2_knot_watch": [
            ("partner", "exhibitionism", 1),
        ],
        # Door A, fourth answer (red bikini, Exhibitionism or NTR lane; darryn 2026-11-19).
        "ch01_d2_knot_touch_exhib": [
            ("partner", "exhibitionism", 1),
            ("relationship", "love", 1),
        ],
        # Darryn asked for Exhibitionism +1, Trust -1; the scoring rule forbids that shape, so it
        # ships as Exhibitionism +1 until he picks (Temptation +1/Trust -1 or no stats are the options).
        "ch01_d2_knot_touch_ntr": [
            ("partner", "exhibitionism", 1),
        ],
        # Scene 13 bikini picks (darryn 2026-11-19): flavour, no stats; before the lane record.
        "ch01_d2_bikini_red": [],  # Flavor: no stats
        "ch01_d2_bikini_white": [],  # Flavor: no stats
        "ch01_d2_bikini_red_second": [],  # Flavor: no stats
        "ch01_d2_bikini_white_second": [],  # Flavor: no stats
        "ch01_d2_bikini_ntr_red": [],  # Flavor: no stats
        "ch01_d2_bikini_ntr_white": [],  # Flavor: no stats
        # Post-shop extras (new mechanics program, B1/B3). Each shows only when its condition holds.
        # Leia's version (B1): the boutique slip played with Julian there (Ryan-absent branch).
        "ch01_d2_boutique_her_version": [
            ("relationship", "trust", 1),
        ],
        # Ryan's thoughts (B3): only when he kept the Day One dream thought.
        "ch01_d2_postshop_dream": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
    })

    CHOICE_TAGS.update({
        "ch01_dream_ground": ("supportive", "attentive", "love-route"),
        "ch01_dream_curiosity": ("open", "curious", "exhibitionism-seed"),
        "ch01_dream_withdraw": ("nonchalant", "withdrawal", "ntr-seed"),
        "ch01_d2_morning_reassure": ("supportive", "attentive", "love-route"),
        "ch01_d2_morning_tease": ("encouraging", "open", "playful", "attentive"),
        "ch01_d2_morning_dismiss": ("neutral", "nonchalant", "dismissive"),
        "ch01_d2_postshop_sleep": ("supportive", "attentive", "honest", "repair"),
        "ch01_d2_postshop_head": ("attentive", "honest", "repair"),
        "ch01_d2_postshop_shut_down": ("neutral", "nonchalant", "dismissive"),
        "ch01_d2_overheard_own": ("attentive", "honest", "repair"),
        "ch01_d2_overheard_joke": ("neutral", "playful"),
        "ch01_d2_overheard_pretend": ("nonchalant", "withdrawal"),
        "ch01_d2_maya_reassure": ("supportive", "attentive", "reassuring"),
        "ch01_d2_maya_tease_jealousy": ("playful", "attentive"),
        "ch01_d2_maya_open_honest": ("open", "honest", "trusting"),
        "ch01_d2_maya_include": ("supportive", "attentive", "reassuring"),
        "ch01_d2_maya_catchup": ("neutral", "trusting"),
        "ch01_d2_maya_dismiss_leia": ("neutral", "nonchalant", "dismissive", "distracted"),
        "ch01_d2_photo_pair_encourage": ("encouraging", "open", "participating"),
        "ch01_d2_photo_pair_redirect": ("protective", "attentive", "boundary-setting"),
        "ch01_d2_photo_pair_shrug": ("neutral", "nonchalant", "dismissive"),
        "ch01_d2_pool_reassure": ("supportive", "attentive", "trusting"),
        "ch01_d2_pool_honest_jealous": ("protective", "honest", "attentive"),
        "ch01_d2_pool_accuse": ("protective", "nonchalant", "dismissive"),
        "ch01_d2_sunset_connect": ("supportive", "attentive", "love-route"),
        "ch01_d2_sunset_partial": ("attentive", "honest", "repair"),
        "ch01_d2_sunset_ignore_gate": ("neutral", "nonchalant", "dismissive", "distracted", "ntr-gate"),
        "ch01_d2_bed_pool_love": ("supportive", "attentive", "honest", "repair"),
        "ch01_d2_bed_pool_exhibition": ("encouraging", "open", "honest", "participating", "repair"),
        "ch01_d2_bed_pool_accuse": ("protective", "dismissive", "unresolved"),
        "ch01_d2_wink_repair": ("supportive", "attentive", "honest", "repair"),
        "ch01_d2_wink_accuse_hard": ("protective", "jealous", "accusatory", "ntr-confirm"),
        "ch01_d2_wink_reject_hard": ("neutral", "nonchalant", "dismissive", "ntr-confirm"),
        "ch01_d2_dare_nod": ("encouraging", "open", "playful"),
        "ch01_d2_dare_shrug": ("neutral", "trusting"),
        "ch01_d2_dare_lap": ("supportive", "attentive", "love-route"),
        "ch01_d2_knot_fix": ("protective", "attentive", "supportive"),
        "ch01_d2_knot_tell": ("neutral", "attentive", "honest"),
        "ch01_d2_knot_watch": ("encouraging", "curious", "open"),
        "ch01_d2_knot_touch_exhib": ("encouraging", "open", "participating"),
        "ch01_d2_knot_touch_ntr": ("protective", "jealous"),
        "ch01_d2_bikini_red": ("open", "playful"),
        "ch01_d2_bikini_white": ("neutral",),
        "ch01_d2_bikini_red_second": ("open", "playful"),
        "ch01_d2_bikini_white_second": ("neutral",),
        "ch01_d2_bikini_ntr_red": ("open",),
        "ch01_d2_bikini_ntr_white": ("honest",),
        "ch01_d2_boutique_her_version": ("attentive", "honest", "curious"),
        "ch01_d2_postshop_dream": ("supportive", "attentive", "honest", "repair"),
    })


    def ch01_d2_choice_ids():
        return choice_ids_with_prefix("ch01_d2_")


    # Door A (sc 15, after the pre-split record) must not change which of today's lanes plays:
    # its Exhibitionism counts for the end-of-day route and Days 3+, not for the lane checks.
    # Leia's errand ids and Ryan's confession reply join this tuple too (docs/LEIA_SIDE.md): the
    # loop subtracts what each really applied (lc_choice_applied_effects), as lc_exhib_gained adds.
    # Leia's errand, Ryan's confession reply and his scene 30 bring-up (Leia's side design,
    # "Lanes and the end route"): they count from Day Three on, never for tonight's lane or end
    # route (ch01_d2_love_exhib_blend below). Door A only skips the lane checks.
    CH01_D2_ERRAND_EXEMPT_CHOICES = (
        "ch01_d2_errand_cafe_love_thank",
        "ch01_d2_errand_cafe_love_brush",
        "ch01_d2_errand_cafe_exhib_linger",
        "ch01_d2_errand_cafe_exhib_mention",
        "ch01_d2_errand_cafe_ntr_linger",
        "ch01_d2_errand_cafe_ntr_shut",
        "ch01_d2_errand_shop_tell",
        "ch01_d2_errand_shop_keep",
        "ch01_d2_errand_shop_mirror_leave",
        "ch01_d2_errand_shop_mirror_fix",
        "ch01_d2_errand_walk_tell",
        "ch01_d2_errand_walk_keep",
        "ch01_d2_confession_ask",
        "ch01_d2_confession_protect",
        "ch01_d2_confession_brush",
        "ch01_d2_feed_love_tease",
        "ch01_d2_feed_exhib_show",
        "ch01_d2_feed_told_aside",
        "ch01_d2_feed_kept_ask",
        "ch01_d2_feed_kept_silent",
        "ch01_d2_feed_let_go",
    )
    CH01_D2_LANE_EXEMPT_CHOICES = ("ch01_d2_knot_watch", "ch01_d2_knot_touch_exhib", "ch01_d2_knot_touch_ntr") + CH01_D2_ERRAND_EXEMPT_CHOICES

    def ch01_d2_route_lane():
        """Resolve the active Day Two lane (stat model v2: lc_stat_model.d2_route_lane).

        Choices in CH01_D2_LANE_EXEMPT_CHOICES are left out of today's lane checks.

        NTR risk needs Temptation, with a Day One NTR seed or high enough on its
        own. The Love + Exhibitionism lane needs Exhibitionism plus some gained
        today. Protection and closeness never create NTR pressure. A save that
        was converted mid-Day-Two keeps its old lane until the day ends.
        """
        migrated = None
        if not has_story_flag("ch01_day_02_complete"):
            migrated = get_story_value("ch01_d2_lane_migrated", None)
        stats = dict(lc_stats_flat())
        gained = lc_exhib_gained("ch01_d2_")
        for exempt_id in CH01_D2_LANE_EXEMPT_CHOICES:
            if exempt_id in renpy.store.choice_history and exempt_id in CHOICE_EFFECTS:
                for _group, stat, amount in lc_choice_applied_effects(exempt_id):
                    stats[stat] = stats.get(stat, 0) - amount
                    if stat == "exhibitionism":
                        gained -= amount
        return lc_stat_model.d2_route_lane(
            stats,
            get_story_value("ch01_day1_route_pressure", "mixed"),
            gained,
            focus=lc_route_explorer_for_lane(),
            migrated_lane=migrated,
        )


    def ch01_d2_love_exhib_blend(lane):
        """Scene 30's Love + Exhibitionism blend (the end route) without Leia's errand ids.

        Stats and today's Exhibitionism minus what each CH01_D2_ERRAND_EXEMPT_CHOICES pick really
        applied (lc_choice_applied_effects, as the lane does), so her side and Ryan's replies to
        it never change tonight's end route. Door A still counts here, as before.
        """
        stats = dict(lc_stats_flat())
        gained = lc_exhib_gained("ch01_d2_")
        for exempt_id in CH01_D2_ERRAND_EXEMPT_CHOICES:
            if exempt_id in renpy.store.choice_history and exempt_id in CHOICE_EFFECTS:
                for _group, stat, amount in lc_choice_applied_effects(exempt_id):
                    stats[stat] = stats.get(stat, 0) - amount
                    if stat == "exhibitionism":
                        gained -= amount
        return lc_stat_model.d2_love_exhib_blend(lane, stats, gained)


    def format_day2_risk_choice(choice_id, base_text, severity="soft"):
        """Risk-aware choice labels that respect the player's visibility mode."""
        mode = current_choice_mode()
        if mode == "normal":
            return base_text

        if severity == "hard":
            marker = "{color=#ff4242}◆◆{/color}"
            if mode == "insight":
                return "{} {}\n[Critical relationship choice]".format(marker, base_text)
            if mode == "full":
                return "{} {}\n[CRITICAL ROUTE CHOICE] [{}]".format(
                    marker, base_text, _choice_effect_text(choice_id, exact=True)
                )
            return "{} {}\n[CONFIRM NTR ROUTE] [{}]  [ID: {}]".format(
                marker, base_text, _choice_effect_text(choice_id, exact=True), choice_id
            )

        marker = "{color=#d85a5a}◆{/color}"
        if mode == "insight":
            return "{} {}\n[Major relationship consequence]".format(marker, base_text)
        if mode == "full":
            return "{} {}\n[MAJOR RELATIONSHIP CONSEQUENCE] [{}]".format(
                marker, base_text, _choice_effect_text(choice_id, exact=True)
            )
        return "{} {}\n[NTR GATE 1] [{}]  [ID: {}]".format(
            marker, base_text, _choice_effect_text(choice_id, exact=True), choice_id
        )


# Scenes 16-30 (was ch01_day2_scenes_16_30.rpy): choice rows and the Maya DM phone moment.
init 1 python:

    # Day Two phone moment (docs/PHONE_MOMENTS.md): Maya's late DM in scene 30. The reply card
    # itself is stat-free; ch01_d2_maya_dm_settle() scores the pick once, in the story (the card
    # shows the stat line in Insight/Full through each option's choice_id). Leaving it on read is
    # the card's default and neutral, so a player who never opens the phone plays the scene as
    # before (one extra narration line). Only a pick made during the bedroom beat, with
    # [girlfriend_name] right there, moves a stat: after it, "show" is gone and a late reply
    # settles neutrally (ch01_d2_maya_dm_reply_late).
    CHOICE_EFFECTS.update({
        "ch01_d2_maya_dm_reply": [
            ("relationship", "trust", 1),
        ],
        "ch01_d2_maya_dm_read": [],
        "ch01_d2_maya_dm_show": [
            ("relationship", "love", 1),
        ],
        "ch01_d2_maya_dm_reply_late": [],
    })
    CHOICE_TAGS.update({
        "ch01_d2_maya_dm_reply": ("attentive",),
        "ch01_d2_maya_dm_read": (),
        "ch01_d2_maya_dm_show": ("open", "supportive"),
        "ch01_d2_maya_dm_reply_late": (),
    })
    lc_phone_moment_register("ch01_d2_maya_dm", "ch01_d2", "Maya, a late text", "nosy",
                             found_on=("reply", "show"))

    # What Leia types when he shows her, and Maya's answer, by the bedroom branch that follows.
    CH01_D2_MAYA_DM_SHOW = {
        "love": ("it's [girlfriend_name] 🙂 we're really good. go be nice to [friend_name] 💕",
                 "BABE 😭 okay okay, leaving you alone. goodnight lovebirds"),
        "exhib": ("it's [girlfriend_name] 😇 we're very okay. don't ask",
                  "oh I'm asking. tomorrow. in detail 👀"),
        "shy": ("hi it's [girlfriend_name] 🙈 we're fine!! goodnight",
                "🙈 cute. goodnight you two"),
        "cool": ("it's [girlfriend_name]. we're fine. go to sleep lol",
                 "rude 😂 night babe"),
    }

    def ch01_d2_maya_dm_mood(lane, tint, soft_gate, wink, pool_suspicion, love_exhib_blend):
        """Leia's answer follows the branch scene 30 takes next: the nightmare or the pool talk
        (cool), the open curtains (exhib), the Love lane (love), else her shy baseline."""
        if tint == "temptation" or (soft_gate and wink) or (
                pool_suspicion and not soft_gate and lane == "ntr_risk"):
            return "cool"
        if lane == "exhibitionism" or love_exhib_blend:
            return "exhib"
        if lane == "love":
            return "love"
        return "shy"

    def ch01_d2_maya_dm_offer(mood):
        leia_text, maya_answer = CH01_D2_MAYA_DM_SHOW.get(mood, CH01_D2_MAYA_DM_SHOW["shy"])
        lc_phone_set_story_time("23:52")
        phone_add_message("maya", "maya", text="you two okay in there? 👀",
                          message_id="ch01_d2_maya_dm_01", mark_unread=True, notify=True,
                          notification_title="Maya")
        phone_add_message("maya", "maya",
                          text="asking because it's very quiet through this wall and [friend_name] is pretending to be asleep. badly.",
                          message_id="ch01_d2_maya_dm_02", mark_unread=True, notify=False)
        phone_offer_reply("maya", "ch01_d2_maya_dm", [
            {"id": "reply", "text": "We're good. Go to sleep, Maya.", "hesitate": True,
             "draft": "why are you listening through the w",
             "followups": [("maya", "\"we're good.\" wow. riveting. goodnight 😘")],
             "choice_id": "ch01_d2_maya_dm_reply"},
            {"id": "read", "text": "Leave it on read", "leave_on_read": True,
             "choice_id": "ch01_d2_maya_dm_read"},
            {"id": "show", "text": "Show [girlfriend_name]", "send": leia_text,
             "followups": [("maya", maya_answer)], "choice_id": "ch01_d2_maya_dm_show"},
        ], "read")
        return None

    def ch01_d2_maya_dm_end_show():
        """End of the bedroom beat: [girlfriend_name] is no longer looking at the screen. A card
        still open keeps reply / leave on read only, and a late reply is unscored (nobody on
        screen sees it), which its stat line now says."""
        prompt = phone_pending_reply("maya")
        if prompt and prompt.get("id") == "ch01_d2_maya_dm":
            options = []
            for option in prompt["options"]:
                if option["id"] == "show":
                    continue
                if option["id"] == "reply":
                    option = dict(option, choice_id="ch01_d2_maya_dm_reply_late")
                options.append(option)
            store.phone_reply_prompts["maya"] = dict(prompt, options=options)
            set_story_flag("ch01_d2_maya_dm_late")
        return None

    def ch01_d2_maya_dm_settle(close=False):
        """Score the DM pick once. close=True (end of Day Two): a card nobody answered runs out
        as left on read (unopened), and the phone clock goes back to the device clock."""
        if close and (phone_pending_reply("maya") or {}).get("id") == "ch01_d2_maya_dm":
            phone_default_reply("maya")
        pick = get_story_value("ch01_d2_maya_dm")
        if pick and not has_story_flag("ch01_d2_maya_dm_scored"):
            set_story_flag("ch01_d2_maya_dm_scored")
            if pick == "show":
                apply_choice("ch01_d2_maya_dm_show")
            elif pick == "reply" and has_story_flag("ch01_d2_maya_dm_late"):
                apply_choice("ch01_d2_maya_dm_reply_late")
            elif pick == "reply":
                apply_choice("ch01_d2_maya_dm_reply")
            else:
                apply_choice("ch01_d2_maya_dm_read")
        # Back to the device clock once nothing is waiting on the 23:52 thread.
        if close or not phone_pending_reply("maya"):
            lc_phone_clear_story_time()
        return None

    def ch01_d2_maya_dm_review_lines():
        """The day review's readable line for each pick (lc_review_choice_catalog scans these)."""
        return [
            format_choice("ch01_d2_maya_dm_reply", "Texted Maya back that we were good."),
            format_choice("ch01_d2_maya_dm_read", "Left Maya's late text on read."),
            format_choice("ch01_d2_maya_dm_show", "Showed " + girlfriend_name + " Maya's late text."),
            format_choice("ch01_d2_maya_dm_reply_late", "Texted Maya back later that night."),
        ]


# Things Ryan noticed (docs/NOTICES.md): the extra sunset-talk option offered after a morning
# notice. Scored like any choice (Love shape); noticing itself never moves stats.
init 1 python:
    CHOICE_EFFECTS.update({
        "ch01_d2_sunset_noticed": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
    })
    CHOICE_TAGS.update({
        "ch01_d2_sunset_noticed": ("supportive", "attentive", "honest"),
    })


# Day Two pool-outfit names and descriptions (folded from the retired
# zzzz_ch01_day2_polish_revision.rpy in clean-up PR 3, with its four label overrides).
# load order: init 998, kept from that file so these overwrite the
# systems/outfits_data.rpy entries at the same point of the init sequence as before.
init 998 python:
    # Both Day One/Day Two pool options are two-piece tie bikinis. The bolder
    # version shows more skin; the classic version simply has more coverage.
    OUTFIT_DEFINITIONS["pool_conservative"]["name"] = "Classic Tie Bikini"
    OUTFIT_DEFINITIONS["pool_conservative"]["description"] = "A two-piece tie bikini with fuller coverage and a familiar, comfortable fit."
    OUTFIT_DEFINITIONS["pool_bolder"]["name"] = "Bolder Tie Bikini"
    OUTFIT_DEFINITIONS["pool_bolder"]["description"] = "A more revealing two-piece tie bikini with less coverage and a bolder resort cut."


# Engine hooks (systems/stats.rpy, systems/choice_path_tags.rpy): Day Two's Full "Current lean"
#   reader, the pre-v2 save migration that keeps a mid-Day-2 lane, and the gate formatter.
init 1 python:
    def ch01_d2_current_lean(lean, flat):
        """current_lean hook: the stored Day Two end route, or today's lane while Day Two runs."""
        if has_story_flag("ch01_day_02_complete"):
            return lc_stat_model.lean_from_route_value(get_story_value("ch01_d2_end_route", "love"))
        if has_story_flag("ch01_day_02_started"):
            lane = ch01_d2_route_lane()
            if ch01_d2_love_exhib_blend(lane):
                return "love_exhib"
            return lc_stat_model.lean_from_route_value(lane)
        return lean

    def ch01_d2_keep_legacy_lane(rel, par, ply):
        """stats_v2_migrate hook: a save made mid-Day-2 keeps the lane the old rules gave it for the
        rest of that day (ch01_d2_lane_migrated), so loading can't flip it."""
        if (has_story_flag("ch01_day_02_started") and not has_story_flag("ch01_day_02_complete")
                and get_story_value("ch01_d2_lane_migrated", None) is None):
            d2_ids = choice_ids_with_prefix("ch01_d2_")
            lane = lc_stat_model.legacy_d2_lane(
                rel, par, ply,
                get_story_value("ch01_day1_route_pressure", "mixed"),
                chapter_nonchalant_count("ch01"),
                choice_tag_count("nonchalant", d2_ids),
                choice_tag_count("open", d2_ids),
                choice_tag_count("attentive", d2_ids),
            )
            set_story_value("ch01_d2_lane_migrated", lane)
    lc_hook_add("current_lean", ch01_d2_current_lean)
    lc_hook_add("stats_v2_migrate", ch01_d2_keep_legacy_lane)
    LC_GATE_FORMATTERS.append("format_day2_risk_choice")


# Love outfit control (systems/love_outfit_control.rpy): Day Two's narrative evening outfit, and the
#   stored end route that earns Love outfit control.
# load order: init 10, as when it lived in love_outfit_control.rpy (after the wardrobe data).
init 10 python:
    LOVE_OUTFIT_ROUTE_KEY = "ch01_d2_end_route"

    # Day Two needs a distinct narrative outfit even though final art is still
    # pending. Until final layers are generated it reuses the current bold
    # placeholder layer.
    if "d2_loose_low_cut" not in OUTFIT_DEFINITIONS:
        OUTFIT_DEFINITIONS["d2_loose_low_cut"] = {
            "name": "Loose Low-Cut Top + Fitted Skirt",
            "category": "bold",
            "description": "A loose low-cut evening top with a fitted skirt. The neckline shifts noticeably when Leia leans forward.",
            "cost": 0,
            "shop_visible": False,
            "story_grant": True,
            "shop_requirements": [],
            "boldness": 70,
            "exposure": 65,
            "public_risk": 55,
            "comfort": 45,
            "playfulness": 65,
            "elegance": 55,
            "contexts": ("date", "restaurant", "nightlife", "evening"),
            "asset_id": "leia_outfit_d2_loose_low_cut",
            "wear_paths": [
                {
                    "id": "story_d2_evening",
                    "label": "Day Two evening outfit",
                    "requirements": [],
                },
            ],
        }


# ------------------------------------------------------------------ story-key ledger
# Every story flag / value this Day sets, one line each (tests/test_day_packs.py checks it):
#   # key <name>: read-by <who reads it>     or     # key <name>: pending <why nothing reads it yet>
# Patterns with * cover dynamic keys. Keys are save data: never rename one.
# key ch01_d2_bedroom_variant: pending set by ch01_day2_scenes_16_30.rpy, chapter_select.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_bikini_tie_loose: pending set by ch01_day2_scenes_01_15.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_boutique_black_mini_reserved_day3: pending set by ch01_day2_scenes_16_30.rpy, chapter_select.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_boutique_outfit_owned: pending set by ch01_day2_scenes_01_15.rpy, chapter_select.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_bikini_jealousy: read-by ch01_day2_scenes_01_15.rpy
# key ch01_d2_boutique_shop_open: read-by outfits_data.rpy
# key ch01_d2_boutique_slip_witness: read-by ch01_day2_scenes_01_15.rpy, lc_thoughts.py
# key ch01_d2_boutique_trial_outfit: pending set by ch01_day2_scenes_01_15.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_confession_reply: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_dare_signal: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_dinner_outfit: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_dinner_outfit_id: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_dinner_outfit_source: pending set by ch01_day2_scenes_16_30.rpy, chapter_select.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_dinner_reach: read-by ch01_day2_gallery.rpy, ch01_day2_scenes_16_30.rpy, lc_thoughts.py
# key ch01_d2_dinner_wink: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_end_route: read-by ch01_day2_chapter.rpy, ch01_day3_scenes.rpy, ch01_day4_registrations.rpy +4 more
# key ch01_d2_errand_lane: read-by ch01_day2_feed.rpy, ch01_day2_scene_19b_leia_asks_maya.rpy, ch01_day2_scenes_16_30.rpy
# key ch01_d2_errand_reason: read-by ch01_day2_scene_19b_leia_asks_maya.rpy
# key ch01_d2_errand_ryan_mood: read-by ch01_day2_leia_errand.rpy, ch01_day2_scene_19b_leia_asks_maya.rpy, ch01_day2_scenes_16_30.rpy
# key ch01_d2_exhibition_bedroom_open_curtains: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_exhibition_pool_shared_with_ryan: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_exhibition_pool_tease: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_exhibition_sunset_shared: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_feed_bringup: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_julian_bee_fear_seeded: pending set by ch01_day2_scenes_01_15.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_julian_reveal_seen: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_julian_shades_removed: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_julian_sleeping: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_julian_upstairs_before_sunset: pending set by ch01_day2_scene_19b_leia_asks_maya.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_knot_response: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_lane_migrated: read-by ch01_day2_scenes_01_15.rpy, stats.rpy
# key ch01_d2_leia_maya_comfort: pending set by ch01_day2_scene_19b_leia_asks_maya.rpy, ch01_day2_scenes_01_15.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_leia_noticed_julian_stare: read-by ch01_day2_scenes_01_15.rpy
# key ch01_d2_leia_told: read-by ch01_day2_feed.rpy, ch01_day2_scene_19b_leia_asks_maya.rpy, ch01_day2_scenes_16_30.rpy
# key ch01_d2_love_sunset_oral: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_mall_entry_lane: read-by ch01_day2_scenes_01_15.rpy
# key ch01_d2_mall_outfit_source: read-by ch01_day4_scenes_09_16.rpy, ch01_day5_scenes_01_08.rpy, ch01_day5_scenes_09_16.rpy
# key ch01_d2_mall_ryan_response: read-by ch01_day2_scenes_01_15.rpy
# key ch01_d2_maya_dm_late: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_maya_dm_scored: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_maya_julian_consent_established: pending set by ch01_day2_scene_19b_leia_asks_maya.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_maya_julian_share_room: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_maya_julian_talk: pending set by ch01_day2_scene_19b_leia_asks_maya.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_maya_julian_talk_complete: pending set by ch01_day2_scene_19b_leia_asks_maya.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_maya_left_before_sunset: pending set by ch01_day2_scene_19b_leia_asks_maya.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_maya_meetup_confirmed: pending set by ch01_day2_scenes_01_15.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_maya_pushed_boutique_tryon: pending set by ch01_day2_scenes_01_15.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_maya_sleeping: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_maya_stays_for_drinks: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_nhie_julian_clothes: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_nhie_leia_clothes: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_nhie_leia_topless_covering: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_nhie_maya_clothes: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_nhie_maya_nude: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_ntr_confirmed: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_ntr_soft_gate: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_ntr_soft_gate_repaired: pending set by ch01_day2_scenes_16_30.rpy, chapter_select.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_overheard_response: read-by ch01_day2_scenes_01_15.rpy, ch01_day2_scenes_16_30.rpy
# key ch01_d2_overheard_talk: read-by ch01_day2_scenes_01_15.rpy, ch01_day2_scenes_16_30.rpy
# key ch01_d2_photo_group: read-by phone_group_avatar.rpy
# key ch01_d2_photo_leia_maya: read-by ch01_day2_gallery.rpy
# key ch01_d2_pool_attention: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_pool_incident: read-by ch01_day2_scenes_16_30.rpy, lc_thoughts.py
# key ch01_d2_pool_outfit: read-by ch01_day2_scenes_01_15.rpy, ch01_day5_registrations.rpy
# key ch01_d2_pool_response: read-by ch01_day2_leia_errand.rpy, ch01_day2_scene_19b_leia_asks_maya.rpy, ch01_day2_scenes_16_30.rpy
# key ch01_d2_pool_suspicion: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_route_lane_dinner: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_route_lane_post_pool: read-by ch01_day2_leia_errand.rpy, ch01_day2_scenes_16_30.rpy
# key ch01_d2_route_lane_post_sunset: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_route_lane_pre_split: read-by ch01_day2_scenes_01_15.rpy, ch01_day2_scenes_16_30.rpy
# key ch01_d2_scene_04_complete: read-by lc_thoughts.py
# key ch01_d2_scene_07_complete: read-by lc_thoughts.py
# key ch01_d2_scene_30_complete: read-by chapter_select.rpy
# key ch01_d2_split: read-by ch01_day2_leia_errand.rpy, ch01_day2_scenes_16_30.rpy
# key ch01_d2_strip_penalty_agreed: read-by lc_thoughts.py
# key ch01_d2_sunset_noticed: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_sunset_response: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_day_02_complete: read-by ch01_day2_scenes_01_15.rpy, chapter_select.rpy, full_transparency_route_explorer.rpy +3 more
# key ch01_day_02_started: read-by chapter_select.rpy, lc_ui_logic.py, stats.rpy
# key ch01_d2_scene_*_complete: pending scene-done markers (27 keys; scene-done helper), nothing reads them yet
# key ch01_d2_route_lane_*: pending dynamic keys set by chapter_select.rpy
