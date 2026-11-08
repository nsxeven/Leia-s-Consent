"""Every story choice leads down one clear path, and Full Transparency shows it.

darryn (2026-11-08): "make sure all the options currently, and in future, all
lead players down proper paths rather than to have overlapping stats that might
confuse players that play on Insight/Full Transparency", plus a small Full-only
tag naming the path each choice leads (or may lead) to.

A new choice fails here when:
- its id (format_choice / gate formatter / apply_choice) has no registered effects;
- its effects break the scoring rule (two route stats, NTR with a gain, ...);
- no single path tag can be derived from them;
- its caption shows one choice id but the branch applies another;
- it looks the same as another option in its menu (same stat line) but leads
  to a different path.
How to score a new choice: docs/STAT_MODEL.md, "How to score a new choice".
"""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "game" / "python-packages"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import lc_stat_model as m  # noqa: E402
import lc_ui_logic as ui  # noqa: E402
from lc_effective_effects import effective_effects, rpy_files  # noqa: E402
from lc_story_menus import applied_ids, formatted_ids, menus, story_files  # noqa: E402

GAME = ROOT / "game"
TAGS_RPY = GAME / "systems" / "choice_path_tags.rpy"


def _deltas(effects):
    return tuple(sorted(m.effect_deltas(effects).items()))


class StoryChoicesStayOnOnePathTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.effects = effective_effects()
        cls.menus = menus()

    def story_ids(self):
        ids = {}
        for path in story_files():
            rel = path.relative_to(GAME).as_posix()
            for cid in formatted_ids(path) | applied_ids(path):
                ids.setdefault(cid, rel)
        return ids

    def test_story_scan_finds_the_whole_game(self):
        # Prologue-Day 5 had 85 live menus and 252 options when this test landed.
        self.assertGreaterEqual(len(self.menus), 80)
        self.assertGreaterEqual(sum(len(mn["options"]) for mn in self.menus), 240)
        self.assertGreaterEqual(len(self.story_ids()), 230)

    def test_every_story_choice_id_has_registered_effects(self):
        missing = sorted("{} ({})".format(cid, rel) for cid, rel in self.story_ids().items()
                         if cid not in self.effects)
        self.assertEqual(missing, [], "register these in CHOICE_EFFECTS:\n" + "\n".join(missing))

    def test_every_story_choice_passes_the_scoring_rule(self):
        problems = []
        for cid, rel in sorted(self.story_ids().items()):
            if cid in self.effects:
                for why in m.scoring_violations(cid, self.effects[cid]):
                    problems.append("{} ({}): {}  {}".format(cid, rel, why, self.effects[cid]))
        self.assertEqual(problems, [], "\n" + "\n".join(problems))

    def test_every_story_choice_has_one_clear_path_tag(self):
        problems = []
        for cid in sorted(self.story_ids()):
            if cid not in self.effects:
                continue
            effects = self.effects[cid]
            tag = m.choice_route_tag(cid, effects)
            lean = m.lean_of(m.effect_deltas(effects))
            if tag not in m.TAGS or lean is None:
                problems.append("{}: no single path ({}, {})".format(cid, tag, effects))
                continue
            # The stamp agrees with what the stat line shows.
            d = m.effect_deltas(effects)
            gains = [s for s, v in d.items() if v > 0 and s != "temptation"]
            if tag in m.NTR_TAGS and lean == "NTR" and gains:
                problems.append("{}: NTR path with a gain {}".format(cid, effects))
            if tag in ("Love", "Repair", "Love+Exhib", "NTS") and d.get("temptation", 0) > 0:
                problems.append("{}: {} path with Temptation up".format(cid, tag))
            if tag in m.NTR_TAGS and lean in ("Love+Exhib", "NTS"):
                problems.append("{}: NTR route value on a {} choice".format(cid, lean))
            if tag != "Neutral":
                self.assertIsNotNone(m.path_stamp(tag), cid)
        self.assertEqual(problems, [], "\n" + "\n".join(problems))

    def test_caption_and_branch_use_the_same_choice(self):
        problems = []
        for mn in self.menus:
            for opt in mn["options"]:
                shown, applied = opt["shown"], set(opt["applied"])
                where = "{}:{}".format(mn["file"], opt["line"])
                if shown and not applied:
                    problems.append("{} shows {} but applies nothing".format(where, sorted(shown)))
                elif shown and applied and shown != applied:
                    problems.append("{} shows {} but applies {}".format(where, sorted(shown), sorted(applied)))
                elif len(applied) > 1 and not shown:
                    problems.append("{} applies {} choices".format(where, sorted(applied)))
                elif applied and not shown and any(self.effects.get(c) for c in applied):
                    problems.append("{} applies {} with a plain caption: Insight/Full can't show its stats"
                                    .format(where, sorted(applied)))
        self.assertEqual(problems, [], "\n" + "\n".join(problems))

    def test_look_alike_options_lead_to_the_same_path(self):
        problems = []
        for mn in self.menus:
            seen = {}
            for opt in mn["options"]:
                for cid in opt["shown"] or set(opt["applied"]):
                    if cid not in self.effects or not self.effects[cid]:
                        continue
                    key = _deltas(self.effects[cid])
                    tag = m.choice_route_tag(cid, self.effects[cid])
                    if key in seen and seen[key][1] != tag:
                        problems.append("{}:{} {} and {} show the same stats but lead to {} / {}".format(
                            mn["file"], mn["line"], seen[key][0], cid, seen[key][1], tag))
                    seen.setdefault(key, (cid, tag))
        self.assertEqual(problems, [], "\n" + "\n".join(problems))

    def test_every_gate_formatter_is_wrapped_for_the_stamp(self):
        defined = set()
        for path in rpy_files():
            defined |= set(re.findall(r"def (format_day\d+_\w*choice)\(", path.read_text(encoding="utf-8")))
        self.assertTrue(defined)
        src = TAGS_RPY.read_text(encoding="utf-8")
        for name in sorted(defined):
            self.assertIn('"{}"'.format(name), src, "add {} to the wrapper list in {}".format(name, TAGS_RPY.name))


