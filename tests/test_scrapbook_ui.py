"""Scrapbook UI helpers: night paper, day label, choice chips."""

import unittest
from pathlib import Path

from lc_ui_logic import (
    chip_label,
    day_period_label,
    infer_dialogue_theme,
    parse_choice_caption,
    speaker_color,
    story_day_number,
)

ROOT = Path(__file__).resolve().parents[1]


class ThemeTests(unittest.TestCase):
    def test_day_pool_stays_day(self):
        self.assertEqual(infer_dialogue_theme(["bg ch01_pool_day"]), "day")

    def test_night_tokens(self):
        self.assertEqual(infer_dialogue_theme(["bg ch01_restaurant_bar"]), "night")
        self.assertEqual(infer_dialogue_theme(["bg ch01_villa_living_night"]), "night")
        self.assertEqual(infer_dialogue_theme(["bg ch01_d2_sunset"]), "night")
        self.assertEqual(infer_dialogue_theme(["cg ch01_dinner_arrival"]), "night")

    def test_drive_to_dinner_is_day(self):
        self.assertEqual(infer_dialogue_theme(["cg ch01_drive_to_dinner"]), "day")

    def test_manual_override_and_empty_fallback(self):
        self.assertEqual(infer_dialogue_theme(["bg ch01_pool_day"], manual="night"), "night")
        self.assertEqual(infer_dialogue_theme([], fallback="night"), "night")
        self.assertEqual(infer_dialogue_theme([], fallback="day"), "day")


class DayLabelTests(unittest.TestCase):
    def test_story_day_from_flags(self):
        self.assertEqual(story_day_number({}), None)
        self.assertEqual(story_day_number({"prologue_started": True}), 0)
        self.assertEqual(story_day_number({"ch01_started": True}), 1)
        self.assertEqual(
            story_day_number({"ch01_started": True, "ch01_day_01_complete": True, "ch01_day_03_started": True}),
            3,
        )
        self.assertEqual(day_period_label({"ch01_day_03_started": True}, "night"), "DAY 3  NIGHT")
        self.assertEqual(day_period_label({"prologue_started": True}, "day"), "PROLOGUE  DAY")


class ChoiceChipTests(unittest.TestCase):
    def test_insight_and_full_chips(self):
        line, chips = parse_choice_caption("Talk somewhere quieter.\n[Love ↑ • Trust ↑ • Secrecy ↓]")
        self.assertEqual(line, "Talk somewhere quieter.")
        self.assertEqual(chips, [("Love", 1, False), ("Trust", 1, False), ("Secrecy", -1, False)])

        line, chips = parse_choice_caption("Stay.\n[Love +2 • Trust -1]")
        self.assertEqual(chips, [("Love", 2, True), ("Trust", -1, True)])
        self.assertEqual(chip_label("Love", 2, True), "LOVE +2")
        self.assertEqual(chip_label("Trust", -1, False), "TRUST")

    def test_developer_caption_stays_raw(self):
        raw = "Stay.\n[Love +2]  [ID: ch01_stay]\nTags: open"
        line, chips = parse_choice_caption(raw)
        self.assertEqual(line, raw)
        self.assertEqual(chips, [])

    def test_immersive_has_no_chips(self):
        line, chips = parse_choice_caption("Stay and listen.")
        self.assertEqual(line, "Stay and listen.")
        self.assertEqual(chips, [])


class SpeakerTests(unittest.TestCase):
    def test_alias_colors(self):
        aliases = {"leia": ["Ava"], "ryan": ["Noah"]}
        self.assertEqual(speaker_color("Ava", aliases), "#cc0066")
        self.assertEqual(speaker_color("Noah", aliases), "#3f6470")
        self.assertEqual(speaker_color("I SAID"), "#cc0066")
        self.assertEqual(speaker_color(None), "#7a6266")


class AssetTests(unittest.TestCase):
    def test_fonts_and_core_assets_exist(self):
        fonts = ROOT / "game" / "fonts"
        for name in (
            "Silkscreen-Regular.ttf",
            "Silkscreen-Bold.ttf",
            "PatrickHand-Regular.ttf",
            "Caveat[wght].ttf",
            "OFL-Silkscreen.txt",
            "OFL-PatrickHand.txt",
            "OFL-Caveat.txt",
        ):
            self.assertTrue((fonts / name).is_file(), name)
        gui = ROOT / "game" / "gui" / "scrapbook"
        for name in (
            "bg_main_menu.png",
            "bg_game_menu.png",
            "bg_table.png",
            "say_day.png",
            "say_night.png",
            "say_cg_day.png",
            "say_cg_night.png",
            "frame_paper.png",
            "frame_pink.png",
            "tab_pink.png",
            "wax_seal.png",
            "phone_case.png",
        ):
            self.assertTrue((gui / name).is_file(), name)

    def test_day_review_files_untouched_by_ui_module(self):
        screen = (ROOT / "game" / "screens" / "zzzzzzzz_scrapbook_ui.rpy").read_text()
        self.assertNotIn("day_review_screen", screen)
        self.assertNotIn("lc_day_review", screen)


if __name__ == "__main__":
    unittest.main()
