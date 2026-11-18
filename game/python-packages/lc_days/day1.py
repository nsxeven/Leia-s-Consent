"""Day One: pure-Python Day pack data (see lc_days/__init__.py for the names).

Ren'Py side: game/chapters/ch01/day1/. Guide: docs/DAY_PACK.md.
"""

# Chapter registry entry (lc_chapters.CHAPTERS["day1"]).
CHAPTER = {
    "number": 1, "number_word": "One", "day": 1, "day_word": "One",
    "review_day": "ch01_d1",
    "title": 'Sheer Curtains',
    "routes": {
        "love": 'Today Was Good',
        "love_exhib": 'Can He Tell?',
        "nts": 'A Third Person',  # not reachable yet: no NTS beat this day (see NTS_VARIANT_KEYS)
        "ntr": 'Spaces Left Open',
        "repair": None,  # no repair ending this day; falls back to the Love title
    },
}

# ---------------------------------------------------------------- stat model (lc_stat_model)
# Route thresholds (lc_stat_model.THRESHOLDS). Scaled from the old numbers and tuned with
# tests/test_route_simulation.py; Temptation counts slips (one slip never seeds NTR, three do).
STAT_THRESHOLDS = {
    # Day 1 end (ch01_scenes_14_30.rpy)
    "d1_ntr_seed_temptation": 13,      # >= : ntr_seeded (three +1 slips; one never does)
    "d1_exhib_seed": 30,               # >= (and below the NTR seed): nts_seeded ("Exhibition seeded")
    "d1_love_bedtime_love": 54,
    "d1_love_bedtime_trust": 54,
    "d1_love_bedtime_temptation_max": 11,  # one slip still gets the Love bedtime
    # Her own call (Exhibitionism) in Day 1 dialogue
    "d1_pool_shared_glance": 19,       # was exhibitionism/acceptance 14
    "d1_can_tell_unsure": 28,          # was 18
    "d1_can_tell_bold": 45,            # was 26
    "d1_compliment_liked": 21,         # was curiosity 25
    "d1_compliment_restless_temptation": 13,  # was boredom 16; = the Day 1 NTR seed
    "d1_photo_confidence": 14,         # Exhibitionism (+3 bolder outfit), was curiosity+acceptance 38
    "d1_photo_bolder_bonus": 3,
}

# Route resolvers, published as lc_stat_model.<name>.
STAT_MODEL_EXPORTS = ("d1_route_pressure", "d1_love_bedtime")


def d1_route_pressure(stats, focus=None):
    """Day 1 end state: 'ntr_seeded', 'nts_seeded' or 'mixed'.

    `stats` is a flat {stat: value} dict; `focus` is the Route Explorer override.
    """
    if focus == "ntr_risk":
        return "ntr_seeded"
    if focus == "exhibitionism":
        return "nts_seeded"
    if focus is not None:
        return "mixed"
    t = THRESHOLDS
    if stats["temptation"] >= t["d1_ntr_seed_temptation"]:
        return "ntr_seeded"
    if stats["exhibitionism"] >= t["d1_exhib_seed"]:
        return "nts_seeded"
    return "mixed"


def d1_love_bedtime(pressure, stats):
    t = THRESHOLDS
    return (
        pressure == "mixed"
        and stats["love"] >= t["d1_love_bedtime_love"]
        and stats["trust"] >= t["d1_love_bedtime_trust"]
        and stats["temptation"] <= t["d1_love_bedtime_temptation_max"]
    )


# ---------------------------------------------------------------- Ryan's thoughts (lc_thoughts)
# Beats a thought can require (lc_thoughts.BEATS; test kinds are documented there).
THOUGHT_BEATS = {
    "d1_photo_shoot": {"day": "ch01_d1", "test": ("value_min", "ch01_pool_capture_count", 1)},
    "d1_towel": {"day": "ch01_d1", "test": ("flag", "ch01_scene_06_complete")},
    "d1_dinner_stranger": {"day": "ch01_d1", "test": ("flag", "ch01_leia_stranger_second_glance")},
    "d1_julian_carry": {"day": "ch01_d1", "test": ("value_set", "ch01_carry_response")},
    "d1_sofa_glance": {"day": "ch01_d1", "test": ("value_set", "ch01_watching_response")},
    "d1_dream": {"day": "ch01_d1", "test": ("flag", "ch01_day1_towel_dream_seen")},
}

