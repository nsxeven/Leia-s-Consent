"""Day Two: pure-Python Day pack data (see lc_days/__init__.py for the names).

Ren'Py side: game/chapters/ch01/day2/. Guide: docs/DAY_PACK.md.
"""

# Chapter registry entry (lc_chapters.CHAPTERS["day2"]).
CHAPTER = {
    "number": 2, "number_word": "Two", "day": 2, "day_word": "Two",
    "review_day": "ch01_d2",
    "title": 'Plus One',
    "routes": {
        "love": 'They Hide Enough',
        "love_exhib": 'Leave Them Open',
        "nts": 'Terrible Influence',  # not reachable yet: no NTS beat this day (see NTS_VARIANT_KEYS)
        "ntr": 'Are We Okay?',
        "repair": 'Tell Her the Truth',
    },
}


# ---------------------------------------------------------------- stat model (lc_stat_model)
# Route / her-own-call thresholds (lc_stat_model.THRESHOLDS).
STAT_THRESHOLDS = {
    # Day 2 lanes (ch01_d2_route_lane)
    "d2_risk_temptation": 15,          # >= with a Day 1 NTR seed (two more slips) ...
    "d2_risk_temptation_unseeded": 16, # ... or >= this without one (six slips in all)
    "d2_exhib_lane": 36,               # >= and gained Exhibitionism today
    "d2_love_exhib_blend": 28,         # love lane bedroom with an open-curtains edge
    # Her own call (Exhibitionism) in Day 1-2 dialogue
    "d2_morning_unsure": 28,           # was 18
    "d2_morning_bold": 45,             # was 26
    "d2_pool_outfit_bold": 36,         # was exhibitionism 22 or curiosity 27
    "d2_game_drinks": 28,              # was 18
    # Subtle Day Two tint for a handful of Leia's lines (darryn 2026-11-17): the stat furthest
    # above its own threshold colours the line; below every threshold she stays shy.
    # Trust climbs faster than Love on a loving run, so its bar sits higher.
    "d2_tint_love": 60,
    "d2_tint_trust": 78,
    "d2_tint_exhibitionism": 36,       # = d2_exhib_lane
    "d2_tint_sharing": 6,
    "d2_tint_temptation": 14,          # one below d2_risk_temptation
}

# Gate choices (lc_stat_model.CHOICE_GATES): gates may move up to 5; hard gates may move three stats.
STAT_CHOICE_GATES = {
    "ch01_d2_sunset_ignore_gate": "soft",
    "ch01_d2_wink_accuse_hard": "hard",
    "ch01_d2_wink_reject_hard": "hard",
}

# Route value the branch writes (lc_stat_model.CHOICE_ROUTE_FLAGS): "locks", "stays_open",
# "may_lead" or "lean".
STAT_ROUTE_FLAGS = {
    "ch01_d2_errand_walk_keep": "lean",
    "ch01_d2_sunset_ignore_gate": "may_lead",
    "ch01_d2_bed_pool_accuse": "may_lead",
    "ch01_d2_wink_accuse_hard": "locks",
    "ch01_d2_wink_reject_hard": "locks",
}

# Repair beats (lc_stat_model.REPAIR_CHOICES): the only choices allowed to pair Temptation down
# with Love/Trust up.
STAT_REPAIR_CHOICES = frozenset((
    "ch01_d2_bed_pool_love",
    "ch01_d2_overheard_own",
    "ch01_d2_sunset_partial",
    "ch01_d2_wink_repair",
))

# Route resolvers, published as lc_stat_model.<name>.
STAT_MODEL_EXPORTS = ("d2_route_lane", "d2_love_exhib_blend", "leia_tint", "legacy_d2_lane")


