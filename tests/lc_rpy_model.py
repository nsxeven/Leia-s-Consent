"""Static model of the game's Ren'Py source: which definition actually wins.

Used by the structure, fingerprint and characterization tests so they follow a
screen/function/label wherever it lives, instead of hard-coding file paths.

Ren'Py rules mirrored here (checked against renpy-8.5.3 renpy/script.py and
renpy/parser.py):
* Script files load sorted by their path relative to game/ without extension;
  names sorting below "A" (e.g. "00_release_build") load first.
* Init code then runs stably sorted by priority. Priorities: `screen` -500,
  `image` 500, `define`/`default`/`transform` 0 (or an explicit number),
  `init N` / `init N python` N; every one is shifted by the file's current
  `init offset = K`. Statements inside an `init N:` block take N + offset.
  `python early` runs before all of them.
* For a name defined more than once, the definition that runs last wins.
  Screens are keyed by name plus `variant`.
* `config.label_overrides["a"] = "b"` makes `jump a` run label b.
"""
import hashlib
import re
from collections import namedtuple
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"

Def = namedtuple("Def", "kind name priority order relpath line body")

KINDS = ("screen", "label", "def", "class", "define", "default", "image", "transform", "assign", "style")

_INIT_OFFSET = re.compile(r"^init\s+offset\s*=\s*(-?\d+)")
_INIT_BLOCK = re.compile(r"^init(?:\s+(-?\d+))?\s*:")
_INIT_PY = re.compile(r"^init(?:\s+(-?\d+))?\s+python\b.*:")
_PY_EARLY = re.compile(r"^python\s+early\b.*:")
_SCREEN = re.compile(r"^screen\s+([A-Za-z_]\w*)")
_LABEL = re.compile(r"^label\s+([A-Za-z_][\w.]*)")
_DEFINE = re.compile(r"^(define|default)\s+(?:(-?\d+)\s+)?([A-Za-z_][\w.]*)\s*(?:=|\+=|\|=)")
_IMAGE = re.compile(r"^image\s+([^=:]+?)\s*(?:=|:)")
_TRANSFORM = re.compile(r"^transform\s+(?:(-?\d+)\s+)?([A-Za-z_]\w*)")
_STYLE = re.compile(r"^style\s+([A-Za-z_]\w*)")
_PYDEF = re.compile(r"^def\s+([A-Za-z_]\w*)")
_PYCLASS = re.compile(r"^class\s+([A-Za-z_]\w*)")
_PYASSIGN = re.compile(r"^([A-Za-z_][\w.]*)\s*=(?!=)")
_VARIANT = re.compile(r"^\s+variant\s+(['\"])(.+?)\1")
_OVERRIDE = re.compile(r"config\.label_overrides\[\s*['\"](\w+)['\"]\s*\]\s*=\s*['\"](\w+)['\"]")
_JUMP_ONLY = re.compile(r"^jump\s+(\w+)$")

EARLY = -10 ** 6


def rpy_files():
    files = [p for p in GAME.rglob("*.rpy") if "/tl/" not in p.as_posix()]

    def key(p):
        fn = p.relative_to(GAME).with_suffix("").as_posix()
        return (3 if fn >= "A" else 2, fn)

    return sorted(files, key=key)


def relpath(path):
    return path.relative_to(ROOT).as_posix()


def _indent(line):
    return len(line) - len(line.lstrip(" "))


def _block(lines, i):
    """Lines i.. of the block opened at line i (the header plus deeper lines)."""
    base = _indent(lines[i])
    out = [lines[i]]
    j = i + 1
    while j < len(lines):
        s = lines[j]
        if s.strip() and _indent(s) <= base:
            break
        out.append(s)
        j += 1
    while out and not out[-1].strip():
        out.pop()
    return out, j


def _normalise(block):
    base = _indent(block[0])
    keep = []
    for s in block:
        if not s.strip() or s.strip().startswith("#"):
            continue
        keep.append(s[base:].rstrip() if _indent(s) >= base else s.strip())
    return "\n".join(keep)