# The Day's pool, in day order. Ids are save data once shipped: never rename one.
THOUGHT_ORDER = (
    "d1_photo_shoot",
    "d1_towel",
    "d1_dinner_stranger",
    "d1_julian_carry",
    "d1_sofa_glance",
    "d1_dream",
)

THOUGHTS = {
    # Scene 5: Julian takes the pool photos (not offered if Ryan stopped the shoot).
    # Source: ch01_scene_05_photography
    "d1_photo_shoot": {
        "day": "ch01_d1", "requires": "d1_photo_shoot",
        "base": "She says every photo of her is terrible, and then [friend_name] gets one where "
                "she actually looks happy. I should probably learn how to hold a phone properly.",
        "variants": {
            "love_lane": "Halfway through she laughed at herself and forgot to pose, and that was the "
                         "best one. I'd have kept that one even if it came out blurry.",
            "exhibitionism": "She stopped going stiff the moment she knew the camera liked her. I kind "
                             "of loved watching that happen, more than I expected to.",
            "temptation": "It took [friend_name] about two minutes to get the photo I haven't managed in "
                          "four years. I'm trying really hard not to read anything into that.",
        },
    },
    # Scene 6: the towel on the balcony; scene 7: she asks what he saw. Towel shift, "I was trying
    # to tell you to get ready!", "You weren't two seconds ago!"; by the restaurant "the towel
    # incident had disappeared beneath ordinary conversation".
    # Source: ch01_scene_06_friendship_and_towel ch01_scene_07_did_he_see
    "d1_towel": {
        "day": "ch01_d1", "requires": "d1_towel",
        "base": "She stood there arguing with me in a towel, completely sure she was winning. I still "
                "don't know who was more embarrassed, her or [friend_name].",
        "variants": {
            "love_lane": "Bright red, clutching that towel, and she was still telling us off for not "
                         "getting ready. That's just so her. I really wouldn't change a thing.",
            "exhibitionism": "She went bright red, sure. But by the time we got to dinner she'd let it "
                             "go, and I keep picturing the second before she noticed.",
            "temptation": "She said he wasn't looking at the water two seconds before. I keep wondering "
                          "how long he'd been looking, which is probably not a great thing to keep "
                          "wondering.",
            "trust": "Afterwards she asked me what [friend_name] actually saw, and she wanted the real "
                     "answer, not the nice one. I like that she asks me.",
        },
    },
    # Scene 9: she walks into the stranger, his drink soaks them both, he apologizes, her eyes
    # follow his glance down; she turns down his photo offer and laughs at "we're both terrible at
    # walking"; later a different man ("passerby") compliments the dress, then "Still stands" at
    # the table. Source: ch01_scene_09_dinner
    "d1_dinner_stranger": {
        "day": "ch01_d1", "requires": "d1_dinner_stranger",
        "base": "She walks straight into some guy, his drink goes everywhere, and he's the one who "
                "keeps apologizing. I don't know why I'm still thinking about where her eyes went "
                "after.",
        "variants": {
            "love_lane": "Soaked dress, no dinner photo, and a minute later she was laughing about it. "
                         "I don't think she knows how good she is at that.",
            "exhibitionism": "Later some other guy came past our table just to tell her the dress still "
                             "looked incredible, and she lit up a little. Honestly, so did I. He wasn't "
                             "wrong.",
            "temptation": "He offered to take her photo and she took a second too long to answer. It's "
                          "probably nothing. It's probably just me.",
        },
    },
    # Scene 13: Ryan's lift "lasted about three seconds", Julian carries her ("get under the
    # knees"), Ryan has the keys; her head settles on Julian's shoulder and she keeps sleeping;
    # the dress slips on Julian's side and he says so. Source: ch01_scene_13_back_at_villa
    "d1_julian_carry": {
        "day": "ch01_d1", "requires": "d1_julian_carry",
        "base": "I couldn't even get my own girlfriend out of the car. [friend_name] picked her up like "
                "she weighed nothing, and I got to hold the keys.",
        "variants": {
            "love_lane": "I tried to carry her and lasted about three seconds. Next time I'm learning "
                         "the knees thing, so I'm not just the guy holding the keys.",
            "exhibitionism": "Her dress slipped, and he was the one who could see it, not me. I feel "
                             "like I should mind that more than I do.",
            "temptation": "Her head just settled on his shoulder and she kept sleeping. She didn't even "
                          "know she was doing it. I just keep seeing it anyway.",
            "trust": "When her dress slipped he told me straight away, even though it was awkward for "
                     "both of us. I think that's what a real friend does.",
        },
    },
    # Scene 21: legs across Ryan's lap; she "checked where his eyes were before settling again.
    # It was quick. I still caught it." (true on every answer). Source: ch01_scene_21_watching_julian
    "d1_sofa_glance": {
        "day": "ch01_d1", "requires": "d1_sofa_glance",
        "base": "When she moved on the sofa, she checked where [friend_name] was looking first. It was "
                "quick. I'm not sure why I caught it, or why it's stuck with me.",
        "variants": {
            "love_lane": "She ended up with her legs across my lap like it was the most normal thing in "
                         "the world. I'd honestly take a hundred more nights like that.",
            "exhibitionism": "Why did that feel good to watch? She checked whether he could see her, and "
                             "part of me sort of hoped he could.",
            "temptation": "She checked where his eyes were before she settled back against me. It was "
                          "quick, and I keep telling myself it didn't mean anything.",
        },
    },
    # Scene 30: the dream (the dinner stranger, Ryan mute); he wakes and she is asleep beside him.
    # The exhibitionism line recalls the real passerby at dinner, not the dream.
    # Source: ch01_scene_30_end_day_one ch01_scene_09_dinner
    "d1_dream": {
        "day": "ch01_d1", "requires": "d1_dream",
        "base": "It was only a dream. She was asleep right next to me the whole time. I just wish my "
                "head would stop making things up at three in the morning.",
        "variants": {
            "love_lane": "I woke up and she was right there, breathing slow, half of her on my pillow. "
                         "That's the real version, and that's the one I'm keeping.",
            "exhibitionism": "The dream was awful. But at the real dinner, when some other guy went out "
                             "of his way to tell her she looked incredible... I don't hate remembering "
                             "that part. I'm not sure what to do with it.",
            "temptation": "None of it happened, and I know that. So why did I wake up feeling like I'd "
                          "already lost something?",
            "trust": "I could tell her about the dream. She'd probably laugh at me, and then she'd hug "
                     "me. I think I'd actually like that.",
        },
    },
}

