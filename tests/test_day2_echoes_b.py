"""Day Two echoes owned by pass B (scenes 16-30): the looking rule, the bedtime upstairs callback and the
Julian check-in. Each block is run through a tiny Ren'Py-subset interpreter ($, if/elif/else, say lines)
for every stored value, plus None for old saves.
"""
import re
import unittest
from pathlib import Path

CH01 = Path(__file__).resolve().parents[1] / "game" / "chapters" / "ch01"
D2B = CH01 / "ch01_day2_scenes_16_30.rpy"
D2B_19 = CH01 / "ch01_day2_scene_19b_leia_asks_maya.rpy"
SAY = re.compile(r'^(\w+)?\s*"((?:[^"\\]|\\.)*)"\s*$')


def block(start_marker, end_line):
    lines = D2B.read_text(encoding="utf-8").splitlines()
    s = next(i for i, l in enumerate(lines) if start_marker in l)
    e = next(i for i in range(s, len(lines)) if lines[i] == end_line)
    out = []
    for l in lines[s:e]:
        if l.strip() and not l.strip().startswith("#"):
            out.append((len(l) - len(l.lstrip()), l.strip()))
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
    ns = {"get_story_value": lambda k, d=None: values.get(k, d),
          "get_story_flag": lambda k: bool(values.get(k))}
    ns.update(local)
    nodes, _ = parse(lines, 0, lines[0][0])
    return run(nodes, ns, [])


def text(out):
    return " ".join(t for _, t in out)


LOOKING = ("# Day One looking rule", '    maya "Never have I ever enjoyed knowing someone was checking me out."')
UPSTAIRS = ("# Day One upstairs echo", '    "Neither of us was stumbling or confused by the time we got into bed."')
JULIAN = ("# Julian check-in", '    "An hour later the coffee table was crowded with bottles, mixers, snacks and four glasses."')


class LookingRuleEcho(unittest.TestCase):
    VALUES = {"encouragement_boundary": "Looking is looking", "harmless": "hiding anything",
              "enjoy_attention": "jealousy", "indifferent": "try not to care"}

    def test_each_value_quotes_day_one_on_warm_lanes(self):
        b = block(*LOOKING)
        seen = set()
        for lane in ("love", "exhibitionism"):
            for v, phrase in self.VALUES.items():
                out = play(b, {"ch01_looking_philosophy": v}, d2_lane=lane)
                self.assertIn(phrase, text(out), (lane, v))
                self.assertEqual(out[0][0], "gf", (lane, v))       # Leia quotes him
                self.assertTrue(any(w == "maya" for w, _ in out), (lane, v))  # Maya tests the line
                seen.add(text(out))
        self.assertEqual(len(seen), 4)  # four distinct moments, same per warm lane

    def test_ntr_lane_is_ryans_thought(self):
        b = block(*LOOKING)
        quotes = {"encouragement_boundary": "Looking is looking", "harmless": "Trust matters more than arbitrary rules",
                  "enjoy_attention": "A little jealousy can actually be fun", "indifferent": "try not to care"}
        for v, phrase in quotes.items():
            out = play(b, {"ch01_looking_philosophy": v}, d2_lane="ntr_risk")
            self.assertEqual([w for w, _ in out], ["think"], v)
            self.assertIn(phrase, text(out), v)

    def test_old_saves_get_nothing_extra(self):
        b = block(*LOOKING)
        for lane in ("love", "exhibitionism", "ntr_risk"):
            self.assertEqual(play(b, {}, d2_lane=lane), [], lane)

    def test_day_one_wording_still_matches(self):
        d1 = (CH01 / "ch01_scenes_14_30.rpy").read_text(encoding="utf-8")
        for line in ('mc "Looking is looking. Encouraging it is different."',
                     'mc "Trust matters more than arbitrary rules."',
                     'mc "I think a little jealousy can actually be fun."',
                     'mc "I don\'t know. I try not to care about stuff like that."'):
            self.assertIn(line, d1)


