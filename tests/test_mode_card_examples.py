"""Mode cards rotate example choices; Full shows path + camera stamps (darryn 2026-11-08)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UI = (ROOT / "game/screens/zzzzzzzz_scrapbook_ui.rpy").read_text(encoding="utf-8")


class ModeCardExampleTests(unittest.TestCase):

    def card(self):
        return UI.split("screen lc_info_card(mode_id, mode_now):", 1)[1].split("\n## History", 1)[0]

    def test_examples_use_current_stats_only(self):
        block = UI.split("define LC_MODE_CARD_EXAMPLES = (", 1)[1].split("\n)\n", 1)[0]
        for old in ("secrecy", "boredom", "momentum", "jealousy", "curiosity", "acceptance"):
            self.assertNotIn(old, block.lower())
        self.assertNotIn('"SECRECY"', UI)
        self.assertIn('"May lead to NTR"', block)
        self.assertIn('"Love+Exhib", "3"', block)

    def test_card_rotates_and_colours_by_meaning(self):
        card = self.card()
        self.assertIn("lc_mode_example_fade(_ex_slot)", card)  # one wall clock, no timer (#180)
        self.assertIn("at lc_mode_example_fade", card)
        self.assertIn('lc_delta_colour(_stat, _amount, "review")', card)

    def test_stamps_full_only(self):
        card = self.card()
        self.assertIn('if mode_id != "insight":', card)
        self.assertIn("lc_stat_model.path_stamp(ex[2])", card)
        self.assertIn('icon_camera.png', card)


    def test_fixed_heights(self):
        card = self.card()
        self.assertIn("ysize LC_MODE_EXAMPLE_HEIGHT", card)
        self.assertIn("ysize (LC_MODE_CARD_HEIGHT_PLAIN if", card)
        self.assertNotIn("yminimum", card)


    def test_examples_stacked_on_one_clock(self):
        card = self.card()
        self.assertIn("for _ex_slot, ex in enumerate(LC_MODE_CARD_EXAMPLES):", card)
        self.assertIn("vbox at lc_mode_example_fade(_ex_slot):", card)
        self.assertNotIn("timer LC_MODE_EXAMPLE_SECONDS", card)


if __name__ == "__main__":
    unittest.main()
