"""Structure rules that keep the codebase from growing load-order patches again.

Every ALLOW_* set lists what existed when the rules were introduced (main
226101b). Rule for editors: SHRINK, NEVER GROW. When you fold an entry into its
owning file, delete it from the set; the test then keeps it from coming back.
To change a definition, edit the file that owns it; do not add a later file,
a `zz*` filename or a `config.label_overrides` entry.

Days 3-5 story files are out of scope for the clean-up and stay listed in
OUT_OF_SCOPE until their own pass.
"""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))

import lc_rpy_model as m  # noqa: E402
from lc_effective_effects import effective_effects  # noqa: E402

# Definitions that are knowingly duplicated today: shrink, never grow.
ALLOW_DUP = {
    # 26 dead duplicate screens and 6 dead defs removed in clean-up PR 2a.
    "screen": set(),
    # 4 load-time wrapper chains folded into hooks (game/systems/lc_hooks.rpy) in PR 2b.
    "def": set(),
    "label": set(),
}

# Load-order patch files (game/-relative): shrink, never grow.
# systems/ and screens/ entries were retired in clean-up PR 2c, chapter files in PR 3.
ALLOW_PATCH_FILES = set()

# Files that may still contain config.label_overrides: shrink, never grow.
# The last five overrides were folded into their labels in clean-up PR 3.
ALLOW_OVERRIDES = set()

# Days 3-5 belong to their own later pass; their Day 4/5 track-text helpers are
# re-scored in systems/stat_model_v2_later_days.rpy on purpose.
OUT_OF_SCOPE = {"ch01_day3_", "ch01_day4_", "ch01_day5_"}
OUT_OF_SCOPE_DUP = {"def": {"ch01_d4_track_text", "ch01_d5_track_text"}}

PATCH_NAME = re.compile(r"^z+_|_patch\.rpy$")


def game_rel(path):
    return path.relative_to(m.GAME).as_posix()


# Header block every game/systems/*.rpy and game/screens/*.rpy opens with (clean-up
# PR 5). The tests below keep those headers honest: the Public API and Internal lists
# may only name things the file really defines, and every path a header or
# docs/ARCHITECTURE.md mentions must exist.
HEADED_DIRS = ("systems", "screens")
HEADER_SECTION = re.compile(r"^# [A-Z][^:]*:")
API_ENTRY = re.compile(r"^#   (?:(screen|define|default|transform|label|class|style)\s+)?([A-Za-z_][\w.]*)")
# Public API layout: an entry starts 3 spaces after "#", its wrapped meaning text 7 spaces.
# Any other indentation is ambiguous (an entry indented 4-6 spaces used to be read as a
# continuation and skipped), and so is a continuation line that reads like a signature.
API_ENTRY_INDENT, API_CONT_INDENT = 3, 7
LOOKS_LIKE_ENTRY = re.compile(r"^#\s+(?:(?:screen|transform|label|class)\s+)?[A-Za-z_][\w.]*\(")
SIGNATURE_KINDS = ("screen", "label", "transform", "class")
TOP_LEVEL_PYTHON = re.compile(r"^(?:init\b[^:]*\bpython\b|python\s+early\b)[^:]*:")
TOP_LEVEL_DEF = re.compile(r"^    (?:def|class)\s+([A-Za-z_]\w*)")
HEADER_PATH = re.compile(r"(?<![\w/.-])((?:game|docs|tests|tools)/[\w./-]+\.(?:rpy|py|md|json|bat)"
                         r"|(?:systems|screens|chapters|dev|python-packages)/[\w./-]+\.(?:rpy|py))")
DOC_PATH = re.compile(r"`((?:game|tools|tests|docs)/[^`\s]*)`")


def headed_files():
    return sorted(p for d in HEADED_DIRS for p in (m.GAME / d).glob("*.rpy"))


def leading_comments(path):
    """The comment lines a file opens with (blank lines kept as "")."""
    out = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        s = line.strip()
        if s and not s.startswith("#"):
            break
        out.append(line.rstrip())
    return out


def header_sections(lines):
    """{section name: [lines]} for "# Name...:" sections; "#" or a blank line ends one."""
    sections, current = {}, None
    for line in lines:
        if HEADER_SECTION.match(line):
            current = line[2:].split(":", 1)[0].split(" (", 1)[0].strip()
            sections[current] = [line]
        elif current and line.startswith("#") and line.strip() != "#":
            sections[current].append(line)
        else:
            current = None
    return sections


