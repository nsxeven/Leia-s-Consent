"""Ryan wears his home clothes from the Day 1 upstairs change on (darryn 2026-11-09)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCN = (ROOT / "game/chapters/ch01/ch01_scenes_14_30.rpy").read_text(encoding="utf-8")


class RyanHomeClothesTests(unittest.TestCase):

    def test_sprite_defined(self):
        spr = (ROOT / "game/sprites/ryan_prologue_party.rpy").read_text(encoding="utf-8")
        self.assertIn("image ryan_home = ", spr)
        for f in ("Base_HomeClothes.png", "Chest_HomeClothes.png"):
            self.assertTrue((ROOT / "game/images/sprites/ryan" / f).is_file(), f)

    def test_changes_upstairs_and_keeps_them_on(self):
        up = SCN.split("label ch01_scene_14a_upstairs_change:", 1)[1].split("label ch01_scene_14b_back_downstairs:", 1)[0]
        self.assertIn('cast_add(ryan="home")', up)
        rest = SCN.split("label ch01_scene_14b_back_downstairs:", 1)[1]
        self.assertNotIn('ryan="casual"', rest)
        self.assertIn('ryan="home"', rest)


if __name__ == "__main__":
    unittest.main()