def d2_route_lane(stats, day1_pressure, exhib_gained_today, focus=None, migrated_lane=None):
    """Day 2 lane: 'ntr_risk', 'exhibitionism' or 'love'."""
    if focus is not None:
        return focus
    if migrated_lane in ("love", "exhibitionism", "ntr_risk"):
        return migrated_lane
    t = THRESHOLDS
    temptation = stats["temptation"]
    if temptation >= t["d2_risk_temptation"] and (
        day1_pressure == "ntr_seeded" or temptation >= t["d2_risk_temptation_unseeded"]
    ):
        return "ntr_risk"
    if (
        stats["exhibitionism"] >= t["d2_exhib_lane"]
        and exhib_gained_today >= 1
        and temptation < t["d2_risk_temptation"]
    ):
        return "exhibitionism"
    return "love"


def d2_love_exhib_blend(lane, stats, exhib_gained_today):
    return (
        lane == "love"
        and stats["exhibitionism"] >= THRESHOLDS["d2_love_exhib_blend"]
        and exhib_gained_today >= 1
    )


def leia_tint(stats, lane=None, lane_scene=False):
    """Day Two line tint for Leia: 'shy' or the stat id furthest above its d2_tint_* bar.

    The lane decides the scene; the tint only colours lines inside it. The Love lane never
    gets the Temptation tint, and a scene inside the NTR-risk lane never gets the Love tint.
    Missing or non-numeric stats count as their defaults.
    """
    stats = stats or {}
    allowed = list(STAT_ORDER)
    if lane == "love":
        allowed.remove("temptation")
    if lane == "ntr_risk" and lane_scene:
        allowed.remove("love")
    best, best_margin = "shy", -1
    for stat in allowed:
        value = stats.get(stat)
        if not isinstance(value, (int, float)):
            value = DEFAULTS[STAT_GROUPS[stat]][stat]
        margin = value - THRESHOLDS["d2_tint_" + stat]
        if margin >= 0 and margin > best_margin:
            best, best_margin = stat, margin
    return best


def legacy_d2_lane(relationship, partner, player, day1_pressure, d1_nonchalant, d2_nonchalant, d2_open, d2_attentive):
    """The pre-v2 Day 2 resolver, kept only so a save migrated mid-Day-2 keeps its lane."""
    risk_seed = day1_pressure == "ntr_seeded" or d1_nonchalant >= 4 or relationship.get("boredom", 10) >= 17
    risk_now = (
        risk_seed
        and relationship.get("boredom", 10) >= 15
        and (d2_nonchalant >= 1 or relationship.get("love", 50) <= 48)
        and d2_attentive <= d2_nonchalant + 2
    )
    if risk_now:
        return "ntr_risk"
    if (
        partner.get("exhibitionism", 10) >= 22
        and partner.get("curiosity", 20) >= 24
        and player.get("acceptance", 10) >= 15
        and d2_open >= 1
    ):
        return "exhibitionism"
    return "love"


# ---------------------------------------------------------------- Ryan's thoughts (lc_thoughts)
# Beats a thought can require (lc_thoughts.BEATS).
THOUGHT_BEATS = {
    "d2_breakfast": {"day": "ch01_d2", "test": ("flag", "ch01_d2_scene_04_complete")},
    "d2_maya_cafe": {"day": "ch01_d2", "test": ("flag", "ch01_d2_scene_07_complete")},
    "d2_boutique": {"day": "ch01_d2", "test": ("value_set", "ch01_d2_boutique_slip_witness")},
    "d2_pool_bee": {"day": "ch01_d2", "test": ("value_set", "ch01_d2_pool_incident")},
    "d2_dinner": {"day": "ch01_d2", "test": ("value_set", "ch01_d2_dinner_reach")},
    "d2_game_night": {"day": "ch01_d2", "test": ("flag", "ch01_d2_strip_penalty_agreed")},

}

# The pool, in day order. Ids are save data once shipped: never rename one.
THOUGHT_ORDER = (
    "d2_breakfast",
    "d2_maya_cafe",
    "d2_boutique",
    "d2_pool_bee",
    "d2_dinner",
    "d2_game_night",

)

