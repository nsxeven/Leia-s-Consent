"""Leia breath system: files exist, every start has a stop on the same path."""
import re
import unittest
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / "game"
VOICE = GAME / "audio" / "voice" / "leia"


class BreathTests(unittest.TestCase):

    def test_voice_files_follow_the_naming_scheme(self):
        files = sorted(p.name for p in VOICE.glob("*.ogg"))
        self.assertGreaterEqual(len(files), 20)
        for name in files:
            self.assertRegex(name, r"^(inhale|exhale|moan)-i\d+-\d+\.ogg$")
        self.assertTrue(any(n.startswith("inhale") for n in files))
        self.assertTrue(any(n.startswith("moan") for n in files))

    def test_channel_is_under_the_voice_slider(self):
        src = (GAME / "systems" / "lc_breath.rpy").read_text(encoding="utf-8")
        self.assertIn('register_channel("lc_breath", mixer="voice"', src)

    def test_day1_starts_are_stopped(self):
        src = (GAME / "chapters" / "ch01" / "ch01_scenes_14_30.rpy").read_text(encoding="utf-8")
        scene20 = src.split("label ch01_scene_20_no_hiding_place:", 1)[1].split("\nlabel ", 1)[0]
        self.assertIn("lc_breath_start(", scene20)
        self.assertIn("lc_breath_stop(", scene20)
        dream = src.split('scene cg ch01_dream_dinner_beside', 1)[1].split('lc_sfx("gasp_wake")', 1)[0]
        self.assertIn("lc_breath_start(2, moans=False", dream)  # CG 02: inhales only
        self.assertIn("lc_breath_start(4, moan_chance=0.4", dream)  # CG 03: dense inhales + moans, slower
        self.assertIn("lc_moan_once(", dream)
        self.assertIn("lc_breath_stop(", dream)

    def test_single_clips_never_stack_two_voices(self):
        # darryn: the dream moans overlapped and sounded like two people. Single
        # moans/inhales must play on Leia's own channel (replacing the loop's next
        # sound) rather than on the separate lc_voice channel on top of the loop.
        src = (GAME / "systems" / "lc_breath.rpy").read_text(encoding="utf-8")
        single = src.split("def _lc_breath_single(", 1)[1].split("\n    def ", 1)[0]
        self.assertIn('channel="lc_breath"', single)
        self.assertNotIn('channel="lc_voice"', single)
        for fn in ("lc_moan_once", "lc_inhale_over"):
            body = src.split("def %s(" % fn, 1)[1].split("\n    def ", 1)[0]
            self.assertIn("_lc_breath_single(", body)
            self.assertNotIn("lc_voice", body)
        self.assertIn("default lc_breath_loop = None", src)


if __name__ == "__main__":
    unittest.main()
