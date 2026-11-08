"""Story menus as data (no Ren'Py): every `menu:` in the story files with, per
option, the choice id its caption shows (format_choice / gate formatters) and the
choice id(s) its branch applies. Used by tests/test_choice_path_tags.py.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
NOT_STORY = ("dev_sandbox.rpy", "story_state_test.rpy", "systems_vertical_slice.rpy")

FORMATTERS = r"format_choice|format_day\d+_\w*choice"
FORMAT_ASSIGN = re.compile(r'^\s*\$\s*(\w+)\s*=\s*(?:' + FORMATTERS + r')\(\s*"(\w+)"')
FORMAT_ANY = re.compile(r'\b(?:' + FORMATTERS + r')\(\s*"(\w+)"')
APPLY = re.compile(r'apply_choice\(\s*"(\w+)"\s*\)')
CAPTION = re.compile(r'^(\s*)"((?:[^"\\]|\\.)*)"\s*(?:if\s+.+)?:\s*$')
MENU = re.compile(r"^\s*menu\s*\w*\s*:\s*$")
LABEL = re.compile(r"^label\s+(\w+)")


def story_files():
    return sorted(p for p in (GAME / "chapters").rglob("*.rpy") if p.name not in NOT_STORY)


def formatted_ids(path):
    return set(FORMAT_ANY.findall(path.read_text(encoding="utf-8")))


def applied_ids(path):
    return set(APPLY.findall(path.read_text(encoding="utf-8")))


def _indent(line):
    return len(line) - len(line.lstrip(" "))


def menus():
    """[{file, line, label, options: [{line, caption, shown: set, applied: list}]}]"""
    out = []
    for path in story_files():
        rel = path.relative_to(GAME).as_posix()
        lines = path.read_text(encoding="utf-8").splitlines()
        assigned = {}  # var -> [(line_no, choice_id)]
        label = None
        for n, raw in enumerate(lines):
            found = LABEL.match(raw)
            if found:
                label = found.group(1)
            found = FORMAT_ASSIGN.match(raw)
            if found:
                assigned.setdefault(found.group(1), []).append((n, found.group(2)))
            if not MENU.match(raw):
                continue
            base = _indent(raw)
            options, current, nested_at = [], None, None
            for j in range(n + 1, len(lines)):
                s = lines[j]
                if not s.strip() or s.strip().startswith("#"):
                    continue
                ind = _indent(s)
                if ind <= base:
                    break
                cap = CAPTION.match(s)
                if cap and ind == base + 4:
                    current = {"line": j + 1, "caption": cap.group(2), "applied": []}
                    nested_at = None
                    options.append(current)
                    continue
                if current is None:
                    continue
                if nested_at is not None and ind > nested_at:
                    continue
                nested_at = None
                if MENU.match(s):
                    nested_at = ind
                    continue
                current["applied"] += APPLY.findall(s)
            for opt in options:
                var = re.fullmatch(r"\[(\w+)\]", opt["caption"])
                shown = set()
                if var and var.group(1) in assigned:
                    defs = [d for d in assigned[var.group(1)] if d[0] < n]
                    if defs:
                        last = defs[-1][0]
                        # if/else pairs assign the same variable a few lines apart
                        shown = {cid for ln, cid in defs if ln >= last - 40}
                opt["shown"] = shown
            if options:
                out.append({"file": rel, "line": n + 1, "label": label, "options": options})
    return out
