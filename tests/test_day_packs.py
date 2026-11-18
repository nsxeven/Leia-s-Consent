"""Day pack guard rails (modular backend).

Every Day (Prologue, Day 1 ... Day 5) is one "Day pack": a folder under game/chapters/
with its scene files, a *_visuals.rpy, a *_registrations.rpy (choice effects, tags,
path tags, CG counts, lane-exempt choices, thresholds, story-key ledger), a
*_gallery.rpy and a *_chapter.rpy (chapter card, review day, Chapter Select preset),
plus its pure-Python data in game/python-packages/lc_days/<day>.py. docs/DAY_PACK.md
explains where every kind of content goes.

Three guards keep it that way:
* Engine files (game/systems, game/screens, game/python-packages/*.py) hold no Day ids.
  tests/data/engine_day_ids_allow.json lists the honest leftovers with a reason. The
  list may only SHRINK: a listed id that is gone from its file fails, so fixed entries
  must be removed.
* Day contract: each Day's start label exists, it reads the previous Day's end-route key,
  writes its own, has its review and chapter entry, and has all pack files.
* Story-key ledger: every set_story_value / set_story_flag key is declared once in the
  registrations file of the Day that owns it, as `# key <name>: read-by <who>` or
  `# key <name>: pending <why>` (dynamic keys as patterns with `*`). read-by keys must be
  read somewhere; pending keys must not be (change them to read-by when a reader lands).
"""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
sys.path.insert(0, str(GAME / "python-packages"))

# ----------------------------------------------------------------- the Day packs
# reads / writes: the end-route story value a Day reads from the previous Day and the one
# it stores for the next. review: the day-review id. chapter: lc_chapters registry id.
DAY_PACKS = (
    dict(day="prologue", folder="chapters/prologue", prefix="prologue", start="prologue_start",
         reads=None, writes=None, review=None),
    dict(day="day1", folder="chapters/ch01/day1", prefix="ch01_day1", start="chapter_one_start",
         reads=None, writes="ch01_day1_route_pressure", review="ch01_d1"),
    dict(day="day2", folder="chapters/ch01/day2", prefix="ch01_day2", start="ch01_day2_start",
         reads="ch01_day1_route_pressure", writes="ch01_d2_end_route", review="ch01_d2"),
    dict(day="day3", folder="chapters/ch01/day3", prefix="ch01_day3", start="ch01_day3_start",
         reads="ch01_d2_end_route", writes="ch01_d3_lane", review="ch01_d3"),
    dict(day="day4", folder="chapters/ch01/day4", prefix="ch01_day4", start="ch01_day4_start",
         reads="ch01_d3_lane", writes="ch01_d4_end_route", review="ch01_d4"),
    dict(day="day5", folder="chapters/ch01/day5", prefix="ch01_day5", start="ch01_day5_start",
         reads="ch01_d4_end_route", writes="ch01_d5_end_route", review="ch01_d5"),
)
PACK_FILES = ("_registrations.rpy", "_gallery.rpy", "_chapter.rpy")

# Days whose pack is not complete yet (shrink, never grow; ends empty).
PENDING_PACKS = {"prologue", "day1", "day2", "day3", "day4", "day5"}

# ------------------------------------------------------------- engine day ids
ENGINE_DIRS = ("systems", "screens")
DAY_ID = re.compile(r"\b(?:ch01_\w+|prologue_\w+|CH01_\w+|[dD][1-9]_\w+|\w+_day[1-9]\w*|day[1-9]\w*)\b")
ALLOW_FILE = ROOT / "tests" / "data" / "engine_day_ids_allow.json"

