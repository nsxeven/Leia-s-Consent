"""Phone status rows: hover highlight never crops the bar (darryn 2026-11-08)."""
import unittest
from pathlib import Path

PHONE = (Path(__file__).resolve().parents[1] / "game/screens/zzzzzz_phone_ios_presentation.rpy").read_text(encoding="utf-8")


class PhoneRowHoverTests(unittest.TestCase):

    def test_row_padding_clears_hover_border(self):
        row = PHONE.split("screen lc_phone_status_row(row):", 1)[1].split("\nscreen ", 1)[0]
        pad = row.split("padding (", 1)[1].split(")", 1)[0]
        left, top, right, bottom = (int(x) for x in pad.split(","))
        self.assertGreaterEqual(min(left, right), 12)
        self.assertGreaterEqual(bottom, 10)


if __name__ == "__main__":
    unittest.main()
