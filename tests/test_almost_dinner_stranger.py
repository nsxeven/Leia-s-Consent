"""Guard the fixed dinner near-miss without changing route state."""
import re
import unittest
from pathlib import Path


SOURCE = (Path(__file__).resolve().parents[1] / "game/chapters/ch01/ch01_scenes_07_13.rpy")


class AlmostDinnerStrangerTests(unittest.TestCase):
    def test_photo_offer_refusal_and_inner_reaction(self):
        scene = SOURCE.read_text().split('label ch01_scene_09_dinner:', 1)[1].split('label ch01_scene_10_after_dinner_drinks:', 1)[0]
        start = scene.index('    stranger "Seriously, I\'m sorry. Can I get you another drink? Or—')
        end = scene.index('    $ lc_sfx("leia_laugh")', start)
        beat = scene[start:end]
        expected = [
            'stranger "Seriously, I\'m sorry. Can I get you another drink? Or— you were looking for someone to take a photo, right? I could do it. Least I can do."',
            '"[girlfriend_name]\'s phone was still in her hand. She looked down at it, then up at him, and for a second she didn\'t answer."',
            '$ lc_duck(0.5)',
            'think "It\'s a photo. It\'s literally just a photo. Why is she taking so long?"',
            '"Her thumb was already on the screen when she glanced down at the front of her dress, still dripping onto the terrace."',
            '$ lc_unduck()',
            'gf "No, no, it\'s okay. I\'m literally dripping, I\'m not taking a photo like this. And I walked into you, so that one\'s on me."',
            'stranger "Then we\'re both terrible at walking."',
        ]
        self.assertEqual([line.strip() for line in beat.splitlines() if line.strip()], expected)
        self.assertIsNone(re.search(r'\b(?:Ryan|Leia|Julian)\b', beat))
        self.assertIn('[girlfriend_name]', beat)


if __name__ == '__main__':
    unittest.main()
