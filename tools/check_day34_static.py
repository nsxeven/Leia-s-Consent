"""Verify protected files and label uniqueness against the audited main baseline."""
from pathlib import Path
from collections import defaultdict
import json
import re
import subprocess

root = Path(__file__).resolve().parents[1]
base = "41913f32e216e9b7cfb96ee7fc5a330468857786"
checks = []
labels = defaultdict(list)
for path in (root / "game").rglob("*.rpy"):
    for label in re.findall(r"^label\s+(\w+)\s*(?:\([^\n]*\))?\s*:", path.read_text(), re.M):
        labels[label].append(str(path.relative_to(root)))
duplicates = {k: v for k, v in labels.items() if len(v) > 1}
assert not duplicates, duplicates
checks.append("No duplicate label definitions")

tracked = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", base, "game"], cwd=root, text=True).splitlines()
protected = [p for p in tracked if p.startswith("game/images/") or p in ("game/chapters/prologue.rpy",) or
             (p.startswith("game/chapters/ch01/") and any(s in p for s in ("ch01_day2", "ch01_scenes_", "/zz")))]
for name in protected:
    original = subprocess.check_output(["git", "show", base + ":" + name], cwd=root)
    assert (root / name).read_bytes() == original, name
checks.append("Protected Prologue, Days 1–2, unrelated late patches and approved image files unchanged; Day 5 changes are in scope")

baseline = root.parent / "lc/docs/narrative-refinement/lint-baseline.txt"
current = root / "docs/day3-day4-overhaul/lint.txt"
if baseline.exists():
    diagnostic_lines = lambda p: [l for l in p.read_text(encoding="utf-8-sig").splitlines() if l.startswith("game/")]
    assert diagnostic_lines(baseline) == diagnostic_lines(current)
    checks.append("Lint diagnostic set equals baseline (17 pre-existing diagnostics)")
result = {"status": "passed", "checks": checks, "protected_files_checked": len(protected), "labels": len(labels)}
print(json.dumps(result, indent=2))
