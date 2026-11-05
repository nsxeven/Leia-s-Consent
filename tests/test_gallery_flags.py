"""Gallery 18+ flags that darryn set explicitly."""
import re
import unittest
from pathlib import Path

DATA = (Path(__file__).resolve().parents[1] / "game" / "systems" / "gallery_data.rpy").read_text(encoding="utf-8")


def _row(entry_id):
    m = re.search(r'gallery_row\("%s",(.*?)\)\s*\n\s*(?:gallery_row|#|$)' % re.escape(entry_id), DATA, re.S)
    assert m, entry_id
    return m.group(1)


class GalleryMatureFlagTests(unittest.TestCase):

    def test_micro_test_choice_cg_is_18_plus(self):
        row = _row("d1_lounge_micro_test")
        self.assertIn("ch01_lounge_micro_test", row)
        self.assertIn("mature=True", row)

    def test_micro_test_glance_cg_is_not_18_plus(self):
        row = _row("d1_movie_glance")
        self.assertIn("ch01_movie_micro_test_glance", row)
        self.assertNotIn("mature=True", row)
        self.assertNotIn("ch01_lounge_micro_test", row)


if __name__ == "__main__":
    unittest.main()
