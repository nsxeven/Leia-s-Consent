"""Day Two echoes of the earmarked Day One choices (worker A files) + name/tic checks.

Each echo is an if/elif chain on one Day One story value, placed in an effective (not
overridden) Day Two label. Old saves with no value (None) skip the chain and play the
scene's existing neutral lines. Echoes are flavor only: no stats, flags or menus inside.
"""
import re
import unittest
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / "game"
CH = GAME / "chapters" / "ch01"
DAY2 = CH / "ch01_day2_scenes_01_15.rpy"
POLISH = CH / "zzzz_ch01_day2_polish_revision.rpy"
DAY1 = [CH / "ch01_scenes_07_13.rpy", CH / "ch01_scenes_14_30.rpy"]

# key -> (effective label that must contain the echo, values it must branch on)
ECHOES = {
    "ch01_upstairs_response": ("ch01_day2_scene_01_morning_after", {"honest", "liked", "swallowed", "snapped"}),
    "ch01_alone_movie_response": ("ch01_day2_scene_01_morning_after", {"apologized", "curious", "open", "dismissed"}),
    "ch01_private_attention_response": ("ch01_day2_scene_05_meet_maya", {"claimed", "open", "jealous", "indifferent"}),
    "ch01_bra_response": ("ch01_day2_scene_11b_boutique", {"reassuring", "playful_open", "cautious", "distracted"}),
    "ch01_towel_followup": ("ch01_day2_scene_11b_boutique", {"reassured", "honest", "teased", "brushed_off"}),
    "ch01_julian_apology_response": ("ch01_day2_scene_11b_boutique", {"trusted", "honest_discomfort", "joked", "said_fine"}),
}
OVERRIDDEN = {"ch01_day2_scene_03_maya_message", "ch01_day2_scene_08_maya_julian",
              "ch01_day2_scene_13_girls_upstairs", "ch01_day2_scene_14_tie_foreshadow"}
SAY = re.compile(r'^\s*(\w+)?\s*"((?:[^"\\]|\\.)*)"\s*(#.*)?$')
NAME = re.compile(r"\b(Ryan|Leia|Julian)\b")
BANNED = [re.compile(r"\bthere (she|he|it) is\b", re.I),
          re.compile(r"^(exactly|noted|fair|touch[eé])[.!]$", re.I),
          re.compile(r"\bno \w+\. no \w+\.", re.I)]


def lines(path):
    return path.read_text(encoding="utf-8").splitlines()


def label_of(src, idx):
    for j in range(idx, -1, -1):
        m = re.match(r"label (\w+):", src[j])
        if m:
            return m.group(1)
    return None


def echo_block(key):
    """(start index, label, chain lines) for the echo chain that reads `key`."""
    src = lines(DAY2)
    starts = [i for i, l in enumerate(src) if l.strip().startswith("# Day One echo") and "(%s)" % key in l]
    assert len(starts) == 1, (key, starts)
    i = starts[0]
    ind = len(src[i]) - len(src[i].lstrip())
    j = i + 1
    while j < len(src) and src[j].strip().startswith("#"):
        j += 1
    body = []
    while j < len(src):
        l = src[j]
        if l.strip() and len(l) - len(l.lstrip()) < ind:
            break
        at_chain = l.strip() and len(l) - len(l.lstrip()) == ind
        if at_chain and not re.match(r"\s*(if|elif|else)\b", l):
            break
        if at_chain and body and re.match(r"\s*if\b", l):
            break  # the next, unrelated if-chain starts here
        body.append(l)
        j += 1
    return i, label_of(src, i), ind, body


