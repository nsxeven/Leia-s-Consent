"""Day Two content for the optional-mechanics systems (program design B1, B2, B3).

- B1 Who saw what: the cafe witness beat plays only when this save opened Julian's breakfast
  Hidden POV (lc_pov_seen_in_save); "Leia's version" adds one scored option on the post-boutique
  follow-up when the boutique slip played with Julian there.
- B2 Moments strip: the two Day Two doors register as `door` discoveries and are marked when a
  non-neutral answer is picked.
- B3 Ryan's thoughts: four Day Two `think` lines tinted by the thought kept at the end of Day One,
  each with a neutral path (today's text), plus one extra scored reply when the dream was kept.

Each story block is run through a tiny Ren'Py-subset interpreter ($, if/elif/else, say lines) for
every relevant value, plus the old-save case (nothing opened / nothing kept).
"""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "game" / "python-packages"))
sys.path.insert(0, str(ROOT / "tests"))

import lc_discovery  # noqa: E402
import lc_stat_model as m  # noqa: E402
from lc_effective_effects import effective_effects  # noqa: E402
from lc_story_menus import menus  # noqa: E402

DAY2 = ROOT / "game" / "chapters" / "ch01" / "day2"
D2A = DAY2 / "ch01_day2_scenes_01_15.rpy"
D2B = DAY2 / "ch01_day2_scenes_16_30.rpy"
VISUALS = DAY2 / "ch01_day2_visuals.rpy"
SAY = re.compile(r'^(\w+)?\s*"((?:[^"\\]|\\.)*)"\s*$')


def src(path):
    return path.read_text(encoding="utf-8")


def label_body(path, label):
    text = src(path)
    start = text.index("label %s:" % label)
    nxt = text.find("\nlabel ", start + 1)
    return text[start:nxt if nxt != -1 else len(text)]


def block(path, start_marker, end_line):
    lines = src(path).splitlines()
    s = next(i for i, line in enumerate(lines) if start_marker in line)
    e = next(i for i in range(s + 1, len(lines)) if lines[i] == end_line)
    out = []
    for line in lines[s:e]:
        if line.strip() and not line.strip().startswith("#"):
            out.append((len(line) - len(line.lstrip()), line.strip()))
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
            found = SAY.match(t)
            assert found, t
            nodes.append(("say", (found.group(1), found.group(2))))
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


def play(lines, values=None, flags=(), pov_seen=(), kept=None, lane="love", tint="shy", **local):
    values = dict(values or {})
    ns = {
        "get_story_value": lambda k, d=None: values.get(k, d),
        "set_story_value": values.__setitem__,
        "has_story_flag": lambda f: f in flags,
        "get_story_flag": lambda f: f in flags,
        "lc_pov_seen_in_save": lambda mid: mid in pov_seen,
        "lc_thought_kept": lambda day: (kept or {}).get(day),
        "ch01_d2_route_lane": lambda: lane,
        "lc_leia_tint": lambda *a, **kw: tint,
        "marked": [],
    }
    ns["lc_discovery_mark"] = ns["marked"].append
    ns.update(local)
    nodes, _ = parse(lines, 0, lines[0][0])
    return run(nodes, ns, [])


def text(out):
    return " ".join(t for _, t in out)


LANES = ("love", "exhibitionism", "ntr_risk")


# --------------------------------------------------------------------------- B1 witness beat

WITNESS = (D2A, "# Who saw what (B1)", '    $ set_story_value("ch01_d2_leia_maya_comfort", 2)')


