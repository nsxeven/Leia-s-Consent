# Day Five pack - chapter: title-card text, review row and Chapter Select preset. The chapter registry entry (titles) is CHAPTER in
#   game/python-packages/lc_days/day5.py.
#
# Where every kind of content goes: docs/DAY_PACK.md.

# Opening title card (neutral title for everyone), shown by the Day's start label.
define lc_chapter_card_day5 = lc_chapters.card_text("day5")

# End-of-day review: this Day's row (systems/day_review.rpy). route_key = the end-route story key.
init 1 python:
    import lc_chapters
    LC_REVIEW_DAYS["ch01_d5"] = {"label": lc_chapters.review_label("day5"), "chapter": "day5", "route_key": "ch01_d5_end_route"}

# Chapter Select (systems/chapter_select.rpy): the Day Five preset, keyed by the stored Day Four end
#   route, with the Day Four end state each one seeds.
init 1 python:
    import lc_chapters

    # Day Five presets: the five stored Day Four end routes (ch01_d4_end_route).
    CH01_SELECT_DAY5_ROUTES = (
        ("love", "Love"),
        ("exhibitionism", "Exhibitionism"),
        ("love_repaired", "Love (repaired)"),
        ("ntr_unresolved", "NTR unresolved"),
        ("ntr_confirmed", "NTR confirmed"),
    )

    # Day Four end state seeded for the Day Five presets (a typical playthrough of each route; the choices
    # made are recorded in the values below). "d2" is the Day Two end state that leads to that Day Four lane.
    CH01_SELECT_DAY5_PRESETS = {
        "love": dict(
            d2="love", lane="love", d3_variant="love_private",
            stats=dict(love=57, trust=56, exh=12, tem=9),
            d4=dict(end_variant="love_slow_dance", exposure_step="none", exhib_variant="none", photo_style="candid",
                    dusk_outfit_id="resort_dinner_dress", dusk_outfit_source="leia", hook_reply="in", ntr_react=None,
                    ntr_outcome="ntr_confirmed", ntr_fine_count=0, disclosure_when=None, leia_call=None,
                    day_outfit_id="casual_default", day_outfit_source="leia"),
            flags=["ch01_d4_market_honey_bee_callback", "ch01_d4_photo_candid_taken"],
        ),
        "exhibitionism": dict(
            d2="exhibitionism", lane="exhibitionism", d3_variant="exhibition_window",
            stats=dict(love=53, trust=50, exh=66, tem=10),
            d4=dict(end_variant="exhib_shared_step", exposure_step="brief_reveal", exhib_variant="shared_step", photo_style="posed",
                    dusk_outfit_id="boutique_cutout_mini", dusk_outfit_source="leia", hook_reply="in", ntr_react=None,
                    ntr_outcome="ntr_confirmed", ntr_fine_count=0, disclosure_when=None, leia_call="brief_reveal",
                    day_outfit_id="casual_default", day_outfit_source="leia"),
            flags=["ch01_d4_market_honey_bee_callback", "ch01_d4_photo_pose_taken", "ch01_d4_exhib_brief_done"],
        ),
        "love_repaired": dict(
            d2="ntr_confirmed", lane="ntr", d3_variant="ntr_restroom_nightmare",
            stats=dict(love=50, trust=60, exh=11, tem=16),
            d4=dict(end_variant="ntr_repaired_thanks", exposure_step="none", exhib_variant="none", photo_style="candid",
                    dusk_outfit_id="resort_dinner_dress", dusk_outfit_source="leia", hook_reply="in", ntr_react="thanks",
                    ntr_outcome="love_repaired", ntr_fine_count=0, disclosure_when="harbor_wall", leia_call=None,
                    day_outfit_id="casual_default", day_outfit_source="leia"),
            flags=["ch01_d4_market_honey_bee_callback", "ch01_d4_photo_candid_taken", "ch01_d4_cutout_disclosed", "ch01_d4_club_story_deferred"],
        ),
        "ntr_unresolved": dict(
            d2="mixed_unresolved", lane="ntr", d3_variant="ntr_restroom_nightmare",
            stats=dict(love=43, trust=50, exh=10, tem=31),
            d4=dict(end_variant="ntr_unresolved", exposure_step="none", exhib_variant="none", photo_style="candid",
                    dusk_outfit_id="resort_dinner_dress", dusk_outfit_source="leia", hook_reply="maybe", ntr_react=None,
                    ntr_outcome="ntr_unresolved", ntr_fine_count=0, disclosure_when=None, leia_call=None,
                    day_outfit_id="casual_default", day_outfit_source="leia"),
            flags=["ch01_d4_market_honey_bee_callback", "ch01_d4_photo_candid_taken", "ch01_d4_cutout_partial"],
        ),
        "ntr_confirmed": dict(
            d2="ntr_confirmed", lane="ntr", d3_variant="ntr_restroom_nightmare",
            stats=dict(love=35, trust=45, exh=11, tem=45),
            d4=dict(end_variant="ntr_confirmed", exposure_step="none", exhib_variant="none", photo_style="skipped",
                    dusk_outfit_id="resort_dinner_dress", dusk_outfit_source="leia", hook_reply="maybe", ntr_react=None,
                    ntr_outcome="ntr_confirmed", ntr_fine_count=3, disclosure_when=None, leia_call=None,
                    day_outfit_id="casual_default", day_outfit_source="leia"),
            flags=["ch01_d4_market_honey_bee_callback", "ch01_d4_ntr_soft_gate", "ch01_d4_photo_skipped", "ch01_d4_cutout_partial"],
        ),
    }

    def ch01_d5_select_seed(route):
        """Chapter Select "Day Five" preset: Days Two to Four finished on Day Four end route `route`."""
        # Day Five presets are keyed by the Day Four end route; "base" is the Day Two end state behind it.
        d5p = CH01_SELECT_DAY5_PRESETS[route]
        base = d5p["d2"]
        ch01_d2_select_finished(base, d5p["stats"])
        d3_lane_value = ch01_d3_select_finished(base, d5p["lane"])
        ch01_d4_select_finished(route, d5p, d3_lane_value)
        return "ch01_day5_start"

    CHAPTER_SELECT_PRESETS["day5"] = dict(
        label=lc_chapters.select_label("day5"),
        note="Starts at Day Five with Days Two to Four marked complete and a typical Day Four end state stored.",
        heading=_("Stored Day Four ending"), routes=CH01_SELECT_DAY5_ROUTES, seed=ch01_d5_select_seed,
    )
