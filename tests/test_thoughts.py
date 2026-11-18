"""Ryan's thoughts: keep one at the end of a day review; it evolves with stats and lane.

Pure rules: game/python-packages/lc_thoughts.py (thought pool, variant resolution, the offer,
keep/keep-nothing). Ren'Py side: game/systems/thoughts.rpy (save value lc_thoughts_kept, the
review_closed hook, lc_thought_kept / lc_thought_line for later days) and
game/screens/thoughts_screen.rpy (the offer card).
"""
import pickle
import re
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "game" / "python-packages"))
sys.path.insert(0, str(ROOT / "tests"))

import lc_discovery  # noqa: E402
import lc_thoughts  # noqa: E402
from lc_rpy_harness import load_blocks  # noqa: E402

DAY1 = "ch01_d1"
DAY2 = "ch01_d2"
# Defaults: below every tint bar.
CALM = {"love": 50, "trust": 50, "exhibitionism": 10, "sharing": 0, "temptation": 10}


def stats(**over):
    out = dict(CALM)
    out.update(over)
    return out


ALL_DAY1_BEATS = {lc_thoughts.THOUGHTS[t]["requires"] for t in lc_thoughts.THOUGHT_ORDER
                  if lc_thoughts.THOUGHTS[t]["day"] == DAY1}
ALL_DAY2_BEATS = {lc_thoughts.THOUGHTS[t]["requires"] for t in lc_thoughts.THOUGHT_ORDER
                  if lc_thoughts.THOUGHTS[t]["day"] == DAY2}


class PoolTests(unittest.TestCase):
    def test_day_one_has_about_six_thoughts_each_on_its_own_beat(self):
        ids = lc_thoughts.day_thoughts(DAY1)
        self.assertTrue(5 <= len(ids) <= 7, ids)
        beats = [lc_thoughts.THOUGHTS[t]["requires"] for t in ids]
        self.assertEqual(len(beats), len(set(beats)))
        for beat in beats:
            self.assertIn(beat, lc_thoughts.BEATS)
            self.assertEqual(lc_thoughts.BEATS[beat]["day"], DAY1)

    def test_every_thought_has_a_base_and_valid_variant_keys(self):
        valid = set(lc_thoughts.TINT) | set(lc_thoughts.LANES)
        for tid in lc_thoughts.THOUGHT_ORDER:
            entry = lc_thoughts.THOUGHTS[tid]
            self.assertTrue(entry["base"].strip(), tid)
            self.assertTrue(entry["variants"], tid)
            for key, text in entry["variants"].items():
                self.assertIn(key, valid, (tid, key))
                self.assertTrue(text.strip(), (tid, key))

    def all_texts(self):
        for tid in lc_thoughts.THOUGHT_ORDER:
            entry = lc_thoughts.THOUGHTS[tid]
            yield tid, "base", entry["base"]
            for key, text in entry["variants"].items():
                yield tid, key, text

    def test_texts_carry_no_route_or_stat_words_so_immersive_stays_clean(self):
        stat_words = re.compile(r"\b(?:trust|stat|stats|points?)\b", re.IGNORECASE)
        for tid, key, text in self.all_texts():
            self.assertFalse(lc_discovery.has_route_words(text), (tid, key, text))
            self.assertIsNone(stat_words.search(text), (tid, key, text))

    def test_texts_use_name_tokens_never_typed_names(self):
        # Maya has no name token (she is not renameable), so Day Two texts may name her.
        typed = re.compile(r"\b(?:Ryan|Leia|Julian)\b")
        for tid, key, text in self.all_texts():
            self.assertIsNone(typed.search(text), (tid, key, text))
            for token in re.findall(r"\[(\w+)\]", text):
                self.assertIn(token, ("player_name", "girlfriend_name", "friend_name"), (tid, key))

    def test_no_consent_framing_wording(self):
        banned = re.compile(r"\b(?:consent|check(?:ed|ing)? in|boundar(?:y|ies)|comfortable with)\b",
                            re.IGNORECASE)
        for tid, key, text in self.all_texts():
            self.assertIsNone(banned.search(text), (tid, key, text))


