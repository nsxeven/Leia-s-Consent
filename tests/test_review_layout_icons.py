"""Static contracts for the scrapbook grid and generated stat art."""
import re
import unittest
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'game/screens/day_review_screen.rpy'
LOGIC = ROOT / 'game/systems/day_review.rpy'
STATUS = ROOT / 'game/screens/status_screen.rpy'
ART = ROOT / 'game/images/ui/scrapbook'
STATS = ('love', 'trust', 'boredom', 'momentum', 'curiosity', 'temptation',
         'exhibitionism', 'boundary_looseness', 'secrecy', 'jealousy',
         'acceptance', 'sharing', 'distance')

class ReviewLayoutIcons(unittest.TestCase):
    def test_one_icon_registry_covers_both_stat_sets(self):
        logic = LOGIC.read_text()
        screen = SCREEN.read_text()
        status = STATUS.read_text()
        self.assertIn('LC_STAT_ICON = {', logic)
        for stat in STATS:
            self.assertRegex(logic, r'"' + stat + r'": "' + stat + r'"')
            image = ART / ('icon_' + stat + '.png')
            self.assertTrue(image.is_file(), stat)
            with Image.open(image) as icon:
                self.assertEqual(icon.size, (40, 40))
                self.assertEqual(icon.mode, 'RGBA')
                self.assertEqual(icon.getpixel((0, 0))[3], 0)
        self.assertIn('LC_STAT_ICON[row["stat"]]', screen)
        self.assertIn('LC_STAT_ICON.get(row["stat"])', status)

    def test_grid_has_clipped_bounded_choices_and_left_aligned_chips(self):
        screen = SCREEN.read_text()
        self.assertIn('ysize choice_h', screen)
        self.assertIn('clipping True', screen)
        self.assertIn('for chip in row["chips"]:', screen)
        self.assertIn('box_wrap True', screen)
        self.assertNotIn('for line in row["lines"]:', screen)
        self.assertIn('xsize (page_w - 16)', screen)
        self.assertIn('xsize tag_w', screen)
        self.assertIn('add arrow yalign 0.5', screen)

if __name__ == '__main__':
    unittest.main()
