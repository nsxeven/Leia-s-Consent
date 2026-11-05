"""Choice cards colour stat gains green and losses red (Insight + Full visibility)."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "game" / "python-packages"))

from lc_ui_logic import effect_markup, parse_choice_caption  # noqa: E402


class StatDeltaColourTests(unittest.TestCase):

    def test_full_mode_colours_each_stat(self):
        _, chips = parse_choice_caption("Don't overthink it.\n[Love -1 \u2022 Trust -1 \u2022 Boredom +2]")
        markup = effect_markup(chips, "#0f0", "#f00")
        self.assertEqual(markup, "[{color=#f00}Love -1{/color} \u2022 {color=#f00}Trust -1{/color} \u2022 {color=#0f0}Boredom +2{/color}]")

    def test_insight_arrows_use_a_font_that_has_them(self):
        _, chips = parse_choice_caption("Stay.\n[Love \u2191 \u2022 Secrecy \u2193]")
        markup = effect_markup(chips, "#0f0", "#f00")
        self.assertIn("{color=#0f0}Love {font=DejaVuSans.ttf}\u2191{/font}{/color}", markup)
        self.assertIn("{color=#f00}Secrecy {font=DejaVuSans.ttf}\u2193{/font}{/color}", markup)

    def test_choice_screen_substitutes_then_colours(self):
        src = (ROOT / "game" / "screens" / "zzzzzzzz_scrapbook_ui.rpy").read_text(encoding="utf-8")
        body = src.split("screen choice(items):", 1)[1].split("\nscreen ", 1)[0]
        self.assertIn("parse_choice_caption(lc_choice_caption(item.caption))", body)
        self.assertIn("lc_choice_effect_markup(chips)", body)
        logic = (ROOT / "game" / "systems" / "stat_delta_colours.rpy").read_text(encoding="utf-8")
        self.assertIn('define LC_DELTA_UP = "#5aa874"', logic)
        self.assertIn('define LC_DELTA_DOWN = "#d4636e"', logic)


if __name__ == "__main__":
    unittest.main()
