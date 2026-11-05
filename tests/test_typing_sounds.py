"""Name-card typing sounds: Input keeps returning its text on Enter, and every key sound exists."""
import re
import unittest
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / "game"


class TypingSoundTests(unittest.TestCase):

    def setUp(self):
        self.screen = (GAME / "screens" / "zzzzzzzz_scrapbook_ui.rpy").read_text(encoding="utf-8")
        self.system = (GAME / "systems" / "lc_typing_sounds.rpy").read_text(encoding="utf-8")

    def test_input_screen_wires_changed_and_submit(self):
        block = self.screen.split("screen input(prompt):", 1)[1].split("\nscreen ", 1)[0]
        self.assertIn("changed lc_input_typed", block)
        # A changed callback stops Input returning on Enter; the action must return the text.
        self.assertIn("action Function(lc_input_submit)", block)
        self.assertIn('on "show" action Function(lc_input_reset)', block)

    def test_submit_returns_widget_text(self):
        self.assertIn("return text", self.system)
        self.assertIn("widget.edit_text", self.system)

    def test_every_key_sound_exists(self):
        names = set(re.findall(r'"(key_[a-z0-9]+)"', self.system))
        self.assertTrue({"key_1", "key_back", "key_enter"} <= names)
        for name in names:
            self.assertTrue((GAME / "audio" / "ui" / (name + ".ogg")).is_file(), name)


if __name__ == "__main__":
    unittest.main()
