"""Leia's breaths/moans: slower pacing, never two Leias at once (darryn 2026-11-08)."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BREATH = (ROOT / "game/systems/lc_breath.rpy").read_text(encoding="utf-8")
FX = (ROOT / "game/systems/lc_fx.rpy").read_text(encoding="utf-8")


class LeiaVoicePacingTests(unittest.TestCase):

    def test_pace_stretches_all_pauses(self):
        pace = float(re.search(r"LC_BREATH_PACE = ([\d.]+)", BREATH).group(1))
        self.assertGreaterEqual(pace, 1.5)
        self.assertIn("pause_lo * LC_BREATH_PACE, pause_hi * LC_BREATH_PACE", BREATH)
        self.assertIn("moan_chance *= LC_BREATH_MOAN_SCALE", BREATH)

    def test_leia_clips_share_her_channel(self):
        self.assertIn('if path and kind == "voice/leia":', FX)
        self.assertIn("lc_leia_voice_clip(path", FX)
        clip = BREATH.split("def lc_leia_voice_clip", 1)[1].split("def ", 1)[0]
        self.assertIn('channel="lc_breath"', clip)
        self.assertIn("fadeout=0.12", clip)


if __name__ == "__main__":
    unittest.main()
