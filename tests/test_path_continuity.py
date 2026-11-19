"""Path continuity guard (darryn 2026-11-19).

A later line may only mention an event the player could have seen on their path. Each entry in
OPTIONAL_EVENTS names an optional event, a pattern for lines that mention it, the labels where it
actually plays (the source), and a pattern the enclosing if/elif conditions must match to prove it
happened. Any matching say/narration line outside its source labels must sit inside such an if.
Add an entry whenever you write a look-back to an optional event (LC-Brain: Conventions,
"Only mention what happened on this path"; Recipe - Write dialogue for a moment, step 0).
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY2 = ROOT / "game" / "chapters" / "ch01" / "day2"
FILES = sorted(DAY2.glob("ch01_day2_*.rpy"))

# (name, mention regex, source label regex, proof regex for an enclosing condition)
OPTIONAL_EVENTS = [
    ("pool spank / strings (Leia-Julian split)",
     r"smack(ed)? my ass|slapping motion|the strings thing",
     r"ch01_day2_scene_16_forced_split$|ch01_day2_scene_18_pool_aftermath$|ch01_day2_errand_cafe_ntr$",  # the errand smack is its own event
     r"ch01_d2_split|exhibition_pool_tease"),
    ("kiss at the pool (Ryan-Leia split)",
     r"kissed me right in front|kiss situation|The kiss\. In front of",
     r"ch01_day2_scene_16_forced_split$",
     r"ch01_d2_split"),
    ("Ryan quiet / somewhere else all day (detached Ryan)",
     r"quiet all day|somewhere else all (day|morning)|been somewhere else",
     r"^$",
     r"ryan_mood|ryan_detached|overheard_talk|d2_errand_reason|choice_tag_count"),
    ("Leia stayed in her underwear (not topless)",
     r"stayed in her bra and panties",
     r"^$",
     r"nhie_leia_clothes|lane"),
    ("good day ending in the love bedroom (not a strained night)",
     r"really good day",
     r"^$",
     r"strained"),
    ("the café overheard talk",
     r"told Maya I wanted to do something nice",
     r"^$",
     r"overheard_talk"),
]

HEADER = re.compile(r"^(\s*)(if|elif|else|menu|\"[^\"]*\"\s*(if .*)?:)")
SAY = re.compile(r'^\s*(?:[a-z_]+\s+)?"')


def _scan(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    label = None
    stack = []  # (indent, condition text)
    chains = {}  # indent -> conditions of the current if/elif chain at that indent
    for no, raw in enumerate(lines, 1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        m = re.match(r"label ([A-Za-z0-9_]+)", stripped)
        if m and indent == 0:
            label, stack, chains = m.group(1), [], {}
            continue
        while stack and stack[-1][0] >= indent:
            stack.pop()
        if stripped.startswith("if ") and stripped.endswith(":"):
            chains[indent] = [stripped]
            stack.append((indent, stripped))
            continue
        if stripped.startswith(("elif ", "else:")) and stripped.endswith(":"):
            chains.setdefault(indent, []).append(stripped)
            stack.append((indent, " ".join(chains[indent])))
            continue
        if stripped.endswith(":") and not stripped.startswith(("$", "python")):
            stack.append((indent, stripped))
            continue
        if SAY.match(raw):
            yield no, label, raw, " ".join(c for _, c in stack)


class PathContinuityTests(unittest.TestCase):
    def test_mentions_of_optional_events_are_gated(self):
        problems = []
        for path in FILES:
            for no, label, raw, conds in _scan(path):
                for name, mention, source, proof in OPTIONAL_EVENTS:
                    if not re.search(mention, raw):
                        continue
                    if label and re.search(source, label):
                        continue
                    if re.search(proof, conds):
                        continue
                    problems.append("%s:%d [%s] %s" % (path.name, no, name, raw.strip()[:90]))
        self.assertEqual(problems, [], "\n".join(problems))

    def test_registry_patterns_still_match_something(self):
        text = "\n".join(p.read_text(encoding="utf-8") for p in FILES)
        for name, mention, _source, _proof in OPTIONAL_EVENTS:
            self.assertRegex(text, mention, name)


if __name__ == "__main__":
    unittest.main()
