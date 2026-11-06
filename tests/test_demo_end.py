"""Demo end card (darryn): thank-you, upcoming releases, Patreon + Discord, after the Day 1 review."""
import unittest
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / "game"


class DemoEndCardTests(unittest.TestCase):
    def test_card_content_and_links(self):
        ui = (GAME / "screens" / "zzzzzzzz_scrapbook_ui.rpy").read_text(encoding="utf-8")
        card = ui.split("screen lc_demo_end_screen():", 1)[1].split("\nscreen ", 1)[0]
        for needle in ("lc_title_logo()", "Thank you for playing the demo!", "UPCOMING RELEASES",
                       '"Day 2"', "OpenURL(LC_PATREON_URL)", "OpenURL(LC_DISCORD_URL)", "Return()"):
            self.assertIn(needle, card)
        self.assertIn('define LC_PATREON_URL = "https://www.patreon.com/c/LeiasConsent"', ui)
        self.assertIn('define LC_DISCORD_URL = "https://discord.gg/HYmrB8Gjwj"', ui)

    def test_shown_only_through_the_demo_gate(self):
        gate = (GAME / "chapters" / "ch01" / "ch01_release_demo.rpy").read_text(encoding="utf-8")
        self.assertIn("call screen lc_demo_end_screen", gate)
        day1 = (GAME / "chapters" / "ch01" / "ch01_scenes_14_30.rpy").read_text(encoding="utf-8")
        self.assertIn("if LC_DAY1_DEMO_BUILD:\n        jump ch01_day1_demo_complete", day1.replace("\r\n", "\n"))


if __name__ == "__main__":
    unittest.main()
