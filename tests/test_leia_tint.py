"""Subtle Day Two tint for Leia's lines (darryn 2026-11-17).

Leia is shy and affectionate by default; a tint point picks one small variant from the stat
that stands furthest above its own threshold. The lane decides the scene, the tint only
colours lines inside it: no Temptation tint on the Love lane, no Love tint inside an
NTR-risk lane scene. Tints never write stats or flags.
"""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY2 = ROOT / "game" / "chapters" / "ch01" / "day2"
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


class DayTwoTintCallsPassTheLane(unittest.TestCase):
    """PR #226 review I2: a tint never crosses lanes. leia_tint only drops the Temptation tint
    (Love lane) or the Love tint (NTR-risk lane scene) when it is told the lane, so every Day Two
    lc_leia_tint call whose branches include a love or temptation variant must pass one."""

    CALL = re.compile(r"^(\s*)\$\s*(\w+)\s*=\s*lc_leia_tint\((.*?)\)")
    BRANCH = re.compile(r'^(?:if|elif)\s+(\w+)\s*==\s*"(\w+)"\s*:')

    def calls(self):
        for path in sorted(DAY2.glob("*.rpy")):
            lines = path.read_text(encoding="utf-8").splitlines()
            for i, line in enumerate(lines):
                if "lc_leia_tint(" not in line or line.lstrip().startswith("#"):
                    continue
                found = self.CALL.match(line)
                self.assertTrue(found, "%s:%d unrecognised tint call: %s" % (path.name, i + 1, line))
                indent, var, args = len(found.group(1)), found.group(2), found.group(3).strip()
                variants = set()
                for nxt in lines[i + 1:]:
                    if not nxt.strip():
                        continue
                    ind = len(nxt) - len(nxt.lstrip())
                    if ind < indent:
                        break
                    if ind > indent:
                        continue
                    head = nxt.strip()
                    b = self.BRANCH.match(head)
                    if b and b.group(1) == var:
                        variants.add(b.group(2))
                    elif head != "else:":
                        break
                yield "%s:%d" % (path.name, i + 1), args, variants

    def test_lane_sensitive_tints_pass_the_lane(self):
        seen = 0
        for where, args, variants in self.calls():
            seen += 1
            self.assertTrue(variants, where)
            if variants & {"love", "temptation"}:
                self.assertTrue(args, "%s branches on %s but passes no lane" % (where, sorted(variants)))
        self.assertGreaterEqual(seen, 9)

if __name__ == "__main__":
    unittest.main()
