"""Static model of the game's Ren'Py source: which definition actually wins.

Used by the structure, fingerprint and characterization tests so they follow a
screen/function/label wherever it lives, instead of hard-coding file paths.

Ren'Py rules mirrored here (checked against renpy-8.5.3 renpy/script.py,
renpy/parser.py and common/00layeredimage_ren.py, and against an engine-side
dump of the winners during review of PR #215):
* Script files load sorted by their path relative to game/ without extension;
  names sorting below "A" (e.g. "00_release_build") load first.
* Init code then runs stably sorted by priority. Priorities: `screen` -500,
  `image` 500, `define`/`default`/`transform`/`layeredimage`/`style` 0 (or an
  explicit number), `init N` / `init N python` N; every one is shifted by the
  file's current `init offset = K`. Statements inside `init N:` take N + offset.
  `python early` runs before all of them.
* For a name defined more than once, the definition that runs last wins.
  Screens and styles are keyed by name plus `variant`.
* `config.label_overrides["a"] = "b"` makes `jump a` run label b.
* Top-level init-python statements that are not def/class/simple assignment
  (overlay registrations, table updates, loops) are kept as kind "effect".
"""
import hashlib
import re
from collections import namedtuple
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"

Def = namedtuple("Def", "kind name priority order relpath line body")

KINDS = ("screen", "label", "def", "class", "define", "default", "image", "layeredimage",
         "transform", "assign", "effect", "style", "pyblock")

_INIT_OFFSET = re.compile(r"^init\s+offset\s*=\s*(-?\d+)")
_INIT_BLOCK = re.compile(r"^init(?:\s+(-?\d+))?\s*:")
_INIT_PY = re.compile(r"^init(?:\s+(-?\d+))?\s+python\b.*:")
_PY_EARLY = re.compile(r"^python\s+early\b.*:")
_SCREEN = re.compile(r"^screen\s+([A-Za-z_]\w*)")
_LABEL = re.compile(r"^label\s+([A-Za-z_][\w.]*)")
_DEFINE = re.compile(r"^(define|default)\s+(?:(-?\d+)\s+)?([A-Za-z_][\w.]*)\s*(?:=|\+=|\|=)")
_IMAGE = re.compile(r"^image\s+([^=:]+?)\s*(?:=|:)")
_LAYERED = re.compile(r"^layeredimage\s+([^:]+?)\s*:")
_TRANSFORM = re.compile(r"^transform\s+(?:(-?\d+)\s+)?([A-Za-z_]\w*)")
_STYLE = re.compile(r"^style\s+([A-Za-z_]\w*)")
_PYDEF = re.compile(r"^def\s+([A-Za-z_]\w*)")
_PYCLASS = re.compile(r"^class\s+([A-Za-z_]\w*)")
_PYASSIGN = re.compile(r"^([A-Za-z_][\w.]*)\s*=(?!=)")
_VARIANT = re.compile(r"^\s+variant\s+(.+?)\s*$")
_OVERRIDE = re.compile(r"config\.label_overrides\[\s*['\"](\w+)['\"]\s*\]\s*=\s*['\"](\w+)['\"]")
_JUMP_ONLY = re.compile(r"^jump\s+(\w+)$")
_STRING = re.compile(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"")

EARLY = -10 ** 6


def rpy_files():
    files = [p for p in GAME.rglob("*.rpy")
             if not p.relative_to(GAME).as_posix().startswith("tl/")]

    def key(p):
        fn = p.relative_to(GAME).with_suffix("").as_posix()
        return (3 if fn >= "A" else 2, fn)

    return sorted(files, key=key)


def relpath(path):
    return path.relative_to(ROOT).as_posix()


def read(path):
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def _indent(line):
    return len(line) - len(line.lstrip(" "))


