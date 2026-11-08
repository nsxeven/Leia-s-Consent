"""Geometry contract for the effective, sprite-matched phone screens."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHONE = (ROOT / "game/screens/zzzzzz_phone_ios_presentation.rpy").read_text(encoding="utf-8")
TIP = (ROOT / "game/screens/stat_tooltip_screen.rpy").read_text(encoding="utf-8")


class PhoneLayoutTests(unittest.TestCase):
    def test_content_is_centered_inside_the_handset(self):
        values = {key: int(value) for key, value in re.findall(r"^    (LC_PHONE_(?:SCREEN_LEFT|SCREEN_RIGHT|CONTENT_LEFT|CONTENT_WIDTH|VIEWPORT_WIDTH)) = (\d+)$", PHONE, re.M)}
        self.assertEqual(len(values), 5)
        left, right = values["LC_PHONE_SCREEN_LEFT"], values["LC_PHONE_SCREEN_RIGHT"]
        content_left, width = values["LC_PHONE_CONTENT_LEFT"], values["LC_PHONE_CONTENT_WIDTH"]
        self.assertEqual(content_left - left, right - (content_left + width))
        self.assertLessEqual(content_left + width, right)
        self.assertEqual(values["LC_PHONE_VIEWPORT_WIDTH"], width)
        self.assertGreaterEqual(left, 17)
        self.assertLessEqual(right, 523)
        self.assertEqual(PHONE.count('xpos LC_PHONE_CONTENT_LEFT'), 4)
        self.assertEqual(PHONE.count('xsize LC_PHONE_CONTENT_WIDTH'), 4)
        self.assertEqual(PHONE.count('xsize LC_PHONE_VIEWPORT_WIDTH'), 4)
        self.assertNotRegex(PHONE, r'(?m)^\s+xoffset\s+-\d+')

    def test_handset_art_matches_the_declared_screen_edges(self):
        from PIL import Image
        art = ROOT / "game/gui/phone/sprite_match/phone_app.png"
        image = Image.open(art).convert("RGBA")
        self.assertEqual(image.size, (540, 1040))
        # At y=300 the pale display runs from x=17 through x=522.
        for x in (17, 522):
            self.assertTrue(all(c > 220 for c in image.getpixel((x, 300))[:3]))
        for x in (16, 523):
            self.assertTrue(all(c < 60 for c in image.getpixel((x, 300))[:3]))
        hover = Image.open(ROOT / "game/gui/phone/sprite_match/row_hover.png").convert("RGBA")
        self.assertEqual(hover.size, (72, 72))
        self.assertEqual(hover.getpixel((0, 0))[3], 0)

    def test_child_assets_and_hover_stay_within_content(self):
        self.assertNotIn('hover_background Solid(', PHONE.split('screen phone_screen():', 1)[1])
        self.assertIn('hover_background Frame("gui/phone/sprite_match/row_hover.png"', PHONE)
        self.assertIn('lc_phone_rounded_photo(photo_asset, LC_PHONE_CONTENT_WIDTH, 240)', PHONE)
        self.assertIn('xpos 420\n', PHONE)  # message chevron fits the list row
        self.assertIn('xmaximum 410', PHONE)  # shop text fits inside padded card
        self.assertEqual(PHONE.count('xysize (540, 692)'), 0)
        self.assertEqual(PHONE.count('xysize (540, 820)'), 0)

    def test_phone_tooltip_follows_phone_content_width(self):
        self.assertIn('xsize LC_PHONE_CONTENT_WIDTH', TIP)
        self.assertNotIn('xsize 560', TIP)
        self.assertIn('look == "phone"', TIP)


if __name__ == "__main__":
    unittest.main()