class VariantTests(unittest.TestCase):
    def setUp(self):
        # A thought with every kind of variant, registered into a private pool.
        self.thoughts = {
            "t": {"day": DAY1, "requires": "b", "base": "base",
                  "variants": {"love_lane": "love lane", "exhibitionism": "exhib",
                               "temptation": "tempt", "trust": "trust"}},
            "s": {"day": DAY1, "requires": "b", "base": "plain",
                  "variants": {"temptation": "tempt only"}},
        }

    def text(self, tid, st, lane=None):
        return lc_thoughts.thought_text(tid, st, lane, thoughts=self.thoughts)

    def test_below_every_bar_reads_the_base(self):
        self.assertEqual(self.text("t", CALM), "base")
        self.assertIsNone(lc_thoughts.variant_key("t", CALM, None, thoughts=self.thoughts))

    def test_a_stat_over_its_bar_picks_its_variant(self):
        bar = lc_thoughts.TINT["exhibitionism"]
        self.assertEqual(self.text("t", stats(exhibitionism=bar)), "exhib")
        self.assertEqual(self.text("t", stats(exhibitionism=bar - 1)), "base")
        self.assertEqual(self.text("t", stats(temptation=lc_thoughts.TINT["temptation"])), "tempt")

    def test_the_stat_furthest_over_its_bar_wins(self):
        t = lc_thoughts.TINT
        st = stats(exhibitionism=t["exhibitionism"] + 2, temptation=t["temptation"] + 5)
        self.assertEqual(self.text("t", st), "tempt")
        st = stats(exhibitionism=t["exhibitionism"] + 9, temptation=t["temptation"] + 1)
        self.assertEqual(self.text("t", st), "exhib")

    def test_ties_follow_the_priority_order(self):
        t = lc_thoughts.TINT
        st = stats(exhibitionism=t["exhibitionism"] + 3, temptation=t["temptation"] + 3)
        first = [k for k in lc_thoughts.STAT_PRIORITY if k in ("exhibitionism", "temptation")][0]
        self.assertEqual(lc_thoughts.variant_key("t", st, None, thoughts=self.thoughts), first)

    def test_lane_rule_comes_first(self):
        st = stats(temptation=lc_thoughts.TINT["temptation"] + 9)
        self.assertEqual(self.text("t", st, "love_lane"), "love lane")

    def test_a_lane_without_a_variant_falls_through_to_stats(self):
        st = stats(temptation=lc_thoughts.TINT["temptation"] + 1)
        self.assertEqual(self.text("t", st, "ntr_lane"), "tempt")
        self.assertEqual(self.text("s", CALM, "love_lane"), "plain")

    def test_stats_without_a_variant_are_ignored(self):
        st = stats(exhibitionism=90)
        self.assertEqual(self.text("s", st), "plain")

    def test_missing_or_odd_stats_never_raise(self):
        self.assertEqual(self.text("t", {}), "base")
        self.assertEqual(self.text("t", None), "base")
        self.assertEqual(self.text("t", {"temptation": None}), "base")

    def test_unknown_thought_raises(self):
        with self.assertRaises(KeyError):
            lc_thoughts.thought_text("nope", CALM, None)

    def test_real_pool_resolves_for_every_stat_and_lane(self):
        for tid in lc_thoughts.THOUGHT_ORDER:
            entry = lc_thoughts.THOUGHTS[tid]
            for key, text in entry["variants"].items():
                if key in lc_thoughts.LANES:
                    self.assertEqual(lc_thoughts.thought_text(tid, CALM, key), text)
                else:
                    st = stats(**{key: lc_thoughts.TINT[key] + 30})
                    self.assertEqual(lc_thoughts.thought_text(tid, st, None), text, (tid, key))
            self.assertEqual(lc_thoughts.thought_text(tid, CALM, None), entry["base"])


class NameTests(unittest.TestCase):
    def test_fill_names_replaces_only_the_three_tokens(self):
        names = {"player_name": "Sam", "girlfriend_name": "Ana", "friend_name": "Jo"}
        self.assertEqual(lc_thoughts.fill_names("[girlfriend_name] and [friend_name], [player_name]. [x]", names),
                         "Ana and Jo, Sam. [x]")

    def test_missing_names_fall_back_to_the_defaults(self):
        self.assertEqual(lc_thoughts.fill_names("[girlfriend_name]/[friend_name]/[player_name]", {}),
                         "Leia/Julian/Ryan")


class LaneTests(unittest.TestCase):
    def test_lean_maps_to_a_lane(self):
        self.assertEqual(lc_thoughts.lane_from_lean("love"), "love_lane")
        self.assertEqual(lc_thoughts.lane_from_lean("love_exhib"), "exhib_lane")
        self.assertEqual(lc_thoughts.lane_from_lean("ntr"), "ntr_lane")
        for lean in ("undecided", "strained", None, "???"):
            self.assertIsNone(lc_thoughts.lane_from_lean(lean))


