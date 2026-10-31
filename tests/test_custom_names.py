"""Custom names, the age gate, and Day 3 choice effects.

Run with: python3 -m unittest discover -s tests -v
"""
import ast
import re
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CH01 = ROOT / "game" / "chapters" / "ch01"

SCENE_FILES = [
    "ch01_day2_scenes_01_15.rpy",
    "ch01_day2_scenes_16_30.rpy",
    "ch01_day2_scene_19b_leia_asks_maya.rpy",
    "zzzz_ch01_day2_polish_revision.rpy",
    "ch01_day3_scenes.rpy",
    "ch01_day4_scenes_01_08.rpy",
    "ch01_day4_scenes_09_16.rpy",
    "ch01_day4_choice_registration.rpy",
    "ch01_day5_scenes_01_08.rpy",
    "ch01_day5_scenes_09_16.rpy",
    "ch01_day5_choice_registration.rpy",
]
VISUAL_FILES = [
    "ch01_day2_visuals.rpy",
    "ch01_day3_visuals.rpy",
    "ch01_day4_visuals.rpy",
    "ch01_day5_visuals.rpy",
]
NAME_RE = re.compile(r"\b(?:Leia|Ryan|Julian|LEIA|RYAN|JULIAN)\b")
CUSTOM = {"girlfriend_name": "Ava", "player_name": "Noah", "friend_name": "Eli"}
GROUPS = {
    "relationship": ("love", "trust", "boredom", "momentum"),
    "partner": ("curiosity", "temptation", "exhibitionism", "boundary_looseness", "secrecy"),
    "player": ("jealousy", "acceptance"),
}


def _code_lines(text):
    """Yield (lineno, line) with comments and docstrings removed."""
    in_triple = False
    for lineno, line in enumerate(text.splitlines(), 1):
        if in_triple:
            if '"""' in line or "'''" in line:
                in_triple = False
            continue
        stripped = line.lstrip()
        if stripped.startswith('"""') or stripped.startswith("'''"):
            quote = stripped[:3]
            if stripped.count(quote) < 2:
                in_triple = True
            continue
        if stripped.startswith("#"):
            continue
        cut = []
        i = 0
        in_str = None
        while i < len(line):
            ch = line[i]
            if in_str:
                cut.append(ch)
                if ch == "\\":
                    if i + 1 < len(line):
                        cut.append(line[i + 1])
                    i += 2
                    continue
                if ch == in_str:
                    in_str = None
                i += 1
                continue
            if ch == "#":
                break
            if ch in ("'", '"'):
                in_str = ch
            cut.append(ch)
            i += 1
        yield lineno, "".join(cut)


def _render_renpy(text):
    rendered = text
    for key, value in CUSTOM.items():
        rendered = rendered.replace("[" + key + "!u]", value.upper())
        rendered = rendered.replace("[" + key + "]", value)
    return rendered


def _render_placeholder(text):
    shown = text
    shown = shown.replace("{gf}'S", CUSTOM["girlfriend_name"].upper() + "'S")
    shown = shown.replace("{mc}'S", CUSTOM["player_name"].upper() + "'S")
    shown = shown.replace("{friend}'S", CUSTOM["friend_name"].upper() + "'S")
    shown = shown.replace("{gf}", CUSTOM["girlfriend_name"].upper())
    shown = shown.replace("{mc}", CUSTOM["player_name"].upper())
    shown = shown.replace("{friend}", CUSTOM["friend_name"].upper())
    return shown.replace("\\n", "\n")


