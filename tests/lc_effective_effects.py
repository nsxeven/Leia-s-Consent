"""Read the EFFECTIVE CHOICE_EFFECTS table from the game's .rpy files (no Ren'Py).

Every `CHOICE_EFFECTS = {...}` / `CHOICE_EFFECTS.update({...})` literal is
collected with the init priority of the block it sits in. Ren'Py runs init
blocks by priority, then file order, so later definitions win; that gives the
table the game actually uses (e.g. systems/stat_model_v2_later_days.rpy at
init 5 re-scores the Scriptwriter-owned Day 3-5 registrations at init 1).
"""
import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
_INIT = re.compile(r"^init(?:\s+(-?\d+))?\s+python\b", re.M)
_LITERAL = re.compile(r"CHOICE_EFFECTS(?:\s*=\s*|\.update\(\s*)\{")


def _balanced(text, start):
    pairs = {"(": ")", "{": "}", "[": "]"}
    stack, i, quote = [], start, None
    while i < len(text):
        c = text[i]
        if quote:
            if c == "\\":
                i += 2
                continue
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
        elif c == "#":
            j = text.find("\n", i)
            i = j if j != -1 else len(text)
            continue
        elif c in pairs:
            stack.append(pairs[c])
        elif c in ")}]":
            stack.pop()
            if not stack:
                return i + 1
        i += 1
    raise ValueError("unbalanced literal")


def rpy_files():
    return sorted(p for p in GAME.rglob("*.rpy") if "/tl/" not in p.as_posix())


def definitions():
    """[(priority, relpath, choice_id, effects)] for every literal entry."""
    out = []
    for path in rpy_files():
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(GAME).as_posix()
        for m in _LITERAL.finditer(text):
            line_start = text.rfind("\n", 0, m.start()) + 1
            if text[line_start:m.start()].lstrip().startswith("#"):
                continue
            inits = [i for i in _INIT.finditer(text) if i.start() < m.start()]
            priority = int(inits[-1].group(1) or 0) if inits else 0
            body_start = m.end() - 1
            literal = ast.literal_eval(text[body_start:_balanced(text, body_start)])
            for choice_id, effects in literal.items():
                out.append((priority, rel, choice_id, [tuple(e) for e in effects]))
    return out


def effective_effects():
    table = {}
    for _priority, _rel, choice_id, effects in sorted(definitions(), key=lambda d: (d[0], d[1])):
        table[choice_id] = effects
    return table


def applied_choice_ids():
    ids = set()
    for path in rpy_files():
        ids |= set(re.findall(r'apply_choice\("(\w+)"\)', path.read_text(encoding="utf-8")))
    return ids
