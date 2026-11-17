"""Ryan's thoughts: keep one thought at the end of a day review (pure Python, no Ren'Py import).

At the end of a day's review the game may offer up to three *thoughts* drawn from beats the
player actually saw that day, plus "keep nothing". The kept thought is a save-local value that a
later day reads (lc_thought_kept / lc_thought_line in game/systems/thoughts.rpy) to tint a few
`think` lines or add one reply option. It never changes stats by itself.

Each thought has a base text and variants by lane or stat. A variant is resolved whenever the
thought is shown, so a kept thought evolves with the save: the lane rule comes first, then the
stat that sits furthest over its tint bar (TINT), else the base text.

Texts are Ryan's inner voice (docs/characters/ryan.md, LC-Brain Characters/Ryan.md: a bit timid,
self-deprecating, plain words). They use [player_name] / [girlfriend_name] / [friend_name] and
never name a stat or route, so Immersive mode can show them as they are.

Ren'Py side: game/systems/thoughts.rpy, game/screens/thoughts_screen.rpy.
Tests: tests/test_thoughts.py. Doc: docs/THOUGHTS.md.
"""

# Lane keys a variant may use. Mapped from the stats model's lean (lane_from_lean).
LANES = ("love_lane", "exhib_lane", "ntr_lane")

_LEAN_TO_LANE = {"love": "love_lane", "love_exhib": "exhib_lane", "ntr": "ntr_lane"}

# Tint bars: a stat at or over its bar can tint a thought. Day One scale (defaults are
# Love/Trust 50, Exhibitionism/Temptation 10, Sharing 0): a few warm choices pass Love/Trust 58,
# Exhibitionism 19 is the Day One "shared glance" line (lc_stat_model d1_pool_shared_glance),
# Temptation 12 is two slips (one short of the Day One NTR seed at 13).
TINT = {
    "love": 58,
    "trust": 58,
    "exhibitionism": 19,
    "sharing": 3,
    "temptation": 12,
}

# Tie-break when two stats sit equally far over their bars.
STAT_PRIORITY = ("temptation", "exhibitionism", "sharing", "trust", "love")

# Labels for the small tint stamp in Insight/Full (never shown in Immersive).
TINT_LABELS = {
    "love": "Love", "trust": "Trust", "exhibitionism": "Exhibitionism",
    "sharing": "Sharing", "temptation": "Temptation",
    "love_lane": "Love", "exhib_lane": "Love + Exhibitionism", "ntr_lane": "NTR",
}

# Beats a thought can require. test is one of:
#   ("flag", flag_id)            the story flag is set
#   ("value_set", key)           the story value exists (any value but None)
#   ("value_min", key, n)        the story value is a number >= n
BEATS = {
    "d1_photo_shoot": {"day": "ch01_d1", "test": ("value_min", "ch01_pool_capture_count", 1)},
    "d1_towel": {"day": "ch01_d1", "test": ("flag", "ch01_scene_06_complete")},
    "d1_dinner_stranger": {"day": "ch01_d1", "test": ("flag", "ch01_leia_stranger_second_glance")},
    "d1_julian_carry": {"day": "ch01_d1", "test": ("value_set", "ch01_carry_response")},
    "d1_sofa_glance": {"day": "ch01_d1", "test": ("value_set", "ch01_watching_response")},
    "d1_dream": {"day": "ch01_d1", "test": ("flag", "ch01_day1_towel_dream_seen")},
}

