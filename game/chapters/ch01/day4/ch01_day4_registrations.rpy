# Leia's Consent: Chapter One, Day Four choice registration + helpers.
#
# DROP-IN FILE. Follows the exact Day Two pattern from ch01_day2_scenes_01_15.rpy:
#   init 1 python:
#       CHOICE_EFFECTS.update({...})
#       CHOICE_TAGS.update({...})
# Stable ids use the "ch01_d4_" prefix so chapter_nonchalant_count("ch01") and
# choice_ids_with_prefix("ch01_d4_") pick them up.
#
# Effect rows are (group, stat, amount) with group in relationship / partner / player, scored
# with the stat model v2 rule (docs/STAT_MODEL.md, tests/test_choice_scoring.py). These are the
# effective rows: the Day Four pack is the only place they are defined.
#
# Scale note: ordinary Day Four choices are +/-1..2 (slow burn). Gate choices follow the
# Day Two gate scale (soft gate -1..2, hard gate up to -5). Nothing here moves a stat by more
# than 5 in one pick.

init 1 python:

    CHOICE_EFFECTS.update({

        # --- 02 phone morning (Love / Exhibition lanes) ---
        "ch01_d4_text_warm": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d4_text_flirt": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 2),
        ],
        "ch01_d4_text_coffee": [
            ("relationship", "love", 1),
        ],

        # --- 02 phone morning (NTR lane) ---
        "ch01_d4_ntr_text_join": [
            ("relationship", "love", 1),
            ("relationship", "temptation", -1),
        ],
        "ch01_d4_ntr_text_later": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_d4_ntr_text_fine_soft": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 3),
        ],

        # --- 03 wardrobe morning ---
        "ch01_d4_wardrobe_ryan_picks": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 1),
        ],
        "ch01_d4_wardrobe_leia_decides": [
            ("relationship", "love", 1),
            ("relationship", "trust", 2),
        ],
        "ch01_d4_wardrobe_bolder": [
            ("partner", "exhibitionism", 3),
        ],
        "ch01_d4_wardrobe_comfort": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d4_ntr_compliment": [
            ("relationship", "love", 1),
            ("relationship", "temptation", -1),
        ],
        "ch01_d4_ntr_guarded": [
            ("relationship", "trust", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_d4_ntr_flat": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],

        # --- 04 breakfast ---
        "ch01_d4_breakfast_leave_it": [],  # Neutral: no stats
        "ch01_d4_breakfast_tease": [
            ("relationship", "love", 1),
        ],
        "ch01_d4_breakfast_ask_maya": [
            ("relationship", "trust", 1),
        ],

        # --- 06 photo hunt: how Ryan shoots Leia ---
        "ch01_d4_photo_candid": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d4_photo_pose": [
            ("partner", "exhibitionism", 2),
        ],
        "ch01_d4_photo_swap": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d4_photo_skip": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],

        # --- 08 afternoon quiet ---
        "ch01_d4_julian_thanks": [
            ("relationship", "trust", 1),
        ],
        "ch01_d4_julian_joke": [],  # Neutral: no stats
        "ch01_d4_julian_deflect": [
            ("relationship", "temptation", 1),
        ],
        "ch01_d4_ntr_ask_gently": [
            ("relationship", "trust", 2),
            ("relationship", "temptation", -3),
        ],
        "ch01_d4_ntr_fine_soft2": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 3),
        ],
        "ch01_d4_ntr_press_early": [
            ("relationship", "trust", -1),
            ("relationship", "temptation", 1),
        ],

        # --- 09 getting ready for dusk ---
        "ch01_d4_dusk_ryan_picks": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 1),
        ],
        "ch01_d4_dusk_leia_decides": [
            ("relationship", "love", 1),
            ("relationship", "trust", 2),
        ],
        "ch01_d4_dusk_bolder": [
            ("partner", "exhibitionism", 3),
        ],
        "ch01_d4_dusk_comfort": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],

        # --- 10 dinner toast ---
        "ch01_d4_toast_leia": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d4_toast_group": [],  # Neutral: no stats
        "ch01_d4_toast_dare": [
            ("partner", "exhibitionism", 1),
        ],

        # --- 13 Love night ---
        "ch01_d4_love_slow_dance": [
            ("relationship", "love", 2),
            ("relationship", "trust", 1),
        ],
        "ch01_d4_love_terrace_stay": [
            ("relationship", "love", 1),
            ("relationship", "trust", 2),
        ],
        "ch01_d4_love_open_door": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 2),
        ],

        # --- 13 Exhibition night ---
        "ch01_d4_exhib_together": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 3),
        ],
        "ch01_d4_exhib_like_watching": [
            ("partner", "exhibitionism", 3),
        ],
        "ch01_d4_exhib_private": [
            ("relationship", "love", 2),
            ("relationship", "trust", 1),
        ],
        "ch01_d4_exhib_her_call": [
            ("relationship", "trust", 1),
            ("partner", "exhibitionism", 2),
        ],
        "ch01_d4_exhib_tease_then_me": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 1),
        ],

        # --- 13 NTR night: repair gate ---
        "ch01_d4_ntr_gate_reconnect": [
            ("relationship", "trust", 3),
            ("relationship", "temptation", -5),
        ],
        "ch01_d4_ntr_gate_accuse_hard": [
            ("relationship", "love", -3),
            ("relationship", "trust", -3),
            ("relationship", "temptation", 4),
        ],
        "ch01_d4_ntr_gate_withdraw_hard": [
            ("relationship", "love", -5),
            ("relationship", "trust", -4),
            ("relationship", "temptation", 5),
        ],
        "ch01_d4_ntr_react_thanks": [
            ("relationship", "love", 1),
            ("relationship", "trust", 2),
        ],
        "ch01_d4_ntr_react_boundary": [
            ("relationship", "love", 1),
            ("relationship", "temptation", -1),
        ],
        "ch01_d4_ntr_react_curious": [
            ("relationship", "trust", 1),
            ("partner", "exhibitionism", 3),
        ],

        # --- 15 phone hook ---
        "ch01_d4_hook_in": [],  # Neutral: no stats
        "ch01_d4_hook_ask_leia": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d4_hook_maybe": [
            ("relationship", "temptation", 1),
        ],
    })

    CHOICE_TAGS.update({
        "ch01_d4_text_warm": ("supportive", "attentive", "love-route"),
        "ch01_d4_text_flirt": ("encouraging", "open", "playful", "attentive"),
        "ch01_d4_text_coffee": ("neutral", "lighthearted", "attentive"),
        "ch01_d4_ntr_text_join": ("supportive", "attentive", "honest", "repair"),
        "ch01_d4_ntr_text_later": ("neutral", "unresolved", "distracted"),
        "ch01_d4_ntr_text_fine_soft": ("neutral", "nonchalant", "dismissive", "distracted", "ntr-gate"),

        "ch01_d4_wardrobe_ryan_picks": ("supportive", "attentive", "participating", "love-route"),
        "ch01_d4_wardrobe_leia_decides": ("supportive", "respectful", "comfort-first"),
        "ch01_d4_wardrobe_bolder": ("encouraging", "open", "participating", "playful"),
        "ch01_d4_wardrobe_comfort": ("supportive", "comfort-first", "attentive"),
        "ch01_d4_ntr_compliment": ("supportive", "attentive", "repair"),
        "ch01_d4_ntr_guarded": ("protective", "jealous", "guarded"),
        "ch01_d4_ntr_flat": ("neutral", "nonchalant", "dismissive"),

        "ch01_d4_breakfast_leave_it": ("neutral", "trusting", "respectful"),
        "ch01_d4_breakfast_tease": ("encouraging", "lighthearted", "playful"),
        "ch01_d4_breakfast_ask_maya": ("supportive", "attentive", "honest"),

        "ch01_d4_photo_candid": ("supportive", "attentive", "love-route"),
        "ch01_d4_photo_pose": ("encouraging", "open", "playful", "attentive"),
        "ch01_d4_photo_swap": ("playful", "attentive", "reciprocal"),
        "ch01_d4_photo_skip": ("neutral", "nonchalant", "dismissive", "distracted"),

        "ch01_d4_julian_thanks": ("supportive", "honest", "trusting"),
        "ch01_d4_julian_joke": ("encouraging", "lighthearted"),
        "ch01_d4_julian_deflect": ("neutral", "nonchalant", "distracted"),
        "ch01_d4_ntr_ask_gently": ("supportive", "attentive", "honest", "repair"),
        "ch01_d4_ntr_fine_soft2": ("neutral", "nonchalant", "dismissive", "distracted", "ntr-gate"),
        "ch01_d4_ntr_press_early": ("protective", "jealous", "pressing"),

        "ch01_d4_dusk_ryan_picks": ("supportive", "attentive", "participating", "love-route"),
        "ch01_d4_dusk_leia_decides": ("supportive", "respectful", "comfort-first"),
        "ch01_d4_dusk_bolder": ("encouraging", "open", "participating", "playful"),
        "ch01_d4_dusk_comfort": ("supportive", "comfort-first", "attentive"),

        "ch01_d4_toast_leia": ("supportive", "attentive", "love-route"),
        "ch01_d4_toast_group": ("neutral", "trusting", "lighthearted"),
        "ch01_d4_toast_dare": ("encouraging", "open", "playful"),

        "ch01_d4_love_slow_dance": ("attentive", "supportive", "love-route"),
        "ch01_d4_love_terrace_stay": ("attentive", "honest", "supportive"),
        "ch01_d4_love_open_door": ("encouraging", "open", "playful", "attentive", "exhibitionism-seed"),

        "ch01_d4_exhib_together": ("encouraging", "open", "participating", "attentive"),
        "ch01_d4_exhib_like_watching": ("encouraging", "open", "honest", "participating", "watching"),
        "ch01_d4_exhib_private": ("protective", "attentive", "supportive", "boundary-setting"),
        "ch01_d4_exhib_her_call": ("supportive", "open", "attentive", "her-pace"),
        "ch01_d4_exhib_tease_then_me": ("encouraging", "playful", "possessive", "attentive"),

        "ch01_d4_ntr_gate_reconnect": ("supportive", "attentive", "honest", "repair"),
        "ch01_d4_ntr_gate_accuse_hard": ("protective", "jealous", "accusatory", "ntr-confirm"),
        "ch01_d4_ntr_gate_withdraw_hard": ("neutral", "nonchalant", "dismissive", "ntr-confirm"),
        "ch01_d4_ntr_react_thanks": ("supportive", "honest", "repair"),
        "ch01_d4_ntr_react_boundary": ("protective", "boundary-setting", "honest", "repair"),
        "ch01_d4_ntr_react_curious": ("open", "honest", "attentive", "repair", "exhibitionism-seed"),

        "ch01_d4_hook_in": ("encouraging", "open", "participating"),
        "ch01_d4_hook_ask_leia": ("supportive", "attentive", "respectful"),
        "ch01_d4_hook_maybe": ("neutral", "unresolved"),
    })


