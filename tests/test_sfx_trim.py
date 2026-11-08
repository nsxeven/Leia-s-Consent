"""SFX-slider sounds trimmed 30% across the board (darryn 2026-11-08)."""
import re
import unittest
from pathlib import Path

FX = (Path(__file__).resolve().parents[1] / "game/systems/lc_fx.rpy").read_text(encoding="utf-8")


class SfxTrimTests(unittest.TestCase):

    def test_sfx_amb_ui_at_70_percent_others_untouched(self):
        block = FX.split("LC_KIND_GAIN = {", 1)[1].split("}", 1)[0]
        gains = dict((k, float(v)) for k, v in re.findall(r'"(\w+)": ([\d.]+)', block))
        self.assertEqual(gains, {"sfx": 0.7, "amb": 0.7, "ui": 0.7})
        self.assertIn("LC_KIND_GAIN.get(kind, 1.0)", FX)

    def test_ducking_still_relative(self):
        self.assertIn('renpy.music.set_volume(level, delay=delay, channel="music")', FX)


if __name__ == "__main__":
    unittest.main()