class LaneLimitTests(unittest.TestCase):
    """A lane limits which stat variants may tint a thought (Love warmth, NTR temptation)."""

    # Every value Day One can reach and then some (the simulation's ranges are Love 40-66,
    # Trust 46-72, Exhibitionism 10-49, Temptation 10-26).
    GRID = [dict(CALM, love=lo, trust=tr, exhibitionism=ex, temptation=te)
            for lo in (40, 58, 70) for tr in (40, 57, 58, 66, 80)
            for ex in (10, 18, 19, 30, 49, 60) for te in (10, 11, 12, 20, 26, 40)]

    def keys(self, lane):
        for tid in lc_thoughts.THOUGHT_ORDER:
            for st in self.GRID:
                yield tid, st, lc_thoughts.variant_key(tid, st, lane)

    def test_love_lane_only_shows_love_or_trust_words(self):
        for tid, st, key in self.keys("love_lane"):
            self.assertIn(key, (None, "love_lane", "love", "trust"), (tid, st))

    def test_every_day_one_thought_has_a_love_lane_line(self):
        for tid in lc_thoughts.day_thoughts(DAY1):
            self.assertIn("love_lane", lc_thoughts.THOUGHTS[tid]["variants"], tid)

    def test_ntr_lane_never_shows_love_and_prefers_temptation_over_exhibitionism(self):
        for tid, st, key in self.keys("ntr_lane"):
            self.assertNotIn(key, ("love", "love_lane"), (tid, st))
            variants = lc_thoughts.THOUGHTS[tid]["variants"]
            if "temptation" in variants and st["temptation"] >= lc_thoughts.TINT["temptation"]:
                self.assertEqual(key, "temptation", (tid, st))

    def test_exhib_lane_never_shows_temptation_over_exhibitionism(self):
        for tid, st, key in self.keys("exhib_lane"):
            variants = lc_thoughts.THOUGHTS[tid]["variants"]
            if "exhibitionism" in variants and st["exhibitionism"] >= lc_thoughts.TINT["exhibitionism"]:
                self.assertEqual(key, "exhibitionism", (tid, st))

    def test_every_lane_key_has_a_stat_limit(self):
        self.assertEqual(set(lc_thoughts.LANE_STATS), set(lc_thoughts.LANES))
        for lane, allowed in lc_thoughts.LANE_STATS.items():
            for stat in allowed:
                self.assertIn(stat, lc_thoughts.TINT, lane)


