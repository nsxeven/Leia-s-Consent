"""Ryan's direct inner voice uses the italic `think` speaker (darryn 2026-11-09)."""
import re
import unittest
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / "game"
# Story scripts plus the dev sandbox scenes (game/dev/ since clean-up PR 4).
SCRIPTS = sorted([*(GAME / "chapters").rglob("*.rpy"), *(GAME / "dev").rglob("*.rpy")])


class ThinkLineTests(unittest.TestCase):

    def test_known_thoughts_use_think(self):
        src = "".join(p.read_text(encoding="utf-8") for p in SCRIPTS)
        for line in ('think "What the hell was that?"', 'think "Babe, are you okay?"',
                     'think "Don\'t think about it. Don\'t make it a thing."'):
            self.assertIn(line, src)

    def test_no_whole_line_italic_narration_left(self):
        # Whole-line {i}...{/i} narration should be a `think` line instead.
        for p in SCRIPTS:
            for n, ln in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                self.assertNotRegex(ln, r'^\s+"\{i\}[^"]*\{/i\}"\s*$', "%s:%d" % (p.name, n))


    def test_upstairs_replay_is_thought(self):
        src = (GAME / "chapters" / "ch01" / "day1" / "ch01_scenes_14_30.rpy").read_text(encoding="utf-8")
        self.assertIn('think "The guy with a drink spilled all down his white trousers.', src)
        self.assertIn('think "Nobody had done anything wrong.', src)
        self.assertIn('    "I swapped my dinner shirt for a T-shirt', src)


if __name__ == "__main__":
    unittest.main()
