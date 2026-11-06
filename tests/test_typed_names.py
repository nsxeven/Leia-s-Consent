"""Player-visible text must use the typed names, not the defaults (Prologue-Day 1 demo check)."""
import re
import unittest
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / "game"
STORY = ["chapters/prologue.rpy", "chapters/ch01/ch01_main.rpy", "chapters/ch01/ch01_scenes_04_06.rpy",
         "chapters/ch01/ch01_scenes_07_13.rpy", "chapters/ch01/ch01_scenes_14_30.rpy",
         "chapters/ch01/zzzz_ch01_scene27_staged_phone.rpy", "chapters/ch01/zz_ch01_phone_sequence_revision.rpy"]
DEFAULTS = {'entered_player_name else "Ryan"', 'entered_girlfriend_name else "Leia"', 'entered_friend_name else "Julian"'}


class TypedNameTests(unittest.TestCase):
    def test_demo_story_has_no_hardcoded_names_in_text(self):
        bad = []
        for rel in STORY:
            for n, line in enumerate((GAME / rel).read_text(encoding="utf-8").splitlines(), 1):
                code = line.split("#", 1)[0] if not line.lstrip().startswith(("\"", "gf ", "mc ", "friend ")) else line
                for s in re.findall(r'"((?:[^"\\]|\\.)*)"', code):
                    if re.search(r"\b(Ryan|Leia|Julian)\b", s) and not any(d in line for d in DEFAULTS):
                        bad.append("%s:%d %s" % (rel, n, s[:60]))
        self.assertEqual(bad, [])

    def test_ui_text_with_default_names_is_customised(self):
        self.assertIn("gallery_customize_names(STATUS_MODE_NOTES", (GAME / "systems/status_display.rpy").read_text(encoding="utf-8"))
        self.assertIn('gallery_customize_names(page_info["label"])', (GAME / "screens/gallery_screen.rpy").read_text(encoding="utf-8"))
        self.assertIn('gallery_customize_names(phone_outfit["description"])',
                      (GAME / "screens/zzzzzz_phone_ios_presentation.rpy").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