class OfferTests(unittest.TestCase):
    def test_offer_is_one_card_per_part_of_the_day(self):
        got = lc_thoughts.offer(DAY1, CALM, None, ALL_DAY1_BEATS)
        self.assertEqual(len(got), 3)
        parts = lc_thoughts.OFFER_PARTS[DAY1]
        for part, tid in zip(parts, got):
            self.assertIn(tid, part)

    def test_parts_cover_the_day_once_in_day_order(self):
        for day in {e["day"] for e in lc_thoughts.THOUGHTS.values()}:
            flat = [tid for part in lc_thoughts.OFFER_PARTS[day] for tid in part]
            self.assertEqual(flat, lc_thoughts.day_thoughts(day), day)

    def test_day_one_parts_are_daytime_evening_night(self):
        self.assertEqual(lc_thoughts.OFFER_PARTS[DAY1], (
            ("d1_photo_shoot", "d1_towel"),
            ("d1_dinner_stranger", "d1_julian_carry"),
            ("d1_sofa_glance", "d1_dream")))

    def test_a_part_with_nothing_seen_gives_no_card(self):
        seen = {lc_thoughts.THOUGHTS[t]["requires"] for t in ("d1_towel", "d1_dream")}
        self.assertEqual(lc_thoughts.offer(DAY1, CALM, None, seen), ["d1_towel", "d1_dream"])

    def test_uncoloured_parts_fall_back_to_day_order(self):
        got = lc_thoughts.offer(DAY1, CALM, None, ALL_DAY1_BEATS)
        self.assertEqual(got, ["d1_photo_shoot", "d1_dinner_stranger", "d1_sofa_glance"])

    def test_a_coloured_thought_beats_an_uncoloured_one_in_its_part(self):
        # Trust colours the towel, carry and dream, never the photo, dinner or sofa.
        st = stats(trust=lc_thoughts.TINT["trust"] + 5)
        got = lc_thoughts.offer(DAY1, st, None, ALL_DAY1_BEATS)
        self.assertEqual(got, ["d1_towel", "d1_julian_carry", "d1_dream"])

    def test_the_thought_this_save_colours_most_wins_its_part(self):
        t = lc_thoughts.TINT
        # Temptation and Exhibitionism colour all six; Trust adds a colour to towel/carry/dream.
        hot = stats(exhibitionism=t["exhibitionism"] + 5, temptation=t["temptation"] + 5)
        self.assertEqual(lc_thoughts.offer(DAY1, hot, "ntr_lane", ALL_DAY1_BEATS),
                         ["d1_photo_shoot", "d1_dinner_stranger", "d1_sofa_glance"])
        hot["trust"] = t["trust"] + 1
        self.assertEqual(lc_thoughts.offer(DAY1, hot, "ntr_lane", ALL_DAY1_BEATS),
                         ["d1_towel", "d1_julian_carry", "d1_dream"])
        # Love lane: every thought has a love line; Trust decides between the two.
        self.assertEqual(lc_thoughts.offer(DAY1, stats(trust=t["trust"] + 9), "love_lane", ALL_DAY1_BEATS),
                         ["d1_towel", "d1_julian_carry", "d1_dream"])
        self.assertEqual(lc_thoughts.offer(DAY1, CALM, "love_lane", ALL_DAY1_BEATS),
                         ["d1_photo_shoot", "d1_dinner_stranger", "d1_sofa_glance"])

    def test_a_lane_never_counts_a_stat_it_forbids(self):
        # Love lane ignores Exhibitionism/Temptation when picking, as it does when tinting.
        t = lc_thoughts.TINT
        st = stats(exhibitionism=t["exhibitionism"] + 20, temptation=t["temptation"] + 20)
        self.assertEqual(lc_thoughts.offer(DAY1, st, "love_lane", ALL_DAY1_BEATS),
                         ["d1_photo_shoot", "d1_dinner_stranger", "d1_sofa_glance"])

    def test_every_day_one_thought_can_be_offered(self):
        t = lc_thoughts.TINT
        offered = set()
        for lane in (None,) + lc_thoughts.LANES:
            for trust in (50, t["trust"] + 3):
                for seen in (ALL_DAY1_BEATS, ALL_DAY1_BEATS - {"d1_photo_shoot"}):
                    offered.update(lc_thoughts.offer(DAY1, stats(trust=trust), lane, seen))
        self.assertEqual(offered, set(lc_thoughts.day_thoughts(DAY1)))

    def test_unseen_beats_are_never_offered(self):
        ids = lc_thoughts.day_thoughts(DAY1)
        one = lc_thoughts.THOUGHTS[ids[0]]["requires"]
        self.assertEqual(lc_thoughts.offer(DAY1, CALM, None, {one}), [ids[0]])
        self.assertEqual(lc_thoughts.offer(DAY1, CALM, None, set()), [])
        self.assertEqual(lc_thoughts.offer(DAY1, CALM, None, None), [])
        self.assertEqual(lc_thoughts.offer(DAY1, CALM, None, {"some_other_beat"}), [])

    def test_other_days_and_unknown_days_offer_nothing(self):
        self.assertEqual(lc_thoughts.offer("ch01_d2", CALM, None, ALL_DAY1_BEATS), [])
        self.assertEqual(lc_thoughts.offer("nope", CALM, None, ALL_DAY1_BEATS), [])

    def test_demo_build_offers_nothing(self):
        self.assertEqual(lc_thoughts.offer(DAY1, CALM, None, ALL_DAY1_BEATS, demo=True), [])

    def test_offer_is_deterministic(self):
        a = lc_thoughts.offer(DAY1, CALM, "love_lane", ALL_DAY1_BEATS)
        b = lc_thoughts.offer(DAY1, CALM, "love_lane", set(ALL_DAY1_BEATS))
        self.assertEqual(a, b)


