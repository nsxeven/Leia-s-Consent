"""Day Two opening: Julian's 11:00 wake-up text + the two sleeping CGs (darryn 2026-11-09)."""
import unittest
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / "game"


class DayTwoWakeUp(unittest.TestCase):

    def test_cgs_defined_shown_and_in_gallery(self):
        vis = (GAME / "chapters/ch01/ch01_day2_visuals.rpy").read_text(encoding="utf-8")
        scene = (GAME / "chapters/ch01/ch01_day2_scenes_01_15.rpy").read_text(encoding="utf-8")
        gal = (GAME / "systems/gallery_data.rpy").read_text(encoding="utf-8")
        for name, n in (("ch01_d2_leia_sleeping", "01"), ("ch01_d2_leia_waking", "02")):
            self.assertIn("image cg %s = " % name, vis)
            self.assertIn("CH2D2_CG_LeiaSleeping_%s.webp" % n, vis)
            self.assertTrue((GAME / ("images/cg/ch02/CH2D2_CG_LeiaSleeping_%s.webp" % n)).exists())
            self.assertIn("scene cg " + name, scene)
            self.assertIn('"%s"' % name, gal)

    def test_julian_wake_text_at_eleven_before_the_cgs(self):
        scene = (GAME / "chapters/ch01/ch01_day2_scenes_01_15.rpy").read_text(encoding="utf-8")
        body = scene.split("label ch01_day2_scene_01_morning_after:", 1)[1]
        self.assertLess(body.index('text="Bro wake up"'), body.index("scene cg ch01_d2_leia_sleeping"))
        self.assertLess(body.index("scene cg ch01_d2_leia_sleeping"), body.index("scene cg ch01_d2_leia_waking"))
        self.assertIn("11:00", body.split("scene cg ch01_d2_leia_sleeping", 1)[0])
    def test_wake_scene_stages_and_clears_cast_and_story_time(self):
        scene = (GAME / "chapters/ch01/ch01_day2_scenes_01_15.rpy").read_text(encoding="utf-8")
        body = scene.split("label ch01_day2_scene_01_morning_after:", 1)[1]
        self.assertIn('$ cast(ryan="home", leia="lounge")', body)
        self.assertIn('$ cast_remove("leia")', body)
        self.assertIn('$ lc_phone_clear_story_time()', body)
        self.assertIn('$ cast()', body)


if __name__ == "__main__":
    unittest.main()
