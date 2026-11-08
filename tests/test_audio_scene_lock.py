"""One-shot audio belongs to its scene; nothing plays from skipped content (darryn 2026-11-08)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = (ROOT / "game/systems/lc_audio_scene_lock.rpy").read_text(encoding="utf-8")
FX = (ROOT / "game/systems/lc_fx.rpy").read_text(encoding="utf-8")
BREATH = (ROOT / "game/systems/lc_breath.rpy").read_text(encoding="utf-8")


class AudioSceneLockTests(unittest.TestCase):

    def test_skip_mode_drops_one_shots(self):
        self.assertIn("define config.skip_sounds = True", LOCK)

    def test_scene_statement_cuts_earlier_one_shots_not_loops(self):
        self.assertIn("config.scene = _lc_scene_with_audio_lock", LOCK)
        self.assertIn('LC_SCENE_LOCKED_CHANNELS = ("audio", "lc_voice", "lc_lewd", "lc_breath")', LOCK)
        for loop in ("ambience", "sfx_loop", "lc_lewd_loop", "music"):
            self.assertNotIn('"%s"' % loop, LOCK.split("LC_SCENE_LOCKED_CHANNELS", 1)[1].split("\n", 1)[0])
        self.assertIn('if ch == "lc_breath" and getattr(store, "lc_breath_loop", None):', LOCK)
        self.assertIn("now - started < LC_SCENE_CUT_GRACE", LOCK)
        self.assertIn("python_dict()", LOCK)

    def test_every_one_shot_is_marked(self):
        self.assertIn("lc_audio_mark(channel)", FX)
        self.assertEqual(BREATH.count('lc_audio_mark("lc_breath")'), 3)


if __name__ == "__main__":
    unittest.main()