class SeenBeatTests(unittest.TestCase):
    def test_every_beat_reads_a_flag_or_value_day_one_really_sets(self):
        # Canon guard: a renamed Day One flag would otherwise silently hide a thought forever.
        day1 = ROOT / "game/chapters/ch01/day1"
        script = "\n".join(p.read_text(encoding="utf-8") for p in sorted(day1.glob("*.rpy")))
        for beat, spec in lc_thoughts.BEATS.items():
            if spec["day"] != DAY1:
                continue
            kind, key = spec["test"][0], spec["test"][1]
            if kind == "flag":
                self.assertIn('set_story_flag("%s")' % key, script, beat)
            elif kind == "value_set":
                self.assertIn('set_story_value("%s",' % key, script, beat)
            else:
                values = [int(n) for n in re.findall(r'set_story_value\("%s", (\d+)\)' % re.escape(key), script)]
                self.assertTrue(values, beat)
                self.assertTrue(any(v >= spec["test"][2] for v in values), beat)
                self.assertTrue(any(v < spec["test"][2] for v in values), beat)

    def test_every_thought_names_its_source_label(self):
        # Each thought's comment names the Day One label its words are checked against.
        source = (ROOT / "game/python-packages/lc_days/day1.py").read_text(encoding="utf-8")
        day1 = ROOT / "game/chapters/ch01/day1"
        script = "\n".join(p.read_text(encoding="utf-8") for p in sorted(day1.glob("*.rpy")))
        for tid in lc_thoughts.day_thoughts(DAY1):
            before = source[:source.index('    "%s": {\n        "day"' % tid)].split("\n")[:-1]
            comment = []
            while before and before[-1].startswith("    #"):
                comment.append(before.pop())
            labels = " ".join(re.findall(r"Source:((?: \w+)+)", "\n".join(comment))).split()
            self.assertTrue(labels, tid)
            for label in labels:
                self.assertIn("label %s:" % label, script, (tid, label))

    def test_beats_read_flags_and_values(self):
        flags, values = set(), {}
        has_flag = flags.__contains__
        get_value = values.get
        self.assertEqual(lc_thoughts.seen_beats(DAY1, has_flag, get_value), set())
        for beat, spec in lc_thoughts.BEATS.items():
            test = spec["test"]
            if test[0] == "flag":
                flags.add(test[1])
            elif test[0] == "value_set":
                values[test[1]] = "anything"
            elif test[0] == "value_min":
                values[test[1]] = test[2]
            else:
                self.fail("unknown beat test %r" % (test,))
        seen = lc_thoughts.seen_beats(DAY1, has_flag, get_value)
        self.assertEqual(seen, {b for b, s in lc_thoughts.BEATS.items() if s["day"] == DAY1})

    def test_value_min_needs_the_minimum(self):
        beats = {"x": {"day": DAY1, "test": ("value_min", "count", 1)}}
        self.assertEqual(lc_thoughts.seen_beats(DAY1, lambda f: False, {"count": 0}.get, beats=beats), set())
        self.assertEqual(lc_thoughts.seen_beats(DAY1, lambda f: False, {"count": 2}.get, beats=beats), {"x"})
        self.assertEqual(lc_thoughts.seen_beats(DAY1, lambda f: False, {}.get, beats=beats), set())


class DayTwoPoolTests(unittest.TestCase):
    """Day Two's thoughts: offered at the end of the Day Two review, kept for Day Three."""

    DAY2_DIR = ROOT / "game/chapters/ch01/day2"

    def script(self):
        return "\n".join(p.read_text(encoding="utf-8") for p in sorted(self.DAY2_DIR.glob("*.rpy")))

    def test_day_two_has_about_six_thoughts_each_on_its_own_beat(self):
        ids = lc_thoughts.day_thoughts(DAY2)
        self.assertTrue(5 <= len(ids) <= 7, ids)
        beats = [lc_thoughts.THOUGHTS[t]["requires"] for t in ids]
        self.assertEqual(len(beats), len(set(beats)))
        for beat in beats:
            self.assertEqual(lc_thoughts.BEATS[beat]["day"], DAY2)

    def test_day_two_parts_are_morning_afternoon_night(self):
        self.assertEqual(lc_thoughts.OFFER_PARTS[DAY2], (
            ("d2_breakfast", "d2_maya_cafe"),
            ("d2_boutique", "d2_pool_bee"),
            ("d2_dinner", "d2_game_night")))

    def test_every_day_two_beat_reads_a_flag_or_value_day_two_really_sets(self):
        script = self.script()
        for beat, spec in lc_thoughts.BEATS.items():
            if spec["day"] != DAY2:
                continue
            kind, key = spec["test"][0], spec["test"][1]
            self.assertIn(kind, ("flag", "value_set"), beat)
            if kind == "flag":
                self.assertIn('set_story_flag("%s")' % key, script, beat)
            else:
                self.assertIn('set_story_value("%s",' % key, script, beat)

    def test_every_day_two_thought_names_its_source_label(self):
        source = (ROOT / "game/python-packages/lc_days/day2.py").read_text(encoding="utf-8")
        script = self.script()
        for tid in lc_thoughts.day_thoughts(DAY2):
            before = source[:source.index('    "%s": {\n        "day"' % tid)].split("\n")[:-1]
            comment = []
            while before and before[-1].startswith("    #"):
                comment.append(before.pop())
            labels = " ".join(re.findall(r"Source:((?: \w+)+)", "\n".join(comment))).split()
            self.assertTrue(labels, tid)
            for label in labels:
                self.assertIn("label %s:" % label, script, (tid, label))

    def test_every_day_two_thought_has_a_love_lane_line(self):
        for tid in lc_thoughts.day_thoughts(DAY2):
            self.assertIn("love_lane", lc_thoughts.THOUGHTS[tid]["variants"], tid)

    def test_day_two_offer_is_three_cards_from_the_day_two_pool(self):
        got = lc_thoughts.offer(DAY2, CALM, None, ALL_DAY2_BEATS)
        self.assertEqual(got, ["d2_breakfast", "d2_boutique", "d2_dinner"])
        self.assertEqual(lc_thoughts.offer(DAY2, CALM, None, ALL_DAY1_BEATS), [])
        self.assertEqual(lc_thoughts.offer(DAY1, CALM, None, ALL_DAY2_BEATS), [])

    def test_every_day_two_thought_can_be_offered(self):
        # Monte Carlo over the stats Day Two can reach (wider than Day One) and every lane.
        import random
        rng = random.Random(2)
        t = lc_thoughts.TINT
        offered, love_keys = set(), set()
        for _ in range(4000):
            st = stats(love=rng.randint(40, 80), trust=rng.randint(40, 80),
                       exhibitionism=rng.randint(10, 60), temptation=rng.randint(10, 40),
                       sharing=rng.randint(0, 8))
            lane = rng.choice((None,) + lc_thoughts.LANES)
            for tid in lc_thoughts.offer(DAY2, st, lane, ALL_DAY2_BEATS):
                offered.add(tid)
                key = lc_thoughts.variant_key(tid, st, lane)
                if lane == "love_lane":
                    love_keys.add(key)
        self.assertEqual(offered, set(lc_thoughts.day_thoughts(DAY2)))
        self.assertEqual(love_keys, {"love_lane"})
        self.assertTrue(t)

    def test_keep_a_day_two_thought_for_day_three(self):
        kept = lc_thoughts.keep({DAY1: "d1_dream"}, DAY2, "d2_game_night")
        self.assertEqual(lc_thoughts.kept_id(kept, DAY2), "d2_game_night")
        self.assertEqual(lc_thoughts.kept_id(kept, DAY1), "d1_dream")
        with self.assertRaises(ValueError):
            lc_thoughts.keep({}, DAY2, "d1_dream")