# One card per part of the day, in day order (lc_thoughts.OFFER_PARTS).
THOUGHT_OFFER_PARTS = {
    "ch01_d1": (
        ("d1_photo_shoot", "d1_towel"),               # daytime
        ("d1_dinner_stranger", "d1_julian_carry"),    # evening
        ("d1_sofa_glance", "d1_dream"),               # night
    ),
}

# ---------------------------------------------------------------- dialogue paper (lc_ui_logic)
# (day number, started flag, complete flag): the journal's "DAY N" heading.
UI_DAY_FLAG = (1, "ch01_started", "ch01_day_01_complete")

# Night or late-evening images whose names carry no night token.
UI_NIGHT_EXCEPTIONS = (
    "ch01_walk_back_01",
    "ch01_walk_back_call",
    "ch01_trip_catch",
    "ch01_trip_catch_followup",
    "ch01_trip_catch_aftermath",
    "ch01_drive_back_seating",
    "ch01_julian_carry",
    "ch01_carry_walk",
    "ch01_carry_dress_shift",
    "ch01_lounge_micro_test",
)

# Image attributes that contain a night token but are daytime scenes.
UI_DAY_EXCEPTIONS = (
    "ch01_drive_to_dinner",
)


# lc_stat_model imports lc_days; importing it last keeps the cycle safe (the resolvers above
# read the shared THRESHOLDS table at call time).
from lc_stat_model import THRESHOLDS  # noqa: E402