# The pool, in day order. Ids are save data once shipped: never rename one.
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
    # Scene 6: the towel on the balcony.
    "d1_towel": {
        "day": "ch01_d1", "requires": "d1_towel",
        "base": "She stood there arguing with me in a towel, completely sure she was winning. I still "
                "don't know who was more embarrassed, her or [friend_name].",
        "variants": {
            "exhibitionism": "She went bright red, sure. But by dinner she was laughing about it, and I "
                             "keep picturing the second before she noticed.",
            "temptation": "[friend_name] saw it before I said anything. I keep wondering how long he'd "
                          "been looking, which is probably not a great thing to keep wondering.",
            "trust": "Afterwards she asked me what [friend_name] actually saw, and she wanted the real "
                     "answer, not the nice one. I like that she asks me.",
        },
    },
    # Scene 9: the stranger at dinner.
    "d1_dinner_stranger": {
        "day": "ch01_d1", "requires": "d1_dinner_stranger",
        "base": "Some guy spills a drink down her dress, apologizes twice and goes back to his table. "
                "I don't know why I'm still thinking about the way he looked at her.",
        "variants": {
            "love_lane": "Soaked dress, ruined dinner, and she still made him laugh about it. I don't "
                         "think she knows how good she is at that.",
            "exhibitionism": "He told her she looked great, and she lit up a little. Honestly, so did I. "
                             "He wasn't wrong.",
            "temptation": "He offered to take her photo and she took a second too long to answer. It's "
                          "probably nothing. It's probably just me.",
        },
    },
    # Scenes 12-13: Julian carries her in from the car.
    "d1_julian_carry": {
        "day": "ch01_d1", "requires": "d1_julian_carry",
        "base": "I couldn't even get my own girlfriend out of the car. [friend_name] picked her up like "
                "she weighed nothing, and I got to hold the keys.",
        "variants": {
            "exhibitionism": "Her dress slipped, and he was the one who could see it, not me. I feel "
                             "like I should mind that more than I do.",
            "temptation": "She slept the whole way in with her head on his shoulder. It was an accident, "
                          "I know it was. I just keep seeing it anyway.",
            "trust": "When her dress slipped he told me straight away, even though it was awkward for "
                     "both of us. I think that's what a real friend does.",
        },
    },
    # Scene 21: on the sofa she checks where Julian is looking.
    "d1_sofa_glance": {
        "day": "ch01_d1", "requires": "d1_sofa_glance",
        "base": "When she moved on the sofa, she checked where [friend_name] was looking first. It was "
                "quick. I'm not sure why I caught it, or why it's stuck with me.",
        "variants": {
            "love_lane": "She ended up with her legs across my lap like it was the most normal thing in "
                         "the world. I'd honestly take a hundred more nights like that.",
            "exhibitionism": "Why did that feel good to watch? She checked whether he could see her, and "
                             "part of me sort of hoped he could.",
            "temptation": "She checked where his eyes were before she checked mine. I noticed and didn't "
                          "say anything, which is kind of my whole thing lately.",
        },
    },
    # Scene 30: the dream.
    "d1_dream": {
        "day": "ch01_d1", "requires": "d1_dream",
        "base": "It was only a dream. She was asleep right next to me the whole time. I just wish my "
                "head would stop making things up at three in the morning.",
        "variants": {
            "love_lane": "I woke up and she was right there, breathing slow, half of her on my pillow. "
                         "That's the real version, and that's the one I'm keeping.",
            "exhibitionism": "The dream was awful, but the part before it, how he looked at her at "
                             "dinner... I don't hate that part. I don't really know what to do with that.",
            "temptation": "None of it happened, and I know that. So why did I wake up feeling like I'd "
                          "already lost something?",
            "trust": "I could tell her about the dream. She'd probably laugh at me, and then she'd hug "
                     "me. I think I'd actually like that.",
        },
    },
}

OFFER_LIMIT = 3

_DEFAULT_NAMES = {"player_name": "Ryan", "girlfriend_name": "Leia", "friend_name": "Julian"}


def day_thoughts(day_id, thoughts=None, order=None):
    """Thought ids for day_id, in day order."""
    thoughts = THOUGHTS if thoughts is None else thoughts
    order = THOUGHT_ORDER if order is None else order
    return [tid for tid in order if thoughts[tid]["day"] == day_id]


def lane_from_lean(lean):
    """Lane key for a stats-model lean ('love' / 'love_exhib' / 'ntr'); None otherwise."""
    return _LEAN_TO_LANE.get(lean)


