"""Phone stat tip + settings button polish (darryn 2026-11-08)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TIP = (ROOT / "game/screens/stat_tooltip_screen.rpy").read_text(encoding="utf-8")
PHONE = (ROOT / "game/screens/zzzzzz_phone_ios_presentation.rpy").read_text(encoding="utf-8")


class PhoneTipPolishTests(unittest.TestCase):

    def test_tip_keeps_last_rect_so_hide_fade_plays(self):
        self.assertIn('GetFocusRect("tooltip")', TIP)
        self.assertIn("rect _last_rect", TIP)
        self.assertNotIn('focus "tooltip"', TIP)
        self.assertIn("on hide:", TIP)

    def test_phone_tip_on_theme_and_compact(self):
        self.assertIn("tip_card.png", TIP)
        self.assertNotIn("key_berry", TIP)
        self.assertIn('"phone": (None, 176)', TIP)
        self.assertTrue((ROOT / "game/gui/phone/sprite_match/tip_card.png").is_file())

    def test_open_settings_label_centred(self):
        block = PHONE.split('textbutton "Open settings":', 1)[1].split("action", 1)[0]
        # Centred via the shared phone button style (test_phone_buttons.py).
        self.assertIn('style "lc_phone_btn"', block)


if __name__ == "__main__":
    unittest.main()
