"""Behaviour pins for the clean-up: effective definitions must not change.

tests/data/effective_fingerprints.json records, for every screen, function,
class, define/default, transform, image, module-level assignment and style,
what the copy Ren'Py actually uses looks like, and for every label the body
that really runs (label_overrides and single-`jump` aliases followed).

Moving a definition to another file, deleting a dead duplicate or folding a
label override keeps these prints identical. A change that is MEANT to rewrite
an effective body (e.g. folding a load-time wrapper into one function) lists the
name in FOLDED with the reason, and needs a test in test_behaviour_freeze.py.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "dev"))
sys.path.insert(0, str(ROOT / "tests"))

from snapshot_baselines import fingerprints  # noqa: E402

# kind -> {name: reason}. Keep reasons short; each must be covered by a behaviour test.
FOLDED = {}


class EffectiveFingerprintTests(unittest.TestCase):
    def test_effective_definitions_unchanged(self):
        baseline = json.loads((ROOT / "tests/data/effective_fingerprints.json").read_text(encoding="utf-8"))
        current = fingerprints()
        problems = []
        for kind, names in baseline.items():
            allowed = FOLDED.get(kind, {})
            for name, print_ in names.items():
                if name in allowed:
                    continue
                now = current.get(kind, {}).get(name)
                if now is None:
                    problems.append(f"{kind} {name}: missing")
                elif now != print_:
                    problems.append(f"{kind} {name}: changed")
        self.assertEqual(problems, [], "\n" + "\n".join(problems))

    def test_folded_entries_have_reasons(self):
        for kind, names in FOLDED.items():
            for name, reason in names.items():
                self.assertTrue(reason.strip(), f"{kind} {name} needs a reason")


if __name__ == "__main__":
    unittest.main()
