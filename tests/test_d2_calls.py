"""Day Two calls (Darryn, 15 Nov 2026): Shop_01 dresses beat, Leia's casual
café/mall outfit, the restored "Is she pretty?" breakfast menu, Hidden POV cue
visibility, and the proofread overflow/grammar fixes."""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
CH01 = GAME / "chapters/ch01"
sys.path.insert(0, str(GAME / "python-packages"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

SCENES = (CH01 / "day2" / "ch01_day2_scenes_01_15.rpy").read_text(encoding="utf-8")
POLISH = (CH01 / "day2" / "ch01_day2_scenes_01_15.rpy").read_text(encoding="utf-8")
VISUALS = (CH01 / "day2" / "ch01_day2_visuals.rpy").read_text(encoding="utf-8")
GALLERY = (GAME / "systems/gallery_data.rpy").read_text(encoding="utf-8")
POV = (GAME / "systems/hidden_pov.rpy").read_text(encoding="utf-8")


def block(source, label):
    return source.split("label %s:" % label, 1)[1].split("\nlabel ", 1)[0]


class ShopDressesTests(unittest.TestCase):
    def test_shop_01_is_declared_and_in_the_gallery(self):
        path = "images/cg/ch02/CH2D2_CG_Shop_01.webp"
        self.assertTrue((GAME / path).is_file())
        self.assertIn('image cg ch01_d2_shop_dresses = At("%s", prologue_fullscreen)' % path, VISUALS)
        self.assertIn('("ch01_d2_shop_dresses", "Red or black?")', GALLERY)

    def test_shop_01_plays_inside_the_boutique_before_leias_rack(self):
        body = block(SCENES, "ch01_day2_scene_11b_boutique")
        order = ['scene cg ch01_d2_mall_boutique_window', '"[girlfriend_name] still followed her inside."',
                 'scene cg ch01_d2_shop_dresses', 'maya "Okay. Be honest. Red or black?"',
                 '"Maya kept the red dress over her arm.',
                 'stared at something less daunting', 'scene cg ch01_d2_boutique_changing_room']
        offsets = [body.index(part) for part in order]
        self.assertEqual(offsets, sorted(offsets))
        dresses = body.split("scene cg ch01_d2_shop_dresses", 1)[1].split("stared at something less daunting", 1)[0]
        self.assertNotIn("cutout", dresses.lower())
        self.assertIn("long red slip", dresses)
        self.assertNotIn("red asymmetric cutout mini", SCENES)


class LeiaCasualOutfitTests(unittest.TestCase):
    def test_cafe_and_mall_use_the_casual_sprite(self):
        self.assertTrue((GAME / "images/sprites/leia/PRO/Base_Casual.png").is_file())
        self.assertNotIn('leia="lounge"', SCENES)
        self.assertEqual(SCENES.count('cast(ryan="casual", leia="casual", julian="evening", maya="green_tube_top")'), 3)
        self.assertNotIn("TODO: Leia's café/mall CGs", SCENES)

    def test_boutique_casts_casual_then_hides_her_in_the_changing_room(self):
        body = block(SCENES, "ch01_day2_scene_11b_boutique")
        before, after = body.split("scene cg ch01_d2_boutique_changing_room", 1)
        # Changing-room rework: Leia and Maya leave the stage (try-on dresses have no
        # sprites yet) before the first changing-room CG. Leia comes back in the try-on
        # dress (Latex Dress sprite) after she turns around; both return in their own
        # clothes once they have changed back.
        self.assertIn('$ cast_remove("leia", "maya")', before.split('"Maya kept the red dress', 1)[1])
        boutique = after.split("label ", 1)[0]
        self.assertIn('$ cast(ryan="casual", leia="latex_dress", maya="red_dress")', boutique)
        self.assertLess(boutique.index('leia="latex_dress"'), boutique.index('cast_add(leia="casual", maya="green_tube_top")'))
        self.assertLess(boutique.index('cast_add(leia="casual"'), boutique.index("emerged in their normal clothes"))
        self.assertIn('$ cast(ryan="casual", leia="casual", maya="green_tube_top")\n    "Maya kept the red dress', body)
        villa = block(SCENES, "ch01_day2_scene_12_villa_pool_plan")
        self.assertIn("$ cast()", villa.split('"We headed back', 1)[0])


class IsShePrettyMenuTests(unittest.TestCase):
    CHOICES = ("ch01_d2_maya_reassure", "ch01_d2_maya_tease_jealousy", "ch01_d2_maya_open_honest")

    def setUp(self):
        self.body = block(POLISH, "ch01_day2_scene_03_maya_message")

    def test_menu_follows_the_phone_reply_while_breakfast_is_up(self):
        order = ['phone_offer_reply("maya"', 'gf "Is she pretty?"', "    menu:",
                 'set_story_flag("ch01_d2_maya_meetup_confirmed")', "$ lc_pov_end()",
                 "jump ch01_day2_scene_04_jealousy_callback"]
        offsets = [self.body.index(part) for part in order]
        self.assertEqual(offsets, sorted(offsets))
        # No jump/return between the start of the label and the menu: always reachable.
        before_menu = self.body.split("    menu:", 1)[0]
        self.assertNotRegex(before_menu, r"\n\s+(jump|return)\b")
        self.assertNotRegex(before_menu, r"\n    if ")

    def test_lead_in_does_not_repeat_the_loudest_nothing_beat(self):
        self.assertEqual(self.body.count("loudest 'nothing'"), 1)
        self.assertNotIn("We're doing 'nothing' again?", self.body)

    def test_each_choice_applies_its_effects(self):
        from lc_effective_effects import effective_effects
        effects = effective_effects()
        menu = self.body.split("    menu:", 1)[1].split("\n    if ", 1)[0]
        branches = re.split(r'\n        "\[(d2_maya_\w+_text)\]":', menu)[1:]
        self.assertEqual(len(branches), 6)
        for (var, text), cid in zip(zip(branches[::2], branches[1::2]), self.CHOICES):
            self.assertIn('$ %s = format_choice("%s"' % (var, cid), self.body)
            self.assertIn('$ apply_choice("%s")' % cid, text)
            self.assertTrue(effects.get(cid), cid)


class HiddenPovCueVisibilityTests(unittest.TestCase):
    def test_immersive_sparkle_is_larger_and_never_fades_low(self):
        self.assertIn("LC_POV_STAR_ZOOM_IDLE = 1.6", POV)
        self.assertIn("LC_POV_STAR_ZOOM_HOVER = 1.8", POV)
        self.assertIn("Transform(glow_t(glow), zoom=0.55", POV)
        twinkle = POV.split("transform lc_pov_twinkle:", 1)[1].split("repeat", 1)[0]
        self.assertEqual(min(float(a) for a in re.findall(r"alpha ([\d.]+)", twinkle)), 0.88)

    def test_insight_bang_reacts_to_hover_and_reduced_motion_stays_static(self):
        insight = POV.split('if mode == "insight":', 1)[1].split('if mode == "developer":', 1)[0]
        self.assertIn('hover_color "#ffffff"', insight)
        self.assertIn("hover_outlines", insight)
        self.assertIn("lc_pov_static(0.95, 1.06) if still else lc_pov_glow_breathe", POV)
        self.assertIn("lc_pov_static(1.0) if still else lc_pov_twinkle", POV)


    def test_hovering_the_cue_does_not_advance_dialogue(self):
        self.assertIn("hovered Function(lc_pov_hover_sound)", POV)
        self.assertNotIn("hovered Function(lc_ui_sound", POV)
        body = POV.split("def lc_pov_hover_sound():", 1)[1].split("\n\n", 1)[0]
        self.assertTrue(body.rstrip().endswith("return None"))


class ProofreadOverflowTests(unittest.TestCase):
    def test_three_long_lines_are_split_and_grammar_fixed(self):
        b19 = (CH01 / "day2" / "ch01_day2_scene_19b_leia_asks_maya.rpy").read_text(encoding="utf-8")
        d16 = (CH01 / "day2" / "ch01_day2_scenes_16_30.rpy").read_text(encoding="utf-8")
        d1 = (CH01 / "day1" / "ch01_scenes_07_13.rpy").read_text(encoding="utf-8")
        self.assertIn('everybody leaves eventually."\n    gf "I was ready', b19)
        self.assertIn('at some point in the night."\n    "One arm', SCENES)
        self.assertIn('what kind of guy says that."\n        think "Instead', d16)
        self.assertIn("and more of him than he probably intended", d1)


if __name__ == "__main__":
    unittest.main()
