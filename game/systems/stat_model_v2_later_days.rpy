# Stat model v2 for Days Three to Five (darryn, 2026-11-08).
#
# The Day Three/Four/Five registration files are Scriptwriter-owned, so their
# CHOICE_EFFECTS entries are re-scored here instead (init 5 runs after their
# init 1/2 blocks, so these are the effective definitions). Same scoring rule
# as systems/choice_engine.rpy; tests/test_choice_scoring.py checks the
# effective table. When the Scriptwriter adds a Day 3-5 choice, add its v2
# effects here (or switch that file to v2 stats) or the test fails.
#
# Also here: the Day Four/Five "her own call" Exhibitionism thresholds, rescaled
# for v2 (Exhibitionism climbs about 2.2x faster than the old stat), and the
# Day Four/Five track-card headings renamed to the route names.

init 5 python:

    CHOICE_EFFECTS.update({
        # Day Three (ch01_day3_scenes.rpy)
        "ch01_d3_ntr_enjoy": [
            ("relationship", "love", 1),
            ("relationship", "temptation", -1),
        ],
        "ch01_d3_ntr_talk": [
            ("relationship", "love", 2),
            ("relationship", "temptation", -3),
        ],
        "ch01_d3_ntr_withdraw": [
            ("relationship", "love", -2),
            ("relationship", "temptation", 3),
        ],
        "ch01_d3_dessert_chocolate": [
            ("relationship", "trust", 1),
        ],
        "ch01_d3_dessert_recommended": [],  # Neutral: no stats
        "ch01_d3_dessert_surprise": [
            ("relationship", "love", 1),
        ],
        # Day Four (ch01_day4_choice_registration.rpy)
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
        "ch01_d4_ntr_text_join": [
            ("relationship", "love", 1),
            ("relationship", "temptation", -1),
        ],
        "ch01_d4_ntr_text_later": [
            ("relationship", "temptation", 1),
        ],
        "ch01_d4_ntr_text_fine_soft": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 3),
        ],
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
            ("relationship", "temptation", 1),
        ],
        "ch01_d4_ntr_flat": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 2),
        ],
        "ch01_d4_breakfast_leave_it": [
            ("relationship", "trust", 1),
            ("partner", "exhibitionism", 1),
        ],
        "ch01_d4_breakfast_tease": [
            ("relationship", "love", 1),
        ],
        "ch01_d4_breakfast_ask_maya": [
            ("relationship", "trust", 1),
            ("partner", "exhibitionism", 1),
        ],
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
            ("relationship", "temptation", 3),
        ],
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
        "ch01_d4_toast_leia": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d4_toast_group": [
            ("partner", "exhibitionism", 1),
        ],
        "ch01_d4_toast_dare": [
            ("partner", "exhibitionism", 2),
        ],
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
        "ch01_d4_hook_in": [
            ("partner", "exhibitionism", 1),
        ],
        "ch01_d4_hook_ask_leia": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d4_hook_maybe": [
            ("relationship", "temptation", 1),
        ],
        # Day Five (ch01_day5_choice_registration.rpy)
        "ch01_d5_pack_ryan_picks": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 1),
        ],
        "ch01_d5_pack_leia_decides": [
            ("relationship", "love", 1),
            ("relationship", "trust", 2),
        ],
        "ch01_d5_pack_bolder": [
            ("partner", "exhibitionism", 3),
        ],
        "ch01_d5_pack_classic": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d5_pack_her_call": [
            ("relationship", "trust", 1),
            ("partner", "exhibitionism", 2),
        ],
        "ch01_d5_ntr_pack_help": [
            ("relationship", "love", 1),
            ("relationship", "temptation", -1),
        ],
        "ch01_d5_ntr_pack_joke": [
            ("relationship", "trust", 1),
        ],
        "ch01_d5_ntr_pack_nothing": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_d5_julian_stay": [
            ("relationship", "trust", 1),
            ("partner", "exhibitionism", 1),
        ],
        "ch01_d5_julian_joke": [],  # Neutral: no stats
        "ch01_d5_julian_leave": [
            ("relationship", "temptation", 1),
        ],
        "ch01_d5_bars_bag": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d5_bars_check": [
            ("relationship", "temptation", 1),
        ],
        "ch01_d5_snorkel_leia_first": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d5_snorkel_maya_first": [],  # Neutral: no stats
        "ch01_d5_snorkel_julian_first": [
            ("relationship", "temptation", 1),
        ],
        "ch01_d5_ntr_snorkel_stay": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 3),
        ],
        "ch01_d5_bee_calm": [
            ("relationship", "trust", 1),
            ("partner", "exhibitionism", 1),
        ],
        "ch01_d5_bee_film": [
            ("partner", "exhibitionism", 1),
        ],
        "ch01_d5_photo_share_group": [
            ("partner", "exhibitionism", 1),
        ],
        "ch01_d5_photo_keep_album": [
            ("relationship", "love", 1),
        ],
        "ch01_d5_eaves_announce": [
            ("relationship", "trust", 1),
        ],
        "ch01_d5_eaves_listen": [
            ("relationship", "trust", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_d5_stern_thanks": [
            ("relationship", "trust", 1),
        ],
        "ch01_d5_stern_joke": [],  # Neutral: no stats
        "ch01_d5_stern_push": [
            ("relationship", "trust", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_d5_love_swim_close": [
            ("relationship", "love", 2),
            ("relationship", "trust", 1),
        ],
        "ch01_d5_love_swim_race": [
            ("relationship", "love", 1),
        ],
        "ch01_d5_love_secret_dream": [
            ("relationship", "love", 1),
            ("relationship", "trust", 3),
        ],
        "ch01_d5_love_secret_mirror": [
            ("relationship", "love", 2),
            ("relationship", "trust", 2),
        ],
        "ch01_d5_love_secret_owe": [
            ("relationship", "temptation", 1),
        ],
        "ch01_d5_exhib_stay": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 3),
        ],
        "ch01_d5_exhib_watching": [
            ("partner", "exhibitionism", 3),
        ],
        "ch01_d5_exhib_private": [
            ("relationship", "love", 2),
            ("relationship", "trust", 1),
        ],
        "ch01_d5_exhib_her_call": [
            ("relationship", "trust", 1),
            ("partner", "exhibitionism", 2),
        ],
        "ch01_d5_exhib_tease_then_me": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 1),
        ],
        "ch01_d5_photo_private_face": [
            ("relationship", "love", 1),
            ("relationship", "trust", 2),
        ],
        "ch01_d5_photo_private_moment": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 2),
        ],
        "ch01_d5_photo_private_none": [
            ("relationship", "love", 2),
            ("relationship", "trust", 2),
        ],
        "ch01_d5_ntr_react_thanks": [
            ("relationship", "love", 1),
            ("relationship", "trust", 2),
        ],
        "ch01_d5_ntr_react_boundary": [
            ("relationship", "love", 1),
            ("relationship", "temptation", -1),
        ],
        "ch01_d5_ntr_react_curious": [
            ("relationship", "trust", 1),
            ("partner", "exhibitionism", 3),
        ],
        "ch01_d5_ntr_gate_fine_hard": [
            ("relationship", "love", -3),
            ("relationship", "trust", -3),
            ("relationship", "temptation", 4),
        ],
        "ch01_d5_ntr_u_ask_gently": [
            ("relationship", "trust", 3),
            ("relationship", "temptation", -4),
        ],
        "ch01_d5_ntr_u_press_hard": [
            ("relationship", "love", -3),
            ("relationship", "trust", -3),
            ("relationship", "temptation", 4),
        ],
        "ch01_d5_ntr_u_fine_hard": [
            ("relationship", "love", -4),
            ("relationship", "trust", -3),
            ("relationship", "temptation", 5),
        ],
        "ch01_d5_ntr_c_go_to_her": [
            ("relationship", "love", 2),
            ("relationship", "temptation", -4),
        ],
        "ch01_d5_ntr_c_accuse_hard": [
            ("relationship", "love", -2),
            ("relationship", "trust", -2),
            ("relationship", "temptation", 3),
        ],
        "ch01_d5_ntr_c_fine_hard": [
            ("relationship", "love", -4),
            ("relationship", "trust", -3),
            ("relationship", "temptation", 5),
        ],
        "ch01_d5_evening_ryan_picks": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 1),
        ],
        "ch01_d5_evening_leia_decides": [
            ("relationship", "love", 1),
            ("relationship", "trust", 2),
        ],
        "ch01_d5_truth_honest": [
            ("relationship", "love", 1),
            ("relationship", "trust", 2),
        ],
        "ch01_d5_truth_funny": [
            ("relationship", "temptation", -1),
        ],
        "ch01_d5_truth_dodge": [
            ("relationship", "trust", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_d5_ask_sweet": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d5_ask_brave": [
            ("relationship", "trust", 1),
            ("partner", "exhibitionism", 1),
        ],
        "ch01_d5_ask_silly": [
            ("relationship", "temptation", -1),
        ],
        "ch01_d5_bunk_cabin": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d5_bunk_deck": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 1),
        ],
        "ch01_d5_bunk_apart": [
            ("relationship", "trust", 1),
        ],
        "ch01_d5_ntr_bunk_apart": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 3),
        ],
        "ch01_d5_love_bracelet_hers": [
            ("relationship", "love", 2),
            ("relationship", "trust", 2),
        ],
        "ch01_d5_love_bracelet_his": [
            ("relationship", "love", 2),
            ("relationship", "trust", 2),
        ],
        "ch01_d5_exhib_rule_wrist": [
            ("relationship", "trust", 3),
            ("partner", "exhibitionism", 2),
        ],
        "ch01_d5_exhib_rule_dare": [
            ("partner", "exhibitionism", 2),
        ],
        "ch01_d5_exhib_rule_skip": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d5_invite_in": [
            ("partner", "exhibitionism", 1),
        ],
        "ch01_d5_invite_ask_leia": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d5_invite_maybe": [
            ("relationship", "temptation", 1),
        ],
        "ch01_d5_invite_read_aloud": [
            ("relationship", "love", 1),
            ("relationship", "temptation", -1),
        ],
        "ch01_d5_invite_keep_quiet": [
            ("relationship", "temptation", 1),
        ],
    })

    D4_EXHIBITION_BRIEF_REVEAL_MIN = LC_T["d4_brief_reveal"]
    D5_BOLDER_SWIM_MIN = LC_T["d5_bolder_swim"]
    D5_COMFORTABLE_MIN = LC_T["d5_comfortable"]
    D5_COMFORTABLE_MIN_AFTER_BRIEF = LC_T["d5_comfortable_after_brief"]

    # Old heading -> route name. "SHARED EXHIBITION (NTS)" was the Love +
    # Exhibitionism track (nobody else joins in), so it no longer says NTS.
    LC_TRACK_HEADINGS_V2 = (
        ("TRACK: SHARED EXHIBITION (NTS)", "TRACK: LOVE + EXHIBITIONISM"),
        ("TRACK: DISTANCE, REPAIRED (NTR pressure)", "TRACK: NTR, REPAIRED"),
        ("TRACK: DISTANCE, UNRESOLVED (NTR pressure)", "TRACK: NTR, UNRESOLVED"),
        ("TRACK: DISTANCE, CONFIRMED (NTR pressure)", "TRACK: NTR, CONFIRMED"),
        ("TRACK: DISTANCE (NTR pressure)", "TRACK: NTR"),
    )

    def lc_track_text_v2(text):
        if not text:
            return text
        for old, new in LC_TRACK_HEADINGS_V2:
            if text.startswith(old):
                return new + text[len(old):]
        return text

    _lc_d4_track_text_v1 = ch01_d4_track_text
    _lc_d5_track_text_v1 = ch01_d5_track_text

    def ch01_d4_track_text():
        return lc_track_text_v2(_lc_d4_track_text_v1())

    def ch01_d5_track_text():
        return lc_track_text_v2(_lc_d5_track_text_v1())
