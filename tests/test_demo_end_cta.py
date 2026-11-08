"""Demo end card: Patreon, Discord, X and F95 calls to action (darryn 2026-11-09)."""
import unittest
from pathlib import Path

UI = (Path(__file__).resolve().parents[1] / "game/screens/zzzzzzzz_scrapbook_ui.rpy").read_text(encoding="utf-8")


class DemoEndCtaTests(unittest.TestCase):

    def test_four_links(self):
        scr = UI.split("screen lc_demo_end_screen():", 1)[1].split("\nscreen ", 1)[0]
        for url in ("LC_PATREON_URL", "LC_DISCORD_URL", "LC_X_URL", "LC_F95_URL"):
            self.assertIn("OpenURL(%s)" % url, scr)
        self.assertIn('define LC_X_URL = "https://x.com/LeiasConsent"', UI)
        self.assertIn('define LC_F95_URL = "https://f95zone.to/threads/321815/"', UI)


if __name__ == "__main__":
    unittest.main()