init 2 python:

    D4_EXHIBITION_BRIEF_REVEAL_MIN = LC_T["d4_brief_reveal"]   # Leia's own Exhibitionism needed for her to choose 'brief reveal' (stat model v2 scale)
    D4_NO_DAY_OUTFITS = ("boutique_cutout_mini", "after_hours_dress")
    D4_NO_DUSK_OUTFITS = ("casual_default",)


    def ch01_d4_choice_ids():
        return choice_ids_with_prefix("ch01_d4_")


    def ch01_d4_nonchalant_count():
        return choice_tag_count("nonchalant", ch01_d4_choice_ids())


    def _lc_d4_track_text_v1():
        """Track card for Insight / Full / Developer modes. Returns None in Normal mode.

        Reads stored state only. It never recomputes a lane.
        """
        mode = current_choice_mode()
        if mode == "normal":
            return None

        lane = get_story_value("ch01_d4_lane", "love")
        if lane == "love":
            head = "TRACK: LOVE (pure couple track)"
            line = ('No outside-attention beats today. Intimacy stays between ' + player_name + ' and ' + girlfriend_name + '.')
        elif lane == "exhibitionism":
            head = "TRACK: SHARED EXHIBITION (NTS)"
            line = (player_name + " stays included. 'Keep it just us' is always available tonight.")
        else:
            head = "TRACK: DISTANCE (NTR pressure)"
            line = "Repair is still possible. Gate choices carry a red diamond."

        if mode == "insight":
            return "{}\n\n{}".format(head, line)

        detail = "Day 2 end: {}  |  Day 3 variant: {}".format(
            get_story_value("ch01_d2_end_route", "?"),
            get_story_value("ch01_d3_end_variant", "?"),
        )
        if mode == "full":
            return "{}\n\n{}\n{}".format(head, line, detail)

        return "{}\n\n{}\n{}\nlane={}  d3_effort={}  cutout_secret={}".format(
            head, line, detail, lane,
            get_story_value("ch01_d3_ntr_repair_effort", "?"),
            has_story_flag("ch01_d3_cutout_secret"),
        )


    def ch01_d4_track_text():
        """The track card with route-name headings (lc_track_text_v2, systems/choice_engine.rpy)."""
        return lc_track_text_v2(_lc_d4_track_text_v1())


    def format_day4_gate_choice(choice_id, base_text, severity="soft", gate_label="D4-1"):
        """Risk-aware label for Day Four NTR gates (mirrors format_day2_risk_choice).

        Written as its own helper so the Developer-mode tag reads 'NTR GATE D4-x' instead of
        reusing the Day Two 'NTR GATE 1' wording.
        """
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
            return "{} {}\n[CONFIRM NTR ROUTE {}] [{}]  [ID: {}]".format(
                marker, base_text, gate_label, _choice_effect_text(choice_id, exact=True), choice_id
            )

        marker = "{color=#d85a5a}◆{/color}"
        if mode == "insight":
            return "{} {}\n[Major relationship consequence]".format(marker, base_text)
        if mode == "full":
            return "{} {}\n[MAJOR RELATIONSHIP CONSEQUENCE] [{}]".format(
                marker, base_text, _choice_effect_text(choice_id, exact=True)
            )
        return "{} {}\n[NTR GATE {}] [{}]  [ID: {}]".format(
            marker, base_text, gate_label, _choice_effect_text(choice_id, exact=True), choice_id
        )


    def ch01_d4_wear(outfit_id):
        """Ask Leia to wear a story outfit through the NORMAL wear-path rules.

        grant_story_outfit(..., equip=True) grants the outfit and equips it only if a wear path
        passes. Returns True when she is wearing it. Only valid for story_grant outfits
        (boutique_cutout_mini, resort_dinner_dress, d2_loose_low_cut ...).
        """
        return bool(grant_story_outfit(outfit_id, equip=True))


    def ch01_d4_day_outfit_options():
        """Love picker options for the market day: outdoor daywear, no swimwear, no nightlife."""
        options = []
        for outfit_id in love_outfit_candidates(
            story_ids=("casual_default", "resort_dinner_dress", "d2_loose_low_cut"),
        ):
            if outfit_id in D4_NO_DAY_OUTFITS or love_outfit_is_swimwear(outfit_id):
                continue
            options.append(outfit_id)
        return options


    def ch01_d4_dusk_outfit_options():
        """Love picker options for the dusk dinner: evening-capable, no swimwear, no plain casual."""
        options = []
        for outfit_id in love_outfit_candidates(
            story_ids=("resort_dinner_dress", "d2_loose_low_cut", "boutique_cutout_mini"),
        ):
            if outfit_id in D4_NO_DUSK_OUTFITS or love_outfit_is_swimwear(outfit_id):
                continue
            options.append(outfit_id)
        return options


