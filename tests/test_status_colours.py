"""Status colours by stat meaning, icons on both Status screens (darryn 2026-11-09)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISP = (ROOT / "game/systems/status_display.rpy").read_text(encoding="utf-8")
OPT = (ROOT / "game/screens/status_screen.rpy").read_text(encoding="utf-8")
PHONE = (ROOT / "game/screens/zzzzzz_phone_ios_presentation.rpy").read_text(encoding="utf-8")
GEN = (ROOT / "tools/gen_glass_menu_ui.py").read_text(encoding="utf-8")
ICONS = (ROOT / "tools/gen_sprite_match_ui.py").read_text(encoding="utf-8")
STATS = ("love", "trust", "exhibitionism", "temptation", "sharing")


class StatusColourTests(unittest.TestCase):

    def test_bar_art_exists_per_stat(self):
        for s in STATS:
            self.assertTrue((ROOT / ("game/gui/glass/stat_%s.png" % s)).is_file(), s)
            self.assertIn('"%s": {"ink": ' % s, DISP)
        self.assertTrue((ROOT / "game/gui/glass/stat_track.png").is_file())

    def test_icons_match_bars(self):
        bars = GEN.split("STAT_BARS = {", 1)[1].split("}", 1)[0]
        for s in STATS:
            colours = bars.split('"%s": ' % s, 1)[1].split(")", 1)[0] + ")"
            self.assertIn('"%s": %s' % (s, colours), ICONS)

    def test_options_status_uses_glass_bars(self):
        self.assertIn('Frame("gui/glass/stat_{}.png".format(lc_status_colour_stat(row)), 10, 10)', OPT)
        self.assertNotIn("bar_love.png", OPT)
        self.assertIn('LC_STATUS_SECTION_INK["ryan"]', OPT)

    def test_phone_status_has_icons_and_tints(self):
        row = PHONE.split("screen lc_phone_status_row(row):", 1)[1].split("\nscreen ", 1)[0]
        self.assertIn("images/ui/scrapbook/icon_{}.png", row)
        self.assertIn('LC_STAT_COLOUR[_cs]["phone"]', row)
        self.assertNotIn("#3D8FD4", row)

    def test_lean_row_uses_route_colour(self):
        self.assertIn('"bar_stat": driver', DISP)


    def test_bar_art_is_opaque_inside(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow not installed")
        for s in STATS:
            im = Image.open(ROOT / ("game/gui/glass/stat_%s.png" % s)).convert("RGBA")
            self.assertEqual(im.getpixel((12, 6))[3], 255, s)   # the shine band
            self.assertEqual(im.getpixel((12, 12))[3], 255, s)


    def test_line_icons_own_the_live_stats(self):
        gen = (ROOT / "tools/gen_stat_icons.py").read_text(encoding="utf-8")
        for s in STATS:
            self.assertIn('"%s": ' % s, gen)
        self.assertIn("if name in LINE_ICON_STATS:", ICONS)


if __name__ == "__main__":
    unittest.main()