# --------------------------------------------------------------- story keys
STORY_SET = re.compile(r"set_story_(?:value|flag)\(\s*([^,)]*)")
LEDGER = re.compile(r"^#\s+key\s+([\w*]+):\s+(read-by|pending)\b\s*(.*)$", re.M)
# Keys the engine sets for itself (not Day content).
ENGINE_KEYS = {
    "chapter_select_used": "Chapter Select marks a seeded game (systems/chapter_select.rpy)",
    "chapter_select_preset": "Chapter Select records the (day, route) preset (systems/chapter_select.rpy)",
}
# Keys not declared in a ledger yet (shrink, never grow; ends empty).
PENDING_KEYS_FILE = ROOT / "tests" / "data" / "story_keys_pending.json"


def strip_code(text):
    """Source with comments and triple-quoted strings removed (quotes kept)."""
    out, in_triple = [], None
    for line in text.splitlines():
        res, i, q = [], 0, None
        while i < len(line):
            if in_triple:
                j = line.find(in_triple, i)
                if j < 0:
                    i = len(line)
                    break
                i, in_triple = j + 3, None
                continue
            c = line[i]
            if q:
                res.append(c)
                if c == "\\":
                    res.append(line[i + 1:i + 2])
                    i += 2
                    continue
                if c == q:
                    q = None
                i += 1
                continue
            if line.startswith('"""', i) or line.startswith("'''", i):
                in_triple = line[i:i + 3]
                i += 3
                continue
            if c in "\"'":
                q = c
            elif c == "#":
                break
            res.append(c)
            i += 1
        out.append("".join(res))
    return "\n".join(out)


def engine_files():
    files = [p for d in ENGINE_DIRS for p in (GAME / d).glob("*.rpy")]
    files += list((GAME / "python-packages").glob("*.py"))
    return sorted(files)


def engine_day_ids():
    """{game/-relative path: set of day ids in code} for every engine file."""
    found = {}
    for path in engine_files():
        ids = set(DAY_ID.findall(strip_code(path.read_text(encoding="utf-8-sig"))))
        if ids:
            found[path.relative_to(ROOT).as_posix()] = ids
    return found


def pack_dir(pack):
    return GAME / pack["folder"]


def pack_text(pack):
    folder = pack_dir(pack)
    if not folder.is_dir():
        return ""
    return "\n".join(p.read_text(encoding="utf-8-sig") for p in sorted(folder.glob("*.rpy")))


def day_folders():
    return [(pack["day"], pack_dir(pack)) for pack in DAY_PACKS]


def story_files():
    """Every story .rpy (Day folders and the shared chapter files), not dev/QA files."""
    return sorted(p for p in (GAME / "chapters").rglob("*.rpy"))


def set_keys():
    """({literal key: [paths]}, {dynamic prefix: [paths]}) for set_story_value/flag calls
    in story files and engine systems (dev files excluded)."""
    literal, dynamic = {}, {}
    for path in story_files() + sorted((GAME / "systems").glob("*.rpy")):
        rel = path.relative_to(GAME).as_posix()
        for arg in STORY_SET.findall(strip_code(path.read_text(encoding="utf-8-sig"))):
            arg = arg.strip()
            m = re.match(r'^["\'](\w+)["\']$', arg)
            if m:
                literal.setdefault(m.group(1), []).append(rel)
                continue
            m = re.match(r'^["\'](\w+)["\']\s*\+', arg)
            if m:
                dynamic.setdefault(m.group(1), []).append(rel)
    return literal, dynamic


def ledger():
    """[(key or pattern, kind, text, pack day, path)] from every Day's registrations file."""
    out = []
    for pack in DAY_PACKS:
        path = pack_dir(pack) / (pack["prefix"] + "_registrations.rpy")
        if path.exists():
            for key, kind, text in LEDGER.findall(path.read_text(encoding="utf-8-sig")):
                out.append((key, kind, text.strip(), pack["day"], path.relative_to(GAME).as_posix()))
    return out


def pattern_re(key):
    return re.compile("^" + re.escape(key).replace(r"\*", r"\w+") + "$")


