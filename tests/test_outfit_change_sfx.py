"""Outfit changes mid-scene play a fabric rustle (darryn 2026-11-09)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAST = (ROOT / "game/systems/cast_staging.rpy").read_text(encoding="utf-8")


class OutfitChangeSfxTests(unittest.TestCase):

    def test_rustle_on_change_not_on_join(self):
        body = CAST.split("def cast_add(**members):", 1)[1].split("def cast_remove", 1)[0]
        changed = body.split("elif changed:", 1)[1]
        self.assertIn("lc_sfx(LC_OUTFIT_CHANGE_SFX)", changed)
        self.assertNotIn("lc_sfx", body.split("elif changed:", 1)[0])
        self.assertIn('LC_OUTFIT_CHANGE_SFX = "cloth_change"', CAST)
        self.assertTrue((ROOT / "game/audio/sfx/cloth_change.ogg").is_file())


if __name__ == "__main__":
    unittest.main()
