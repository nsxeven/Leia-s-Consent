"""Source-level regression contracts for optional POVs ."""
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


class HiddenPovHardeningTests(unittest.TestCase):
    def setUp(self):
        self.system = SYSTEM.read_text(encoding="utf-8")
        self.registry = REGISTRY.read_text(encoding="utf-8")

    def test_hit_target_is_large_with_touch_variant_and_hover_state(self):
        self.assertIn("LC_POV_HITBOX = 120", self.system)
        self.assertIn("LC_POV_HITBOX_TOUCH = 160", self.system)
        self.assertIn('variant "touch"', self.system)
        self.assertIn("hover_background lc_pov_cue_art(size, True", self.system)
        self.assertIn("transform lc_pov_hover_pop:", self.system)
        self.assertTrue((ROOT / "game/gui/pov/glow_idle.svg").is_file())
        self.assertTrue((ROOT / "game/gui/pov/glow_hover.svg").is_file())
        # Breakfast cue sits at Julian's temple, beside and above his eye.
        self.assertIn("center=(1785, 255)", self.registry)

    def test_static_cue_path_never_binds_child_to_zoom(self):
        # Regression: an ATL `transform lc_pov_static(a, z)` called as
        # lc_pov_static(a)(child) bound the image path to z and crashed the
        # Full/Developer cue and reduced motion.
        self.assertNotIn("transform lc_pov_static", self.system)
        self.assertIn("def lc_pov_static(a=1.0, z=1.0):", self.system)
        self.assertIn("return Transform(child, alpha=a, zoom=z)", self.system)
        # Execute the real helper with a stand-in Transform.
        start = self.system.index("    def lc_pov_static(")
        end = self.system.index("        return apply", start) + len("        return apply")
        source = "\n".join(line[4:] for line in self.system[start:end].splitlines())
        calls = []
        scope = {"Transform": lambda child, **kw: calls.append((child, kw)) or kw}
        exec(source, scope)
        for a, z in ((0.5, 1.0), (0.75, 1.0), (1.0, 1.1)):
            kw = scope["lc_pov_static"](a, z)("gui/pov/glow_idle.svg")
            self.assertIsInstance(kw["zoom"], float)
            self.assertIsInstance(kw["alpha"], float)
        self.assertTrue(all(child == "gui/pov/glow_idle.svg" for child, _ in calls))

    def test_full_transparency_cue_is_a_red_circular_button(self):
        for name in ("bang_idle", "bang_hover", "bang_ring"):
            svg = (ROOT / "game/gui/pov" / (name + ".svg")).read_text(encoding="utf-8")
            self.assertIn("<circle", svg)
        idle = (ROOT / "game/gui/pov/bang_idle.svg").read_text(encoding="utf-8")
        hover = (ROOT / "game/gui/pov/bang_hover.svg").read_text(encoding="utf-8")
        self.assertIn('fill="#d6334a"', idle)
        self.assertIn('stroke="#ffffff"', hover)   # white ring highlight on hover
        self.assertNotIn('stroke="#ffffff"', idle)
        art = self.system[self.system.index("def lc_pov_cue_art"):self.system.index("screen lc_pov_hotspot():")]
        bang = art[art.index("if bang:"):]
        self.assertIn("gui/pov/bang_idle.svg", bang)
        self.assertIn("gui/pov/bang_hover.svg", bang)
        self.assertIn("lc_pov_bang_ring", bang)
        self.assertNotIn("DejaVu", bang)
        self.assertNotIn('Text("!"', bang)

    def test_registration_is_validated_after_init(self):
        self.assertIn("init 999 python:", self.system)
        self.assertIn("renpy.has_image(entry[key], exact=True)", self.system)
        self.assertIn('("dialogue box / phone HUD / quick menu", (0, 792, 1920, 288))', self.system)
        self.assertIn("disagrees with Gallery row", self.system)
        self.assertIn("if fatal and config.developer:", self.system)

    def test_begin_while_active_warns_and_ends_previous(self):
        begin = self.system[self.system.index("def lc_pov_begin"):self.system.index("def lc_pov_end")]
        self.assertIn("_lc_pov_warn(", begin)
        self.assertIn("lc_pov_end()", begin)

    def test_accessibility_sfx_and_reduced_motion(self):
        self.assertIn('alt "Hidden moment: [cue_title]"', self.system)
        self.assertIn("renpy.music.play(LC_POV_CUE_AUDIO", self.system)
        chime = (ROOT / "game/systems/hidden_pov_chime.rpy").read_text(encoding="utf-8")
        self.assertIn("LC_POV_CUE_AUDIO = AudioData(", chime)
        credits = (ROOT / "game/audio/CREDITS.md").read_text(encoding="utf-8")
        self.assertIn("hidden_pov_chime.rpy", credits)
        self.assertIn("def lc_pov_reduce_motion", self.system)

    def test_viewer_sits_above_phone_banner(self):
        viewer = self.system[self.system.index("screen lc_pov_viewer"):]
        zorder = int(viewer.split("zorder", 1)[1].split()[0])
        self.assertGreater(zorder, 620)

    def test_legacy_breakfast_screen_stub_exists_for_old_saves(self):
        self.assertIn("screen lc_breakfast_julian_pov(", self.registry)
        self.assertIn("timer 0.01 action Return(None)", self.registry)

    def test_gallery_hint_for_missed_hidden_pov(self):
        gallery = (ROOT / "game/screens/gallery_screen.rpy").read_text(encoding="utf-8")
        logic = (ROOT / "game/systems/gallery.rpy").read_text(encoding="utf-8")
        self.assertIn("def gallery_is_hidden_pov", logic)
        self.assertIn("gallery_is_hidden_pov(gallery_id)", gallery)
        self.assertIn('"look for the sparkle"', gallery)


if __name__ == "__main__":
    unittest.main()