THOUGHTS = {
    # ---- Day Two (offered at the end of the Day Two review, kept for Day Three). Each text holds
    # on every path where its beat is seen; the parts' variant sets differ so every thought can win
    # its part (tests: test_every_day_two_thought_can_be_offered).
    # Scene 3: "Is she pretty?" while she turns her cup a slow quarter-turn; scene 4: breakfast_04,
    # "[friend_name], caught watching our faces, looked away." (every path).
    # Source: ch01_day2_scene_03_maya_message ch01_day2_scene_04_jealousy_callback
    "d2_breakfast": {
        "day": "ch01_d2", "requires": "d2_breakfast",
        "base": "She asked me if Maya was pretty and tried really hard to make it sound like nothing. "
                "Then I looked up and [friend_name] was watching the two of us.",
        "variants": {
            "love_lane": "She asked if Maya was pretty, turning her cup like it was a totally casual "
                         "question. Four years in, and a name on my phone can still do that to her. "
                         "It's really cute.",
            "exhibitionism": "[friend_name] got caught watching us at breakfast and looked away like "
                             "he'd touched something hot. Part of me wanted to know what he'd been "
                             "looking at.",
            "temptation": "[friend_name] was watching her at breakfast, not us. I'm almost sure of it. "
                          "I'm trying very hard not to be.",
        },
    },
    # Scene 5: she glances at Ryan before telling Maya the "bad stuff"; scene 7: airports, "a loose
    # plan with times on it", "don't pose. Just talk to whoever's holding the phone", "This is their
    # table now. We're just sitting at it.", "I like her, she's staying." (every path).
    # Source: ch01_day2_scene_05_meet_maya ch01_day2_scene_07_leia_maya_click
    "d2_maya_cafe": {
        "day": "ch01_d2", "requires": "d2_maya_cafe",
        "base": "I was nervous about her meeting Maya. It took them about ten minutes to start ganging "
                "up on me about airports, and by the end of lunch they were keeping each other.",
        "variants": {
            "love_lane": "She told Maya she likes a loose plan with times on it. I already knew that. "
                         "I just really liked hearing her say it to somebody new.",
            "exhibitionism": "Maya told her to stop posing and just talk to whoever's holding the "
                             "phone. I have a feeling [girlfriend_name] is going to remember that one.",
            "trust": "When Maya asked her for the bad stuff about me, she glanced at me first. Like "
                     "she was checking which version I'd want her to tell. I noticed that.",
        },
    },
    # Scene 11b: Maya lets go of the top (Ryan or [friend_name] there); the black mini comes home
    # either way; "not wearing it outside" / Maya's "yet" / "Not yet"; at the table afterwards she
    # talks about it with Ryan (she raises it, or tells him when he asks). Every witness path.
    # Source: ch01_day2_scene_11b_boutique
    "d2_boutique": {
        "day": "ch01_d2", "requires": "d2_boutique",
        "base": "Maya let go of that top for one second in the middle of a shop, and now that's the "
                "only thing anyone's going to remember about that dress.",
        "variants": {
            "love_lane": "She swore she'd never wear that dress outside, ever, and it still came home "
                         "with us. I really want to be there the day she changes her mind.",
            "exhibitionism": "She said she'd never wear it outside. Maya heard 'yet.' Honestly, so "
                             "did I.",
            "trust": "Afterwards, at the table, she still talked to me about it. Even the parts she'd "
                     "rather have forgotten.",
        },
    },
    # Scene 17: the bee, the top comes off, the strangers on the deck see it (every split); scene 22:
    # Maya's honey joke and Leia's "it was a really big bee" at dinner (every path).
    # Source: ch01_day2_scene_17_pool_return ch01_day2_scene_22_sunset_couple
    "d2_pool_bee": {
        "day": "ch01_d2", "requires": "d2_pool_bee",
        "base": "One bee, and the whole afternoon went sideways. [friend_name] is never going to live "
                "it down, and to be fair, neither is that bikini top.",
        "variants": {
            "love_lane": "By dinner she was the one sticking up for [friend_name]. 'It was a really "
                         "big bee.' She can laugh about anything eventually. That's my favorite thing "
                         "about her.",
            "exhibitionism": "Those guys down the deck saw the whole thing. I keep waiting to feel "
                             "worse about that than I actually do.",
            "temptation": "It was over in about ten seconds, and I keep replaying it like I could've "
                          "done something different. I don't even know what.",
        },
    },
    # Scene 22: Maya's honey joke, everyone's favorite part of the trip, [friend_name] on Ryan's
    # ten-minute menu habit (every lane); scene 23 only decides who reaches for the dish.
    # Source: ch01_day2_scene_22_sunset_couple ch01_day2_scene_23_dinner_reach
    "d2_dinner": {
        "day": "ch01_d2", "requires": "d2_dinner",
        "base": "Dinner was [friend_name] getting roasted about bees and me getting roasted about "
                "menus. Weirdly, that was the most normal I'd felt all day.",
        "variants": {
            "love_lane": "Maya made everybody pick a favorite part of the trip. I never said mine out "
                         "loud. It's the way [girlfriend_name] laughs at her own jokes before she "
                         "gets to the end of them.",
            "trust": "[friend_name] told the whole table I still can't order in under ten minutes. "
                     "[girlfriend_name] has watched me do it for four years and still lets me read "
                     "her the whole menu.",
            "temptation": "Somewhere around dessert I stopped keeping track of where everyone at that "
                          "table was looking. I'm not sure that was a good idea.",
        },
    },
    # Scene 26: Maya's burning-question rule; scene 27: Leia won't answer "Who here has found someone
    # else in this room attractive?" and sits back down in her bra and panties, cheeks burning;
    # [friend_name]'s shirt catches on his sunglasses; at Maya's question for her, her eyes come to
    # Ryan first (every lane).
    # Source: ch01_day2_scene_26_game_rules ch01_day2_scene_27_game_escalates
    "d2_game_night": {
        "day": "ch01_d2", "requires": "d2_game_night",
        "base": "Maya made up a rule five minutes into the game, and everybody just went along with "
                "it. [friend_name] got his shirt stuck on his sunglasses. Somehow that was the least "
                "weird part.",
        "variants": {
            "love_lane": "When Maya finally asked her the one that actually mattered, she looked at "
                         "me before she answered. I keep coming back to that.",
            "exhibitionism": "She sat back down in her underwear with her cheeks burning, and I "
                             "couldn't stop looking. Neither could anyone else, and I didn't hate it.",
            "temptation": "Maya asked who'd found someone else in the room attractive, and "
                          "[girlfriend_name] would rather take her clothes off than answer. I keep "
                          "turning that over.",
        },
    },

}