def public_api_entries(path):
    """([(kind or None, name, line)], [problems]) for the Public API section of a header."""
    entries, problems = [], []
    for line in header_sections(leading_comments(path)).get("Public API", [])[1:]:
        indent = len(line) - len(line[1:].lstrip(" ")) - 1
        if indent == API_CONT_INDENT and not LOOKS_LIKE_ENTRY.match(line):
            continue  # continuation of the previous entry's meaning
        entry = API_ENTRY.match(line) if indent == API_ENTRY_INDENT else None
        if entry:
            entries.append((entry.group(1), entry.group(2), line))
        elif indent in (API_ENTRY_INDENT, API_CONT_INDENT):
            problems.append(f"{game_rel(path)}: unreadable Public API line {line!r}")
        else:
            problems.append(f"{game_rel(path)}: ambiguous Public API line {line!r} (entries are indented "
                            f"{API_ENTRY_INDENT} spaces after '#', wrapped meaning text {API_CONT_INDENT})")
    return entries, problems


def header_args(line, name):
    """The text between the parentheses after `name` in a header entry, or None."""
    start = line.find(name + "(")
    if start < 0:
        return None
    start += len(name)
    depth = 0
    for end in range(start, len(line)):
        depth += {"(": 1, ")": -1}.get(line[end], 0)
        if depth == 0:
            return line[start + 1:end]
    return None


def _norm_args(args):
    return re.sub(r",$", "", re.sub(r"\s+", "", args))


def internal_names(path):
    internal = " ".join(l[1:] for l in header_sections(leading_comments(path)).get("Internal", []))
    return [n for n in re.split(r"[,\s]+", internal.split(":", 1)[1] if ":" in internal else "") if n]


def top_level_defs(text):
    """Names of the defs/classes at the top of `init python` / `python early` blocks."""
    names, in_python = [], False
    for line in text.splitlines():
        if line and not line[0].isspace() and not line.startswith("#"):
            in_python = bool(TOP_LEVEL_PYTHON.match(line))
        elif in_python:
            found = TOP_LEVEL_DEF.match(line)
            if found:
                names.append(found.group(1))
    return names


def is_defined(text, kind, name):
    n = re.escape(name)
    any_kind = (rf"^\s*(?:def|class|screen|transform|label|style)\s+{n}\b"
                rf"|^\s*(?:define|default)\s+(?:-?\d+\s+)?{n}\b|^\s*{n}\s*=")
    pattern = {
        "define": rf"^\s*define\s+(?:-?\d+\s+)?{n}\b",
        "default": rf"^\s*default\s+(?:-?\d+\s+)?{n}\b",
    }.get(kind, rf"^\s*{kind}\s+{n}\b" if kind else any_kind)
    return re.search(pattern, text, re.M) is not None