def _code_parts(line, in_triple):
    """Code on a line outside triple-quoted strings; returns (code, still_open_quote)."""
    code = []
    rest = line
    while rest:
        if in_triple:
            j = rest.find(in_triple)
            if j < 0:
                return "".join(code), in_triple
            rest, in_triple = rest[j + 3:], None
        else:
            hits = [(rest.find(q), q) for q in ('"""', "'''") if rest.find(q) >= 0]
            if not hits:
                code.append(rest)
                break
            j, q = min(hits)
            code.append(rest[:j])
            rest, in_triple = rest[j + 3:], q
    return "".join(code), in_triple


def _depth_change(code):
    s = _STRING.sub("", code).split("#", 1)[0]
    return sum(s.count(c) for c in "([{") - sum(s.count(c) for c in ")]}")


def _block(lines, i):
    """Lines i.. of the block opened at line i (the header plus deeper lines).

    Open brackets or an open triple-quoted string keep the statement going even
    when a continuation line (e.g. a closing `):`) is back at the header indent."""
    base = _indent(lines[i])
    out = [lines[i]]
    code, triple = _code_parts(lines[i], None)
    depth = _depth_change(code)
    j = i + 1
    while j < len(lines):
        s = lines[j]
        if depth <= 0 and not triple and s.strip() and _indent(s) <= base:
            break
        code, triple_after = _code_parts(s, triple)
        if depth > 0 or triple:
            depth += _depth_change(code)
        triple = triple_after
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


def _variant(block):
    for line in block[1:]:
        v = _VARIANT.match(line)
        if v and _indent(line) > _indent(block[0]):
            names = re.findall(r"['\"]([^'\"]+)['\"]", v.group(1))
            return ",".join(names) if names else v.group(1)
    return None


def parse_text(text, rel, file_index):
    lines = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    offset = 0
    out = []
    seq = 0

    def add(kind, name, priority, i, block):
        nonlocal seq
        seq += 1
        out.append(Def(kind, name, priority, (priority, file_index, seq), rel, i + 1, _normalise(block)))

    def scan_python(start, end, priority):
        """Top-level statements inside an init python block body."""
        body = [k for k in range(start, end) if lines[k].strip() and not lines[k].strip().startswith("#")]
        if not body:
            return
        top = _indent(lines[body[0]])
        k = body[0]
        while k < end:
            s = lines[k]
            st = s.strip()
            if not st or st.startswith("#") or _indent(s) != top:
                k += 1
                continue
            block, nxt = _block(lines, k)
            nxt = min(nxt, end)
            md = _PYDEF.match(st) or _PYCLASS.match(st)
            if md:
                add("def" if st.startswith("def") else "class", md.group(1), priority, k, block)
            elif _PYASSIGN.match(st):
                add("assign", _PYASSIGN.match(st).group(1), priority, k, block)
            elif not st.startswith("@"):
                add("effect", _normalise(block), priority, k, block)
            k = nxt

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

            def pr(default, explicit=None):
                if priority is not None:
                    return priority
                return (int(explicit) if explicit else default) + offset

            if _SCREEN.match(st):
                variant = _variant(block)
                name = _SCREEN.match(st).group(1) + (f"@{variant}" if variant else "")
                add("screen", name, pr(-500), k, block)
            elif _LABEL.match(st):
                add("label", _LABEL.match(st).group(1), 0, k, block)
            elif _DEFINE.match(st):
                d = _DEFINE.match(st)
                add(d.group(1), d.group(3), pr(0, d.group(2)), k, block)
            elif _TRANSFORM.match(st):
                t = _TRANSFORM.match(st)
                add("transform", t.group(2), pr(0, t.group(1)), k, block)
            elif _LAYERED.match(st):
                add("layeredimage", " ".join(_LAYERED.match(st).group(1).split()), pr(0), k, block)
            elif _IMAGE.match(st):
                add("image", " ".join(_IMAGE.match(st).group(1).split()), pr(500), k, block)
            elif _STYLE.match(st):
                variant = _variant(block)
                name = _STYLE.match(st).group(1) + (f"@{variant}" if variant else "")
                add("style", name, pr(0), k, block)
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
        mo = _INIT_OFFSET.match(st)
        if mo:
            offset = int(mo.group(1))
            i += 1
            continue
        block, nxt = _block(lines, i)
        mp = _INIT_PY.match(st)
        if mp:
            # Whole block too (kind "pyblock", named by file) so tests can exec it as the game does.
            add("pyblock", rel, int(mp.group(1) or 0) + offset, i, block)
            scan_python(i + 1, nxt, int(mp.group(1) or 0) + offset)
        elif _PY_EARLY.match(st):
            scan_python(i + 1, nxt, EARLY)
        elif _INIT_BLOCK.match(st):
            pri = int(_INIT_BLOCK.match(st).group(1) or 0) + offset
            inner = [k for k in range(i + 1, nxt) if lines[k].strip()]
            if inner:
                scan_statements(i + 1, nxt, pri, _indent(lines[inner[0]]))
        else:
            scan_statements(i, nxt, None, 0)
        i = nxt
    return out


