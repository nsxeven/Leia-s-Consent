# Day Two pack - registrations: the mall-scene choice rows that used to sit in
#   systems/choice_engine.rpy, and the story-key ledger. Most Day Two choice rows are registered
#   next to their scenes (ch01_day2_scenes_01_15.rpy and the other Day Two files, init 1).
#
# Where every kind of content goes: docs/DAY_PACK.md. Scoring rules: docs/STAT_MODEL.md.
# Load order: init 1 (the engine tables exist at init <= 0).

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

# ------------------------------------------------------------------ story-key ledger
# Every story flag / value this Day sets, one line each (tests/test_day_packs.py checks it):
#   # key <name>: read-by <who reads it>     or     # key <name>: pending <why nothing reads it yet>
# Patterns with * cover dynamic keys. Keys are save data: never rename one.
# key ch01_d2_bedroom_variant: pending set by ch01_day2_scenes_16_30.rpy, chapter_select.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_bikini_tie_loose: pending set by ch01_day2_scenes_01_15.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_boutique_black_mini_reserved_day3: pending set by ch01_day2_scenes_16_30.rpy, chapter_select.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_boutique_outfit_owned: pending set by ch01_day2_scenes_01_15.rpy, chapter_select.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_boutique_selfie_reply: read-by ch01_day2_scenes_01_15.rpy
# key ch01_d2_boutique_shop_open: read-by outfits_data.rpy
# key ch01_d2_boutique_slip_witness: read-by ch01_day2_scenes_01_15.rpy, lc_thoughts.py
# key ch01_d2_boutique_trial_outfit: pending set by ch01_day2_scenes_01_15.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_confession_reply: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_dare_signal: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_dinner_outfit: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_dinner_outfit_id: pending set by ch01_day2_scenes_16_30.rpy, chapter_select.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_dinner_outfit_source: pending set by ch01_day2_scenes_16_30.rpy, chapter_select.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_dinner_reach: read-by ch01_day2_gallery.rpy, ch01_day2_scenes_16_30.rpy, lc_thoughts.py
# key ch01_d2_dinner_wink: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_end_route: read-by ch01_day2_chapter.rpy, ch01_day3_scenes.rpy, ch01_day4_registrations.rpy +4 more
# key ch01_d2_errand_lane: read-by ch01_day2_feed.rpy, ch01_day2_scene_19b_leia_asks_maya.rpy, ch01_day2_scenes_16_30.rpy
# key ch01_d2_errand_reason: read-by ch01_day2_scene_19b_leia_asks_maya.rpy
# key ch01_d2_exhibition_bedroom_open_curtains: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_exhibition_pool_shared_with_ryan: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_exhibition_pool_tease: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_exhibition_sunset_shared: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_feed_bringup: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_julian_bee_fear_seeded: pending set by ch01_day2_scenes_01_15.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_julian_reveal_seen: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_julian_shades_removed: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_julian_sleeping: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_julian_upstairs_before_sunset: pending set by ch01_day2_scene_19b_leia_asks_maya.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_knot_response: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_lane_migrated: read-by ch01_day2_scenes_01_15.rpy, stats.rpy
# key ch01_d2_leia_julian_photo: pending set by ch01_day2_scenes_01_15.rpy; nothing reads it yet (kept for later Days and saves)
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
# key ch01_d2_nhie_leia_clothes: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_nhie_leia_topless_covering: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_nhie_maya_clothes: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_nhie_maya_nude: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_ntr_confirmed: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_ntr_soft_gate: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_ntr_soft_gate_repaired: pending set by ch01_day2_scenes_16_30.rpy, chapter_select.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_overheard_response: read-by ch01_day2_scenes_01_15.rpy, ch01_day2_scenes_16_30.rpy
# key ch01_d2_overheard_talk: read-by ch01_day2_scenes_01_15.rpy, ch01_day2_scenes_16_30.rpy
# key ch01_d2_photo_group: read-by phone_group_avatar.rpy
# key ch01_d2_photo_julian_maya: pending set by ch01_day2_scenes_01_15.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_photo_leia_maya: read-by ch01_day2_gallery.rpy
# key ch01_d2_photo_ryan_leia: pending set by ch01_day2_scenes_01_15.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_photo_ryan_maya: pending set by ch01_day2_scenes_01_15.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_pool_attention: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_d2_pool_incident: read-by ch01_day2_scenes_16_30.rpy, lc_thoughts.py
# key ch01_d2_pool_outfit: read-by ch01_day2_scenes_01_15.rpy, ch01_day5_registrations.rpy
# key ch01_d2_pool_response: read-by ch01_day2_leia_errand.rpy
# key ch01_d2_pool_suspicion: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_route_lane_dinner: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_route_lane_post_pool: read-by ch01_day2_leia_errand.rpy, ch01_day2_scenes_16_30.rpy
# key ch01_d2_route_lane_post_sunset: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_route_lane_pre_split: read-by ch01_day2_scenes_01_15.rpy, ch01_day2_scenes_16_30.rpy
# key ch01_d2_scene_04_complete: read-by lc_thoughts.py
# key ch01_d2_scene_07_complete: read-by lc_thoughts.py
# key ch01_d2_scene_30_complete: read-by chapter_select.rpy
# key ch01_d2_split: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_strip_penalty_agreed: read-by lc_thoughts.py
# key ch01_d2_sunset_noticed: read-by ch01_day2_scenes_16_30.rpy
# key ch01_d2_sunset_response: pending set by ch01_day2_scenes_16_30.rpy; nothing reads it yet (kept for later Days and saves)
# key ch01_day_02_complete: read-by ch01_day2_scenes_01_15.rpy, chapter_select.rpy, full_transparency_route_explorer.rpy +3 more
# key ch01_day_02_started: read-by chapter_select.rpy, lc_ui_logic.py, stats.rpy
# key ch01_d2_scene_*_complete: pending scene-done markers (27 keys; scene-done helper), nothing reads them yet
# key ch01_d2_route_lane_*: pending dynamic keys set by chapter_select.rpy
