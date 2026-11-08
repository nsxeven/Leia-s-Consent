"""Reply tray options grow for two-line replies (darryn 2026-11-08)."""
import unittest
from pathlib import Path

PHONE = (Path(__file__).resolve().parents[1] / "game/screens/zzzzzz_phone_ios_presentation.rpy").read_text(encoding="utf-8")


class PhoneReplyWrapTests(unittest.TestCase):

    def test_reply_buttons_not_fixed_height(self):
        tray = PHONE.split('for reply_option in reply_prompt["options"]:', 1)[1].split("text \"+\"", 1)[0]
        self.assertIn("yminimum 58", tray)
        self.assertNotIn("ysize 58", tray)

    def test_tray_grows_upward(self):
        self.assertIn("ypos 891\n                    yanchor 1.0", PHONE)


if __name__ == "__main__":
    unittest.main()
