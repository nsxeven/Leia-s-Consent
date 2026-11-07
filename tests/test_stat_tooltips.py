"""Stat rows explain themselves on hover/focus, per display mode, with no numbers.

Owner decision (darryn): the stat values don't map to anything fixed yet, so
the tooltips must not quote numbers, thresholds or exact effects. Numbers get
retrofitted later through LC_STAT_TOOLTIP_NUMBERS in stat_tooltips.rpy; update
the "no numbers yet" test below when that happens.
"""
import ast
import re
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
TOOLTIPS_RPY = GAME / "systems" / "stat_tooltips.rpy"
MODES = ("normal", "insight", "full")
NAME_TOKENS = {"[girlfriend_name]", "[player_name]", "[friend_name]"}


def _init_python_assignments(path):
    """Literal values assigned at the top level of the file's init python block."""
    src = path.read_text(encoding="utf-8")
    block = src.split("init python:\n", 1)[1]
    tree = ast.parse(textwrap.dedent(block))
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                values[node.targets[0].id] = ast.literal_eval(node.value)
            except ValueError:
                pass
    return values


def _shown_stat_ids():
    """Every stat id that a status row or day-review bar can show."""
    status = (GAME / "systems" / "status_display.rpy").read_text(encoding="utf-8")
    ids = set(re.findall(r'_status_row\("\w+", "(\w+)"', status))
    ids |= set(re.findall(r'lc_stat_tooltip\("(\w+)"', status))
    review = (GAME / "systems" / "day_review.rpy").read_text(encoding="utf-8")
    order = review.split("LC_REVIEW_STAT_ORDER = (", 1)[1].split("\n    )", 1)[0]
    ids |= set(re.findall(r'\("(?:relationship|partner|player)", "(\w+)"\)', order))
    return ids


class StatTooltipTextTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.values = _init_python_assignments(TOOLTIPS_RPY)
        cls.tips = cls.values["LC_STAT_TOOLTIPS"]

    def test_shown_stats_are_found(self):
        ids = _shown_stat_ids()
        for stat in ("boredom", "momentum", "temptation", "boundary_looseness", "secrecy",
                     "love", "trust", "curiosity", "exhibitionism", "jealousy", "acceptance",
                     "nts_score", "ntr_score"):
            self.assertIn(stat, ids)

    def test_every_stat_and_mode_has_text(self):
        for stat in sorted(_shown_stat_ids()):
            self.assertIn(stat, self.tips, stat)
            for mode in MODES:
                text = self.tips[stat].get(mode, "")
                self.assertTrue(text.strip(), "{} / {} has no tooltip".format(stat, mode))

    def test_developer_reuses_full_text(self):
        self.assertEqual(self.values["LC_STAT_TOOLTIP_MODES"], MODES)
        self.assertEqual(self.values["LC_STAT_TOOLTIP_MODE_FALLBACK"], {"developer": "full"})

    def test_no_numbers_in_any_tooltip(self):
        for stat, modes in self.tips.items():
            for mode, text in modes.items():
                self.assertIsNone(re.search(r"\d", text), "{} / {}: {}".format(stat, mode, text))

    def test_no_numbers_retrofitted_yet(self):
        self.assertEqual(self.values["LC_STAT_TOOLTIP_NUMBERS"], {},
                         "Numbers were added: confirm with darryn, then update this test.")

    def test_names_are_tokens_not_defaults(self):
        for stat, modes in self.tips.items():
            for mode, text in modes.items():
                where = "{} / {}".format(stat, mode)
                self.assertIsNone(re.search(r"\b(Ryan|Leia|Julian)\b", text), where)
                self.assertTrue(set(re.findall(r"\[[^\]]*\]", text)) <= NAME_TOKENS, where)
                self.assertNotIn("{", text, where)


class StatTooltipWiringTests(unittest.TestCase):

    def _screen(self, rel, name):
        src = (GAME / rel).read_text(encoding="utf-8")
        return src.split("screen {}(".format(name), 1)[1].split("\nscreen ", 1)[0]

    def test_rows_carry_tooltips(self):
        status = (GAME / "systems" / "status_display.rpy").read_text(encoding="utf-8")
        self.assertIn('"tooltip": lc_stat_tooltip(stat_name, mode)', status)
        row = self._screen("screens/status_screen.rpy", "status_stat_row")
        self.assertIn('tooltip row.get("tooltip")', row)
        phone_row = self._screen("screens/zzzzzz_phone_ios_presentation.rpy", "lc_phone_status_row")
        self.assertIn('tooltip row.get("tooltip")', phone_row)
        review_row = self._screen("screens/day_review_screen.rpy", "lc_review_bar_row")
        self.assertIn('lc_stat_tooltip(row["stat"])', review_row)

    def test_screens_draw_the_card(self):
        self.assertIn('use lc_stat_tip(GetTooltip("status_screen"))',
                      self._screen("screens/status_screen.rpy", "status_screen"))
        self.assertIn('use lc_stat_tip(GetTooltip("lc_phone_status"), look="phone")',
                      self._screen("screens/zzzzzz_phone_ios_presentation.rpy", "lc_phone_status"))
        self.assertIn("use lc_stat_tip(GetTooltip(",
                      self._screen("screens/day_review_screen.rpy", "lc_day_review_screen"))

    def test_card_uses_focus_not_hover_variables(self):
        card = (GAME / "screens" / "stat_tooltip_screen.rpy").read_text(encoding="utf-8")
        self.assertIn('focus "tooltip"', card)
        self.assertIn("substitute False", card)
        code = "\n".join(line for line in card.splitlines() if not line.lstrip().startswith("#"))
        self.assertNotIn("hovered", code)


if __name__ == "__main__":
    unittest.main()
