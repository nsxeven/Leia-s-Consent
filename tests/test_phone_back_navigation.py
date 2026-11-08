"""Phone navigation regression checks against the effective late-loaded screen."""
import re
import textwrap
import unittest
from pathlib import Path


SOURCE = (Path(__file__).resolve().parents[1] / "game/screens/zzzzzz_phone_ios_presentation.rpy").read_text()


class FakeRenpy:
    def __init__(self, app="home", thread=None, overlays=()):
        self.screens = {"phone_screen", *overlays}
        self.variables = {"phone_app": app, "phone_thread": thread}
        self.hidden = []
        self.restarts = 0

    def get_screen(self, name):
        return name in self.screens

    def hide_screen(self, name):
        self.screens.discard(name)
        self.hidden.append(name)

    def get_screen_variable(self, name, screen=None):
        assert screen == "phone_screen"
        return self.variables[name]

    def set_screen_variable(self, name, value, screen=None):
        assert screen == "phone_screen"
        self.variables[name] = value

    def restart_interaction(self):
        self.restarts += 1


class PhoneNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        block = SOURCE.split("    def lc_phone_close():", 1)[1].split("    def lc_phone_clock_text():", 1)[0]
        cls.code = compile(textwrap.dedent("    def lc_phone_close():" + block), "phone_navigation", "exec")

    def setUp(self):
        self.renpy = FakeRenpy()
        self.sounds = []
        self.left = []
        scope = {"renpy": self.renpy,
                 "lc_ui_play": self.sounds.append,
                 "lc_phone_leave_thread": lambda app, thread: self.left.append((app, thread))}
        exec(self.code, scope)
        self.back = scope["lc_phone_back"]
        self.close = scope["lc_phone_close"]

    def test_thread_then_messages_then_home_then_closed(self):
        self.renpy.variables.update(phone_app="thread", phone_thread="group")
        self.assertIsNone(self.back())
        self.assertEqual(self.renpy.variables, {"phone_app": "messages", "phone_thread": "group"})
        self.assertEqual(self.left, [("thread", "group")])
        self.back()
        self.assertEqual(self.renpy.variables, {"phone_app": "home", "phone_thread": None})
        self.assertIn("phone_screen", self.renpy.screens)
        self.back()
        self.assertNotIn("phone_screen", self.renpy.screens)
        self.assertEqual(self.sounds, ["back", "back"])

    def test_each_app_returns_home(self):
        for app in ("messages", "photos", "shop", "wallet", "delivery", "other"):
            with self.subTest(app=app):
                self.renpy.variables["phone_app"] = app
                self.back()
                self.assertEqual(self.renpy.variables["phone_app"], "home")
                self.assertIn("phone_screen", self.renpy.screens)

    def test_overlays_return_to_underlying_app_one_at_a_time(self):
        for overlay in ("lc_phone_status", "lc_phone_settings", "lc_phone_photo_viewer"):
            with self.subTest(overlay=overlay):
                self.renpy.screens.add(overlay)
                self.renpy.variables["phone_app"] = "photos"
                self.back()
                self.assertNotIn(overlay, self.renpy.screens)
                self.assertEqual(self.renpy.variables["phone_app"], "photos")
                self.assertIn("phone_screen", self.renpy.screens)

    def test_back_prioritizes_viewer_over_app_and_close_dismisses_everything(self):
        self.renpy.screens.update(("lc_phone_status", "lc_phone_photo_viewer"))
        self.back()
        self.assertIn("lc_phone_status", self.renpy.screens)
        self.assertNotIn("lc_phone_photo_viewer", self.renpy.screens)
        self.assertIsNone(self.close())
        self.assertFalse(self.renpy.screens)
        self.assertEqual(self.sounds, ["back"])

    def test_every_screen_uses_one_back_function_and_backdrop_closes_all(self):
        for name in ("phone_screen", "lc_phone_status", "lc_phone_settings", "lc_phone_photo_viewer"):
            match = re.search(r"(?m)^screen " + name + r"\([^\n]*\):\n(.*?)(?=^screen |\Z)", SOURCE, re.S | re.M)
            self.assertIsNotNone(match, name)
            body = match.group(1)
            self.assertIn('key "K_ESCAPE" action Function(lc_phone_back)', body)
            self.assertIn('key "game_menu" action Function(lc_phone_back)', body)
            if name != "lc_phone_photo_viewer":
                self.assertIn('use lc_phone_backdrop(Function(lc_phone_close))', body)
        self.assertIn('hover_background LC_PHONE_BACKDROP', SOURCE)
        self.assertIn('background LC_PHONE_BACKDROP', SOURCE)
        self.assertIn('define LC_PHONE_BACKDROP = Solid("#071225c4")', SOURCE)
        self.assertIn('on "hide" action [Function(lc_phone_leave_thread, phone_app, phone_thread), Function(lc_ui_play, "phone_close")]', SOURCE)


if __name__ == "__main__":
    unittest.main()