class CustomNameTests(unittest.TestCase):
    def test_story_strings_render_custom_names(self):
        leftovers = []
        rendered_samples = []
        for name in SCENE_FILES:
            for lineno, line in _code_lines((CH01 / name).read_text()):
                if NAME_RE.search(line):
                    leftovers.append("{}:{}: {}".format(name, lineno, line.strip()[:160]))
                if any(token in line for token in ("[girlfriend_name]", "[player_name]", "[friend_name]")):
                    rendered = _render_renpy(line)
                    rendered_samples.append(rendered)
                    if NAME_RE.search(rendered):
                        leftovers.append("rendered {}:{}: {}".format(name, lineno, rendered.strip()[:160]))
        self.assertEqual(leftovers, [])
        self.assertGreater(len(rendered_samples), 400)
        joined = "\n".join(rendered_samples)
        self.assertIn("Ava", joined)
        self.assertIn("Noah", joined)
        self.assertIn("Eli", joined)
        self.assertNotIn("Leia", joined)
        self.assertNotIn("Ryan", joined)
        self.assertNotIn("Julian", joined)

    def test_python_name_expressions_use_custom_names(self):
        checked = 0
        for name in SCENE_FILES:
            for lineno, line in _code_lines((CH01 / name).read_text()):
                if not any(token in line for token in ("girlfriend_name", "player_name", "friend_name")):
                    continue
                if "[girlfriend_name]" in line or "[player_name]" in line or "[friend_name]" in line:
                    continue
                statement = line.strip()
                if statement.startswith("$ "):
                    statement = statement[2:]
                # Keyword arguments are valid inside a call, not as a module.
                if statement.endswith(",") and "=" in statement and not statement.startswith(("if ", "elif ", "for ")):
                    statement = "f(" + statement + ")"
                try:
                    tree = ast.parse(statement)
                except SyntaxError:
                    continue
                for node in ast.walk(tree):
                    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                        try:
                            value = eval(compile(ast.Expression(node), "<expr>", "eval"), dict(CUSTOM))
                        except Exception:
                            continue
                        if isinstance(value, str):
                            checked += 1
                            self.assertIsNone(NAME_RE.search(value), "{}:{} -> {}".format(name, lineno, value))
                            self.assertTrue(any(part in value for part in CUSTOM.values()))
        self.assertGreater(checked, 20)

    def test_placeholder_cards_render_custom_names(self):
        cards = 0
        for name in VISUAL_FILES:
            text = (CH01 / name).read_text()
            for lineno, line in _code_lines(text):
                if "lc_placeholder_text(" not in line and "Text(" not in line:
                    continue
                shown = _render_placeholder(line)
                self.assertIsNone(NAME_RE.search(shown), "{}:{}".format(name, lineno))
                if 'lc_placeholder_text("' in line:
                    cards += 1
                    self.assertNotIn("{gf}", shown)
                    self.assertNotIn("{mc}", shown)
                    self.assertNotIn("{friend}", shown)
                    self.assertTrue(any(part in shown for part in ("AVA", "NOAH", "ELI")))
        self.assertGreaterEqual(cards, 30)

    def test_names_inside_other_words_were_not_rewritten(self):
        # Identifiers such as choice ids and thread ids stay lowercase.
        text = "\n".join((CH01 / name).read_text() for name in SCENE_FILES)
        self.assertIn('"leia"', text)
        self.assertIn("ch01_d5_snorkel_leia_first", text)
        self.assertIn("ch01_day3_leia_returns", text)


class AgeGateTests(unittest.TestCase):
    def test_start_shows_the_notice_without_the_demo_flag(self):
        script = (ROOT / "game" / "script.rpy").read_text()
        start = script.split("label start:", 1)[1].split("label ", 1)[0]
        self.assertEqual(start.count("call lc_adult_notice"), 1)
        self.assertNotIn("LC_DAY1_DEMO_BUILD", start)
        self.assertIn("if not persistent.lc_adult_notice_accepted:", start)
        self.assertIn("return", start)
        self.assertIn("jump prologue_name_setup", start)

        day1 = (CH01 / "ch01_scenes_14_30.rpy").read_text()
        self.assertIn("if LC_DAY1_DEMO_BUILD:", day1)
        self.assertIn("jump ch01_day1_demo_complete", day1)