def read_sites(key):
    """Files that use `key` as a string literal outside set calls and ledger comments."""
    lit = re.compile(r"[\"']" + re.escape(key) + r"[\"']")
    setter = re.compile(r"set_story_(?:value|flag)\(\s*[\"']" + re.escape(key) + r"[\"']")
    sites = []
    for path in sorted(GAME.rglob("*.rpy")) + sorted((GAME / "python-packages").rglob("*.py")):
        code = strip_code(path.read_text(encoding="utf-8-sig"))
        if len(lit.findall(code)) > len(setter.findall(code)):
            sites.append(path.relative_to(GAME).as_posix())
    return sites


class EngineDayAgnosticTests(unittest.TestCase):
    def test_engine_files_hold_no_new_day_ids(self):
        allow = json.loads(ALLOW_FILE.read_text(encoding="utf-8"))
        problems = []
        for rel, ids in sorted(engine_day_ids().items()):
            extra = ids - set(allow.get(rel, {}).get("ids", ()))
            if extra:
                problems.append(f"{rel}: {sorted(extra)} (move Day content into its Day pack)")
        self.assertEqual(problems, [], "\n" + "\n".join(problems))

    def test_allow_list_only_shrinks(self):
        """A fixed entry left in the allow-list fails: remove it so it cannot come back."""
        allow = json.loads(ALLOW_FILE.read_text(encoding="utf-8"))
        found = engine_day_ids()
        stale = []
        for rel, entry in sorted(allow.items()):
            self.assertTrue(entry.get("reason", "").strip(), f"{rel}: allow-list entry needs a reason")
            gone = set(entry.get("ids", ())) - found.get(rel, set())
            if gone:
                stale.append(f"{rel}: {sorted(gone)}")
        self.assertEqual(stale, [], "remove fixed ids from tests/data/engine_day_ids_allow.json:\n"
                         + "\n".join(stale))

    def test_scanner_ignores_comments_and_docstrings(self):
        code = strip_code('x = 1  # ch01_d2_example\n"""ch01_d3_doc"""\ny = "#ch01_d4_kept"\n')
        self.assertEqual(sorted(DAY_ID.findall(code)), ["ch01_d4_kept"])


class DayContractTests(unittest.TestCase):
    def pack_problems(self, pack):
        import importlib
        problems = []
        folder = pack_dir(pack)
        text = pack_text(pack)
        if not folder.is_dir():
            return [f"{pack['folder']}: folder missing"]
        if not re.search(rf"^label {re.escape(pack['start'])}\b", text, re.M):
            problems.append(f"start label {pack['start']} not in {pack['folder']}")
        if pack["reads"] and not re.search(rf"get_story_value\(\s*[\"']{pack['reads']}[\"']", text):
            problems.append(f"does not read the previous Day's end route {pack['reads']}")
        if pack["writes"] and not re.search(rf"set_story_value\(\s*[\"']{pack['writes']}[\"']", text):
            problems.append(f"does not store its end route {pack['writes']}")
        if pack["review"]:
            for needed in (rf"lc_review_begin\(\s*[\"']{pack['review']}[\"']",
                           rf"call lc_day_review\(\s*[\"']{pack['review']}[\"']",
                           rf"lc_review_day\(\s*[\"']{pack['review']}[\"']"):
                if not re.search(needed, text):
                    problems.append(f"review {pack['review']}: no match for {needed!r}")
        for suffix in PACK_FILES:
            if not (folder / (pack["prefix"] + suffix)).exists():
                problems.append(f"missing {pack['folder']}/{pack['prefix']}{suffix}")
        if not list(folder.glob("*_visuals.rpy")):
            problems.append(f"no *_visuals.rpy in {pack['folder']}")
        module = GAME / "python-packages" / "lc_days" / (pack["day"] + ".py")
        if not module.exists():
            problems.append(f"missing {module.relative_to(ROOT).as_posix()}")
        else:
            mod = importlib.import_module("lc_days." + pack["day"])
            if not isinstance(getattr(mod, "CHAPTER", None), dict):
                problems.append(f"lc_days.{pack['day']} has no CHAPTER registry entry")
            import lc_chapters
            if pack["day"] not in lc_chapters.CHAPTER_ORDER:
                problems.append(f"{pack['day']} not in lc_chapters.CHAPTER_ORDER")
        return problems

    def test_every_day_pack_keeps_the_contract(self):
        problems = []
        for pack in DAY_PACKS:
            found = self.pack_problems(pack)
            if pack["day"] in PENDING_PACKS:
                if not found:
                    problems.append(f"{pack['day']}: pack complete, remove it from PENDING_PACKS")
            else:
                problems += [f"{pack['day']}: {p}" for p in found]
        self.assertEqual(problems, [], "\n" + "\n".join(problems))

    def test_days_chain(self):
        """Each Day reads exactly the key the previous Day writes."""
        for prev, pack in zip(DAY_PACKS, DAY_PACKS[1:]):
            if pack["reads"]:
                self.assertEqual(pack["reads"], prev["writes"], pack["day"])


