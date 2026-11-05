import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
EFFECTS = (ROOT / "game" / "systems" / "effects.rpy").read_text(encoding="utf-8")
UI = (ROOT / "game" / "screens" / "zzzzzzzz_scrapbook_ui.rpy").read_text(encoding="utf-8")


class EffectsFoundationTests(unittest.TestCase):
    def test_shakes_target_visible_camera_and_respect_toggle(self):
        self.assertIn('renpy.show_layer_at([transform], layer="master", reset=True, camera=True)', EFFECTS)
        self.assertIn('not getattr(persistent, "lc_screen_shake", True)', EFFECTS)
        self.assertIn('def lc_reset_camera()', EFFECTS)

    def test_flash_is_overlay_and_off_is_noop(self):
        self.assertIn('image lc_effect_flash_white = Solid("#ffffff")', EFFECTS)
        self.assertIn('trans.alpha = 0.0', EFFECTS)
        self.assertNotIn('scene lc_photo_flash_white at lc_flash', EFFECTS)

    def test_bloom_is_brief_overlay_not_permanent_tint(self):
        bloom = EFFECTS.split("transform lc_warm_bloom:", 1)[1].split("transform lc_punch_zoom:", 1)[0]
        self.assertIn("alpha 0.0", bloom)
        self.assertNotIn("TintMatrix", bloom)

    def test_dream_sway_overscans_and_has_motion_without_rotation(self):
        dream = EFFECTS.split("transform lc_dream_sway:", 1)[1].split("image lc_effect_flash_white", 1)[0]
        self.assertIn("zoom 1.05", dream)
        self.assertIn("blur", dream)
        self.assertNotIn("rotate", dream)
        self.assertIn("lc_effect_dream_vignette", EFFECTS)

    def test_existing_ui_hook_calls_cue_directly(self):
        hook = UI.split("def lc_ui_play", 1)[1].split("def lc_shown_scene_names", 1)[0]
        self.assertIn('return globals().get("cue"', hook)
        self.assertNotIn("renpy.play(path", hook)


if __name__ == "__main__":
    unittest.main()
