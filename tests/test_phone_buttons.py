"""Every phone textbutton uses the shared phone button format (darryn 2026-11-08)."""
import re
import unittest
from pathlib import Path

PHONE = (Path(__file__).resolve().parents[1] / "game/screens/zzzzzz_phone_ios_presentation.rpy").read_text(encoding="utf-8")


class PhoneButtonTests(unittest.TestCase):

    def test_styles_centre_the_label(self):
        text = PHONE.split("style lc_phone_btn_text is lc_sw_hand:", 1)[1].split("\nstyle ", 1)[0]
        for prop in ("xalign 0.5", "yalign 0.5", "text_align 0.5", "size 24"):
            self.assertIn(prop, text)
        self.assertIn("ysize 52", PHONE.split("style lc_phone_btn is lc_sw_hit:", 1)[1].split("\nstyle ", 1)[0])

    def test_every_textbutton_uses_a_phone_style(self):
        blocks = re.findall(r"textbutton [^\n]+:\n((?:\s+[^\n]*\n){1,3})", PHONE)
        self.assertGreaterEqual(len(blocks), 6)
        for b in blocks:
            self.assertRegex(b, r'style "lc_phone_btn(_primary)?"')
        self.assertNotIn("text_idle_color", PHONE)


if __name__ == "__main__":
    unittest.main()
