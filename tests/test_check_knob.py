"""Toggle knob sits inside the honey outline (darryn 2026-11-09)."""
import unittest
from pathlib import Path

UI = (Path(__file__).resolve().parents[1] / "game/screens/zzzzzzzz_scrapbook_ui.rpy").read_text(encoding="utf-8")


class CheckKnobTests(unittest.TestCase):

    def test_knob_inset(self):
        self.assertIn('define LC_CHECK_KNOB_OFF = Transform("gui/scrapbook/check_off.png", xpos=5, yalign=0.5)', UI)
        style = UI.split("style lc_check_button is button:", 1)[1].split("\nstyle ", 1)[0]
        self.assertIn("foreground LC_CHECK_KNOB_OFF", style)
        self.assertIn("padding (46, 2, 10, 2)", style)


if __name__ == "__main__":
    unittest.main()