class StructureRuleTests(unittest.TestCase):
    def test_no_new_duplicate_definitions(self):
        for kind, allowed in ALLOW_DUP.items():
            dups = set(m.duplicates(kind)) - allowed - OUT_OF_SCOPE_DUP.get(kind, set())
            self.assertEqual(dups, set(), f"{kind} defined more than once; edit the owning file instead")

    def test_allow_lists_only_shrink(self):
        """An allow-list entry that is already fixed must be removed from the list."""
        for kind, allowed in ALLOW_DUP.items():
            stale = allowed - set(m.duplicates(kind))
            self.assertEqual(stale, set(), f"remove fixed {kind} entries from ALLOW_DUP")
        present = {game_rel(p) for p in m.rpy_files()}
        self.assertEqual(ALLOW_PATCH_FILES - present, set(), "remove deleted files from ALLOW_PATCH_FILES")

    def test_no_new_patch_files(self):
        patch_files = {game_rel(p) for p in m.rpy_files() if PATCH_NAME.search(p.name)}
        self.assertEqual(patch_files - ALLOW_PATCH_FILES, set(),
                         "no new zz*/ *_patch.rpy files: edit the owning file")

    def test_no_new_label_overrides(self):
        users = {game_rel(p) for p in m.rpy_files() if m.overrides_in_text(m.read(p))}
        self.assertEqual(users - ALLOW_OVERRIDES, set(),
                         "no new config.label_overrides: edit the label itself")
        self.assertEqual(ALLOW_OVERRIDES - users, set(), "remove fixed files from ALLOW_OVERRIDES")

    def test_every_hidden_pov_moment_is_used(self):
        text = "\n".join(p.read_text(encoding="utf-8") for p in m.rpy_files())
        registered = set(re.findall(r"lc_pov_register\(\s*['\"](\w+)", text))
        begun = set(re.findall(r"lc_pov_begin\(\s*['\"](\w+)", text))
        self.assertEqual(registered - begun, set(), "registered Hidden POV moment never begins")
        self.assertEqual(begun - registered, set(), "lc_pov_begin for an unregistered moment")

    def test_every_story_choice_id_is_registered(self):
        effects = effective_effects()
        missing = []
        for path in m.rpy_files():
            if "/chapters/" not in path.as_posix():
                continue
            for cid in re.findall(r"\b(?:apply_choice|format_choice|format_\w*choice)\(\s*['\"](\w+)",
                                  path.read_text(encoding="utf-8")):
                if cid not in effects:
                    missing.append(f"{path.name}: {cid}")
        self.assertEqual(missing, [])

    def test_no_empty_python_blocks(self):
        """Deleting the last statement of an `init python:` block is a script error at
        launch that lint does not report (seen in clean-up PR 2a)."""
        empty = [f"{d.relpath}:{d.line}" for d in m.definitions("pyblock")
                 if not m.body_without_header(d).strip()]
        self.assertEqual(empty, [])

    def test_no_orphan_compiled_scripts(self):
        """Ren'Py still loads a .rpyc whose .rpy was moved or deleted (local builds only)."""
        orphans = [p.relative_to(m.GAME).as_posix() for p in m.GAME.rglob("*.rpyc")
                   if not p.with_suffix(".rpy").exists()]
        self.assertEqual(orphans, [], "delete stale .rpyc files left behind by a move")

    def test_paths_named_in_tests_exist(self):
        """A moved file must take its tests with it, or they silently test nothing."""
        ref = re.compile(r"['\"]((?:game|tests|tools|docs)/[\w./-]+\.(?:rpy|py|md|json))['\"]")
        missing = []
        for test in (ROOT / "tests").glob("*.py"):
            for rel in ref.findall(test.read_text(encoding="utf-8")):
                if not (ROOT / rel).exists():
                    missing.append(f"{test.name}: {rel}")
        self.assertEqual(missing, [])


    def test_system_and_screen_files_open_with_header(self):
        """Every system/screen file starts with the documented header block."""
        missing = []
        for path in headed_files():
            head = "\n".join(leading_comments(path))
            for needed in ("# Purpose:", "# Public API"):
                if needed not in head:
                    missing.append(f"{game_rel(path)}: no {needed!r} in the opening comment block")
        self.assertEqual(missing, [])

    def test_header_api_names_are_defined(self):
        """Names listed under Public API / Internal must exist in that file, so headers cannot rot."""
        problems = []
        for path in headed_files():
            text = m.read(path)
            entries, unreadable = public_api_entries(path)
            problems += unreadable
            for kind, name, _line in entries:
                if not is_defined(text, kind, name):
                    problems.append(f"{game_rel(path)}: Public API names {name!r}, not defined here")
            for name in internal_names(path):
                if not is_defined(text, None, name):
                    problems.append(f"{game_rel(path)}: Internal names {name!r}, not defined here")
        self.assertEqual(problems, [])

    def test_header_signatures_match_code(self):
        """A Public API entry written as name(args) must show the real parameters of the
        def / screen / label / transform / class it names (whitespace and a trailing comma
        aside), so a renamed or added argument cannot leave the header behind."""
        problems = []
        for path in headed_files():
            text = m.read(path)
            for kind, name, line in public_api_entries(path)[0]:
                if kind not in SIGNATURE_KINDS + (None,):
                    continue
                args = header_args(line, name)
                if args is None:
                    continue
                kind = kind or "def"
                code = re.search(rf"^[ \t]*{kind}\s+{re.escape(name)}\s*\((.*?)\)\s*(?:->[^:]*)?:", text,
                                 re.M | re.S)
                if code is None or _norm_args(code.group(1)) != _norm_args(args):
                    found = " ".join(code.group(1).split()) if code else "not found"
                    problems.append(f"{game_rel(path)}: header {kind} {name}({args}) vs code ({found})")
        self.assertEqual(problems, [])

    def test_every_top_level_def_is_documented(self):
        """Every def/class at the top of an init python block in a system/screen file is
        listed under Public API or Internal in its header, so headers cannot fall behind."""
        missing = []
        for path in headed_files():
            listed = {name for _kind, name, _line in public_api_entries(path)[0]}
            listed |= set(internal_names(path))
            for name in top_level_defs(m.read(path)):
                if name not in listed:
                    missing.append(f"{game_rel(path)}: {name} (add it under Public API or Internal)")
        self.assertEqual(missing, [])

    def test_paths_named_in_headers_exist(self):
        missing = []
        for path in headed_files():
            for rel in HEADER_PATH.findall("\n".join(leading_comments(path))):
                if not ((ROOT / rel).exists() or (m.GAME / rel).exists()):
                    missing.append(f"{game_rel(path)}: {rel}")
        self.assertEqual(missing, [])

    def test_architecture_doc_paths_exist(self):
        """docs/ARCHITECTURE.md exists and every `game/...`, `tools/...`, `tests/...` or
        `docs/...` path it names in backticks exists (globs must match something)."""
        doc = ROOT / "docs" / "ARCHITECTURE.md"
        self.assertTrue(doc.exists(), "docs/ARCHITECTURE.md is missing")
        missing = []
        for rel in DOC_PATH.findall(doc.read_text(encoding="utf-8")):
            rel = rel.rstrip("/")
            if "*" in rel:
                found = list(ROOT.glob(rel))
            else:
                found = (ROOT / rel).exists()
            if not found:
                missing.append(rel)
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
