"""Sprite-matched phone, day review and preferences stay on the real screens."""

import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
PHONE_SRC = (GAME / "screens" / "zzzzzz_phone_ios_presentation.rpy").read_text(encoding="utf-8")
PREFS_SRC = (GAME / "screens" / "zzzzzzzz_scrapbook_ui.rpy").read_text(encoding="utf-8")
REVIEW_SRC = (GAME / "screens" / "day_review_screen.rpy").read_text(encoding="utf-8")

# Native stat fills. The material pass must not recolor them.
STAT_FILL_SHA256 = {
    "bar_fill_acceptance.png": "21a6cf5865c1ebc2",
    "bar_fill_boredom.png": "0dac6d2923180500",
    "bar_fill_boundary_looseness.png": "0ad00ec78f8fcf43",
    "bar_fill_curiosity.png": "e163ff720be4d730",
    "bar_fill_exhibitionism.png": "5f92c86d24c57930",
    "bar_fill_jealousy.png": "2692cafa3ffd949c",
    "bar_fill_love.png": "c506d96716d77248",
    "bar_fill_momentum.png": "a9d8d7d290441051",
    "bar_fill_secrecy.png": "34eb6ad1d61977ee",
    "bar_fill_temptation.png": "25fe0459d5fb15d2",
    "bar_fill_trust.png": "e92300f7118025cd",
}

REAL_APPS = ("messages", "photos", "settings", "status", "delivery", "shop", "wallet")
# Decorative glyphs with no phone screen. They must not be home-grid labels.
UNBACKED = ("Notes", "Maps", "Music", "Browser", "Calendar", "Camera")


def _screen(src, name):
    return src.split("screen {}(".format(name), 1)[1].split("\nscreen ", 1)[0]


class PhoneShellTests(unittest.TestCase):
    def test_real_apps_are_on_the_home_grid_and_unbacked_icons_are_not(self):
        home = _screen(PHONE_SRC, "phone_screen")
        for app in REAL_APPS:
            self.assertIn('"%s"' % app, home)
            self.assertTrue((GAME / "gui" / "phone" / "sprite_match" / (app + ".png")).is_file(), app)
        for label in UNBACKED:
            self.assertNotIn('text "%s"' % label, home)
            self.assertNotIn('"%s"' % label.lower(), home)
        self.assertNotIn("Villa Wi-Fi", home)
        self.assertNotIn("Pixelify", PHONE_SRC)

    def test_readable_copy_is_patrick_hand_and_clocks_are_handjet(self):
        self.assertIn('font "fonts/PatrickHand-Regular.ttf"', PHONE_SRC)
        self.assertIn('font "fonts/Handjet-ExtraBold.ttf"', PHONE_SRC)
        home = _screen(PHONE_SRC, "phone_screen")
        # Status time is Handjet size 22. The lock-screen clock is Handjet size 70.
        self.assertIn("size 22", home)
        self.assertIn("size 70", home)
        self.assertIn('style "lc_sw_hand"', home)
        thread = home.split('phone_app == "thread"', 1)[1]
        self.assertIn("bubble_in.png", thread)
        self.assertIn("bubble_out.png", thread)
        self.assertIn("xmaximum (_bubble_max - 36)", thread)
        self.assertIn("lc_phone_thread_adjustment()", home)

    def test_handjet_clocks_fit_the_handset(self):
        try:
            from PIL import ImageFont
        except ImportError:
            self.skipTest("Pillow is not installed")
        scale = 1.3
        bold = ImageFont.truetype(str(GAME / "fonts" / "Handjet-ExtraBold.ttf"), 70)
        # Centred on the 540-wide handset, with room for the bezel.
        self.assertLess(bold.getlength("21:42") * scale, 420)
        status = ImageFont.truetype(str(GAME / "fonts" / "Handjet-ExtraBold.ttf"), 22)
        # Sits left of the punch-hole (the hole starts near x=228; the time starts at x=40).
        self.assertLess(status.getlength("21:42") * scale, 170)
        hand = ImageFont.truetype(str(GAME / "fonts" / "PatrickHand-Regular.ttf"), 22)
        self.assertLess(hand.getlength("Delivery"), 108)
        bubble = ImageFont.truetype(str(GAME / "fonts" / "PatrickHand-Regular.ttf"), 32)
        # A long line must be wider than the bubble interior so Ren'Py wraps it
        # instead of letting one wordless-looking run spill past the frame.
        sample = "Give me five minutes. Bringing your sunglasses."
        self.assertGreater(bubble.getlength(sample), 360)

    def test_existing_phone_features_are_still_wired(self):
        self.assertIn('if phone_app == "shop" and not LC_SHOP_ENABLED:', PHONE_SRC)
        self.assertLess(
            PHONE_SRC.index('if phone_app == "shop" and not LC_SHOP_ENABLED:'),
            PHONE_SRC.index("for outfit_id in shop_outfit_ids():"),
        )
        self.assertIn('gallery_customize_names(phone_outfit["description"])', PHONE_SRC)
        self.assertIn('tooltip row.get("tooltip")', _screen(PHONE_SRC, "lc_phone_status_row"))
        self.assertIn(
            'use lc_stat_tip(GetTooltip("lc_phone_status"), look="phone")',
            _screen(PHONE_SRC, "lc_phone_status"),
        )
        self.assertIn("phone_add_message", (GAME / "systems" / "phone_state.rpy").read_text(encoding="utf-8"))
        self.assertIn("lc_phone_open_from_notification", (GAME / "systems" / "zz_phone_presentation_logic.rpy").read_text(encoding="utf-8"))
        for name in ("avatar_leia.png", "avatar_julian.png", "avatar_ryan.png", "avatar_maya.png", "avatar_group.png", "phone_home.png", "phone_thread.png", "phone_app.png"):
            self.assertTrue((GAME / "gui" / "phone" / "sprite_match" / name).is_file(), name)


