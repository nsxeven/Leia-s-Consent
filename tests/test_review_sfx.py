"""Screen-action sound hooks must return None, or `call screen` ends early."""
import re
import unittest
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / "game"


class ReviewSfxTests(unittest.TestCase):

    def test_review_sfx_never_returns_a_value(self):
        src = (GAME / "systems" / "day_review.rpy").read_text(encoding="utf-8")
        body = src.split("    def lc_review_sfx(name):", 1)[1].split("\n    def ", 1)[0].split("\n    # ", 1)[0]
        returns = re.findall(r"^\s*return\b(.*)$", body, re.M)
        self.assertTrue(returns)
        for r in returns:
            self.assertEqual(r.strip(), "None", "lc_review_sfx returns %r" % r)


if __name__ == "__main__":
    unittest.main()
