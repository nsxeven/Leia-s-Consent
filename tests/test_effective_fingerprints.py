"""Behaviour pins for the clean-up: effective definitions must not change.

tests/data/effective_fingerprints.json records, for every screen, function,
class, define/default, transform, image, layeredimage, module-level assignment
and style (per variant), what the copy Ren'Py actually uses looks like; for
every label the parameters + body that really run (label_overrides and
single-`jump` aliases followed); the multiset of init side-effect statements
(overlay registrations, table updates, loops); the overlay registration order;
and the final choice-effects table.

Moving a definition to another file, deleting a dead duplicate or folding a
label override keeps these prints identical. A change that is MEANT to rewrite
an effective body (e.g. folding a load-time wrapper into one function) lists the
name in FOLDED with a reason AND the dotted name of a behaviour test that pins
what the folded code does (see test_behaviour_freeze.py).
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "dev"))
sys.path.insert(0, str(ROOT / "tests"))

from snapshot_baselines import fingerprints  # noqa: E402

# kind -> {name: (reason, "tests.module.Class.test_method")}.
FOLDED = {}
# How to use FOLDED: a PR that intentionally rewrites an effective body lists it
# here while it proves the fold (behaviour tests + transcripts). Once proven, the
# SAME PR re-runs tools/dev/snapshot_baselines.py and empties FOLDED again, so the
# new code is pinned too (clean-up 2b review). Never merge with FOLDED non-empty.

# Kinds where a NEW entry is as suspicious as a missing one.
BOTH_WAYS = ("effect",)


class EffectiveFingerprintTests(unittest.TestCase):
    def test_effective_definitions_unchanged(self):
        baseline = json.loads((ROOT / "tests/data/effective_fingerprints.json").read_text(encoding="utf-8"))
        current = fingerprints()
        problems = []
        for kind, names in baseline.items():
            allowed = FOLDED.get(kind, {})
            now_kind = current.get(kind, {})
            for name, print_ in names.items():
                if name in allowed:
                    continue
                now = now_kind.get(name)
                if now is None:
                    problems.append(f"{kind} {name}: missing")
                elif now != print_:
                    problems.append(f"{kind} {name}: changed")
            if kind in BOTH_WAYS:
                for name in set(now_kind) - set(names) - set(allowed):
                    problems.append(f"{kind} {name}: new")
        self.assertEqual(problems, [], "\n" + "\n".join(problems))

    def test_folded_is_empty_when_merged(self):
        """FOLDED is a temporary list while a PR proves a fold; re-baseline and empty it."""
        self.assertEqual(FOLDED, {}, "re-run tools/dev/snapshot_baselines.py and empty FOLDED")

    def test_folded_entries_name_a_behaviour_test(self):
        loader = unittest.TestLoader()
        for kind, names in FOLDED.items():
            for name, (reason, test_name) in names.items():
                self.assertTrue(reason.strip(), f"{kind} {name} needs a reason")
                suite = loader.loadTestsFromName(test_name)
                self.assertGreater(suite.countTestCases(), 0, f"{kind} {name}: {test_name} not found")


if __name__ == "__main__":
    unittest.main()