_CACHE = {}


def all_definitions():
    if "all" not in _CACHE:
        defs = []
        for index, path in enumerate(rpy_files()):
            defs.extend(parse_text(read(path), relpath(path), index))
        _CACHE["all"] = defs
    return _CACHE["all"]


def definitions(kind):
    assert kind in KINDS, kind
    return [d for d in all_definitions() if d.kind == kind]


def in_run_order(kinds=KINDS):
    return sorted((d for d in all_definitions() if d.kind in kinds), key=lambda d: d.order)


def effective(kind):
    """{name: winning Def} (for 'style', see style_chain)."""
    table = {}
    for d in in_run_order((kind,)):
        table[d.name] = d
    return table


def duplicates(kind):
    seen = {}
    for d in definitions(kind):
        seen.setdefault(d.name, []).append(d)
    return {n: ds for n, ds in seen.items() if len(ds) > 1}


def style_chain(name):
    """Every block for one style (name or name@variant) in run order."""
    return [d for d in in_run_order(("style",)) if d.name == name]


def overrides_in_text(text):
    pairs = {}
    for line in text.split("\n"):
        if line.lstrip().startswith("#"):
            continue
        for mo in _OVERRIDE.finditer(line):
            pairs[mo.group(1)] = mo.group(2)
    return pairs


def label_overrides():
    pairs = {}
    for path in rpy_files():
        pairs.update(overrides_in_text(read(path)))
    return pairs


def files_using_overrides():
    return {relpath(p) for p in rpy_files() if overrides_in_text(read(p))}


def overlay_order():
    """config.overlay_screens / always_shown_screens registrations in run order."""
    out = {"overlay_screens": [], "always_shown_screens": []}
    pat = re.compile(r"config\.(overlay_screens|always_shown_screens)\.append\(\s*['\"](\w+)['\"]")
    for d in in_run_order(("effect", "assign", "define")):
        for mo in pat.finditer(d.body):
            if mo.group(2) not in out[mo.group(1)]:
                out[mo.group(1)].append(mo.group(2))
    return out


def effective_label_body(name, _seen=None):
    """Parameters + body that actually run for `jump name`: follows
    label_overrides and labels whose whole body is a single `jump other`
    (compatibility aliases)."""
    seen = _seen or set()
    if name in seen:
        return None
    seen.add(name)
    labels = effective("label")
    target = label_overrides().get(name, name)
    d = labels.get(target)
    if d is None:
        return None
    header, *rest = d.body.split("\n")
    if len(rest) == 1:
        mo = _JUMP_ONLY.match(rest[0].strip())
        if mo:
            resolved = effective_label_body(mo.group(1), seen)
            if resolved is not None:
                return resolved
    params = header[header.find("("):] if "(" in header else ""
    return params + "\n" + "\n".join(rest)


def fingerprint(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]


def body_without_header(d):
    return "\n".join(d.body.split("\n")[1:])
