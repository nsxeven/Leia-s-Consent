"""Ryan's direct inner voice uses the italic `think` speaker (darryn 2026-11-09)."""
import re
import unittest
from pathlib import Path

CH = Path(__file__).resolve().parents[1] / "game" / "chapters"


class ThinkLineTests(unittest.TestCase):

    def test_known_thoughts_use_think(self):
        src = "".join(p.read_text(encoding="utf-8") for p in CH.rglob("*.rpy"))
        for line in ('think "What the hell was that?"', 'think "Babe, are you okay?"',
                     'think "Don\'t think about it. Don\'t make it a thing."'):
            self.assertIn(line, src)

    def test_no_whole_line_italic_narration_left(self):
        # Whole-line {i}...{/i} narration should be a `think` line instead.
        for p in CH.rglob("*.rpy"):
            for n, ln in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                self.assertNotRegex(ln, r'^\s+"\{i\}[^"]*\{/i\}"\s*$', "%s:%d" % (p.name, n))


if __name__ == "__main__":
    unittest.main()
