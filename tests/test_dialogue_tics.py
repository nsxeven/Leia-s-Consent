"""Dialogue tic check (docs/DIALOGUE_STYLE.md).

darryn's rule: dialogue should feel like real people talking, not LLMs. Numbers are not hard
limits. Only BANNED phrases fail; length/ping-pong/no-long-line stats are printed as flags
for a read-aloud pass (run this file directly to see them).

KNOWN was a ratchet for the 12 banned lines at f97c318; rewrite pass A removed them all.
Any banned line now fails.
"""
import collections
import re
import unittest
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / "game"
STORY = ["chapters/prologue.rpy", "chapters/ch01/ch01_main.rpy", "chapters/ch01/ch01_scenes_04_06.rpy",
         "chapters/ch01/ch01_scenes_07_13.rpy", "chapters/ch01/ch01_scenes_14_30.rpy"]
SAY = re.compile(r'^\s*(\w+)?\s*"((?:[^"\\]|\\.)*)"')
BANNED = {
    "There she is / There it is": re.compile(r"\bthere (she|he|it) is\b", re.I),
    "lone Exactly./Noted./Fair./Touche.": re.compile(r"^(exactly|noted|fair|touch[eé])[.!]$", re.I),
    "'No X. No Y.' narration fragments": re.compile(r"\bno \w+\. no \w+\.", re.I),
}
# (file, banned kind) -> count still allowed. Shrink to zero during rewrite pass A.
KNOWN = {}  # rewrite pass A removed all 12 (2026-11-08); keep it empty


def spoken_lines(rel):
    for n, line in enumerate((GAME / rel).read_text(encoding="utf-8").splitlines(), 1):
        m = SAY.match(line)
        if m:
            yield n, m.group(1), re.sub(r"\{[^}]*\}", "", m.group(2)).strip()


def banned_hits():
    hits = collections.defaultdict(list)
    for rel in STORY:
        for n, who, text in spoken_lines(rel):
            for kind, pat in BANNED.items():
                if pat.search(text):
                    hits[(rel, kind)].append("%s:%d %s" % (rel, n, text[:60]))
    return hits


def flags():
    """Read-aloud flags, never failures."""
    out = []
    for rel in STORY:
        sizes = [len(t.split()) for _, who, t in spoken_lines(rel) if who not in (None, "centered", "extend")]
        if not sizes:
            continue
        short = sum(s <= 4 for s in sizes) / len(sizes)
        run = runs = 0
        for s in sizes + [99]:
            if s <= 4:
                run += 1
            else:
                runs += run >= 6
                run = 0
        out.append("%s: %d spoken, %.0f%% <=4 words, %d runs of 6+ short, %d lines of 15+ words"
                   % (rel, len(sizes), 100 * short, runs, sum(s >= 15 for s in sizes)))
    return out


class DialogueTicTests(unittest.TestCase):
    def test_no_new_banned_phrases(self):
        over = []
        for key, lines in banned_hits().items():
            if len(lines) > KNOWN.get(key, 0):
                over.append("%s %s (allowed %d): %s" % (key[1], key[0], KNOWN.get(key, 0), lines))
        self.assertEqual(over, [], "New banned phrase(s); see docs/DIALOGUE_STYLE.md")

    def test_known_list_is_not_stale(self):
        # When pass A removes a line, lower its KNOWN count so it can't creep back.
        hits = banned_hits()
        stale = ["%s %s: allowed %d, found %d" % (k[1], k[0], v, len(hits.get(k, [])))
                 for k, v in KNOWN.items() if len(hits.get(k, [])) < v]
        self.assertEqual(stale, [])


if __name__ == "__main__":
    print("\n".join(flags()))
    unittest.main()
