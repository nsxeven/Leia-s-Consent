"""Day One choice echoes E1-E9 (v0.2.0). Each echo block is found by its "# Day One echo En" comment and run
through a tiny Ren'Py-subset interpreter ($, if/elif/else, say lines) for every stored value, plus None for old
saves. Echoes are flavor only: no stat, story-value, flag, jump or menu changes, and no typed default names.
"""
import re
import unittest
from pathlib import Path

CH01 = Path(__file__).resolve().parents[1] / "game" / "chapters" / "ch01"
S04 = CH01 / "ch01_scenes_04_06.rpy"
S07 = CH01 / "ch01_scenes_07_13.rpy"
S14 = CH01 / "ch01_scenes_14_30.rpy"
D2B = CH01 / "ch01_day2_scenes_16_30.rpy"
SAY = re.compile(r'^(\w+)?\s*"((?:[^"\\]|\\.)*)"\s*$')


def block(path, marker):
    """The if/elif/else chain right after the marker comment, as (indent, text) pairs."""
    lines = path.read_text(encoding="utf-8").splitlines()
    hits = [i for i, l in enumerate(lines) if l.strip().startswith("# " + marker + ":")]
    assert len(hits) == 1, (marker, hits)
    i = hits[0] + 1
    while lines[i].strip().startswith("#"):
        i += 1
    top = len(lines[i]) - len(lines[i].lstrip())
    assert lines[i].strip().startswith("if "), lines[i]
    out = [(top, lines[i].strip())]
    i += 1
    while i < len(lines):
        l = lines[i]
        if not l.strip() or l.strip().startswith("#"):
            i += 1
            continue
        ind = len(l) - len(l.lstrip())
        if ind > top or (ind == top and l.strip().startswith(("elif ", "else:"))):
            out.append((ind, l.strip()))
            i += 1
        else:
            break
    return out


def parse(lines, i, indent):
    nodes = []
    while i < len(lines) and lines[i][0] >= indent:
        ind, t = lines[i]
        assert ind == indent, (ind, indent, t)
        if t.startswith("if ") and t.endswith(":"):
            branches, other = [], []
            body, i = parse(lines, i + 1, lines[i + 1][0])
            branches.append((t[3:-1], body))
            while i < len(lines) and lines[i][0] == indent and lines[i][1].startswith(("elif ", "else:")):
                head = lines[i][1]
                body, i = parse(lines, i + 1, lines[i + 1][0])
                if head == "else:":
                    other = body
                else:
                    branches.append((head[5:-1], body))
            nodes.append(("if", branches, other))
        elif t.startswith("$ "):
            nodes.append(("py", t[2:]))
            i += 1
        else:
            m = SAY.match(t)
            assert m, t
            nodes.append(("say", (m.group(1), m.group(2))))
            i += 1
    return nodes, i


def run(nodes, ns, out):
    for n in nodes:
        if n[0] == "py":
            exec(n[1], ns)
        elif n[0] == "say":
            out.append(n[1])
        else:
            for cond, body in n[1]:
                if eval(cond, ns):
                    run(body, ns, out)
                    break
            else:
                run(n[2], ns, out)
    return out


def play(lines, values, **local):
    ns = {"get_story_value": lambda k, d=None: values.get(k, d)}
    ns.update(local)
    nodes, _ = parse(lines, 0, lines[0][0])
    return run(nodes, ns, [])


def text(out):
    return " ".join(t for _, t in out)


# marker -> (file, story key, every value the game stores, values that get an echo)
ECHOES = {
    "Day One echo E1": (S14, "ch01_upstairs_response", ("honest", "liked", "swallowed", "snapped"), ("liked",)),
    "Day One echo E2": (S14, "ch01_upstairs_response", ("honest", "liked", "swallowed", "snapped"), ("honest",)),
    "Day One echo E3": (S14, "ch01_upstairs_response", ("honest", "liked", "swallowed", "snapped"), ("swallowed",)),
    "Day One echo E4": (S14, "ch01_upstairs_response", ("honest", "liked", "swallowed", "snapped"), ("snapped",)),
    "Day One echo E5": (S14, "ch01_towel_followup", ("reassured", "honest", "teased", "brushed_off"), ("honest",)),
    "Day One echo E6": (S14, "ch01_julian_apology_response", ("trusted", "honest_discomfort", "joked", "said_fine"),
                        ("honest_discomfort", "said_fine")),
    "Day One echo E7": (S07, "ch01_bra_response", ("reassuring", "playful_open", "cautious", "distracted"),
                        ("playful_open", "distracted")),
    "Day One echo E8": (S14, "ch01_looking_philosophy", ("encouragement_boundary", "harmless", "enjoy_attention",
                                                          "indifferent"),
                        ("encouragement_boundary", "harmless", "enjoy_attention", "indifferent")),
    "Day One echo E9": (S04, "ch01_outfit_stance", ("encouraging", "neutral", "protective", "rushed"), ("rushed",)),
}
LOCALS = {"Day One echo E4": {"ch01_day1_love_ending": False}}