class StoryKeyLedgerTests(unittest.TestCase):
    def test_every_set_key_is_declared_once(self):
        literal, dynamic = set_keys()
        pending = set(json.loads(PENDING_KEYS_FILE.read_text(encoding="utf-8")))
        entries = ledger()
        problems = []
        counts = {}
        for key, _kind, _text, _day, rel in entries:
            counts[key] = counts.get(key, 0) + 1
        problems += [f"{k}: declared {n} times" for k, n in sorted(counts.items()) if n > 1]
        patterns = [(pattern_re(k), k) for k in counts if "*" in k]
        for key in sorted(literal):
            if key in ENGINE_KEYS:
                continue
            declared = key in counts or any(rx.match(key) for rx, _k in patterns)
            if declared and key in pending:
                problems.append(f"{key}: declared, remove it from story_keys_pending.json")
            elif not declared and key not in pending:
                problems.append(f"{key}: set in {sorted(set(literal[key]))} but not declared in a Day ledger")
        for prefix in sorted(dynamic):
            covered = any(k.startswith(prefix) and "*" in k for k in counts) or (prefix + "*") in pending
            if not covered:
                problems.append(f"{prefix}*: dynamic key set in {sorted(set(dynamic[prefix]))} needs a pattern")
        stale = sorted(k for k in pending if k not in literal and not k.endswith("*"))
        problems += [f"{k}: in story_keys_pending.json but never set" for k in stale]
        self.assertEqual(problems, [], "\n" + "\n".join(problems))

    def test_ledger_entries_are_honest(self):
        literal, dynamic = set_keys()
        problems = []
        folders = {pack["day"]: pack["folder"] for pack in DAY_PACKS}
        for key, kind, text, day, rel in ledger():
            if "*" in key:
                rx = pattern_re(key)
                matched = [k for k in literal if rx.match(k)]
                prefix = key.split("*", 1)[0]
                if not matched and not any(p.startswith(prefix) or prefix.startswith(p) for p in dynamic):
                    problems.append(f"{rel}: pattern {key} matches no set key")
                continue
            if key not in literal:
                problems.append(f"{rel}: {key} is never set (remove it)")
                continue
            if kind == "read-by" and not read_sites(key):
                problems.append(f"{rel}: {key} says read-by but nothing reads it (make it pending)")
            if kind == "pending" and read_sites(key):
                problems.append(f"{rel}: {key} is pending but is read in {read_sites(key)} (make it read-by)")
            if not text:
                problems.append(f"{rel}: {key} needs who reads it or why it is pending")
            sites = literal[key]
            in_days = {d for d, f in folders.items() for s in sites if s.startswith(f + "/")}
            if in_days and day not in in_days:
                problems.append(f"{rel}: {key} is set by {sorted(in_days)}, not by {day}")
        self.assertEqual(problems, [], "\n" + "\n".join(problems))


if __name__ == "__main__":
    unittest.main()
