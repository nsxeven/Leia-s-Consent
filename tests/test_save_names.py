"""Save safety: every runtime name present before the clean-up still exists.

Baseline: tests/data/save_names_baseline.json (labels, store variables, story
flag/value keys, choice ids, phone message ids, image tags, screen names),
written by tools/dev/snapshot_baselines.py. New names are fine; a missing one
means an old save or a story line can no longer find what it refers to.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))

from lc_save_names import save_names  # noqa: E402


class SaveNameTests(unittest.TestCase):
    def test_no_runtime_name_disappears(self):
        baseline = json.loads((ROOT / "tests/data/save_names_baseline.json").read_text(encoding="utf-8"))
        current = save_names()
        missing = {k: sorted(set(v) - current.get(k, set())) for k, v in baseline.items()}
        missing = {k: v for k, v in missing.items() if v}
        self.assertEqual(missing, {})

    def test_baseline_is_not_empty(self):
        baseline = json.loads((ROOT / "tests/data/save_names_baseline.json").read_text(encoding="utf-8"))
        for kind in ("label", "store", "story_key", "choice_id", "message_id", "image", "screen"):
            self.assertGreater(len(baseline[kind]), 0, kind)


if __name__ == "__main__":
    unittest.main()
