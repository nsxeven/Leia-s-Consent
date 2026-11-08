"""Phone wallpaper: crop maths, save format and screen wiring (darryn 2026-11-09)."""
import unittest
from pathlib import Path

import lc_wallpaper_crop as wp

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
PHONE = (GAME / "screens" / "zzzzzz_phone_ios_presentation.rpy").read_text(encoding="utf-8")
WALL = (GAME / "screens" / "zzzzzz_phone_wallpaper.rpy").read_text(encoding="utf-8")
ART = GAME / "gui" / "phone" / "sprite_match"

SW, SH = 506, 1020  # flat phone screen


def _screen(src, name):
    return src.split("screen {}(".format(name), 1)[1].split("\nscreen ", 1)[0]


class CropMathTests(unittest.TestCase):
    def assertCovers(self, iw, ih, zoom, cx, cy):
        x, y, w, h = wp.crop_rect(iw, ih, SW, SH, zoom, cx, cy)
        self.assertGreaterEqual(x, -1e-9)
        self.assertGreaterEqual(y, -1e-9)
        self.assertLessEqual(x + w, iw + 1e-6)
        self.assertLessEqual(y + h, ih + 1e-6)
        # Same aspect as the screen, so nothing is stretched.
        self.assertAlmostEqual(w / h, SW / SH, places=6)

    def test_min_zoom_just_covers_a_landscape_photo(self):
        x, y, w, h = wp.crop_rect(1920, 1080, SW, SH, 1.0, 0.5, 0.5)
        self.assertAlmostEqual(h, 1080)
        self.assertAlmostEqual(w, 1080 * SW / SH)
        self.assertAlmostEqual(x, (1920 - w) / 2)
        self.assertCovers(1920, 1080, 1.0, 0.5, 0.5)

    def test_zoom_is_clamped_between_cover_and_4x(self):
        self.assertEqual(wp.clamp_zoom(0.2), 1.0)
        self.assertEqual(wp.clamp_zoom(9), 4.0)
        self.assertEqual(wp.clamp_zoom("junk"), 1.0)
        self.assertEqual(wp.step_zoom(1.0, -3), 1.0)
        self.assertEqual(wp.step_zoom(3.9, 2), 4.0)
        self.assertAlmostEqual(wp.step_zoom(wp.step_zoom(1.0, 1), -1), 1.0)

    def test_pan_is_clamped_so_the_screen_is_always_covered(self):
        for dx, dy in ((5000, 0), (-5000, 0), (0, 5000), (0, -5000), (999, -999)):
            for zoom in (1.0, 2.0, 4.0):
                cx, cy = wp.pan(0.5, 0.5, dx, dy, 1920, 1080, SW, SH, zoom)
                self.assertCovers(1920, 1080, zoom, cx, cy)
        # At cover zoom a landscape photo cannot move vertically at all.
        cx, cy = wp.pan(0.5, 0.5, 0, 300, 1920, 1080, SW, SH, 1.0)
        self.assertAlmostEqual(cy, 0.5)

    def test_drag_moves_the_photo_with_the_finger(self):
        cx, _ = wp.pan(0.5, 0.5, 100, 0, 1920, 1080, SW, SH, 1.0)
        self.assertLess(cx, 0.5)  # dragging right shows more of the left side
        scale = wp.cover_scale(1920, 1080, SW, SH)
        self.assertAlmostEqual((0.5 - cx) * 1920 * scale, 100)

    def test_wheel_zoom_keeps_the_point_under_the_pointer(self):
        iw, ih = 1920, 1080
        px, py = 400, 300
        cx, cy, zoom = wp.zoom_at(0.5, 0.5, 2.0, 2.5, px, py, iw, ih, SW, SH)
        def under(cx, cy, zoom):
            s = wp.cover_scale(iw, ih, SW, SH) * zoom
            return cx + (px - SW / 2) / (iw * s), cy + (py - SH / 2) / (ih * s)
        before = under(0.5, 0.5, 2.0)
        after = under(cx, cy, zoom)
        self.assertAlmostEqual(before[0], after[0], places=9)
        self.assertAlmostEqual(before[1], after[1], places=9)
        self.assertEqual(zoom, 2.5)

    def test_zoom_out_near_an_edge_stays_covered(self):
        cx, cy = wp.pan(0.5, 0.5, 4000, 4000, 1920, 1080, SW, SH, 4.0)
        cx, cy, zoom = wp.zoom_at(cx, cy, 4.0, 1.0, 0, 0, 1920, 1080, SW, SH)
        self.assertEqual(zoom, 1.0)
        self.assertCovers(1920, 1080, zoom, cx, cy)

    def test_portrait_and_tiny_photos(self):
        for iw, ih in ((600, 1600), (100, 80), (506, 1020)):
            for zoom in (1.0, 3.0):
                self.assertCovers(iw, ih, zoom, 0.0, 1.0)


