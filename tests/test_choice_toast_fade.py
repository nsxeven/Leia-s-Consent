"""Stat-change toast fades out as well as in (darryn 2026-11-09)."""
import unittest
from pathlib import Path

UI = (Path(__file__).resolve().parents[1] / "game/screens/zzzzzzzz_scrapbook_ui.rpy").read_text(encoding="utf-8")


class ChoiceToastFadeTests(unittest.TestCase):

    def test_showif_keeps_card_for_hide(self):
        scr = UI.split("screen choice_feedback_overlay():", 1)[1].split("\nscreen ", 1)[0]
        self.assertIn("default _last_choice_toast = None", scr)
        self.assertIn("showif _runtime.payload:", scr)
        self.assertIn("frame at gameplay_toast_appear:", scr.split("showif _runtime.payload:", 1)[1])
        self.assertIn("timer 3.20 action Function(clear_choice_feedback", scr)


if __name__ == "__main__":
    unittest.main()
