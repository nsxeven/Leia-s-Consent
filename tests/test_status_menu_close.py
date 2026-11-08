"""Status uses a menu replacement, not a modal Show over a menu."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "game" / "screens"


class StatusMenuCloseTests(unittest.TestCase):
    def test_status_tab_replaces_current_menu_and_tracks_origin(self):
        source = (ROOT / "zzzzzzzz_scrapbook_ui.rpy").read_text(encoding="utf-8")
        self.assertIn('ShowMenu("status_screen", return_to=lc_journal_status_origin())', source)
        self.assertNotIn('Show("status_screen")', source)
        self.assertIn('renpy.get_screen(name) is not None', source)

    def test_origin_lookup_uses_the_visible_menu_page(self):
        import textwrap
        from types import SimpleNamespace
        source = (ROOT / "zzzzzzzz_scrapbook_ui.rpy").read_text(encoding="utf-8")
        body = source.split("    def lc_journal_status_origin():", 1)[1].split("\n    def lc_journal_tab_rows():", 1)[0]
        code = "def lc_journal_status_origin():" + body
        visible = {"preferences"}
        scope = {
            "JOURNAL_MENU_SCREENS": ("save", "load", "preferences", "status_screen", "main_menu"),
            "renpy": SimpleNamespace(get_screen=lambda name: object() if name in visible else None),
        }
        exec(textwrap.dedent(code), scope)
        origin = scope["lc_journal_status_origin"]
        self.assertEqual(origin(), "preferences")
        visible.clear()
        visible.add("save")
        self.assertEqual(origin(), "save")
        visible.clear()
        self.assertIsNone(origin())

    def test_phone_status_right_click_goes_back_to_phone(self):
        source = (ROOT / "zzzzzz_phone_ios_presentation.rpy").read_text(encoding="utf-8")
        screen = source.split("screen lc_phone_status():", 1)[1].split("\nscreen ", 1)[0]
        self.assertIn('key "game_menu" action Hide("lc_phone_status")', screen)
        self.assertIn('key "K_ESCAPE" action Hide("lc_phone_status")', screen)
        self.assertIn('Hide("lc_phone_status")', screen)

    def test_status_has_menu_tag_and_origin_aware_closing_actions(self):
        source = (ROOT / "status_screen.rpy").read_text(encoding="utf-8")
        screen = source.split("screen status_screen(", 1)[1]
        self.assertIn("tag menu", screen)
        self.assertIn('ShowMenu(return_to) if return_to else Return()', screen)
        self.assertIn('key "K_ESCAPE" action _status_close', screen)
        self.assertIn('key "game_menu" action _status_close', screen)
        self.assertIn('action _status_close', screen)


if __name__ == "__main__":
    unittest.main()
