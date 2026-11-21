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

    def test_route_subtitles(self):
        vals = {"ch01_d2_route_lane_post_pool": None}
        get = lambda k, d=None: vals.get(k, d)
        self.assertEqual(lc_chapters.part_title("day2", 1, get), ("Morning", ""))
        self.assertEqual(lc_chapters.part_title("day2", 2, get), ("The Pool", ""))
        self.assertEqual(lc_chapters.part_title("day2", 3, get), ("Evening", ""))  # old saves: neutral
        for lane, sub in (("love", "Just Us"), ("exhibitionism", "Showing Off"), ("ntr_risk", "Somewhere Else")):
            vals["ch01_d2_route_lane_post_pool"] = lane
            self.assertEqual(lc_chapters.part_title("day2", 3, get), ("Evening", sub))
        self.assertEqual(lc_chapters.part_save_name("day2", "Evening", "Just Us"),
                         lc_chapters.save_name("day2") + " \u00b7 Evening: Just Us")
        src = (D2 / "ch01_day2_scenes_16_30.rpy").read_text(encoding="utf-8")
        self.assertLess(src.index('set_story_value("ch01_d2_route_lane_post_pool"'), src.index('call lc_part_card("day2", 3)'))

    def test_three_parts_in_order(self):
        src = (D2 / "ch01_day2_scenes_01_15.rpy").read_text(encoding="utf-8") + \
              (D2 / "ch01_day2_scenes_16_30.rpy").read_text(encoding="utf-8")
        marks = ['call lc_chapter_card("day2")', 'call lc_part_card("day2", 1)', "label ch01_day2_scene_01_morning_after:",
                 'call lc_part_card("day2", 2)', "label ch01_day2_scene_13_girls_upstairs:",
                 'call lc_part_card("day2", 3)', "label ch01_day2_scene_19_change_for_evening:"]
        idx = [src.index(m) for m in marks]
        self.assertEqual(idx, sorted(idx))


class Cards(unittest.TestCase):
    def test_cards_animate_and_skip(self):
        src = (ROOT / "game/screens/lc_title_cards.rpy").read_text(encoding="utf-8")
        for name in ("label lc_chapter_card(chapter_id):", "label lc_part_card(chapter_id, number):",
                     "transform lc_polaroid_motion:", "transform lc_ticket_motion:", "on show:", "on hide:"):
            self.assertIn(name, src)
        self.assertIn("$ lc_part_begin(chapter_id, number, _lc_part[0], _lc_part[1])", src)
        self.assertNotIn("hard=True)\n    hide", src)  # the hold is click-skippable


if __name__ == "__main__":
    unittest.main()