# One card per part of the day (lc_thoughts.OFFER_PARTS).
THOUGHT_OFFER_PARTS = {
    "ch01_d2": (
        ("d2_breakfast", "d2_maya_cafe"),             # morning
        ("d2_boutique", "d2_pool_bee"),               # afternoon
        ("d2_dinner", "d2_game_night"),               # night
    ),

}


# ---------------------------------------------------------------- UI (lc_ui_logic)
# Night images whose names carry no night token (lc_ui_logic.NIGHT_EXCEPTIONS).
UI_NIGHT_EXCEPTIONS = (
    # Day 2: sunset pool, game night, bedroom finales
    "ch01_d2_love_pool_oral_01",
    "ch01_d2_love_pool_oral_02",
    "ch01_d2_julian_underwear_reveal",
    "ch01_d2_love_bedroom_01",
    "ch01_d2_love_bedroom_02",
    "ch01_d2_exhib_bed_open_01",
    "ch01_d2_exhib_bed_open_02",
    "ch01_d2_exhib_bed_open_03",
    "ch01_d2_exhib_bed_open_04",
)

# Journal day number and its started / complete flags (lc_ui_logic.DAY_FLAGS).
UI_DAY_FLAG = (2, "ch01_day_02_started", "ch01_day_02_complete")


# lc_stat_model imports lc_days; importing it last keeps the cycle safe (the resolvers above
# read the shared tables at call time).
from lc_stat_model import THRESHOLDS, STAT_ORDER, STAT_GROUPS, DEFAULTS  # noqa: E402
