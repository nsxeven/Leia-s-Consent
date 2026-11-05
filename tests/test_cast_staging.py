import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATED = [
    "game/chapters/prologue.rpy",
    "game/chapters/ch01/ch01_main.rpy",
    "game/chapters/ch01/ch01_scenes_04_06.rpy",
    "game/chapters/ch01/ch01_scenes_07_13.rpy",
    "game/chapters/ch01/ch01_scenes_14_30.rpy",
]
SPRITE_LINE = re.compile(r"^\s*(show|hide) (leia|ryan|julian|stranger)_\w*")


class CastStagingTests(unittest.TestCase):
    def setUp(self):
        self.engine = (ROOT / "game/systems/cast_staging.rpy").read_text(encoding="utf-8")

    def test_engine_api(self):
        for name in ("def cast(", "def cast_add(", "def cast_remove(", "def face(",
                     "def cast_hold(", "def cast_resume(", "def lc_stage_speaker("):
            self.assertIn(name, self.engine)
        self.assertIn("config.say_arguments_callback = lc_cast_say_callback", self.engine)
        # Leia always right; guests on the right only when Leia is not in the cast.
        self.assertIn('if who == "leia":\n            return "right"', self.engine)

    def test_old_swap_system_is_gone(self):
        julian = (ROOT / "game/sprites/julian.rpy").read_text(encoding="utf-8")
        ryan = (ROOT / "game/sprites/ryan_prologue_party.rpy").read_text(encoding="utf-8")
        for text in (julian, ryan):
            self.assertNotIn("lc_left_slot", text)
            self.assertNotIn("say_arguments_callback", text)

    def test_scripts_use_cast_not_hand_placed_sprites(self):
        """Outside cast_hold()/cast_resume() blocks, no direct sprite show/hide lines."""
        for rel in MIGRATED:
            held = False
            for n, line in enumerate((ROOT / rel).read_text(encoding="utf-8").splitlines(), 1):
                if "cast_hold()" in line:
                    held = True
                elif "cast_resume(" in line:
                    held = False
                elif SPRITE_LINE.match(line) and not held:
                    if line.strip().startswith("hide stranger_casual_wet"):
                        continue  # retires the hand-placed sprite right before cast_resume
                    self.fail("%s:%d hand-placed sprite outside cast_hold: %s" % (rel, n, line.strip()))
                self.assertNotIn("lc_julian_outfit", line, "%s:%d" % (rel, n))


if __name__ == "__main__":
    unittest.main()