class Day3ChoiceTests(unittest.TestCase):
    def setUp(self):
        source = (CH01 / "ch01_day3_scenes.rpy").read_text()
        block = source.split("init 1 python:\n", 1)[1].split("\nlabel ch01_day3_start", 1)[0]
        self.env = {"CHOICE_EFFECTS": {}, "CHOICE_TAGS": {}}
        exec(compile(textwrap.dedent(block), "day3_choices", "exec"), self.env)
        self.effects = self.env["CHOICE_EFFECTS"]
        self.scene = source

    def test_both_menus_change_stats_and_keep_story_flags(self):
        club = ("ch01_d3_ntr_enjoy", "ch01_d3_ntr_talk", "ch01_d3_ntr_withdraw")
        dessert = ("ch01_d3_dessert_chocolate", "ch01_d3_dessert_recommended", "ch01_d3_dessert_surprise")
        for choice_id in club + dessert:
            self.assertEqual(self.scene.count('apply_choice("{}")'.format(choice_id)), 1)
            rows = self.effects[choice_id]
            self.assertTrue(rows)
            for group, stat, amount in rows:
                self.assertIn(stat, GROUPS[group])
                self.assertNotEqual(amount, 0)
                self.assertGreaterEqual(amount, -2)
                self.assertLessEqual(amount, 2)

        def totals(choice_id):
            stats = {group: {stat: 0 for stat in names} for group, names in GROUPS.items()}
            for group, stat, amount in self.effects[choice_id]:
                stats[group][stat] += amount
            return stats

        enjoy = totals("ch01_d3_ntr_enjoy")
        talk = totals("ch01_d3_ntr_talk")
        withdraw = totals("ch01_d3_ntr_withdraw")
        self.assertGreater(talk["relationship"]["love"], enjoy["relationship"]["love"])
        self.assertGreater(talk["relationship"]["trust"], 0)
        self.assertLess(talk["partner"]["secrecy"], 0)
        self.assertLess(withdraw["relationship"]["love"], 0)
        self.assertGreater(withdraw["relationship"]["boredom"], 0)
        self.assertGreater(withdraw["partner"]["temptation"], 0)
        self.assertGreater(withdraw["partner"]["secrecy"], 0)
        self.assertEqual(totals("ch01_d3_dessert_chocolate")["relationship"]["trust"], 1)
        self.assertEqual(totals("ch01_d3_dessert_recommended")["player"]["acceptance"], 1)
        self.assertEqual(totals("ch01_d3_dessert_surprise")["relationship"]["love"], 1)

        self.assertIn('set_story_value("ch01_d3_ntr_repair_effort", "enjoy")', self.scene)
        self.assertIn('set_story_value("ch01_d3_ntr_repair_effort", "talk")', self.scene)
        self.assertIn('set_story_value("ch01_d3_ntr_repair_effort", "withdraw")', self.scene)
        self.assertIn('set_story_value("ch01_d3_maya_dessert", "chocolate")', self.scene)
        self.assertIn('set_story_value("ch01_d3_end_variant", "ntr_restroom_nightmare_talk")', self.scene)
        self.assertIn('set_story_value("ch01_d3_end_variant", "ntr_restroom_nightmare_withdraw")', self.scene)
        self.assertIn('set_story_value("ch01_d3_end_variant", "ntr_restroom_nightmare")', self.scene)
        self.assertIn('set_story_value("ch01_d3_lane", d3_lane)', self.scene)

    def test_effective_apply_choice_records_the_review(self):
        source = (ROOT / "game" / "screens" / "zz_day1_ui_qol_patch.rpy").read_text()
        body = source.split("def apply_choice(choice_id):", 1)[1].split("\n    def ", 1)[0]
        self.assertIn("lc_review_note_choice(choice_id, review_before)", body)
        self.assertLess(body.index("review_before = lc_review_stats()"), body.index("change_stat("))


if __name__ == "__main__":
    unittest.main()
