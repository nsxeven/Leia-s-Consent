"""Day 2 backgrounds follow the time of day (darryn): day art in the morning, night art after sunset."""
import re
import unittest
from pathlib import Path

CH01 = Path(__file__).resolve().parents[1] / "game" / "chapters" / "ch01"


def label_scenes(path, label):
    src = path.read_text(encoding="utf-8")
    body = src.split("label %s:" % label, 1)[1].split("\nlabel ", 1)[0]
    return re.findall(r"^\s*scene bg (\w+)", body, re.M)


class Day2BackgroundTimeTests(unittest.TestCase):

    def test_morning_uses_day_art(self):
        scenes = label_scenes(CH01 / "ch01_day2_scenes_01_15.rpy", "ch01_day2_scene_01_morning_after")
        self.assertTrue(scenes)
        for bg in scenes:
            self.assertNotRegex(bg, r"evening|night", bg)

    def test_after_sunset_bedroom_uses_night_art(self):
        f = CH01 / "ch01_day2_scenes_16_30.rpy"
        for label in ("ch01_day2_scene_21_pre_sunset", "ch01_day2_scene_30_bedroom", "ch01_day2_scene_30_love",
                      "ch01_day2_scene_30_exhibition", "ch01_day2_scene_30_ntr_nightmare"):
            scenes = label_scenes(f, label)
            self.assertTrue(scenes, label)
            for bg in scenes:
                if bg.startswith("ch01_d2_"):
                    continue  # placeholders
                self.assertIn("night", bg, "%s uses %s" % (label, bg))


if __name__ == "__main__":
    unittest.main()