class ScrapbookAndPrefsTests(unittest.TestCase):
    def test_stat_fills_keep_native_bytes(self):
        folder = GAME / "images" / "ui" / "scrapbook"
        for name, prefix in STAT_FILL_SHA256.items():
            digest = hashlib.sha256((folder / name).read_bytes()).hexdigest()
            self.assertTrue(digest.startswith(prefix), name)

    def test_review_keeps_sequencer_polaroids_tape_and_ticket(self):
        self.assertIn('default seq_phase = "lead"', REVIEW_SRC)
        self.assertIn("polaroid.png", REVIEW_SRC)
        self.assertIn("ticket.png", REVIEW_SRC)
        self.assertIn("tape_corner_flip.png", REVIEW_SRC)
        self.assertNotIn('for tape_name in slot["tapes"]', REVIEW_SRC)
        self.assertIn('bar_fill_{}.png', REVIEW_SRC)

    def test_preferences_keep_every_control_and_audio_channel(self):
        prefs = _screen(PREFS_SRC, "preferences")
        for label in (
            "TEXT SPEED",
            "AUTO-FORWARD",
            "BGM",
            "SFX",
            "VOICE",
            "LEWD",
            "MUTE ALL",
            "SCREEN SHAKE",
            "CAMERA FLASH",
            "UNSEEN TEXT",
            "AFTER CHOICES",
            "TRANSITIONS",
            "WINDOW",
            "FULLSCREEN",
            "DEVELOPER",
            "ROUTE EXPLORER",
        ):
            self.assertIn(label, prefs)
        self.assertIn('Preference("music volume")', prefs)
        self.assertIn('Preference("sound volume")', prefs)
        self.assertIn('Preference("voice volume")', prefs)
        self.assertIn('Preference("mixer lewd volume")', prefs)
        self.assertIn("check_on.png", PREFS_SRC)
        self.assertIn("slider_thumb.png", PREFS_SRC)

    def test_generator_is_reproducible_and_does_not_recolor_fills(self):
        gen = (ROOT / "tools" / "gen_sprite_match_ui.py").read_text(encoding="utf-8")
        self.assertNotIn("Pixelify", gen)
        self.assertNotIn("sprite-match-proto", gen)
        self.assertIn("pristine", gen)
        self.assertTrue((ROOT / "tools" / "sprite_match" / "pristine" / "images" / "ui" / "scrapbook" / "polaroid.png").is_file())
        before = hashlib.sha256((GAME / "images" / "ui" / "scrapbook" / "bar_fill_love.png").read_bytes()).hexdigest()
        home = hashlib.sha256((GAME / "gui" / "phone" / "sprite_match" / "phone_home.png").read_bytes()).hexdigest()
        import runpy
        runpy.run_path(str(ROOT / "tools" / "gen_sprite_match_ui.py"), run_name="__main__")
        after = hashlib.sha256((GAME / "images" / "ui" / "scrapbook" / "bar_fill_love.png").read_bytes()).hexdigest()
        home_again = hashlib.sha256((GAME / "gui" / "phone" / "sprite_match" / "phone_home.png").read_bytes()).hexdigest()
        self.assertEqual(before, after)
        self.assertEqual(home, home_again)


if __name__ == "__main__":
    unittest.main()
