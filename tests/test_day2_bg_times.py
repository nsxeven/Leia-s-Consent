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
        scenes = label_scenes(CH01 / "day2" / "ch01_day2_scenes_01_15.rpy", "ch01_day2_scene_01_morning_after")
        self.assertTrue(scenes)
        for bg in scenes:
            self.assertNotRegex(bg, r"evening|night", bg)

    def test_after_sunset_bedroom_uses_night_art(self):
        f = CH01 / "day2" / "ch01_day2_scenes_16_30.rpy"
        for label in ("ch01_day2_scene_21_pre_sunset", "ch01_day2_scene_30_bedroom", "ch01_day2_scene_30_love",
                      "ch01_day2_scene_30_exhibition", "ch01_day2_scene_30_ntr_nightmare"):
            scenes = label_scenes(f, label)
            self.assertTrue(scenes, label)
            for bg in scenes:
                if bg.startswith("ch01_d2_"):
                    continue  # placeholders
                self.assertIn("night", bg, "%s uses %s" % (label, bg))

    def test_leia_errand_uses_day_art(self):
        f = CH01 / "day2" / "ch01_day2_leia_errand.rpy"
        labels = re.findall(r"^label (\w+):", f.read_text(encoding="utf-8"), re.M)
        self.assertIn("ch01_day2_errand_shop", labels)
        used = set()
        for label in labels:
            for bg in label_scenes(f, label):
                used.add(bg)
                self.assertNotRegex(bg, r"evening|night", "%s uses %s" % (label, bg))
                # Single-variant night art (skill note): the night shop and the night roadside.
                self.assertNotIn(bg, ("ch01_conveniencestore", "ch01_roadside"), label)
        self.assertIn("ch01_shop_day", used)       # K2: darryn's daytime shop (placeholder until rendered)
        self.assertIn("ch01_d2_island_day", used)  # the walks


if __name__ == "__main__":
    unittest.main()