class KeepTests(unittest.TestCase):
    def test_keep_nothing_stores_none(self):
        kept = lc_thoughts.keep({}, DAY1, None)
        self.assertEqual(kept, {DAY1: None})
        self.assertIn(DAY1, kept)
        self.assertIsNone(lc_thoughts.kept_id(kept, DAY1))

    def test_keep_one_returns_a_new_dict(self):
        before = {}
        tid = lc_thoughts.day_thoughts(DAY1)[0]
        after = lc_thoughts.keep(before, DAY1, tid)
        self.assertEqual(before, {})
        self.assertEqual(lc_thoughts.kept_id(after, DAY1), tid)

    def test_keep_rejects_unknown_or_other_day_ids(self):
        with self.assertRaises(ValueError):
            lc_thoughts.keep({}, DAY1, "nope")
        with self.assertRaises(ValueError):
            lc_thoughts.keep({}, "ch01_d2", lc_thoughts.day_thoughts(DAY1)[0])

    def test_keep_and_kept_id_use_an_injected_pool(self):
        pool = {"x1": {"day": DAY1, "requires": "b", "base": "x", "variants": {}}}
        kept = lc_thoughts.keep({}, DAY1, "x1", thoughts=pool)
        self.assertEqual(lc_thoughts.kept_id(kept, DAY1, thoughts=pool), "x1")
        self.assertIsNone(lc_thoughts.kept_id(kept, DAY1))

    def test_old_saves_read_nothing_kept(self):
        self.assertIsNone(lc_thoughts.kept_id(None, DAY1))
        self.assertIsNone(lc_thoughts.kept_id({}, DAY1))
        self.assertIsNone(lc_thoughts.kept_id({DAY1: "retired_id"}, DAY1))


