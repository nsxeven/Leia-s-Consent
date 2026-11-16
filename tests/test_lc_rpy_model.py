"""The static Ren'Py model picks the same winners Ren'Py does.

Expectations were checked by hand against init priorities and load order on
main 226101b (e.g. screens.rpy runs at `init offset = -1`, so its stock screens
sit at -501 and every later file's copy replaces them).
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lc_rpy_model as m  # noqa: E402


class RpyModelTests(unittest.TestCase):
    def test_files_load_in_renpy_order(self):
        names = [p.relative_to(m.GAME).as_posix() for p in m.rpy_files()]
        # "00_release_build" sorts below "A", so it loads before everything else.
        self.assertEqual(names[0], "00_release_build.rpy")
        self.assertLess(names.index("screens.rpy"), names.index("script.rpy"))

    def test_init_offset_and_screen_priority(self):
        defs = m.parse_text("init offset = -1\nscreen s():\n    null\nimage i = 'x.png'\n", "synthetic.rpy", 0)
        self.assertEqual([(d.kind, d.priority) for d in defs], [("screen", -501), ("image", 499)])

    def test_effective_screen_winners(self):
        eff = m.effective("screen")
        self.assertTrue(eff["quick_menu"].relpath.endswith(".rpy"))
        self.assertIn("scrapbook_ui", eff["quick_menu"].relpath)
        self.assertIn("scrapbook_ui", eff["quick_menu@touch"].relpath)
        self.assertIn("phone_sweetheart", eff["phone_screen"].relpath)
        self.assertIn("phone_sweetheart", eff["lc_phone_extra_apps"].relpath)

    def test_effective_function_winners(self):
        eff = m.effective("def")
        # apply_choice: the only copy, in choice_engine's init 90 block (folded in clean-up 2c).
        self.assertIn("choice_engine", eff["apply_choice"].relpath)
        self.assertEqual(eff["apply_choice"].priority, 90)
        # ch01_d4_track_text: the init 5 re-score copy wins over the Day Four file.
        self.assertIn("stat_model_v2_later_days", eff["ch01_d4_track_text"].relpath)
        self.assertEqual(eff["ch01_d4_track_text"].priority, 5)

    def test_label_override_resolution(self):
        self.assertEqual(m.effective_label_body("ch01_scene_27_late_photo_drop"),
                         m.effective_label_body("ch01_scene_27_late_photo_drop_staged"))
        self.assertNotEqual(m.effective_label_body("ch01_scene_27_late_photo_drop"),
                            m.effective_label_body("ch01_scene_26_the_compliment"))

    def test_single_jump_alias_resolves_to_target(self):
        labels = m.effective("label")
        aliases = [n for n, d in labels.items()
                   if len(d.body.split("\n")) == 2 and d.body.split("\n")[1].startswith("jump ")]
        for name in aliases:
            target = labels[name].body.split("\n")[1].split()[1]
            if target in labels:
                self.assertEqual(m.effective_label_body(name), m.effective_label_body(target), name)

    def test_python_defs_only_top_level(self):
        names = {d.name for d in m.definitions("def")}
        self.assertNotIn("__init__", names)
        self.assertNotIn("render", names)

    def test_multiline_signature_keeps_whole_body(self):
        """A def whose `):` closes back at the def indent is still one block."""
        base = [d for d in m.definitions("def") if d.name == "phone_store_message"][0]
        self.assertIn("save_attachment", base.body)
        self.assertIn("return True", base.body)


if __name__ == "__main__":
    unittest.main()
