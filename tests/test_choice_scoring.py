"""Stat model v2 scoring rule, enforced for EVERY current and future choice.

The rule (game/python-packages/lc_stat_model.py, scoring_violations):
- only Love, Trust, Exhibitionism, Sharing, Temptation, each in its own group;
- at most 2 stats per choice (hard gates 3), deltas within +-3 (gates +-5);
- one route stat at most (Exhibitionism, Sharing or Temptation);
- Temptation up never together with another stat going up;
- allowed shapes only (Love, Love+Exhib, NTS, NTR, Repair on repair beats,
  Temptation down alone, Neutral), so no choice can push two routes at once;
- the Full route tag is derivable from the effects.

A new choice that breaks any of these fails here with the choice id and reason.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "game" / "python-packages"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import lc_stat_model as m  # noqa: E402
from lc_effective_effects import applied_choice_ids, definitions, effective_effects  # noqa: E402


class ChoiceScoringRuleTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.effects = effective_effects()

    def test_every_effective_choice_follows_the_scoring_rule(self):
        problems = []
        for choice_id, effects in sorted(self.effects.items()):
            for reason in m.scoring_violations(choice_id, effects):
                problems.append("{}: {}  {}".format(choice_id, reason, effects))
        self.assertEqual(problems, [], "\n" + "\n".join(problems))

    def test_no_retired_stat_survives_in_the_effective_table(self):
        for choice_id, effects in self.effects.items():
            for _group, stat, _amount in effects:
                self.assertNotIn(stat, m.RETIRED_STATS, choice_id)

    def test_every_applied_choice_has_effects(self):
        missing = sorted(applied_choice_ids() - set(self.effects))
        self.assertEqual(missing, [])

    def test_all_known_choices_are_kept(self):
        # 248 choice ids existed when the v2 model landed (8 of them unused but kept).
        self.assertGreaterEqual(len(self.effects), 248)
        for unused in ("ch01_fidget_cover", "ch01_fidget_tease", "ch01_fidget_push", "ch01_fidget_dismiss",
                       "ch01_looking_enjoy", "ch01_looking_harmless", "ch01_looking_boundary", "ch01_looking_dont_care"):
            self.assertIn(unused, self.effects)

    def test_one_definition_per_choice_and_priority(self):
        seen = {}
        for priority, rel, choice_id, _effects in definitions():
            key = (priority, choice_id)
            self.assertNotIn(key, seen, "{} defined twice at init {} ({} and {})".format(
                choice_id, priority, seen.get(key), rel))
            seen[key] = rel

    def test_gate_metadata_points_at_real_choices(self):
        for choice_id in list(m.CHOICE_GATES) + list(m.CHOICE_ROUTE_FLAGS) + list(m.REPAIR_CHOICES):
            self.assertIn(choice_id, self.effects)

    def test_route_tags_are_derived_from_effects(self):
        tag = lambda cid: m.choice_route_tag(cid, self.effects[cid])
        self.assertEqual(tag("ch01_d2_morning_reassure"), "Love")
        self.assertEqual(tag("ch01_photo_more"), "Love+Exhib")
        self.assertEqual(tag("ch01_compliment_shrug"), "NTR")
        self.assertEqual(tag("ch01_d2_wink_repair"), "Repair")
        self.assertEqual(tag("ch01_d2_sunset_ignore_gate"), "May lead to NTR")
        self.assertEqual(tag("ch01_d2_wink_reject_hard"), "Locks NTR")
        self.assertEqual(tag("ch01_d4_ntr_gate_accuse_hard"), "NTR stays open")
        self.assertEqual(tag("ch01_d5_ntr_c_go_to_her"), "Repair, NTR stays open")
        self.assertEqual(tag("ch01_julian_joke"), "Neutral")
        for choice_id, effects in self.effects.items():
            self.assertIn(m.choice_route_tag(choice_id, effects), m.TAGS, choice_id)

    def test_rule_catches_confusing_choices(self):
        bad = {
            "retired stat": [("relationship", "boredom", 1)],
            "two routes": [("partner", "exhibitionism", 1), ("relationship", "temptation", 1)],
            "ntr with a gain": [("relationship", "love", 1), ("relationship", "temptation", 2)],
            "three stats": [("relationship", "love", 1), ("relationship", "trust", 1), ("partner", "exhibitionism", 1)],
            "over cap": [("relationship", "love", 4)],
            "wrong group": [("relationship", "exhibitionism", 1)],
            "loss only": [("relationship", "love", -1)],
            "repair off a repair beat": [("relationship", "love", 1), ("relationship", "temptation", -1)],
            "sharing with love": [("relationship", "sharing", 1), ("relationship", "love", 1)],
        }
        for why, effects in bad.items():
            self.assertTrue(m.scoring_violations("ch01_new_test_choice", effects), why)
        good = [
            [],
            [("relationship", "love", 1), ("relationship", "trust", 2)],
            [("relationship", "trust", 1), ("partner", "exhibitionism", 2)],
            [("relationship", "trust", 1), ("relationship", "sharing", 2)],
            [("relationship", "love", -1), ("relationship", "temptation", 2)],
            [("relationship", "temptation", -1)],
        ]
        for effects in good:
            self.assertEqual(m.scoring_violations("ch01_new_test_choice", effects), [], effects)


if __name__ == "__main__":
    unittest.main()
