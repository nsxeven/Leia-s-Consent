"""Source-level regression contracts for optional POVs (not run by this change)."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCENE = ROOT / "game/chapters/ch01/zzzz_ch01_day2_polish_revision.rpy"
SYSTEM = ROOT / "game/systems/hidden_pov.rpy"
REGISTRY = ROOT / "game/zzzz_ch01_breakfast_presentation.rpy"


class HiddenPovSourceTests(unittest.TestCase):
    def test_scene_keeps_phone_and_story_order_without_blocking_prompt(self):
        scene = SCENE.read_text(encoding="utf-8")
        start = scene.index("label ch01_day2_scene_03_maya_message_v2:")
        end = scene.index("label ch01_day2_scene_08_maya_julian_v2:")
        block = scene[start:end]
        self.assertNotIn("call screen lc_breakfast_julian_pov", block)
        self.assertNotIn('if _return == "pov"', block)
        ordered = (
            'phone_add_message(', 'scene cg ch01_d2_breakfast_02',
            '$ lc_pov_begin("d2_breakfast_julian")', '$ exit_cinematic_mode()',
            '$ lc_phone_hud_on_cg = True', 'gf "Oh. Maya."',
            'phone_offer_reply(', 'set_story_flag("ch01_d2_maya_meetup_confirmed")',
            '$ lc_pov_end()', 'jump ch01_day2_scene_04_jealousy_callback',
        )
        offsets = [block.index(item) for item in ordered]
        self.assertEqual(offsets, sorted(offsets))

    def test_gallery_id_and_source_scope_stay_stable(self):
        registry = REGISTRY.read_text(encoding="utf-8")
        gallery = (ROOT / "game/systems/gallery_data.rpy").read_text(encoding="utf-8")
        self.assertIn('image="cg ch01_d2_breakfast_julian_pov"', registry)
        self.assertIn('source="cg ch01_d2_breakfast_02"', registry)
        self.assertIn('gallery_row("d2_breakfast_pov"', gallery)
        self.assertIn('[("ch01_d2_breakfast_julian_pov", "Julian\'s POV")], mature=True)', gallery)

    def test_only_click_handler_marks_seen_and_screens_do_not_return(self):
        source = SYSTEM.read_text(encoding="utf-8")
        self.assertEqual(source.count("renpy.mark_image_seen(image)"), 1)
        self.assertIn('action Function(lc_pov_open, moment_id)', source)
        self.assertIn('action Function(lc_pov_close)', source)
        self.assertIn('modal True', source)
        self.assertIn('config.afm_callback = lc_pov_afm_callback', source)
        self.assertIn('renpy.stop_skipping()', source)
        self.assertIn('renpy.showing(entry["source"], layer="master")', source)
        self.assertNotIn('action Return(', source)
        self.assertNotIn('call screen', source)


if __name__ == "__main__":
    unittest.main()
