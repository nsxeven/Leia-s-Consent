"""The game draws its own animated Sparkle cursor (darryn 2026-11-08, draft E)."""
import unittest
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / "game"
SRC = (GAME / "systems" / "lc_cursor.rpy").read_text(encoding="utf-8")


class CursorTests(unittest.TestCase):

    def test_sparkle_cursor_installed_off_touch(self):
        self.assertIn("config.mouse_displayable = LCCursor()", SRC)
        self.assertIn('if not renpy.variant("touch")', SRC)
        for name in ("sparkle_idle.png", "sparkle_hover.png", "sparkle_twin.png", "sparkle_mote.png"):
            self.assertTrue((GAME / "gui" / "cursor" / name).is_file(), name)

    def test_hotspot_is_centre_and_hover_eases(self):
        self.assertIn('"sparkle_idle.png", 22, 22)', SRC)
        self.assertIn("LC_HOVER_IN", SRC)
        self.assertIn("LC_HOVER_OUT", SRC)
        self.assertIn("renpy.redraw(self, 0)", SRC)

    def test_no_rollback_tracked_state_per_frame(self):
        self.assertIn("self.trail = python_list()", SRC)
        self.assertNotIn("self.trail = []", SRC)

    def test_nothing_else_overrides_the_mouse(self):
        for path in GAME.rglob("*.rpy"):
            if path.name == "lc_cursor.rpy" or "tl" in path.parts:
                continue
            src = path.read_text(encoding="utf-8")
            self.assertNotIn("config.mouse_displayable", src, path.name)
            self.assertNotIn("config.mouse =", src, path.name)


if __name__ == "__main__":
    unittest.main()
