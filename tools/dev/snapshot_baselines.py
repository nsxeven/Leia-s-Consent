"""Snapshot the behaviour pins used by the clean-up guard-rail tests.

    python tools/dev/snapshot_baselines.py

Writes tests/data/effective_fingerprints.json (what each effective screen,
function, label, define, ... looks like) and tests/data/save_names_baseline.json
(every runtime name a save file or story code may refer to). Re-run it only
when a change is MEANT to alter behaviour or add names, and say so in the PR.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests"))

import lc_rpy_model as m  # noqa: E402
from lc_save_names import save_names  # noqa: E402

PINNED_KINDS = ("screen", "def", "class", "define", "default", "transform", "image", "assign")


def style_print(name):
    """Final merged properties of a style: later blocks override earlier keys."""
    merged = {}
    for d in m.style_chain(name):
        header, *rest = d.body.split("\n")
        if " is " in header:
            merged["is"] = header.split(" is ", 1)[1].rstrip(":").strip()
        for line in rest:
            s = line.strip()
            key = s if s.startswith("properties") else s.split(" ", 1)[0]
            merged[key] = s
    return m.fingerprint(json.dumps(merged, sort_keys=True))


def fingerprints():
    out = {}
    for kind in PINNED_KINDS:
        out[kind] = {name: m.fingerprint(d.body) for name, d in sorted(m.effective(kind).items())}
    out["label"] = {name: m.fingerprint(m.effective_label_body(name) or "")
                    for name in sorted(m.effective("label"))}
    out["style"] = {name: style_print(name) for name in sorted({d.name for d in m.definitions("style")})}
    return out


def main():
    data = ROOT / "tests" / "data"
    data.mkdir(exist_ok=True)
    (data / "effective_fingerprints.json").write_text(
        json.dumps(fingerprints(), indent=1, sort_keys=True) + "\n", encoding="utf-8")
    (data / "save_names_baseline.json").write_text(
        json.dumps({k: sorted(v) for k, v in save_names().items()}, indent=1, sort_keys=True) + "\n",
        encoding="utf-8")
    print("wrote", data)


if __name__ == "__main__":
    main()