# Engine hooks (systems/stats.rpy, systems/choice_path_tags.rpy): Day Four's Full "Current lean"
#   reader and its gate formatter.
init 1 python:
    def ch01_d4_current_lean(lean, flat):
        """current_lean hook: the stored Day Four end route once it is set."""
        value = get_story_value("ch01_d4_end_route", None)
        if value:
            return lc_stat_model.lean_from_route_value(value)
        return lean

    lc_hook_add("current_lean", ch01_d4_current_lean)
    LC_GATE_FORMATTERS.append("format_day4_gate_choice")


# ------------------------------------------------------------------ story-key ledger
# Every story flag / value this Day sets, one line each (tests/test_day_packs.py checks it):
#   # key <name>: read-by <who reads it>     or     # key <name>: pending <why nothing reads it yet>
# Patterns with * cover dynamic keys. Keys are save data: never rename one.
# key ch01_d4_club_story_deferred: read-by ch01_day5_registrations.rpy, chapter_select.rpy
# key ch01_d4_cutout_disclosed: read-by ch01_day4_scenes_09_16.rpy, ch01_day5_registrations.rpy, chapter_select.rpy
# key ch01_d4_cutout_partial: read-by chapter_select.rpy
# key ch01_d4_d3_variant: read-by ch01_day4_scenes_01_08.rpy
# key ch01_d4_day_outfit_id: pending set by ch01_day4_scenes_01_08.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d4_day_outfit_source: pending set by ch01_day4_scenes_01_08.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d4_disclosure_when: pending set by ch01_day4_scenes_01_08.rpy, ch01_day4_scenes_09_16.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d4_dusk_daring: pending set by ch01_day4_scenes_09_16.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d4_dusk_outfit_id: read-by ch01_day4_scenes_09_16.rpy
# key ch01_d4_dusk_outfit_source: read-by ch01_day4_scenes_09_16.rpy
# key ch01_d4_end_route: read-by ch01_day4_chapter.rpy, ch01_day5_registrations.rpy, ch01_day5_scenes_01_08.rpy +1 more
# key ch01_d4_end_route_pending: read-by ch01_day4_scenes_09_16.rpy
# key ch01_d4_end_variant: read-by ch01_day5_registrations.rpy
# key ch01_d4_exhib_brief_done: read-by chapter_select.rpy
# key ch01_d4_exhib_framing: read-by ch01_day4_scenes_09_16.rpy
# key ch01_d4_exhib_ryan_likes_watching: read-by ch01_day5_scenes_01_08.rpy
# key ch01_d4_exhib_tease_done: pending set by ch01_day4_scenes_09_16.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d4_exhib_variant: read-by ch01_day4_scenes_09_16.rpy, ch01_day5_scenes_01_08.rpy, day4.py
# key ch01_d4_exposure_step: read-by ch01_day5_scenes_01_08.rpy
# key ch01_d4_hook_reply: read-by ch01_day5_scenes_01_08.rpy
# key ch01_d4_hunt_winner: read-by ch01_day4_scenes_01_08.rpy, ch01_day4_scenes_09_16.rpy
# key ch01_d4_lane: read-by ch01_day4_registrations.rpy, ch01_day4_scenes_01_08.rpy, ch01_day4_scenes_09_16.rpy +2 more
# key ch01_d4_leia_call: pending set by ch01_day4_scenes_09_16.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d4_love_exhib_seed: read-by ch01_day4_scenes_09_16.rpy, ch01_day5_scenes_01_08.rpy
# key ch01_d4_love_mini_thanks: read-by ch01_day4_scenes_09_16.rpy
# key ch01_d4_love_strained: pending set by ch01_day4_scenes_09_16.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d4_market_honey_bee_callback: read-by chapter_select.rpy
# key ch01_d4_maya_real_talk: pending set by ch01_day4_scenes_01_08.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d4_morning_reply: read-by ch01_day4_scenes_01_08.rpy
# key ch01_d4_ntr_boundary_set: pending set by ch01_day4_scenes_09_16.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d4_ntr_confirmed: read-by ch01_day4_scenes_09_16.rpy
# key ch01_d4_ntr_fine_count: read-by ch01_day4_scenes_01_08.rpy, ch01_day4_scenes_09_16.rpy, ch01_day5_registrations.rpy
# key ch01_d4_ntr_outcome: read-by ch01_day4_scenes_09_16.rpy
# key ch01_d4_ntr_pressed_early: read-by ch01_day4_scenes_09_16.rpy
# key ch01_d4_ntr_react: read-by ch01_day4_scenes_09_16.rpy
# key ch01_d4_ntr_repaired: pending set by ch01_day4_scenes_09_16.rpy, chapter_select.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d4_ntr_repaired_curious: pending set by ch01_day4_scenes_09_16.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d4_ntr_soft_gate: read-by chapter_select.rpy
# key ch01_d4_photo_candid_taken: read-by chapter_select.rpy
# key ch01_d4_photo_pose_taken: read-by chapter_select.rpy
# key ch01_d4_photo_skipped: read-by chapter_select.rpy
# key ch01_d4_photo_style: read-by ch01_day4_scenes_01_08.rpy, ch01_day4_scenes_09_16.rpy, ch01_day5_scenes_01_08.rpy
# key ch01_d4_photo_swap_taken: pending set by ch01_day4_scenes_01_08.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d4_scene_16_complete: read-by chapter_select.rpy
# key ch01_d4_wardrobe_friction: pending set by ch01_day4_scenes_01_08.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_day_04_complete: read-by chapter_select.rpy, lc_ui_logic.py
# key ch01_day_04_started: read-by chapter_select.rpy, lc_ui_logic.py
# key ch01_d4_scene_*_complete: pending scene-done markers (15 keys; scene-done helper), nothing reads them yet
# key ch01_d4_*: pending dynamic keys set by chapter_select.rpy