class EchoBranches(unittest.TestCase):
    def test_every_value_is_really_stored_by_day_one(self):
        src = "".join(p.read_text(encoding="utf-8") for p in CH01.glob("ch01_*.rpy")
                      if "day2" not in p.name and "day3" not in p.name and "day4" not in p.name
                      and "day5" not in p.name)
        for marker, (_, key, values, _) in ECHOES.items():
            for v in values:
                self.assertIn('set_story_value("%s", "%s")' % (key, v), src, (marker, v))

    def test_each_value_gets_its_own_branch_and_old_saves_stay_neutral(self):
        for marker, (path, key, values, echoed) in ECHOES.items():
            b = block(path, marker)
            loc = LOCALS.get(marker, {})
            neutral = text(play(b, {}, **loc))
            seen = {}
            for v in values:
                out = text(play(b, {key: v}, **loc))
                seen[v] = out
                if v in echoed:
                    self.assertTrue(out, (marker, v))
                    self.assertNotEqual(out, neutral, (marker, v))
                else:
                    self.assertEqual(out, neutral, (marker, v))
            self.assertEqual(len({seen[v] for v in echoed}), len(echoed), marker)

    def test_replaced_lines_keep_the_original_wording_on_the_neutral_path(self):
        self.assertIn("I like it when you just tell me stuff. And next time I fall asleep",
                      text(play(block(S14, "Day One echo E5"), {})))
        self.assertIn("I can see you thinking it", text(play(block(S07, "Day One echo E7"), {})))
        self.assertIn("three beaches", text(play(block(S04, "Day One echo E9"), {})))

    def test_e3_skips_the_dismissed_talk_and_makes_no_promise(self):
        b = block(S14, "Day One echo E3")
        for alone in ("apologized", "curious", "open", None):
            out = text(play(b, {"ch01_upstairs_response": "swallowed", "ch01_alone_movie_response": alone}))
            self.assertIn("just tired", out, alone)
            self.assertNotIn("tomorrow", out.lower(), alone)
        self.assertEqual(play(b, {"ch01_upstairs_response": "swallowed", "ch01_alone_movie_response": "dismissed"}), [])

    def test_e4_fits_both_bedtimes(self):
        b = block(S14, "Day One echo E4")
        for love in (True, False):
            out = play(b, {"ch01_upstairs_response": "snapped"}, ch01_day1_love_ending=love)
            self.assertIn("fall asleep on you", text(out))
            self.assertEqual("breathing slowed" in text(out), not love)

    def test_e8_does_not_reuse_day_two_looking_rule_words(self):
        b = block(S14, "Day One echo E8")
        day_two = ("Looking is looking", "Encouraging it is different", "nobody's hiding anything",
                   "hiding anything", "As long as we're honest", "could actually be fun", "Is it fun yet",
                   "try not to care")
        for v in ECHOES["Day One echo E8"][2]:
            out = text(play(b, {"ch01_looking_philosophy": v}))
            for phrase in day_two:
                self.assertNotIn(phrase.lower(), out.lower(), (v, phrase))


class FlavorOnly(unittest.TestCase):
    def test_no_stat_story_or_route_changes(self):
        for marker, (path, *_rest) in ECHOES.items():
            for _, t in block(path, marker):
                if SAY.match(t):
                    continue  # dialogue text may say "menu"
                self.assertNotRegex(t, r"apply_choice|change_stat|set_story_value|set_story_flag|clear_story_flag|"
                                       r"lc_stat|^jump |^call |^menu|renpy\.", (marker, t))
                self.assertRegex(t, r"^(if |elif |else:)", (marker, t))  # only branches and say lines

    def test_no_typed_default_names(self):
        for marker, (path, *_rest) in ECHOES.items():
            for _, t in block(path, marker):
                m = SAY.match(t)
                if m:
                    self.assertNotRegex(m.group(2), r"\b(Ryan|Leia|Julian)\b", (marker, t))


class DayTwoReconcile(unittest.TestCase):
    def test_bedtime_liked_builds_on_the_talk_they_had(self):
        src = D2B.read_text(encoding="utf-8")
        self.assertNotIn("Daylight didn't cancel it", src)
        self.assertNotIn("I'm still holding you to the proper talk", src)
        self.assertIn("Last night was a good start", src)


if __name__ == "__main__":
    unittest.main()
