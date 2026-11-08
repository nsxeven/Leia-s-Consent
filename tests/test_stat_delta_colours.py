"""Choice cards colour stat changes by meaning (stat model v2), not by sign."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "game" / "python-packages"))

from lc_ui_logic import effect_markup, parse_choice_caption  # noqa: E402


class StatDeltaColourTests(unittest.TestCase):

    def test_full_mode_colours_each_stat(self):
        _, chips = parse_choice_caption("Don't overthink it.\n[Love -1 \u2022 Trust -1 \u2022 Temptation +2]")
        markup = effect_markup(chips, "#0f0", "#f00")
        self.assertEqual(markup, "[{color=#f00}Love -1{/color} \u2022 {color=#f00}Trust -1{/color} \u2022 {color=#0f0}Temptation +2{/color}]")

    def test_colour_by_meaning_not_sign(self):
        import lc_stat_model
        palette = {"good": "#0f0", "bad": "#f00", "exhibitionism": "#f0f", "sharing": "#80f"}
        colour_for = lambda name, amount: palette.get(lc_stat_model.delta_kind(lc_stat_model.stat_id_for_label(name), amount))
        _, chips = parse_choice_caption("Shrug.\n[Love -2 \u2022 Temptation +3]")
        self.assertEqual(effect_markup(chips, colour_for=colour_for),
                         "[{color=#f00}Love -2{/color} \u2022 {color=#f00}Temptation +3{/color}]")
        _, chips = parse_choice_caption("Talk.\n[Love +2 \u2022 Temptation -3]")
        self.assertEqual(effect_markup(chips, colour_for=colour_for),
                         "[{color=#0f0}Love +2{/color} \u2022 {color=#0f0}Temptation -3{/color}]")
        _, chips = parse_choice_caption("Pose.\n[Exhibitionism +3 \u2022 Sharing +1]")
        self.assertEqual(effect_markup(chips, colour_for=colour_for),
                         "[{color=#f0f}Exhibitionism +3{/color} \u2022 {color=#80f}Sharing +1{/color}]")

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
        self.assertIn("colour_for=lc_delta_colour_for_label", logic)
        self.assertIn("define LC_DELTA_EXHIBITIONISM", logic)
        self.assertIn("define LC_DELTA_SHARING", logic)
        review = (ROOT / "game" / "screens" / "day_review_screen.rpy").read_text(encoding="utf-8")
        self.assertIn('chip.get("ink")', review)
        self.assertIn('row.get("ink")', review)


if __name__ == "__main__":
    unittest.main()