def _number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def variant_key(thought_id, stats, lane, thoughts=None):
    """The variant key that applies now, or None for the base text.

    The lane rule comes first (when the thought has a variant for that lane), then the stat
    furthest over its TINT bar among the stats the thought has a variant for (ties follow
    STAT_PRIORITY). Missing or non-numeric stats never tint.
    """
    thoughts = THOUGHTS if thoughts is None else thoughts
    variants = thoughts[thought_id]["variants"]
    if lane in LANES and lane in variants:
        return lane
    stats = stats or {}
    best, best_margin = None, None
    for stat in STAT_PRIORITY:
        if stat not in variants:
            continue
        value = _number(stats.get(stat))
        if value is None:
            continue
        margin = value - TINT[stat]
        if margin < 0:
            continue
        if best_margin is None or margin > best_margin:
            best, best_margin = stat, margin
    return best


def thought_text(thought_id, stats, lane, thoughts=None):
    """The thought's text for these stats and lane (unknown id -> KeyError)."""
    thoughts = THOUGHTS if thoughts is None else thoughts
    entry = thoughts[thought_id]
    key = variant_key(thought_id, stats, lane, thoughts=thoughts)
    return entry["variants"][key] if key else entry["base"]


def fill_names(text, names):
    """Replace the three name tokens with the player's names (defaults when missing)."""
    for token, default in _DEFAULT_NAMES.items():
        text = text.replace("[" + token + "]", (names or {}).get(token) or default)
    return text


def _beat_seen(test, has_flag, get_value):
    kind = test[0]
    if kind == "flag":
        return bool(has_flag(test[1]))
    if kind == "value_set":
        return get_value(test[1]) is not None
    if kind == "value_min":
        value = _number(get_value(test[1]))
        return value is not None and value >= test[2]
    raise ValueError("unknown beat test %r" % (test,))


def seen_beats(day_id, has_flag, get_value, beats=None):
    """Ids of day_id's beats this save has seen. has_flag(flag) and get_value(key) read the save
    (get_value returns None when the value is missing)."""
    beats = BEATS if beats is None else beats
    return {beat for beat, spec in beats.items()
            if spec["day"] == day_id and _beat_seen(spec["test"], has_flag, get_value)}


def offer(day_id, stats, lane, seen, demo=False, limit=OFFER_LIMIT, thoughts=None, order=None):
    """Up to `limit` thought ids for the end of day_id's review, in day order.

    Only thoughts whose required beat is in `seen`. Thoughts a lane/stat currently tints come
    first (they reflect how this save played the day), then day order. A demo build offers
    nothing.
    """
    if demo:
        return []
    seen = seen or ()
    thoughts = THOUGHTS if thoughts is None else thoughts
    ids = [tid for tid in day_thoughts(day_id, thoughts, order) if thoughts[tid]["requires"] in seen]
    ranked = sorted(ids, key=lambda tid: (variant_key(tid, stats, lane, thoughts) is None,
                                          ids.index(tid)))
    picked = set(ranked[:max(0, limit)])
    return [tid for tid in ids if tid in picked]


def keep(kept, day_id, thought_id):
    """A new {day_id: thought id or None} dict with day_id's choice recorded.

    thought_id None means "keep nothing" and is stored as None. An unknown id, or one from
    another day, raises ValueError.
    """
    if thought_id is not None:
        entry = THOUGHTS.get(thought_id)
        if entry is None or entry["day"] != day_id:
            raise ValueError("not a %s thought: %r" % (day_id, thought_id))
    out = dict(kept or {})
    out[day_id] = thought_id
    return out


def kept_id(kept, day_id):
    """The thought id kept for day_id, or None (nothing kept, never offered, old save, or an id
    that no longer exists)."""
    tid = (kept or {}).get(day_id)
    return tid if tid in THOUGHTS else None


def tint_label(key):
    """Display label for a variant key (Insight/Full stamp), '' for the base text."""
    return TINT_LABELS.get(key, "") if key else ""
