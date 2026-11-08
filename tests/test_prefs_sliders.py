"""Prefs page: scrolls; sliders aligned (darryn 2026-11-08)."""
import unittest
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
UI = (ROOT / "game/screens/zzzzzzzz_scrapbook_ui.rpy").read_text(encoding="utf-8")


def screen(name):
    return UI.split("screen %s(" % name, 1)[1].split("\nscreen ", 1)[0]


class PrefsSliderTests(unittest.TestCase):

    def test_page_scrolls(self):
        prefs = screen("preferences")
        self.assertIn('id "lc_prefs_vp"', prefs)
        self.assertIn("mousewheel True", prefs)

    def test_thumb_centred_and_art_matches_thumb_height(self):
        row = screen("lc_pref_slider")
        self.assertIn("thumb_offset 15", row)
        thumb = Image.open(ROOT / "game/gui/glass/slider_thumb.png").size
        for name in ("bar_track", "bar_honey", "bar_amber", "bar_peach", "bar_pink"):
            self.assertEqual(Image.open(ROOT / "game/gui/glass" / (name + ".png")).size[1], thumb[1], name)
        self.assertEqual(int(row.split("thumb_offset ", 1)[1].split()[0]) * 2, thumb[0])

    def test_readout_is_slider_position_and_fixed_width(self):
        row = screen("lc_pref_slider")
        self.assertIn("preferences.get_mixer(mixer)", row)
        self.assertNotIn('get_volume("', screen("preferences"))
        self.assertIn("fixed:\n                xsize 72\n                ysize 30", row)

    def test_mute_and_test_buttons_per_channel(self):
        row = screen("lc_pref_slider")
        self.assertIn('Preference("mixer %s mute" % mixer, "toggle")', row)
        self.assertIn("lc_glass_sound_test, sample", row)
        prefs = screen("preferences")
        for kind, mixer in (("bgm", "music"), ("sfx", "sfx"), ("voice", "voice"), ("lewd", "lewd")):
            self.assertIn('"%s", "%s")' % (kind, mixer), prefs)
        for name in ("mute_on", "mute_off", "mute_on_hover", "mute_off_hover"):
            self.assertTrue((ROOT / "game/gui/glass" / (name + ".png")).is_file(), name)


if __name__ == "__main__":
    unittest.main()
