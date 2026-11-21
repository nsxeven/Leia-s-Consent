"""Day Two parts: Morning / The Pool / Evening title cards (darryn 2026-11-19). Display only."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "game/python-packages"))
import lc_chapters  # noqa: E402

D2 = ROOT / "game/chapters/ch01/day2"


class Parts(unittest.TestCase):
    def test_card_and_save_name(self):
        card = lc_chapters.part_card_text("day2", 2, "The Pool")
        self.assertIn("DAY TWO", card)
        self.assertIn("PART TWO", card)
        self.assertIn("THE POOL", card)
        self.assertEqual(lc_chapters.part_save_name("day2", "The Pool"),
                         lc_chapters.save_name("day2") + " \u00b7 The Pool")

    def test_three_parts_in_order(self):
        src = (D2 / "ch01_day2_scenes_01_15.rpy").read_text(encoding="utf-8") + \
              (D2 / "ch01_day2_scenes_16_30.rpy").read_text(encoding="utf-8")
        marks = ['lc_part_begin("day2", 1, "Morning")', "label ch01_day2_scene_01_morning_after:",
                 'lc_part_begin("day2", 2, "The Pool")', "label ch01_day2_scene_13_girls_upstairs:",
                 'lc_part_begin("day2", 3, "Evening")', "label ch01_day2_scene_19_change_for_evening:"]
        idx = [src.index(m) for m in marks]
        self.assertEqual(idx, sorted(idx))


if __name__ == "__main__":
    unittest.main()
