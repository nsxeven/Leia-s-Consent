"""Day 2 morning does not crash when Day 1 left no solo pool captures."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY2 = (ROOT / "game/chapters/ch01/ch01_day2_scenes_01_15.rpy").read_text(encoding="utf-8")
HELPER = (ROOT / "game/chapters/ch01/ch01_photo_route_phone_patch.rpy").read_text(encoding="utf-8")
DAY1 = (ROOT / "game/chapters/ch01/ch01_scenes_04_06.rpy").read_text(encoding="utf-8")


def scene(label):
    return DAY2.split("label %s:" % label, 1)[1].split("\nlabel ", 1)[0]


class Day2PoolPhotoGuardTests(unittest.TestCase):
    def test_helper_can_return_an_empty_list(self):
        self.assertIn("count = max(0, min(3, count))", HELPER)
        self.assertIn("range(1, count + 1)", HELPER)
        self.assertGreaterEqual(DAY1.count('set_story_value("ch01_pool_capture_count", 0)'), 1)

    def test_morning_guards_the_first_photo_and_has_a_selfie_fallback(self):
        source = scene("ch01_day2_scene_01_morning_after")
        self.assertIn("$ d2_morning_pool_photos = ch01_pool_capture_assets()", source)
        self.assertIn("if d2_morning_pool_photos:", source)
        self.assertIn('renpy.show("cg " + d2_morning_pool_photos[0])', source)
        self.assertEqual(source.count("d2_morning_pool_photos[0]"), 1)
        self.assertLess(
            source.index("if d2_morning_pool_photos:"),
            source.index("d2_morning_pool_photos[0]"),
        )
        # The [0] access must not appear before the guard in this label.
        self.assertNotIn("d2_morning_pool_photos[0]", source.split("if d2_morning_pool_photos:", 1)[0])
        self.assertIn("d2_morning_group_selfie", source)
        self.assertIn("ch01_photo_group_blue", source)
        self.assertIn("ch01_photo_group_white", source)
        self.assertIn('renpy.show("cg " + d2_morning_group_selfie)', source)
        self.assertIn("group selfie", source)
        self.assertLess(
            source.index("d2_morning_pool_photos[0]"),
            source.index("d2_morning_group_selfie"),
        )
        # Fallback is the else of the photos guard, not an inner photo-reaction else.
        self.assertRegex(
            source,
            re.compile(
                r"if d2_morning_pool_photos:\n"
                r".*?"
                r"\n    else:\n"
                r"        # No solo captures:.*?"
                r"d2_morning_group_selfie",
                re.S,
            ),
        )


if __name__ == "__main__":
    unittest.main()