class UpstairsBedtimeEcho(unittest.TestCase):
    def play(self, v, soft=False, pool=False, lane="love"):
        vals = {"ch01_upstairs_response": v} if v else {}
        return play(block(*UPSTAIRS), vals, d2_soft_gate=soft, d2_pool_suspicion=pool, d2_lane=lane)

    def test_loving_values_say_thank_you(self):
        for v in ("honest", "liked"):
            out = self.play(v)
            mc = [t for w, t in out if w == "mc"]
            self.assertTrue(any("Thank" in t for t in mc), v)
            self.assertTrue(any(w == "think" for w, _ in out), v)  # gratitude in his head too
            self.assertTrue(any(w == "gf" for w, _ in out), v)
        self.assertNotEqual(text(self.play("honest")), text(self.play("liked")))
        self.assertIn("carrying thing", text(self.play("honest")))
        self.assertIn("noticing her", text(self.play("liked")))

    def test_strained_evening_turns_loving_memory_into_a_thought(self):
        for v in ("honest", "liked"):
            for kw in ({"soft": True}, {"pool": True, "lane": "ntr_risk"}):
                out = self.play(v, **kw)
                self.assertEqual({w for w, _ in out}, {"think"}, (v, kw))
                self.assertNotIn("Thank", text(out))

    def test_swallowed_is_noticed_distance(self):
        out = self.play("swallowed")
        self.assertIn("It's fine. Just a long day.", text(out))
        self.assertNotIn("mc", [w for w, _ in out])

    def test_snapped_owns_it_or_does_not(self):
        warm = self.play("snapped")
        self.assertTrue(any(w == "mc" and "crappy thing to say" in t for w, t in warm))
        cold = self.play("snapped", soft=True)
        self.assertIn("I hadn't apologized", text(cold))
        self.assertNotIn("mc", [w for w, _ in cold])

    def test_old_saves_get_nothing_extra(self):
        self.assertEqual(self.play(None), [])
        self.assertEqual(self.play(None, soft=True), [])


class JulianCheckIn(unittest.TestCase):
    PHRASES = {"trusted": "We're good?", "honest_discomfort": "I said I'd be careful",
               "joked": "less enthusiasm", "said_fine": "'it's fine' voice"}

    def test_each_apology_value(self):
        b = block(*JULIAN)
        outs = set()
        for v, phrase in self.PHRASES.items():
            out = play(b, {"ch01_julian_apology_response": v})
            self.assertIn(phrase, text(out), v)
            self.assertEqual(out[0][0], None)  # shared kitchen narration first
            outs.add(text(out))
        self.assertEqual(len(outs), 4)

    def test_pool_line_only_after_the_julian_pool_incident(self):
        b = block(*JULIAN)
        for v in ("trusted", "honest_discomfort", "joked"):
            plain = play(b, {"ch01_julian_apology_response": v})
            pool = play(b, {"ch01_julian_apology_response": v, "ch01_d2_pool_incident": "leia_julian_bee_top_off"})
            self.assertNotIn("pool", text(plain).replace("pool today", ""), v)
            self.assertIn("pool", text(pool), v)

    def test_old_saves_get_neutral_lines(self):
        out = play(block(*JULIAN), {})
        self.assertIn("limes", text(out))
        self.assertNotIn("car", text(out))


class NoStateChangesInEchoes(unittest.TestCase):
    def test_echo_blocks_are_flavor_only(self):
        for spec in (LOOKING, UPSTAIRS, JULIAN):
            for _, t in block(*spec):
                self.assertNotRegex(t, r"apply_choice|change_stat|set_story_value|set_story_flag|jump |call |menu", t)


class NoTypedNamesOrBannedLines(unittest.TestCase):
    BANNED = [re.compile(r"\bthere (she|he|it) is\b", re.I), re.compile(r"^(exactly|noted|fair|touch[eé])[.!]$", re.I),
              re.compile(r"\bno \w+\. no \w+\.", re.I)]

    def lines(self):
        for p in (D2B, D2B_19):
            for n, l in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                m = SAY.match(l.strip())
                if m and m.group(1) != "label":
                    yield "%s:%d" % (p.name, n), m.group(1), re.sub(r"\{[^}]*\}", "", m.group(2)).strip()

    def test_no_typed_default_names(self):
        bad = [w for w, _, t in self.lines() if re.search(r"\b(Ryan|Leia|Julian)\b", t)]
        self.assertEqual(bad, [])

    def test_no_banned_lines(self):
        bad = [w for w, _, t in self.lines() if any(p.search(t) for p in self.BANNED)]
        self.assertEqual(bad, [])

    def test_us_spelling_in_rewritten_lines(self):
        bad = [w for w, _, t in self.lines() if re.search(r"favourite|criticis|realis|colour|apologis", t)]
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
