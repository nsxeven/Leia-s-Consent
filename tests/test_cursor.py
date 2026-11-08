"""The game draws its own themed cursor so it shows in fullscreen (darryn)."""
import unittest
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / "game"


class CursorTests(unittest.TestCase):

    def test_software_cursor_with_hover_variant(self):
        src = (GAME / "systems" / "lc_cursor.rpy").read_text(encoding="utf-8")
        self.assertIn("config.mouse_displayable = LCCursor(", src)
        self.assertIn('"button", "gui/scrapbook/cursor_button.png"', src)
        self.assertIn('if not renpy.variant("touch")', src)
        for name in ("cursor.png", "cursor_button.png"):
            self.assertTrue((GAME / "gui" / "scrapbook" / name).is_file(), name)

    def test_nothing_else_overrides_the_mouse(self):
        for path in GAME.rglob("*.rpy"):
            if path.name == "lc_cursor.rpy" or "tl" in path.parts:
                continue
            src = path.read_text(encoding="utf-8")
            self.assertNotIn("config.mouse_displayable", src, path.name)
            self.assertNotIn("config.mouse =", src, path.name)


if __name__ == "__main__":
    unittest.main()
