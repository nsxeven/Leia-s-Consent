"""Group events show as centred blue system pills (darryn 2026-11-08)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHONE = (ROOT / "game/screens/zzzzzz_phone_ios_presentation.rpy").read_text(encoding="utf-8")


class PhoneSystemMessageTests(unittest.TestCase):

    def test_system_rows_are_centred_pills(self):
        block = PHONE.split('if _sender == "system":', 1)[1].split("else:", 1)[0]
        self.assertIn("xalign 0.5", block)
        self.assertIn("key.png", block)
        self.assertNotIn("lc_phone_avatar", block)

    def test_group_events_use_system_sender(self):
        src = ((ROOT / "game/chapters/ch01/ch01_scenes_04_06.rpy").read_text(encoding="utf-8")
               + (ROOT / "game/chapters/ch01/ch01_day2_scenes_01_15.rpy").read_text(encoding="utf-8"))
        self.assertEqual(src.count('"system", text='), 3)
        self.assertIn('" changed the group picture."', src)
        self.assertNotIn("Changed the group picture to", src)


if __name__ == "__main__":
    unittest.main()
