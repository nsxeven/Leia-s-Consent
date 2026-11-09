"""Title-screen Leia touch reactions (darryn 2026-11-09)."""
import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "game/python-packages"))
import lc_title_touch as tt  # noqa: E402

TITLE = (ROOT / "game/screens/title_screen.rpy").read_text(encoding="utf-8")
CUSTOM = (ROOT / "game/systems/title_customiser.rpy").read_text(encoding="utf-8")
TOUCH = (ROOT / "game/systems/lc_title_touch.rpy").read_text(encoding="utf-8")


class Rnd(object):
    def random(self):
        return 0.1

    def choice(self, seq):
        return seq[0]


def clicks(region, n, mature, gap=0.6, start=100.0):
    state = tt.new_state()
    out = []
    for i in range(n):
        out.append(tt.plan(state, region, start + i * gap, mature, Rnd()))
    return out


class TitleTouchTests(unittest.TestCase):

    def test_transform_matches_title_screen(self):
        self.assertIn("zoom %s" % tt.TITLE_ZOOM, TITLE)
        self.assertIn("xcenter %d" % tt.TITLE_XCENTER, TITLE)
        self.assertIn("ypos %d" % tt.TITLE_BOTTOM, TITLE)

    def test_regions(self):
        self.assertEqual(tt.region_at(420, 230), "head")
        self.assertEqual(tt.region_at(540, 500), "chest")
        self.assertEqual(tt.region_at(515, 890), "private")
        self.assertEqual(tt.region_at(480, 1300), "body")
        # Screen mapping round-trip: the canvas centre lands at the title xcenter.
        cx, cy = tt.screen_to_canvas(tt.TITLE_XCENTER, tt.TITLE_BOTTOM)
        self.assertAlmostEqual(cx, tt.CANVAS[0] / 2.0, places=3)
        self.assertAlmostEqual(cy, tt.CANVAS[1], places=3)

    def test_head_and_body_are_never_lewd(self):
        for region in ("head", "body"):
            for mature in (False, True):
                for r in clicks(region, 6, mature):
                    self.assertIsNone(r["lewd"])
                    self.assertFalse(r["jiggle"])
                    self.assertNotEqual(r["face"], "ahegao")
                    self.assertEqual(r["voice"][0], "sfx")

    def test_mature_ladder_then_pout(self):
        faces = [r["face"] for r in clicks("private", 5, True)]
        self.assertEqual(faces, ["shy", "flustered", "flustered", "ahegao", "pout"])
        rs = clicks("private", 4, True)
        self.assertTrue(all(r["lewd"] in tt.WET_SOUNDS for r in rs))
        self.assertEqual([r["voice"] for r in rs], [("moan", 1), ("moan", 2), ("moan", 3), ("moan", 4)])
        chest = clicks("chest", 4, True)
        self.assertTrue(all(r["jiggle"] for r in chest))
        self.assertIsNone(chest[0]["lewd"])

    def test_sfw_never_lewd(self):
        rs = clicks("private", 6, False) + clicks("chest", 6, False)
        for r in rs:
            if r is None:
                continue
            self.assertIsNone(r["lewd"])
            self.assertFalse(r["jiggle"])
            self.assertNotEqual(r["face"], "ahegao")
            self.assertNotEqual(r["voice"] and r["voice"][0], "moan")
        faces = [r["face"] for r in clicks("chest", 4, False)]
        self.assertEqual(faces, ["shy", "shy", "flustered", "pout"])

    def test_pout_bubble_and_cooldown(self):
        state = tt.new_state()
        rs = [tt.plan(state, "chest", 10 + i * 0.6, True, Rnd()) for i in range(5)]
        self.assertEqual(rs[-1]["bubble"], tt.POUT_LINE)
        during = tt.plan(state, "chest", 10 + 5 * 0.6, True, Rnd())
        self.assertEqual(during["face"], "pout")
        self.assertIsNone(during["voice"])
        after = tt.plan(state, "chest", 10 + 4 * 0.6 + tt.COOLDOWN + 3.0, True, Rnd())
        self.assertEqual(after["face"], "shy")

    def test_streak_resets_and_click_spam_ignored(self):
        state = tt.new_state()
        tt.plan(state, "private", 1.0, True, Rnd())
        self.assertIsNone(tt.plan(state, "private", 1.1, True, Rnd()))
        again = tt.plan(state, "private", 1.0 + tt.STREAK_GAP + 1, True, Rnd())
        self.assertEqual(again["face"], "shy")

    def test_faces_exist_and_settle(self):
        ids = set(e for e in ("smile", "shy", "flustered", "pout", "ahegao"))
        for i in ids:
            self.assertIn('("%s",' % i, CUSTOM)
        live = tt.new_live()
        tt.apply(live, clicks("head", 1, False)[0], 5.0)
        self.assertIsNotNone(tt.current_face(live, 5.5))
        self.assertIsNone(tt.current_face(live, 5.0 + tt.HOLD + 0.01))

    def test_motion_settles(self):
        for kind in ("hop", "tilt", "flinch", "chest", "squirm", "shake"):
            self.assertEqual(tt.body_offset(kind, 3.0), (0.0, 0.0))
            moved = max(abs(v) for t in range(1, 30) for v in tt.body_offset(kind, t / 100.0))
            self.assertGreater(moved, 1.0, kind)
        self.assertEqual(tt.chest_offset(True, 2.0), 0.0)
        self.assertEqual(tt.chest_offset(False, 0.1), 0.0)

    def test_wiring(self):
        self.assertIn("use lc_title_touch_area()", TITLE)
        self.assertIn("lc_title_face_disp(face)", CUSTOM)
        self.assertIn("lc_title_touch_chest(At(o[\"chest\"], lc_title_chest_breathe))", CUSTOM)
        self.assertIn("lc_title_touch_body(", CUSTOM)
        self.assertIn("focus_mask lc_title_touch_mask()", TOUCH)
        self.assertIn("action Function(lc_title_touch)", TOUCH)
        self.assertIn("lc_title_show_mature()", TOUCH)
        for clip in ("leia_giggle", "leia_laugh", "leia_kiss", "leia_gasp", "leia_grunt"):
            self.assertTrue((ROOT / "game/audio/voice/leia" / (clip + ".ogg")).exists(), clip)
        for w in tt.WET_SOUNDS:
            self.assertTrue((ROOT / "game/audio/lewd" / (w + ".ogg")).exists(), w)


if __name__ == "__main__":
    unittest.main()
