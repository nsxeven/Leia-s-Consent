"""Title screen (Golden Hour + memory reel): assets, wiring and the menu-safe list."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"


class TitleScreenTests(unittest.TestCase):

    def test_main_menu_uses_title_screen(self):
        src = (GAME / "screens" / "zzzzzzzz_scrapbook_ui.rpy").read_text(encoding="utf-8")
        body = src.split("screen main_menu():", 1)[1].split("\nscreen ", 1)[0]
        self.assertIn("use lc_title_screen()", body)
        self.assertIn("screen lc_title_screen():", (GAME / "screens" / "title_screen.rpy").read_text(encoding="utf-8"))

    def test_assets_exist(self):
        for name in ("shade_left.png", "shade_bottom.png", "vignette.png", "light_leak.png", "bokeh.png",
                     "polaroid.png", "polaroid_hover.png", "locked.png", "card.png", "card_hover.png",
                     "chip.png", "chip_hover.png", "logo.png", "badge18.png"):
            self.assertTrue((GAME / "gui" / "title" / name).is_file(), name)
        for name in ("Nunito-Bold.ttf", "Nunito-ExtraBold.ttf", "Fredoka-SemiBold.ttf", "OFL-Nunito.txt", "OFL-Fredoka.txt"):
            self.assertTrue((GAME / "fonts" / name).is_file(), name)
        self.assertTrue((GAME / "images" / "backgrounds" / "villa" / "villa_pool_evening.webp").is_file())

    def test_safe_list_only_names_real_non_mature_entries(self):
        data = (GAME / "systems" / "gallery_data.rpy").read_text(encoding="utf-8")
        rows = {}
        for match in re.finditer(r'gallery_row\("([^"]+)"(.*?)\]\)?(, mature=True)?', data, re.S):
            rows[match.group(1)] = bool(re.search(r"mature=True", data[match.start():data.find("\n    gallery_row(", match.end())] if data.find("\n    gallery_row(", match.end()) != -1 else data[match.start():]))
        logic = (GAME / "systems" / "title_screen.rpy").read_text(encoding="utf-8")
        block = logic.split("LC_TITLE_SAFE_GALLERY = (", 1)[1].split(")", 1)[0]
        safe = re.findall(r'"([^"]+)"', block)
        self.assertTrue(safe)
        for gallery_id in safe:
            self.assertIn(gallery_id, rows, gallery_id)
            self.assertFalse(rows[gallery_id], gallery_id + " is mature but on the safe title list")

    def test_reel_defaults_to_safe(self):
        logic = (GAME / "systems" / "title_screen.rpy").read_text(encoding="utf-8")
        self.assertIn("default persistent.lc_title_all_memories = False", logic)


if __name__ == "__main__":
    unittest.main()
