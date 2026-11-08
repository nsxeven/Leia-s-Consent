"""Three text looks: dialogue, tinted narration, italic thoughts (darryn 2026-11-08)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UI = (ROOT / "game/screens/zzzzzzzz_scrapbook_ui.rpy").read_text(encoding="utf-8")
CHARS = (ROOT / "game/characters.rpy").read_text(encoding="utf-8")


class TextStyleTests(unittest.TestCase):

    def test_think_speaker(self):
        self.assertIn("define think = Character(None, show_think=True)", CHARS)

    def test_say_screen_styles(self):
        say = UI.split("screen say(who, what, think=False):", 1)[1].split("\nscreen ", 1)[0]
        self.assertIn("italic think", say)
        self.assertIn("color text_ink", say)
        self.assertIn("LC_NARRATION_INK[theme] if (who is None and not think) else ink", say)
        self.assertIn('define LC_NARRATION_INK = {"day": ', UI)


if __name__ == "__main__":
    unittest.main()
