"""Golden Hour glass Status content lanes (static screen contract)."""
import re
import unittest
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "game/screens/status_screen.rpy").read_text(encoding="utf-8")
ART = ROOT / "game/gui/glass/panel.png"


def constant(name):
    match = re.search(r"^define " + name + r" = (\d+)", SOURCE, re.M)
    assert match is not None, name
    return int(match.group(1))


class StatusTwoPageTests(unittest.TestCase):
    def test_content_lanes_stay_inside_their_pages(self):
        with Image.open(ART) as art:
            self.assertEqual(art.size, (96, 96))
        left = constant("LC_STATUS_LEFT_X")
        left_end = left + constant("LC_STATUS_LEFT_W")
        right = constant("LC_STATUS_RIGHT_X")
        right_end = right + constant("LC_STATUS_RIGHT_W")
        self.assertGreaterEqual(left, 375)
        self.assertLessEqual(left_end, 1090)  # glass content left lane
        self.assertGreaterEqual(right, 1100)
        self.assertLessEqual(right_end, 1850)  # glass content right edge
        self.assertLessEqual(constant("LC_STATUS_BODY_Y") + constant("LC_STATUS_BODY_H"), 950)
        self.assertIn("xsize (LC_STATUS_LEFT_W - 28)", SOURCE)
        self.assertIn("xsize (LC_STATUS_RIGHT_W - 28)", SOURCE)

    def test_cards_and_scrolls_live_on_the_intended_pages(self):
        screen = SOURCE.split("screen status_screen(return_to=None):", 1)[1]
        left, right = screen.split("    # Right page: mode and close", 1)
        self.assertIn('use status_section("RELATIONSHIP", relationship_rows,', left)
        self.assertIn('if route_rows:', left)
        self.assertIn('use status_section("ROUTE LEAN", route_rows,', left)
        self.assertNotIn('use status_section(girlfriend_name.upper()', left)
        self.assertNotIn('use status_section(player_name.upper()', left)
        self.assertIn('text "[girlfriend_name] right now"', right)
        self.assertIn('use status_section(girlfriend_name.upper(), leia_rows,', right)
        self.assertIn('use status_section(player_name.upper(), ryan_rows,', right)
        self.assertEqual(screen.count('scrollbars "vertical"'), 2)
        self.assertEqual(screen.count('ysize LC_STATUS_BODY_H'), 2)
        self.assertIn('if current_choice_mode() != "normal":', SOURCE)
        self.assertIn('use lc_stat_tip(GetTooltip("status_screen"))', right)


if __name__ == "__main__":
    unittest.main()