class Day2EchoTests(unittest.TestCase):

    def test_each_value_branch_exists_and_reads_its_key(self):
        for key, (label, values) in ECHOES.items():
            _, lab, ind, body = echo_block(key)
            heads = [l for l in body if len(l) - len(l.lstrip()) == ind and l.strip()]
            got = set()
            for h in heads:
                m = re.match(r'\s*(?:if|elif) get_story_value\("(\w+)"\) == "(\w+)":$', h)
                self.assertIsNotNone(m, "%s: unexpected chain line %r" % (key, h))
                self.assertEqual(m.group(1), key)
                got.add(m.group(2))
            self.assertEqual(got, values, key)

    def test_values_match_what_day_one_sets(self):
        day1 = "\n".join(p.read_text(encoding="utf-8") for p in DAY1)
        for key, (_, values) in ECHOES.items():
            set_values = set(re.findall(r'set_story_value\("%s", "(\w+)"\)' % key, day1))
            self.assertEqual(set_values, values, key)

    def test_none_falls_through_to_the_neutral_scene(self):
        # No bare `else:` on the chain, so an old save (value None) plays the scene unchanged.
        for key in ECHOES:
            _, _, ind, body = echo_block(key)
            self.assertFalse([l for l in body if len(l) - len(l.lstrip()) == ind and l.strip() == "else:"], key)

    def test_every_branch_says_something(self):
        for key in ECHOES:
            _, _, ind, body = echo_block(key)
            branch = None
            counts = {}
            for l in body:
                if len(l) - len(l.lstrip()) == ind and l.strip():
                    branch = l.strip()
                    counts[branch] = 0
                elif SAY.match(l):
                    counts[branch] += 1
            self.assertTrue(all(counts.values()), (key, counts))

    def test_echoes_are_flavor_only(self):
        for key in ECHOES:
            _, _, _, body = echo_block(key)
            for l in body:
                if SAY.match(l):
                    continue  # spoken text may say "menu"
                self.assertNotRegex(l, r"apply_choice|change_stat|set_story_value|set_story_flag|\bmenu\b|jump |call ", key)

    def test_echoes_live_in_effective_labels(self):
        for key, (label, _) in ECHOES.items():
            _, lab, _, _ = echo_block(key)
            self.assertEqual(lab, label, key)
            self.assertNotIn(lab, OVERRIDDEN)
        polish = POLISH.read_text(encoding="utf-8")
        for base in OVERRIDDEN:
            self.assertIn('config.label_overrides["%s"] = "%s_v2"' % (base, base), polish)

    def test_upstairs_loving_paths_show_gratitude(self):
        _, _, ind, body = echo_block("ch01_upstairs_response")
        text = "\n".join(body)
        for value in ("honest", "liked"):
            part = text.split('== "%s":' % value, 1)[1].split("elif get_story_value", 1)[0]
            self.assertRegex(part, r'mc "[^"]*[Tt]hank', value)
            self.assertIn("think \"", part, value)


class Day2NameAndTicTests(unittest.TestCase):

    def test_no_typed_default_names_in_dialogue(self):
        bad = []
        for p in (DAY2, POLISH):
            for n, l in enumerate(lines(p), 1):
                m = SAY.match(l)
                if m and NAME.search(m.group(2)):
                    bad.append("%s:%d %s" % (p.name, n, l.strip()[:60]))
        self.assertEqual(bad, [])

    def test_no_banned_tic_lines(self):
        bad = []
        for p in (DAY2, POLISH):
            for n, l in enumerate(lines(p), 1):
                m = SAY.match(l)
                if m:
                    t = re.sub(r"\{[^}]*\}", "", m.group(2)).strip()
                    if any(b.search(t) for b in BANNED):
                        bad.append("%s:%d %s" % (p.name, n, t))
        self.assertEqual(bad, [])

    def test_canon_dare_not_introduced(self):
        # Nobody "introduced" Ryan and Leia; Julian's dare started them.
        for p in (DAY2, POLISH):
            for n, l in enumerate(lines(p), 1):
                m = SAY.match(l)
                if m and re.search(r"introduc", m.group(2), re.I):
                    self.assertNotRegex(m.group(2), r"introduc\w* (us|you two|them to each other)", "%s:%d" % (p.name, n))


if __name__ == "__main__":
    unittest.main()