class PathStampTests(unittest.TestCase):

    def test_every_tag_has_a_stamp_except_neutral(self):
        self.assertEqual(set(m.PATH_STAMPS), set(m.TAGS))
        self.assertIsNone(m.path_stamp("Neutral"))
        self.assertIsNone(m.path_stamp(None))
        texts = {tag: m.path_stamp(tag)[0] for tag in m.TAGS if tag != "Neutral"}
        self.assertEqual(texts["Love"], "-> Love")
        self.assertEqual(texts["Love+Exhib"], "-> Love+Exhib")
        self.assertEqual(texts["NTS"], "-> NTS")
        self.assertEqual(texts["NTR"], "-> NTR")
        self.assertEqual(texts["May lead to NTR"], "may lead to NTR")
        self.assertEqual(texts["Repair"], "Repair")
        self.assertEqual(len(set(texts.values())), len(texts))

    def test_stamp_colours_follow_the_delta_meanings(self):
        kind = lambda tag: m.path_stamp(tag)[1]
        self.assertEqual(kind("Love"), m.delta_kind("love", 1))
        self.assertEqual(kind("Repair"), m.delta_kind("temptation", -1))
        self.assertEqual(kind("Love+Exhib"), m.delta_kind("exhibitionism", 1))
        self.assertEqual(kind("NTS"), m.delta_kind("sharing", 1))
        for tag in m.NTR_TAGS:
            self.assertEqual(kind(tag), m.delta_kind("temptation", 1), tag)
        colours = (GAME / "systems" / "stat_delta_colours.rpy").read_text(encoding="utf-8")
        for tag in m.TAGS:
            if m.path_stamp(tag):
                self.assertIn('"{}"'.format(m.path_stamp(tag)[1]), colours)

    def test_stamp_from_literal_stat_line_uses_the_same_rule(self):
        _line, chips = ui.parse_choice_caption("Pose for him.\n[Love +1 \u2022 Exhibitionism +2]")
        self.assertEqual(m.route_tag(m.effects_from_chips(chips)), "Love+Exhib")
        _line, chips = ui.parse_choice_caption("Shrug.\n[Love -1 \u2022 Temptation +2]")
        self.assertEqual(m.route_tag(m.effects_from_chips(chips)), "NTR")
        _line, chips = ui.parse_choice_caption("Stay.\n[Love \u2191]")
        self.assertIsNone(m.effects_from_chips(chips))


