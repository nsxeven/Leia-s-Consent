"""Static invariants for the three new café CGs and the limited Maya rig."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "game"
SCENES = (ROOT / "chapters/ch01/ch01_day2_scenes_01_15.rpy").read_text(encoding="utf-8")
VISUALS = (ROOT / "chapters/ch01/ch01_day2_visuals.rpy").read_text(encoding="utf-8")
GALLERY = (ROOT / "systems/gallery_data.rpy").read_text(encoding="utf-8")
GALLERY_LOGIC = (ROOT / "systems/gallery.rpy").read_text(encoding="utf-8")
RIG = (ROOT / "sprites/maya.rpy").read_text(encoding="utf-8")


def scene(label):
    return SCENES.split("label %s:" % label, 1)[1].split("\nlabel ", 1)[0]


class MayaCafeTests(unittest.TestCase):
    def test_cg_files_exist_and_are_declared(self):
        for slug, filename in (
            ("reveal", "MayaReveal_01"),
            ("cafe_01", "MayaCafe_01"),
            ("cafe_02", "MayaCafe_02"),
        ):
            path = "images/cg/ch02/CH2D2_CG_%s.webp" % filename
            self.assertTrue((ROOT / path).is_file(), path)
            self.assertIn('image cg ch01_d2_maya_%s = At("%s"' % (slug, path), VISUALS)

    def test_scene_05_doorway_before_hug_then_table(self):
        source = scene("ch01_day2_scene_05_meet_maya")
        locations = [source.index(part) for part in (
            '"Maya spotted us before I spotted her."',
            'scene cg ch01_d2_maya_reveal',
            'maya "[player_name]! Wait, you\'re tan?',
            '"She hugged me',
            '"We ordered drinks and found a table',
            'scene cg ch01_d2_maya_cafe_01',
            'mc "This is character assassination.',
        )]
        self.assertEqual(locations, sorted(locations))
        for cg, next_action in (("reveal", '"She hugged me'),
                                ("cafe_01", 'mc "This is character assassination.')):
            segment = source.split("scene cg ch01_d2_maya_%s" % cg, 1)[1].split(next_action, 1)[0]
            self.assertEqual(segment.count("$ exit_cinematic_mode()"), 1)
            self.assertIn("$ exit_cinematic_mode()\n    scene bg ch01_d2_cafe", segment)
            self.assertIn('$ cast(ryan="casual", leia="lounge", julian="travel", maya="green_tube_top")', segment)
        self.assertIn('cast(ryan="casual", leia="lounge", julian="travel", maya="green_tube_top")', source)

    def test_all_three_scene_06_choices_rejoin_before_friendship_cg(self):
        choices = scene("ch01_day2_scene_06_jealousy_test")
        self.assertEqual(choices.count("apply_choice("), 3)
        self.assertEqual(len(re.findall(r'^        "\[d2_maya_(?:include|catchup|dismiss)_text\]":', choices, re.M)), 3)
        self.assertRegex(choices, r'(?m)^    jump ch01_day2_scene_07_leia_maya_click\s*$')
        self.assertLess(choices.rindex('apply_choice("ch01_d2_maya_dismiss_leia")'),
                        choices.rindex('jump ch01_day2_scene_07_leia_maya_click'))
        source = scene("ch01_day2_scene_07_leia_maya_click")
        self.assertLess(source.index('"[girlfriend_name] laughed hard enough'),
                        source.index("scene cg ch01_d2_maya_cafe_02"))
        self.assertLess(source.index("scene cg ch01_d2_maya_cafe_02"),
                        source.index('maya "What about you?'))
        segment = source.split("scene cg ch01_d2_maya_cafe_02", 1)[1].split('maya "What about you?', 1)[0]
        self.assertEqual(segment.count("$ exit_cinematic_mode()"), 1)
        self.assertIn("$ exit_cinematic_mode()\n    scene bg ch01_d2_cafe", segment)
        self.assertIn('$ cast(ryan="casual", leia="lounge", julian="travel", maya="green_tube_top")', segment)

    def test_walk_photo_is_separate_and_cafe_cast_ends(self):
        self.assertIn('image cg ch01_d2_photo_leia_maya = Composite(', VISUALS)
        self.assertIn('gallery_row("d2_photo_leia_maya"', GALLERY)
        self.assertIn('"ch01_d2_photo_leia_maya",', GALLERY)  # still a placeholder
        self.assertIn("$ cast()", scene("ch01_day2_scene_09_photo_walk"))

    def test_gallery_has_distinct_three_page_sequence(self):
        row = GALLERY.split('gallery_row("d2_meet_maya"', 1)[1].split('gallery_row("d2_photo_leia_maya"', 1)[0]
        names = re.findall(r'"(ch01_d2_maya_(?:reveal|cafe_01|cafe_02))"', row)
        self.assertEqual(names, ["ch01_d2_maya_reveal", "ch01_d2_maya_cafe_01", "ch01_d2_maya_cafe_02"])
        self.assertNotIn("mature=True", row)
        # The gallery's existing per-page unlock uses the stable cg image name.
        self.assertIn('renpy.seen_image(("cg", image_name))', GALLERY_LOGIC)
        self.assertIn('gallery_image_seen(entry["pages"][page_index]["image"])', GALLERY_LOGIC)
        self.assertIn('page_index >= len(entry["pages"])', GALLERY_LOGIC)

    def test_maya_rig_uses_only_own_green_top_and_four_faces(self):
        self.assertIn('always "images/sprites/maya/CH2/Chest_GreenTubeTop.png" at leia_chest_breathe', RIG)
        self.assertIn('image maya_green_tube_top = Fixed(lc_sprite_silhouette(', RIG)
        for face in ("smile", "shy", "skeptical", "angry"):
            self.assertIn("image maya_green_tube_top %s = Fixed(" % face, RIG)
        self.assertNotIn("image maya_green_tube_top neutral", RIG)
        self.assertNotIn('"images/sprites/leia/', RIG)
        self.assertNotIn('always "images/sprites/maya/Base_Nude', RIG)


if __name__ == "__main__":
    unittest.main()