class ThoughtRuntimeTests(unittest.TestCase):
    """The production init block of game/systems/thoughts.rpy with engine boundaries stubbed."""

    def setUp(self):
        self.store = SimpleNamespace(lc_thoughts_kept={})
        self.flags, self.values = set(), {}
        self.stats = dict(CALM)
        self.lean = "undecided"
        self.screens = []
        self.reply = None

        def call_screen(name, *args, **kw):
            self.screens.append((name, args, kw))
            return self.reply

        self.renpy = SimpleNamespace(store=self.store, call_screen=call_screen,
                                     log=lambda *a: None)
        self.config = SimpleNamespace(developer=False)
        self.env = dict(store=self.store, renpy=self.renpy, config=self.config,
                        has_story_flag=self.flags.__contains__,
                        get_story_value=lambda k, d=None: self.values.get(k, d),
                        lc_stats_flat=lambda: dict(self.stats),
                        lc_current_lean=lambda: self.lean,
                        current_choice_mode=lambda: "full",
                        LC_DAY1_DEMO_BUILD=False)
        load_blocks(["lc_thought_kept"], self.env)

    def call(self, name, *a, **kw):
        return self.env[name](*a, **kw)

    def see_all_day1(self):
        for beat in ALL_DAY1_BEATS:
            test = lc_thoughts.BEATS[beat]["test"]
            if test[0] == "flag":
                self.flags.add(test[1])
            elif test[0] == "value_set":
                self.values[test[1]] = "x"
            else:
                self.values[test[1]] = test[2]

    def test_old_save_without_the_value_reads_nothing_kept(self):
        del self.store.lc_thoughts_kept
        self.assertIsNone(self.call("lc_thought_kept", DAY1))
        self.assertIsNone(self.call("lc_thought_line", DAY1))

    def test_nothing_seen_offers_nothing_and_shows_no_screen(self):
        self.assertEqual(self.call("lc_thought_offer_ids", DAY1), [])
        self.assertIsNone(self.call("lc_thought_offer", DAY1))
        self.assertEqual(self.screens, [])
        self.assertEqual(self.store.lc_thoughts_kept, {})

    def test_offer_keeps_the_picked_thought(self):
        self.see_all_day1()
        ids = self.call("lc_thought_offer_ids", DAY1)
        self.assertEqual(len(ids), 3)
        self.reply = ids[1]
        self.call("lc_thought_offer", DAY1)
        self.assertEqual(self.screens[0][0], "lc_thought_offer_screen")
        self.assertEqual(self.call("lc_thought_kept", DAY1), ids[1])
        restored = pickle.loads(pickle.dumps(self.store.lc_thoughts_kept))
        self.assertEqual(restored, {DAY1: ids[1]})

    def test_keep_nothing_stores_none_and_is_not_offered_again(self):
        self.see_all_day1()
        self.reply = None
        self.call("lc_thought_offer", DAY1)
        self.assertEqual(self.store.lc_thoughts_kept, {DAY1: None})
        self.assertIsNone(self.call("lc_thought_kept", DAY1))
        self.call("lc_thought_offer", DAY1)
        self.assertEqual(len(self.screens), 1)

    def test_a_reply_that_was_not_offered_keeps_nothing(self):
        self.see_all_day1()
        offered = self.call("lc_thought_offer_ids", DAY1)
        self.reply = [t for t in lc_thoughts.day_thoughts(DAY1) if t not in offered][0]
        self.call("lc_thought_offer", DAY1)
        self.assertEqual(self.store.lc_thoughts_kept, {DAY1: None})

    def test_day_two_review_offers_the_day_two_pool(self):
        for beat in ALL_DAY2_BEATS:
            test = lc_thoughts.BEATS[beat]["test"]
            if test[0] == "flag":
                self.flags.add(test[1])
            else:
                self.values[test[1]] = "x"
        self.store.lc_thoughts_kept = {DAY1: "d1_dream"}
        ids = self.call("lc_thought_offer_ids", DAY2)
        self.assertEqual(len(ids), 3)
        self.reply = ids[2]
        self.call("lc_thought_on_review_closed", DAY2)
        self.assertEqual(self.store.lc_thoughts_kept, {DAY1: "d1_dream", DAY2: ids[2]})
        self.assertEqual(self.call("lc_thought_kept", DAY2), ids[2])

    def test_demo_build_hides_the_offer(self):
        self.see_all_day1()
        self.env["LC_DAY1_DEMO_BUILD"] = True
        self.assertEqual(self.call("lc_thought_offer_ids", DAY1), [])
        self.call("lc_thought_offer", DAY1)
        self.assertEqual(self.screens, [])
        self.assertEqual(self.store.lc_thoughts_kept, {})

    def test_line_evolves_with_the_current_stats_and_lane(self):
        tid = "d1_dream"
        fill = lambda text: lc_thoughts.fill_names(text, {})  # noqa: E731
        self.store.lc_thoughts_kept = {DAY1: tid}
        self.assertEqual(self.call("lc_thought_line", DAY1), fill(lc_thoughts.THOUGHTS[tid]["base"]))
        self.stats["temptation"] = lc_thoughts.TINT["temptation"] + 4
        self.assertEqual(self.call("lc_thought_line", DAY1),
                         fill(lc_thoughts.THOUGHTS[tid]["variants"]["temptation"]))
        self.lean = "love"
        self.assertEqual(self.call("lc_thought_line", DAY1),
                         fill(lc_thoughts.THOUGHTS[tid]["variants"]["love_lane"]))

    def test_line_fills_the_players_names(self):
        self.store.player_name, self.store.girlfriend_name, self.store.friend_name = "Sam", "Ana", "Jo"
        tid = "d1_julian_carry"
        self.store.lc_thoughts_kept = {DAY1: tid}
        line = self.call("lc_thought_line", DAY1)
        self.assertNotIn("[", line)
        self.assertEqual(line, lc_thoughts.fill_names(lc_thoughts.THOUGHTS[tid]["base"],
                                                      {"player_name": "Sam", "girlfriend_name": "Ana",
                                                       "friend_name": "Jo"}))

    def test_review_closed_hook_never_breaks_the_review_in_release(self):
        self.see_all_day1()

        def boom(*a, **kw):
            raise RuntimeError("screen failed")
        self.renpy.call_screen = boom
        self.assertIsNone(self.call("lc_thought_on_review_closed", DAY1))
        self.config.developer = True
        with self.assertRaises(RuntimeError):
            self.call("lc_thought_on_review_closed", DAY1)

    def test_renpy_control_flow_always_passes_through_the_hook(self):
        self.see_all_day1()

        class Rollback(Exception):
            pass

        def rollback(*a, **kw):
            raise Rollback()
        self.renpy.call_screen = rollback
        self.renpy.game = SimpleNamespace(CONTROL_EXCEPTIONS=(Rollback,))
        with self.assertRaises(Rollback):
            self.call("lc_thought_on_review_closed", DAY1)
        self.assertEqual(self.store.lc_thoughts_kept, {})


