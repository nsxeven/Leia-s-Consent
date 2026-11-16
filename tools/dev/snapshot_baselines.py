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
from lc_effective_effects import effective_effects  # noqa: E402
from lc_save_names import save_names  # noqa: E402

PINNED_KINDS = ("screen", "def", "class", "define", "default", "transform", "image",
                "layeredimage", "assign")


def pinned_effect(d):
    """Init side effects worth pinning: everything except imports (merging files
    may drop a duplicate import harmlessly) and label_overrides entries (the
    label pins already resolve them, so folding one is proved there)."""
    first = d.body.split("\n", 1)[0]
    return not (first.startswith(("import ", "from ")) or first.startswith("config.label_overrides["))


def effect_counts():
    """Multiset of init side-effect statements: moving one to another file keeps
    the count; dropping, duplicating or editing one changes it."""
    counts = {}
    for d in m.definitions("effect"):
        if pinned_effect(d):
            key = d.body.split("\n", 1)[0][:90] + " #" + m.fingerprint(d.body)
            counts[key] = counts.get(key, 0) + 1
    return counts


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
    out["effect"] = effect_counts()
    # Order-sensitive outcomes: overlay stacking and the final choice table.
    out["overlay_order"] = m.overlay_order()
    out["choice_effects"] = {"table": m.fingerprint(json.dumps(effective_effects(), sort_keys=True))}
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
