"""The outfit Shop is switched off ("coming soon") while it's under development."""
import re
import unittest
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / "game"


class ShopComingSoonTests(unittest.TestCase):

    def test_shop_switch_is_off(self):
        src = (GAME / "screens" / "shop_screen.rpy").read_text(encoding="utf-8")
        self.assertIn("define LC_SHOP_ENABLED = False", src)
        body = src.split("screen shop_screen():", 1)[1]
        self.assertIn("if not LC_SHOP_ENABLED:\n        use lc_shop_coming_soon(Return())", body)
        self.assertIn("still under development", src)

    def test_phone_shop_app_shows_coming_soon(self):
        src = (GAME / "screens" / "zzzzzz_phone_ios_presentation.rpy").read_text(encoding="utf-8")
        self.assertIn('if phone_app == "shop" and not LC_SHOP_ENABLED:', src)
        self.assertLess(src.index('if phone_app == "shop" and not LC_SHOP_ENABLED:'),
                        src.index("for outfit_id in shop_outfit_ids():"))

    def test_day2_boutique_still_lets_ryan_buy_without_the_shop(self):
        src = (GAME / "chapters" / "ch01" / "ch01_day2_scenes_01_15.rpy").read_text(encoding="utf-8")
        block = src.split('$ set_story_flag("ch01_d2_boutique_shop_open")', 1)[1][:1500]
        self.assertIn("if LC_SHOP_ENABLED:", block)
        self.assertRegex(block, r'"Buy the black mini for her\." if can_afford\(')
        self.assertIn('$ purchase_outfit("boutique_cutout_mini")', block)
        self.assertIn('"Leave it.":', block)


if __name__ == "__main__":
    unittest.main()