class WitnessBeat(unittest.TestCase):
    def test_sits_in_the_cafe_with_julian_after_the_breakfast_pov(self):
        body = label_body(D2A, "ch01_day2_scene_07_leia_maya_click")
        self.assertIn('if lc_pov_seen_in_save("d2_breakfast_julian"):', body)
        # Later than the POV (scene 3) and with Julian in the cast.
        self.assertIn('julian="evening"', body[:body.index("# Who saw what (B1)")])
        breakfast = label_body(D2A, "ch01_day2_scene_03_maya_message")
        self.assertIn('lc_pov_begin("d2_breakfast_julian")', breakfast)

    def test_not_opened_plays_exactly_as_today(self):
        for lane in LANES:
            self.assertEqual(play(block(*WITNESS), lane=lane), [], lane)
            self.assertEqual(play(block(*WITNESS), pov_seen={"some_other_pov"}, lane=lane), [], lane)

    def test_opened_ryan_notices_julian_noticing_and_leia_notices_them(self):
        for lane in LANES:
            out = play(block(*WITNESS), pov_seen={"d2_breakfast_julian"}, lane=lane)
            who = [w for w, _ in out]
            self.assertIn("friend", who, lane)          # Julian's oblique, flustered line
            self.assertIn("think", who, lane)           # Ryan notices him noticing
            self.assertIn("caught us both", text(out), lane)  # Leia notices them noticing
            self.assertIn("breakfast", text(out), lane)

    def test_love_lane_laughs_it_off_and_leans_into_ryan(self):
        out = play(block(*WITNESS), pov_seen={"d2_breakfast_julian"}, lane="love")
        t = text(out)
        self.assertIn("burst out laughing", t)
        self.assertIn("leaned her whole weight against my shoulder", t)
        self.assertIn("I'm right here", t)
        self.assertTrue(any(w == "gf" for w, _ in out))

    def test_other_lanes_stay_subtle(self):
        for lane in ("exhibitionism", "ntr_risk"):
            out = play(block(*WITNESS), pov_seen={"d2_breakfast_julian"}, lane=lane)
            self.assertNotIn("gf", [w for w, _ in out], lane)
            self.assertNotIn("I'm right here", text(out), lane)
        exhib = text(play(block(*WITNESS), pov_seen={"d2_breakfast_julian"}, lane="exhibitionism"))
        ntr = text(play(block(*WITNESS), pov_seen={"d2_breakfast_julian"}, lane="ntr_risk"))
        self.assertIn("checked my face", exhib)
        self.assertIn("waiting for me to say something", ntr)

    def test_flavor_only(self):
        lines = [t for _, t in block(*WITNESS)]
        self.assertFalse(any("apply_choice" in t or "change_stat" in t for t in lines))


# --------------------------------------------------------------------------- B1 Leia's version

def postshop_menu():
    found = [mn for mn in menus() if mn["label"] == "ch01_day2_scene_11b_boutique"
             and any("d2_postshop_sleep_text" in o["caption"] for o in mn["options"])]
    assert len(found) == 1, found
    return found[0]


def option_condition(caption_var):
    for line in src(D2A).splitlines():
        found = re.match(r'^\s*"\[%s\]" if (.+):\s*$' % caption_var, line)
        if found:
            return found.group(1)
    return None


def gate_value(var, values=None, flags=(), kept=None):
    """Evaluate the `$ var = ...` assignment that gates an option."""
    for line in src(D2A).splitlines():
        found = re.match(r"^\s*\$ %s = (.+)$" % var, line)
        if found:
            values = values or {}
            ns = {"get_story_value": lambda k, d=None: values.get(k, d),
                  "has_story_flag": lambda f: f in flags,
                  "lc_thought_kept": lambda day: (kept or {}).get(day)}
            return eval(found.group(1), ns)
    raise AssertionError("no assignment for " + var)


SLIP = {"ch01_d2_boutique_slip_witness": "julian"}
SLIP_FLAGS = ("ch01_d2_leia_noticed_julian_stare",)


