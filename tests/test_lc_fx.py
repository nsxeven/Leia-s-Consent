"""Effects foundation (systems/lc_fx.rpy) and its Prologue/Day 1 use."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
FX = (GAME / "systems" / "lc_fx.rpy").read_text(encoding="utf-8")
STORY = {
    name: (GAME / "chapters" / rel).read_text(encoding="utf-8")
    for name, rel in (
        ("prologue", "prologue.rpy"),
        ("main", "ch01/ch01_main.rpy"),
        ("s04", "ch01/ch01_scenes_04_06.rpy"),
        ("s07", "ch01/ch01_scenes_07_13.rpy"),
        ("s14", "ch01/ch01_scenes_14_30.rpy"),
    )
}


class EffectsFoundationTests(unittest.TestCase):

    def test_helpers_and_settings_exist(self):
        for name in ("def lc_shake(", "def lc_punch(", "def lc_flash(", "def lc_photo(", "def lc_sfx(",
                     "def lc_amb(", "def lc_music(", "def lc_duck(", "def lc_ui_sound(",
                     "transform lc_push_in", "transform lc_dream_sway", "screen lc_flash_overlay"):
            self.assertIn(name, FX)
        self.assertIn("default persistent.lc_screen_shake = True", FX)
        self.assertIn("default persistent.lc_camera_flash = True", FX)
        self.assertIn('register_channel("ambience", mixer="ambience"', FX)
        self.assertIn('register_channel("ui", mixer="ui"', FX)

    def test_effects_respect_the_toggles(self):
        self.assertRegex(FX, r"def lc_shake\(.*\n(.*\n){0,2}\s+if not persistent\.lc_screen_shake:\n\s+return None")
        self.assertRegex(FX, r"def lc_punch\(.*\n(.*\n){0,4}\s+if not persistent\.lc_screen_shake:\n\s+return None")
        self.assertRegex(FX, r"def lc_flash\(.*\n(.*\n){0,2}\s+if not persistent\.lc_camera_flash:\n\s+return")

    def test_preferences_expose_toggles_and_mixers(self):
        ui = (GAME / "screens" / "zzzzzzzz_scrapbook_ui.rpy").read_text(encoding="utf-8")
        prefs = ui.split("screen preferences():", 1)[1].split("\nscreen ", 1)[0]
        self.assertIn('ToggleField(persistent, "lc_screen_shake")', prefs)
        self.assertIn('ToggleField(persistent, "lc_camera_flash")', prefs)
        self.assertIn('Preference("mixer ambience volume")', prefs)
        self.assertIn('Preference("mixer ui volume")', prefs)

    def test_prologue_and_day1_use_the_setting_aware_shakes(self):
        for name, src in STORY.items():
            self.assertNotRegex(src, r"with\s+[hv]punch", name + " should use lc_shake()")
        self.assertIn('friend "Kiss [player_name]." with lc_shake("s")', STORY["prologue"])
        self.assertIn('with lc_shake("m")', STORY["s04"])  # pulled into the pool
        self.assertIn('"My eyes opened." with lc_shake("m")', STORY["s14"])

    def test_photo_and_camera_beats(self):
        self.assertIn("$ lc_photo()", STORY["main"])
        self.assertEqual(STORY["s04"].count("$ lc_photo()"), 2)
        self.assertEqual(STORY["s14"].count("at lc_dream_sway"), 3)
        for name in ("prologue", "main", "s07", "s14"):
            self.assertIn("at lc_push_in", STORY[name])


if __name__ == "__main__":
    unittest.main()