class ChoiceMarkerTests(unittest.TestCase):

    def test_marker_round_trip_and_is_hidden_from_the_card(self):
        caption = ui.choice_mark("ch01_photo_more") + "Take one more.\n[Love +1 \u2022 Exhibitionism +2]"
        self.assertEqual(ui.split_choice_mark(caption)[0], "ch01_photo_more")
        line, chips = ui.parse_choice_caption(caption)
        self.assertEqual(line, "Take one more.")
        self.assertEqual(chips, [("Love", 1, True), ("Exhibitionism", 2, True)])
        self.assertEqual(ui.split_choice_mark("Plain."), (None, "Plain."))
        self.assertTrue(ui.choice_mark("x").startswith("{#"), "must stay a Ren'Py comment tag (renders nothing)")

    def test_gate_caption_keeps_its_stat_line(self):
        caption = ("{#lcpath=ch01_d2_sunset_ignore_gate}{color=#d85a5a}\u25c6{/color} I'm fine.\n"
                   "[MAJOR RELATIONSHIP CONSEQUENCE] [Love -3 \u2022 Temptation +5]")
        line, chips = ui.parse_choice_caption(caption)
        self.assertEqual(line, "{color=#d85a5a}\u25c6{/color} I'm fine.")
        self.assertEqual(chips, [("Love", -3, True), ("Temptation", 5, True)])
        # Insight gate label carries no stats: unchanged (no chips).
        self.assertEqual(ui.parse_choice_caption("x\n[Major relationship consequence]")[1], [])


class ScreenWiringTests(unittest.TestCase):

    def test_full_mode_only(self):
        src = TAGS_RPY.read_text(encoding="utf-8")
        body = src.split("def lc_choice_path_stamp", 1)[1].split("def ", 1)[0]
        self.assertIn('if current_choice_mode() != "full":', body)
        self.assertIn("lc_choice_caption(caption)", body)
        self.assertIn("lc_choice_route_tag(choice_id)", body)
        engine = (GAME / "systems" / "choice_engine.rpy").read_text(encoding="utf-8")
        full = engine.split('if mode == "full":', 1)[1].split("tags = get_choice_tags", 1)[0]
        self.assertIn("lc_ui_logic.choice_mark(choice_id)", full)
        insight = engine.split('if mode == "insight":', 1)[1].split('if mode == "full":', 1)[0]
        self.assertNotIn("choice_mark", insight)

    def test_choice_card_draws_the_stamp(self):
        src = (GAME / "screens" / "zzzzzzzz_scrapbook_ui.rpy").read_text(encoding="utf-8")
        body = src.split("screen choice(items):", 1)[1].split("\nscreen ", 1)[0]
        self.assertIn("$ stamp = lc_choice_path_stamp(item.caption)", body)
        self.assertIn("box_wrap True", body)
        self.assertIn('font "fonts/Handjet-ExtraBold.ttf"', body.split("if stamp:", 1)[1])
        # The arrow is drawn in a font that has the glyph.
        self.assertIn("{font=DejaVuSans.ttf}", (TAGS_RPY).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
