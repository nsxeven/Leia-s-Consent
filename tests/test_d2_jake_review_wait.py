"""Day Two Jake banter + day review 'wait' cue (darryn 2026-11-09)."""
import unittest
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / "game"


class JakeAndWaitCue(unittest.TestCase):

    def test_jake_replaces_lisbon_and_j_joke_is_name_safe(self):
        src = (GAME / "chapters/ch01/ch01_day2_scenes_16_30.rpy").read_text(encoding="utf-8")
        self.assertNotIn("Lisbon", src)
        self.assertIn("His name was Jake", src)
        self.assertIn('if friend_name[:1].upper() == "J":', src)
        block = src.split('if friend_name[:1].upper() == "J":', 1)[1].split("set_story_flag", 1)[0]
        self.assertIn("else:", block)  # renamed Julian still gets a line that makes sense

    def test_early_continue_plays_wait_cue(self):
        src = (GAME / "screens/day_review_screen.rpy").read_text(encoding="utf-8")
        self.assertIn('action If(animating, Function(lc_ui_play, "tock"), leave)', src)
        self.assertTrue((GAME / "audio/ui/tock.ogg").exists())


if __name__ == "__main__":
    unittest.main()