class LeiasVersion(unittest.TestCase):
    def test_option_is_on_the_existing_follow_up_menu(self):
        menu = postshop_menu()
        captions = [o["caption"] for o in menu["options"]]
        self.assertIn("[d2_postshop_version_text]", captions)
        opt = next(o for o in menu["options"] if o["caption"] == "[d2_postshop_version_text]")
        self.assertEqual(opt["shown"], {"ch01_d2_boutique_her_version"})
        self.assertEqual(opt["applied"], ["ch01_d2_boutique_her_version"])
        self.assertEqual(option_condition("d2_postshop_version_text"), "d2_leia_version_offered")

    def test_offered_only_when_the_slip_played_with_julian_there(self):
        self.assertTrue(gate_value("d2_leia_version_offered", SLIP, SLIP_FLAGS))
        self.assertFalse(gate_value("d2_leia_version_offered", {"ch01_d2_boutique_slip_witness": "ryan"}))
        self.assertFalse(gate_value("d2_leia_version_offered", SLIP))           # flag missing
        self.assertFalse(gate_value("d2_leia_version_offered", {}, ()))        # old save

    def test_leia_still_gives_her_first_version_on_that_branch(self):
        body = label_body(D2A, "ch01_day2_scene_11b_boutique")
        self.assertIn("He looked away. He'd already looked away by the time I looked up", body)

    def test_scored_small_trust(self):
        eff = effective_effects()
        self.assertEqual(eff["ch01_d2_boutique_her_version"], [("relationship", "trust", 1)])
        self.assertEqual(m.scoring_violations("ch01_d2_boutique_her_version",
                                              eff["ch01_d2_boutique_her_version"]), [])
        a = src(D2A)
        self.assertIn('"ch01_d2_boutique_her_version": ("attentive", "honest", "curious")', a)

    def test_her_version_differs_from_the_first_one(self):
        body = src(D2A)
        start = body.index('$ apply_choice("ch01_d2_boutique_her_version")')
        part = body[start:body.index('[friend_name] stood and picked up his shopping bag', start)]
        self.assertIn("Not really.", part)
        self.assertIn("He looked for a second.", part)


# --------------------------------------------------------------------------- B2 doors

class DoorMoments(unittest.TestCase):
    REG = re.compile(r'lc_discovery_register\(\s*"(\w+)",\s*"(\w+)",\s*"(\w+)",\s*"([^"]*)",\s*"([^"]*)"')

    def registrations(self):
        return {mid: (day, kind, label, mood) for day, mid, kind, label, mood in self.REG.findall(src(VISUALS))}

    def test_both_doors_register_on_day_two_after_the_pov(self):
        regs = self.registrations()
        for mid in ("d2_knot_door", "d2_dare_door"):
            self.assertIn(mid, regs)
            day, kind, label, mood = regs[mid]
            self.assertEqual((day, kind), ("ch01_d2", "door"), mid)
            self.assertTrue(label and mood, mid)
            # One strip tile (136 px): longer labels/moods are cut (screenshot-checked).
            self.assertLessEqual(len(label), 20, mid)
            self.assertLessEqual(len(mood), 16, mid)
            self.assertFalse(lc_discovery.has_route_words(label), mid)
            self.assertFalse(lc_discovery.has_route_words(mood), mid)
            self.assertNotRegex(label + mood, r"\b(?:Ryan|Leia|Julian)\b")
        v = src(VISUALS)
        self.assertLess(v.index('"d2_breakfast_julian"'), v.index('"d2_knot_door"'))
        self.assertLess(v.index('"d2_knot_door"'), v.index('"d2_dare_door"'))

    def test_registry_accepts_them_in_day_order(self):
        reg = {}
        lc_discovery.register(reg, "ch01_d2", "d2_breakfast_julian", "pov", "Julian, breakfast", "noticed")
        for mid, (day, kind, label, mood) in sorted(self.registrations().items(),
                                                     key=lambda kv: src(VISUALS).index(kv[0])):
            lc_discovery.register(reg, day, mid, kind, label, mood)
        strip = lc_discovery.strip(reg, "ch01_d2", {"d2_knot_door"}, True, "normal")
        self.assertEqual([i["id"] for i in strip], ["d2_breakfast_julian", "d2_knot_door", "d2_dare_door"])
        self.assertEqual([i["found"] for i in strip], [False, True, False])

    def option_body(self, path, choice_id):
        lines = src(path).splitlines()
        s = next(i for i, line in enumerate(lines) if 'apply_choice("%s")' % choice_id in line)
        ind = len(lines[s]) - len(lines[s].lstrip())
        e = s + 1
        while e < len(lines) and (not lines[e].strip() or len(lines[e]) - len(lines[e].lstrip()) >= ind):
            e += 1
        return "\n".join(lines[s:e])

    def test_marked_only_when_the_door_is_taken(self):
        for cid in ("ch01_d2_knot_fix", "ch01_d2_knot_watch"):
            self.assertIn('lc_discovery_mark("d2_knot_door")', self.option_body(D2A, cid), cid)
        self.assertNotIn("lc_discovery_mark", self.option_body(D2A, "ch01_d2_knot_tell"))
        for cid in ("ch01_d2_dare_nod", "ch01_d2_dare_lap"):
            self.assertIn('lc_discovery_mark("d2_dare_door")', self.option_body(D2B, cid), cid)
        self.assertNotIn("lc_discovery_mark", self.option_body(D2B, "ch01_d2_dare_shrug"))

    def test_door_effects_unchanged(self):
        eff = effective_effects()
        self.assertEqual(eff["ch01_d2_knot_tell"], [])
        self.assertEqual(eff["ch01_d2_dare_shrug"], [])


