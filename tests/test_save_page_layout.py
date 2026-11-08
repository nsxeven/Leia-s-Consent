"""Save/Load: slots sit below the page name (darryn 2026-11-08)."""
import re
import unittest
from pathlib import Path

UI = (Path(__file__).resolve().parents[1] / "game/screens/zzzzzzzz_scrapbook_ui.rpy").read_text(encoding="utf-8")


class SavePageLayoutTests(unittest.TestCase):

    def test_slots_clear_header_and_fit_panel(self):
        rows = tuple(int(n) for n in re.search(r"define LC_SLOT_ROW_Y = \((\d+), (\d+)\)", UI).groups())
        # header: title 48 + subtitle 21 + page-name input (Caveat 28, ~44 tall) + spacing
        self.assertGreaterEqual(rows[0], 150)
        self.assertGreaterEqual(rows[1] - rows[0], 310)   # slot height 300 + gap
        self.assertLessEqual(rows[1] + 300, 930 - 42)     # inside the glass panel
        self.assertIn("enumerate((LC_SLOT_ROW_Y))", UI)


if __name__ == "__main__":
    unittest.main()