def _parse_file(path, file_index):
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    rel = relpath(path)
    offset = 0
    out = []
    seq = 0

    def add(kind, name, priority, i, block):
        nonlocal seq
        seq += 1
        out.append(Def(kind, name, priority, (priority, file_index, seq), rel, i + 1, _normalise(block)))

    def scan_python(start, end, priority):
        """Top-level def/class/assign inside an init python block body."""
        body = [k for k in range(start, end) if lines[k].strip() and not lines[k].strip().startswith("#")]
        if not body:
            return
        top = _indent(lines[body[0]])
        for k in body:
            s = lines[k]
            if _indent(s) != top:
                continue
            st = s.strip()
            m = _PYDEF.match(st) or _PYCLASS.match(st)
            if m:
                block, _ = _block(lines, k)
                add("def" if st.startswith("def") else "class", m.group(1), priority, k, block)
                continue
            m = _PYASSIGN.match(st)
            if m:
                block, _ = _block(lines, k)
                add("assign", m.group(1), priority, k, block)

    def scan_statements(start, end, priority, top):
        """Ren'Py statements at indentation `top` in lines[start:end]."""
        k = start
        while k < end:
            s = lines[k]
            st = s.strip()
            if not st or st.startswith("#") or _indent(s) != top:
                k += 1
                continue
            block, nxt = _block(lines, k)
            nxt = min(nxt, end)
            m = _SCREEN.match(st)
            if m:
                variant = next((v.group(2) for v in map(_VARIANT.match, block[1:]) if v), None)
                name = m.group(1) + (f"@{variant}" if variant else "")
                add("screen", name, priority if priority is not None else -500 + offset, k, block)
            elif _LABEL.match(st):
                add("label", _LABEL.match(st).group(1), 0, k, block)
            elif _DEFINE.match(st):
                d = _DEFINE.match(st)
                pr = priority if priority is not None else int(d.group(2) or 0) + offset
                add(d.group(1), d.group(3), pr, k, block)
            elif _TRANSFORM.match(st):
                t = _TRANSFORM.match(st)
                pr = priority if priority is not None else int(t.group(1) or 0) + offset
                add("transform", t.group(2), pr, k, block)
            elif _IMAGE.match(st):
                add("image", " ".join(_IMAGE.match(st).group(1).split()), priority if priority is not None else 500 + offset, k, block)
            elif _STYLE.match(st):
                add("style", _STYLE.match(st).group(1), priority if priority is not None else offset, k, block)
            elif _PY_EARLY.match(st):
                scan_python(k + 1, nxt, EARLY)
            elif st.startswith("python") and st.endswith(":") and priority is not None:
                scan_python(k + 1, nxt, priority)
            k = nxt

    i = 0
    while i < len(lines):
        s = lines[i]
        st = s.strip()
        if not st or st.startswith("#") or _indent(s) != 0:
            i += 1
            continue
        m = _INIT_OFFSET.match(st)
        if m:
            offset = int(m.group(1))
            i += 1
            continue
        block, nxt = _block(lines, i)
        m = _INIT_PY.match(st)
        if m:
            scan_python(i + 1, nxt, int(m.group(1) or 0) + offset)
        elif _PY_EARLY.match(st):
            scan_python(i + 1, nxt, EARLY)
        elif _INIT_BLOCK.match(st):
            pr = int(_INIT_BLOCK.match(st).group(1) or 0) + offset
            inner = [k for k in range(i + 1, nxt) if lines[k].strip()]
            if inner:
                scan_statements(i + 1, nxt, pr, _indent(lines[inner[0]]))
        else:
            scan_statements(i, nxt, None, 0)
        i = nxt
    return out


_CACHE = {}


def all_definitions():
    if "all" not in _CACHE:
        defs = []
        for index, path in enumerate(rpy_files()):
            defs.extend(_parse_file(path, index))
        _CACHE["all"] = defs
    return _CACHE["all"]


def definitions(kind):
    assert kind in KINDS, kind
    return [d for d in all_definitions() if d.kind == kind]


def effective(kind):
    """{name: winning Def}; for 'style' the last block (see style_chain)."""
    table = {}
    for d in sorted(definitions(kind), key=lambda d: d.order):
        table[d.name] = d
    return table


def duplicates(kind):
    seen = {}
    for d in definitions(kind):
        seen.setdefault(d.name, []).append(d)
    return {n: ds for n, ds in seen.items() if len(ds) > 1}


def style_chain(name):
    """Every block for one style in run order: later blocks add/override properties."""
    return [d for d in sorted(definitions("style"), key=lambda d: d.order) if d.name == name]


def label_overrides():
    pairs = {}
    for path in rpy_files():
        text = path.read_text(encoding="utf-8")
        for m in _OVERRIDE.finditer(text):
            pairs[m.group(1)] = m.group(2)
    return pairs


def effective_label_body(name, _seen=None):
    """Body that actually runs for `jump name`: follows label_overrides and
    labels whose whole body is a single `jump other` (compatibility aliases)."""
    seen = _seen or set()
    if name in seen:
        return None
    seen.add(name)
    labels = effective("label")
    target = label_overrides().get(name, name)
    d = labels.get(target)
    if d is None:
        return None
    rest = d.body.split("\n")[1:]
    if len(rest) == 1:
        m = _JUMP_ONLY.match(rest[0].strip())
        if m:
            resolved = effective_label_body(m.group(1), seen)
            if resolved is not None:
                return resolved
    return "\n".join(rest)


def fingerprint(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]


def body_without_header(d):
    """Definition body minus its first line (so moving a screen into an init
    block or changing only its priority prefix does not change the print)."""
    return "\n".join(d.body.split("\n")[1:])
