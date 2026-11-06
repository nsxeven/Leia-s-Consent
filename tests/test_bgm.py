"""BGM themes (darryn's plan): files, credits, game-wide cues, silences and cuts."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
CH = GAME / "chapters" / "ch01"
THEMES = ("party", "polaroid_summer", "cozy_home", "sunny_island", "cheeky",
          "lounge_piano", "warm_night", "under_blanket", "quiet_thoughts")


def src(path):
    return path.read_text(encoding="utf-8")


class BgmTests(unittest.TestCase):
    def test_every_theme_has_a_file_and_credit(self):
        credits = src(GAME / "audio" / "CREDITS.md")
        manifest = src(GAME / "audio" / "manifest.json")
        for t in THEMES:
            self.assertTrue((GAME / "audio" / "music" / (t + ".ogg")).is_file(), t)
            self.assertIn("music/" + t, credits)
            self.assertIn('"music/%s"' % t, manifest)
        json.loads(manifest)

    def test_helpers_return_none_and_remember_theme(self):
        fx = src(GAME / "systems" / "lc_fx.rpy")
        for name in ("lc_bgm", "lc_bgm_cut", "lc_bgm_hush", "lc_bgm_resume", "lc_bgm_stop"):
            self.assertIn("def %s(" % name, fx)
        self.assertIn("default lc_bgm_current = None", fx)

    def test_title_menu_and_default_volume(self):
        opts = src(GAME / "options.rpy")
        self.assertIn('define config.main_menu_music = "audio/music/polaroid_summer.ogg"', opts)
        self.assertIn("define config.default_music_volume = 0.6", opts)

    def test_story_cues(self):
        prologue = src(GAME / "chapters" / "prologue.rpy")
        self.assertIn('lc_bgm("party")', prologue)
        self.assertIn('lc_bgm("cozy_home")', prologue)
        self.assertLess(prologue.index("lc_bgm_cut()"), prologue.index('lc_sfx("record_scratch")'))
        self.assertIn('lc_bgm("sunny_island")', src(CH / "ch01_main.rpy"))
        pool = src(CH / "ch01_scenes_04_06.rpy")
        self.assertIn('lc_bgm("cheeky")', pool)
        self.assertLess(pool.index("lc_bgm_cut()"), pool.index('lc_sfx("record_scratch")'))
        evening = src(CH / "ch01_scenes_07_13.rpy")
        for cue in ('lc_bgm("cozy_home")', 'lc_bgm("lounge_piano")', 'lc_bgm("warm_night")', "lc_duck(0.35)"):
            self.assertIn(cue, evening)
        self.assertNotIn("lc_music_stop()", evening)
        night = src(CH / "ch01_scenes_14_30.rpy")
        for cue in ('lc_bgm("under_blanket"', 'lc_bgm("quiet_thoughts"', "lc_bgm_hush()", "lc_bgm_hush(1.5)"):
            self.assertIn(cue, night)
        grab = night.index("scene cg ch01_movie_ass_grab_01")
        self.assertLess(grab, night.index("lc_bgm_hush()"))
        self.assertLess(night.index("lc_bgm_hush(1.5)"), night.index('if lc_dream_presentation == "summary":'))
        review = src(GAME / "systems" / "day_review.rpy")
        self.assertIn('lc_bgm("polaroid_summer"', review)
        self.assertIn("lc_bgm_stop(2.5)", review)


if __name__ == "__main__":
    unittest.main()