class SourceContractTests(unittest.TestCase):
    def test_review_label_emits_review_closed_after_the_spread(self):
        source = (ROOT / "game/systems/day_review.rpy").read_text(encoding="utf-8")
        label = source[source.index("label lc_day_review(day_id):"):]
        spread = label.index("call screen lc_day_review_screen(")
        hook = label.index('$ lc_hook_run("review_closed", day_id)')
        self.assertLess(spread, hook)
        self.assertLess(hook, label.index("lc_bgm_stop("))

    def test_thoughts_listen_through_the_hook_and_save_per_save(self):
        source = (ROOT / "game/systems/thoughts.rpy").read_text(encoding="utf-8")
        self.assertIn('lc_hook_add("review_closed", lc_thought_on_review_closed)', source)
        self.assertIn("default lc_thoughts_kept = {}", source)
        self.assertNotIn("persistent.", source.split("init")[0])
        self.assertNotIn("_orig", source)

    def test_offer_screen_has_keep_nothing_and_hides_tints_in_immersive(self):
        text = (ROOT / "game/screens/thoughts_screen.rpy").read_text(encoding="utf-8")
        start = text.index("\nscreen lc_thought_offer_screen(")
        screen = text[start:]
        self.assertIn("KEEP NOTHING", screen)
        self.assertIn("Return(None)", screen)
        self.assertIn('if mode != "normal"', screen)
        self.assertIn('style "lc_hand"', screen)
        self.assertIn("substitute False", screen)

    def test_offer_screen_is_reachable_by_keyboard_and_gamepad(self):
        text = (ROOT / "game/screens/thoughts_screen.rpy").read_text(encoding="utf-8")
        screen = text[text.index("\nscreen lc_thought_offer_screen("):]
        # The invisible stray-click catcher must never take keyboard/gamepad focus.
        catcher = screen[screen.index("action NullAction()") - 400:screen.index("action NullAction()")]
        self.assertIn("keyboard_focus False", catcher[catcher.rindex("button:"):])
        # The first card starts focused, and KEEP NOTHING shows when it has focus.
        self.assertIn("default_focus (index == 0)", screen)
        keep_nothing = screen[screen.index('text "KEEP NOTHING"'):]
        self.assertNotIn("hover_background None", keep_nothing)


class ThoughtStatsErrorTests(unittest.TestCase):
    """A broken stats/lean call shows the base text in release but raises in developer mode."""

    def setUp(self):
        self.config = SimpleNamespace(developer=False)

        def boom():
            raise RuntimeError("stats broke")
        self.env = dict(store=SimpleNamespace(lc_thoughts_kept={}), config=self.config,
                        renpy=SimpleNamespace(log=lambda *a: None),
                        lc_stats_flat=boom, lc_current_lean=boom)
        load_blocks(["lc_thought_kept"], self.env)

    def test_release_falls_back_and_developer_mode_raises(self):
        self.assertEqual(self.env["_lc_thought_stats"](), {})
        self.assertIsNone(self.env["lc_thought_lane"]())
        self.config.developer = True
        with self.assertRaises(RuntimeError):
            self.env["_lc_thought_stats"]()
        with self.assertRaises(RuntimeError):
            self.env["lc_thought_lane"]()


if __name__ == "__main__":
    unittest.main()
