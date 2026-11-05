"""Title-screen customiser: registries point at real files, 18+ options are flagged, wiring is in place."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
SRC = (GAME / "systems" / "title_customiser.rpy").read_text(encoding="utf-8")


def _calls(name):
    return [m.group(1) for m in re.finditer(r"^\s*" + name + r"\((.*)\)\s*$", SRC, re.M)]


class TitleCustomiserTests(unittest.TestCase):

    def test_outfit_files_exist_and_mature_flags(self):
        calls = _calls("lc_title_register_outfit")
        self.assertGreaterEqual(len(calls), 9)
        mature = set()
        for call in calls:
            outfit_id = re.match(r'"([^"]+)"', call).group(1)
            for path in re.findall(r'_d \+ "([^"]+)"', call):
                self.assertTrue((GAME / "images" / "sprites" / "leia" / path).is_file(), path)
            self.assertIn("seen_cgs=(", call, outfit_id + " needs seen_cgs for existing players")
            if "mature=True" in call:
                mature.add(outfit_id)
        self.assertEqual(mature, {"towel", "purple_dress_wet", "purple_dress_no_bra"})

    def test_outfit_seen_cgs_are_real_gallery_pages(self):
        data = (GAME / "systems" / "gallery_data.rpy").read_text(encoding="utf-8")
        for call in _calls("lc_title_register_outfit"):
            block = call.split("seen_cgs=(", 1)[1]
            for cg in re.findall(r'"([a-z0-9_]+)"', block):
                self.assertIn('"%s"' % cg, data, cg)

    def test_background_files_exist_and_no_night_art(self):
        calls = _calls("lc_title_register_background")
        self.assertGreaterEqual(len(calls), 10)
        for call in calls:
            path = re.search(r'_b \+ "([^"]+)"', call).group(1)
            self.assertTrue((GAME / "images" / "backgrounds" / path).is_file(), path)
            self.assertNotIn("night", path)  # night art is reserved (darryn 2026-11-04)

    def test_cast_system_records_shown_sprites(self):
        cast = (GAME / "systems" / "cast_staging.rpy").read_text(encoding="utf-8")
        self.assertIn("lc_title_note_sprite(name[0])", cast)

    def test_title_screen_uses_customiser(self):
        screen = (GAME / "screens" / "title_screen.rpy").read_text(encoding="utf-8")
        self.assertIn("lc_title_bg_now()", screen)
        self.assertIn("lc_title_leia_now()", screen)
        self.assertIn('use lc_title_item("Customise"', screen)
        self.assertIn("use lc_title_customiser(", screen)
        for name in ("panel.png", "logo_sheen.png"):
            self.assertTrue((GAME / "gui" / "title" / name).is_file(), name)


if __name__ == "__main__":
    unittest.main()
