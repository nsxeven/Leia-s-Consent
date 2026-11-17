"""Subtle Day Two tint for Leia's lines (darryn 2026-11-17).

Leia is shy and affectionate by default; a tint point picks one small variant from the stat
that stands furthest above its own threshold. The lane decides the scene, the tint only
colours lines inside it: no Temptation tint on the Love lane, no Love tint inside an
NTR-risk lane scene. Tints never write stats or flags.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "game" / "python-packages"))
sys.path.insert(0, str(ROOT / "tests"))

import lc_stat_model as m  # noqa: E402
import test_route_simulation as sim  # noqa: E402

TINTS = ("shy", "love", "trust", "exhibitionism", "sharing", "temptation")


def defaults():
    return {s: m.DEFAULTS[m.STAT_GROUPS[s]][s] for s in m.STAT_ORDER}


def persona_stats(name):
    for pname, d1, d2, branch, _want in sim.PERSONAS:
        if pname == name:
            return sim.play(d1, d2, **branch)[4]
    raise KeyError(name)


class LeiaTintTests(unittest.TestCase):

    def test_thresholds_present(self):
        for stat in m.STAT_ORDER:
            self.assertIn("d2_tint_" + stat, m.THRESHOLDS)

    def test_defaults_are_shy(self):
        self.assertEqual(m.leia_tint(defaults()), "shy")

    def test_each_stat_just_over_threshold_wins(self):
        for stat in m.STAT_ORDER:
            stats = defaults()
            stats[stat] = m.THRESHOLDS["d2_tint_" + stat]
            with self.subTest(stat):
                self.assertEqual(m.leia_tint(stats), stat)

    def test_love_lane_never_temptation(self):
        stats = defaults()
        stats["temptation"] = 40
        self.assertNotEqual(m.leia_tint(stats, lane="love"), "temptation")

    def test_ntr_lane_scene_never_love(self):
        stats = defaults()
        stats["love"] = 90
        stats["temptation"] = m.THRESHOLDS["d2_tint_temptation"]
        self.assertEqual(m.leia_tint(stats, lane="ntr_risk", lane_scene=True), "temptation")
        # Outside a lane scene the strongest stat still wins.
        self.assertEqual(m.leia_tint(stats, lane="ntr_risk"), "love")

    def test_unknown_lane_and_missing_stats_are_shy(self):
        self.assertEqual(m.leia_tint({}, lane="???"), "shy")
        self.assertEqual(m.leia_tint({"love": None}), "shy")

    def test_always_returns_a_known_tint(self):
        for name, *_ in sim.PERSONAS:
            with self.subTest(name):
                self.assertIn(m.leia_tint(persona_stats(name)), TINTS)

    def test_personas(self):
        self.assertEqual(m.leia_tint(persona_stats("pure Love")), "love")
        self.assertEqual(m.leia_tint(persona_stats("Love + Exhibitionism")), "exhibitionism")
        self.assertEqual(m.leia_tint(persona_stats("NTR, locked at the wink"), lane="ntr_risk", lane_scene=True),
                         "temptation")
        self.assertNotEqual(m.leia_tint(persona_stats("Love, two slips on Day 1")), "temptation")


if __name__ == "__main__":
    unittest.main()