# --------------------------------------------------------------------------- B3 tinted think lines

PHOTO = (D2A, "# Ryan's thoughts (B3): the Day One photo thought", '    "[friend_name] looked at me over his drink."')
CARRY = (D2B, "# Ryan's thoughts (B3): the Day One carry thought",
         '        \"Maya caught [friend_name] by the arm and steered him toward the villa, leaving [girlfriend_name] and me beside the pool.\"')
DINNER = (D2B, "# Ryan's thoughts (B3): the Day One dinner thought", '    $ set_story_flag("ch01_d2_scene_22_complete")')
SOFA = (D2B, "# Ryan's thoughts (B3): the Day One sofa thought", '    $ set_story_value("ch01_d2_nhie_leia_clothes", "bra_panties")')

ALL_D1 = ("d1_photo_shoot", "d1_towel", "d1_dinner_stranger", "d1_julian_carry", "d1_sofa_glance", "d1_dream")
TODAY_PHOTO = ("Yesterday I'd been the photographer in this relationship. Apparently that had a shelf life. "
               "At least I was the one she'd been looking at.")


class TintedThinkLines(unittest.TestCase):
    def kept(self, tid):
        return {"ch01_d1": tid} if tid else {}

    def test_photo_line_tinted_only_when_the_photo_thought_was_kept(self):
        out = play(block(*PHOTO), kept=self.kept("d1_photo_shoot"))
        self.assertEqual([w for w, _ in out], ["think"])
        self.assertIn("hold a phone properly", text(out))
        for tid in (None,) + tuple(t for t in ALL_D1 if t != "d1_photo_shoot"):
            self.assertEqual(play(block(*PHOTO), kept=self.kept(tid)), [("think", TODAY_PHOTO)], tid)

    def test_carry_line_when_julian_carries_the_drinks(self):
        lines = block(*CARRY)
        out = play(lines, kept=self.kept("d1_julian_carry"))
        self.assertEqual([w for w, _ in out], ["think"])
        self.assertIn("keys", text(out))
        for tid in (None,) + tuple(t for t in ALL_D1 if t != "d1_julian_carry"):
            self.assertEqual(play(lines, kept=self.kept(tid)), [], tid)
        # It sits right after Julian's "Why am I always the one carrying?" (Love-lane branch).
        b = src(D2B)
        self.assertLess(b.index('friend "Why am I always the one carrying?'), b.index(CARRY[1]))

    def test_dinner_line_per_lane_and_neutral_for_everyone_else(self):
        lines = block(*DINNER)
        for lane in LANES:
            for soft in (False, True):
                out = play(lines, kept=self.kept("d1_dinner_stranger"), lane=lane,
                           d2_lane=lane, values={"ch01_d2_ntr_soft_gate": soft})
                self.assertEqual([w for w, _ in out], ["think"], (lane, soft))
                self.assertIn("night", text(out).lower(), (lane, soft))  # last night's dinner
        love = text(play(lines, kept=self.kept("d1_dinner_stranger"), d2_lane="love"))
        self.assertIn("not if I could help it", love)
        for tid in (None,) + tuple(t for t in ALL_D1 if t != "d1_dinner_stranger"):
            self.assertEqual(play(lines, kept=self.kept(tid), d2_lane="love"), [], tid)

    def test_sofa_line_follows_where_she_looked_tonight(self):
        lines = block(*SOFA)
        k = self.kept("d1_sofa_glance")
        self.assertIn("checked me first", text(play(lines, kept=k, d2_lane="exhibitionism", d2_soft_gate=False)))
        self.assertIn("didn't check where anyone", text(play(lines, kept=k, d2_lane="ntr_risk", d2_soft_gate=True)))
        love = text(play(lines, kept=k, d2_lane="love", d2_soft_gate=False))
        self.assertIn("came straight back to my side", love)
        for tid in (None,) + tuple(t for t in ALL_D1 if t != "d1_sofa_glance"):
            self.assertEqual(play(lines, kept=self.kept(tid), d2_lane="love", d2_soft_gate=False), [], tid)

    def test_four_spots_each_read_the_day_one_thought(self):
        a, b = src(D2A), src(D2B)
        for tid in ("d1_photo_shoot", "d1_julian_carry", "d1_dinner_stranger", "d1_sofa_glance"):
            self.assertEqual((a + b).count('lc_thought_kept("ch01_d1") == "%s"' % tid), 1, tid)

    def test_tinted_lines_never_move_stats(self):
        for spec in (PHOTO, CARRY, DINNER, SOFA):
            lines = [t for _, t in block(*spec)]
            self.assertFalse(any("apply_choice" in t or "change_stat" in t for t in lines), spec[1])


