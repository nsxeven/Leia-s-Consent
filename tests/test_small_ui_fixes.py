"""Stat tip never builds text from None; settings 'On' badge is a right-aligned pill."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SmallUiFixTests(unittest.TestCase):

    def test_stat_tip_text_never_none(self):
        src = (ROOT / "game/screens/stat_tooltip_screen.rpy").read_text(encoding="utf-8")
        self.assertNotRegex(src, r"text _last_tip\b")
        self.assertEqual(src.count('text (_last_tip or "")'), 2)

    def test_settings_on_badge_is_right_aligned_bold_pill(self):
        src = (ROOT / "game/screens/zzzzzz_phone_ios_presentation.rpy").read_text(encoding="utf-8")
        block = src.split("screen lc_phone_settings_mode(mode_id):", 1)[1].split("\nscreen ", 1)[0]
        self.assertIn("xalign 1.0", block)
        self.assertIn('Frame("gui/phone/sprite_match/pill_white.png"', block)
        self.assertIn("bold True", block)
        self.assertIn("ysize 40", block)
        self.assertNotIn("yfit True", block)
        self.assertTrue((ROOT / "game/gui/phone/sprite_match/pill_white.png").is_file())


if __name__ == "__main__":
    unittest.main()
