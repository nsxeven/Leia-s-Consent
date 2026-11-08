"""Phone home icons lift only themselves on hover (darryn 2026-11-08)."""
import unittest
from pathlib import Path

PHONE = (Path(__file__).resolve().parents[1] / "game/screens/zzzzzz_phone_ios_presentation.rpy").read_text(encoding="utf-8")


class PhoneIconHoverTests(unittest.TestCase):

    def test_no_shared_hover_variable(self):
        self.assertNotIn("hovered_app", PHONE)
        self.assertGreaterEqual(PHONE.count("at lc_lift"), 2)


if __name__ == "__main__":
    unittest.main()