class SaveFormatTests(unittest.TestCase):
    def test_record_is_plain_data(self):
        rec = wp.make("ch01_photo_x", 1.23456789, 0.4, 0.6)
        self.assertEqual(set(rec), {"image", "zoom", "x", "y"})
        self.assertIsInstance(rec["image"], str)
        for k in ("zoom", "x", "y"):
            self.assertIsInstance(rec[k], float)

    def test_normalize_rejects_and_repairs_bad_saves(self):
        self.assertIsNone(wp.normalize(None))
        self.assertIsNone(wp.normalize("ch01_photo_x"))
        self.assertIsNone(wp.normalize({"zoom": 2}))
        rec = wp.normalize({"image": "a", "zoom": 99, "x": -3, "y": "nan"})
        self.assertEqual(rec, {"image": "a", "zoom": 4.0, "x": 0.0, "y": 0.5})

    def test_default_keeps_old_saves_working(self):
        self.assertIn("default phone_wallpaper = None", WALL)
        self.assertNotIn("define phone_wallpaper", WALL)


class ScreenWiringTests(unittest.TestCase):
    def test_viewer_offers_set_as_wallpaper(self):
        viewer = _screen(PHONE, "lc_phone_photo_viewer")
        self.assertIn('textbutton "Set as wallpaper":', viewer)
        self.assertIn('Show("lc_phone_wallpaper_editor", photo_asset=photo_asset)', viewer)

    def test_home_draws_the_wallpaper_and_falls_back(self):
        home = _screen(PHONE, "phone_screen").split('elif phone_app == "thread"', 1)[0]
        self.assertIn("use lc_phone_wallpaper_layers(_wallpaper)", home)
        self.assertIn('add "gui/phone/sprite_match/phone_home.png"', home)

    def test_settings_can_reset(self):
        settings = _screen(PHONE, "lc_phone_settings")
        self.assertIn('textbutton "Reset wallpaper":', settings)
        self.assertIn("lc_phone_wallpaper_reset", settings)

    def test_editor_controls(self):
        editor = _screen(WALL, "lc_phone_wallpaper_editor")
        for needle in ('textbutton "Cancel":', 'textbutton "Set":', 'style "lc_phone_btn_primary"',
                       "{font=DejaVuSans.ttf}+{/font}", "{font=DejaVuSans.ttf}−{/font}",
                       'key "K_ESCAPE" action _wp_cancel', "modal True"):
            self.assertIn(needle, editor)
        # Esc is one tier back: it only hides the editor, never the viewer/phone.
        cancel = editor.split("$ _wp_cancel = ", 1)[1].split("\n", 1)[0]
        self.assertIn("lc_phone_back", cancel)
        back = PHONE.split("def lc_phone_back():", 1)[1].split("\n    def ", 1)[0]
        self.assertLess(back.index("lc_phone_wallpaper_editor"), back.index("lc_phone_photo_viewer"))
        self.assertNotIn("lc_phone_photo_viewer", cancel)
        self.assertNotIn("phone_screen", cancel)

    def test_displayable_handles_drag_and_wheel_without_tracked_state(self):
        for needle in ("MOUSEBUTTONDOWN", "MOUSEMOTION", "MOUSEBUTTONUP", "viewport_wheelup",
                       "viewport_wheeldown", "renpy.redraw", "set_grab", "renpy.display.position.absolute"):
            self.assertIn(needle, WALL)
        self.assertNotIn("__slots__", WALL)
        self.assertNotIn("object.__setattr__", WALL)
        # Per-frame caches are plain python containers, not rollback-tracked ones.
        self.assertIn("python_dict()", WALL)

    def test_art_layers_exist(self):
        for name in ("phone_wall_frame.png", "phone_wall_dock.png", "phone_wall_mask.png", "phone_wall_shade.png"):
            self.assertTrue((ART / name).is_file(), name)
        gen = (ROOT / "tools" / "gen_sprite_match_ui.py").read_text(encoding="utf-8")
        self.assertIn("def build_wallpaper_layers", gen)


if __name__ == "__main__":
    unittest.main()
