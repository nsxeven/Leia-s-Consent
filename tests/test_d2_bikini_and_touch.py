"""Scene 13 bikini by lane and the scene 15 'touch her' option (darryn 2026-11-19)."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D2 = ROOT / "game/chapters/ch01/day2"
A = (D2 / "ch01_day2_scenes_01_15.rpy").read_text(encoding="utf-8")
B = (D2 / "ch01_day2_scenes_16_30.rpy").read_text(encoding="utf-8")
REG = (D2 / "ch01_day2_registrations.rpy").read_text(encoding="utf-8")


def label(src, name):
    return re.split(r"\nlabel \w+:", src.split("label %s:" % name, 1)[1], maxsplit=1)[0]


class Bikini(unittest.TestCase):
    def setUp(self):
        self.s13 = label(A, "ch01_day2_scene_13_girls_upstairs")

    def test_no_stat_bar_decides_any_more(self):
        self.assertNotIn('LC_T["d2_pool_outfit_bold"]', self.s13)

    def test_lanes(self):
        exhib = self.s13.split('if d2_bikini_lane == "exhibitionism":', 1)[1].split("elif d2_bikini_lane", 1)[0]
        for cid in ("ch01_d2_bikini_red", "ch01_d2_bikini_white", "ch01_d2_bikini_red_second", "ch01_d2_bikini_white_second"):
            self.assertIn('apply_choice("%s")' % cid, exhib)
        self.assertIn("Last chance", exhib)
        ntr = self.s13.split('elif d2_bikini_lane == "ntr_risk" and d2_ryan_detached:', 1)[1].split("\n    else:", 1)[0]
        self.assertIn("fuck it out", ntr)
        self.assertIn('apply_choice("ch01_d2_bikini_ntr_red")', ntr)
        self.assertIn('apply_choice("ch01_d2_bikini_ntr_white")', ntr)
        rest = self.s13.split("elif d2_bikini_lane == \"ntr_risk\" and d2_ryan_detached:", 1)[1].split("\n    else:", 1)[1]
        self.assertIn('set_story_value("ch01_d2_pool_outfit", "pool_conservative")', rest)
        self.assertNotIn("pool_bolder", rest)  # Love and warm NTR: always white
        warm = self.s13.split('    elif d2_bikini_lane == "ntr_risk":', 1)[1].split("\n    else:", 1)[0]
        self.assertIn("nice, normal pool day with him", warm)  # warm NTR still gets the pick
        self.assertIn('apply_choice("ch01_d2_bikini_ntr_red")', warm)
        self.assertIn('"ch01_d2_bikini_jealousy", "for_him"', warm)
        self.assertIn("it's him. Just him", rest)

    def test_bikini_picks_are_flavour(self):
        for cid in ("ch01_d2_bikini_red", "ch01_d2_bikini_white", "ch01_d2_bikini_red_second",
                    "ch01_d2_bikini_white_second", "ch01_d2_bikini_ntr_red", "ch01_d2_bikini_ntr_white"):
            self.assertIn('"%s": [],' % cid, REG)


class Touch(unittest.TestCase):
    def test_option_only_red_and_exhib_or_ntr(self):
        self.assertIn('"[d2_knot_touch_text]" if d2_touch_open:', A)
        self.assertIn('d2_touch_open = d2_touch_red and d2_touch_lane in ("exhibitionism", "ntr_risk")', A)
        for cid in ("exhib", "ntr", "nts"):
            self.assertIn('apply_choice("ch01_d2_knot_touch_%s")' % cid, A)
        self.assertIn('d2_touch_red = get_story_value("ch01_d2_pool_outfit") == "pool_bolder"', A)

    def test_scores_and_lane_exempt(self):
        self.assertIn('"ch01_d2_knot_touch_exhib": [\n            ("partner", "exhibitionism", 1),\n            ("relationship", "love", 1),', REG.replace("\r\n", "\n"))
        reg = REG.replace("\r\n", "\n")
        self.assertIn('"ch01_d2_knot_touch_ntr": [\n            ("relationship", "temptation", 1),\n            ("relationship", "trust", -1),', reg)
        self.assertIn('"ch01_d2_knot_touch_nts": [\n            ("relationship", "sharing", 1),\n        ],', reg)
        self.assertIn('"ch01_d2_knot_touch_exhib", "ch01_d2_knot_touch_ntr", "ch01_d2_knot_touch_nts") + CH01_D2_ERRAND_EXEMPT_CHOICES', REG)

    def test_scene_consent_cg_and_knot_left_loose(self):
        body = label(A, "ch01_day2_scene_15b_knot_touch")
        order = ["scene cg ch01_d2_pool_ass_01", "scene cg ch01_d2_pool_ass_02", "Not up here.",
                 "Tell me to stop.", "scene cg ch01_d2_underwater_play_01",
                 "scene cg ch01_d2_underwater_play_02", "scene cg ch01_d2_underwater_play_03"]
        idx = [body.index(x) for x in order]
        self.assertEqual(idx, sorted(idx))
        self.assertIn("Don't you dare.", body)
        self.assertIn("loose string was still trailing", body)
        self.assertIn("jump ch01_day2_scene_16_forced_split", body)
        self.assertIn('if lc_pov_seen_in_save("d2_breakfast_julian"):', body)
        self.assertEqual(B.count('get_story_value("ch01_d2_knot_response") == "touched"'), 3)


if __name__ == "__main__":
    unittest.main()