class DreamReplyOption(unittest.TestCase):
    def test_extra_reply_only_when_the_dream_thought_was_kept(self):
        self.assertTrue(gate_value("d2_dream_thought_kept", kept={"ch01_d1": "d1_dream"}))
        for tid in (None,) + tuple(t for t in ALL_D1 if t != "d1_dream"):
            self.assertFalse(gate_value("d2_dream_thought_kept", kept={"ch01_d1": tid} if tid else {}), tid)
        self.assertEqual(option_condition("d2_postshop_dream_text"), "d2_dream_thought_kept")

    def test_registered_and_scored_love(self):
        eff = effective_effects()
        self.assertEqual(eff["ch01_d2_postshop_dream"], [("relationship", "love", 1), ("relationship", "trust", 1)])
        self.assertEqual(m.choice_route_tag("ch01_d2_postshop_dream", eff["ch01_d2_postshop_dream"]), "Love")
        self.assertIn('"ch01_d2_postshop_dream": ("supportive", "attentive", "honest", "repair")', src(D2A))
        opt = next(o for o in postshop_menu()["options"] if o["caption"] == "[d2_postshop_dream_text]")
        self.assertEqual(opt["applied"], ["ch01_d2_postshop_dream"])

    def test_she_laughs_and_then_hugs_him_unless_she_has_drifted(self):
        body = src(D2A)
        start = body.index('$ apply_choice("ch01_d2_postshop_dream")')
        part = body[start:body.index('[friend_name] stood and picked up his shopping bag', start)]
        self.assertIn("laughed at me", part)
        self.assertIn("hugged me", part)
        self.assertIn('if d2_tint == "temptation":', part)

    def test_existing_postshop_options_stay_flavor(self):
        eff = effective_effects()
        for cid in ("ch01_d2_postshop_sleep", "ch01_d2_postshop_head", "ch01_d2_postshop_shut_down"):
            self.assertEqual(eff[cid], [], cid)
        captions = [o["caption"] for o in postshop_menu()["options"]]
        self.assertEqual(captions[:1], ["[d2_postshop_sleep_text]"])
        self.assertLessEqual(len(captions), 5)


class NewDialogueRules(unittest.TestCase):
    NEW = (WITNESS, PHOTO, CARRY, DINNER, SOFA)

    def lines(self):
        for spec in self.NEW:
            for _, t in block(*spec):
                found = SAY.match(t)
                if found:
                    yield found.group(2)
        body = src(D2A)
        for cid in ("ch01_d2_boutique_her_version", "ch01_d2_postshop_dream"):
            start = body.index('$ apply_choice("%s")' % cid)
            part = body[start:body.index('[friend_name] stood and picked up his shopping bag', start)]
            for line in part.splitlines():
                found = SAY.match(line.strip())
                if found:
                    yield found.group(2)

    def test_names_are_tokens_and_spelling_is_us(self):
        for line in self.lines():
            self.assertNotRegex(line, r"\b(?:Ryan|Leia|Julian)\b", line)
            self.assertNotRegex(line, r"(?i)\b(?:colour|favourite|realise|apologise|mum)\w*", line)

    def test_no_consent_framing(self):
        for line in self.lines():
            self.assertNotRegex(line, r"(?i)\b(?:consent|comfortable with|boundar(?:y|ies)|check(?:ed|ing)? in)\b", line)


if __name__ == "__main__":
    unittest.main()
