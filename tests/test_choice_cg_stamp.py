"""Full Transparency camera stamp: how many CGs a choice shows (darryn 2026-11-08)."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAGS = (ROOT / "game/systems/choice_path_tags.rpy").read_text(encoding="utf-8")
CARD = (ROOT / "game/screens/zzzzzzzz_scrapbook_ui.rpy").read_text(encoding="utf-8")
POOL = (ROOT / "game/chapters/ch01/ch01_scenes_04_06.rpy").read_text(encoding="utf-8")


def counts():
    block = TAGS.split("define LC_CHOICE_CG_COUNT = {", 1)[1].split("}", 1)[0]
    return {m.group(1): (int(m.group(2)), int(m.group(3)))
            for m in re.finditer(r'"(\w+)": \((\d+), (\d+)\)', block)}


class ChoiceCgStampTests(unittest.TestCase):

    def test_full_only_and_on_the_card(self):
        fn = TAGS.split("def lc_choice_cg_stamp(caption):", 1)[1].split("\n    def ", 1)[0]
        self.assertIn('if current_choice_mode() != "full":', fn)
        self.assertIn("$ cg_stamp = lc_choice_cg_stamp(item.caption)", CARD)
        self.assertIn('add "images/ui/scrapbook/icon_camera.png"', CARD)
        self.assertTrue((ROOT / "game/images/ui/scrapbook/icon_camera.png").is_file())

    def test_counts_are_sane_and_ids_exist(self):
        data = counts()
        self.assertTrue(data)
        for choice_id, (low, high) in data.items():
            self.assertLessEqual(low, high, choice_id)
            self.assertGreaterEqual(low, 0, choice_id)
            self.assertRegex(
                "".join(p.read_text(encoding="utf-8") for p in (ROOT / "game/chapters").rglob("*.rpy")),
                r'format_choice\("%s"' % choice_id, choice_id)

    def test_pool_photo_counts_match_the_scene(self):
        # Each branch's highest capture number = CGs seen (capture 01 shown before the menu).
        def branch(start, end):
            a = POOL.index('"[%s]":' % start)
            b = POOL.index('"[%s]":' % end) if end else len(POOL)
            return POOL[a:b]
        seen = lambda text: max(int(n) for n in re.findall(r"scene cg ch01_photo_capture_0(\d)_", text))
        data = counts()
        self.assertEqual(data["ch01_photo_support"][1], seen(branch("ch01_photo_support_text", "ch01_photo_more_text")))
        self.assertEqual(data["ch01_photo_more"][1], seen(branch("ch01_photo_more_text", "ch01_photo_exit_text")))
        exit_branch = POOL[POOL.index('"[ch01_photo_exit_text]":'):]
        exit_branch = exit_branch[:exit_branch.index('set_story_value("ch01_pool_capture_count", 0)') + 60]
        self.assertEqual(data["ch01_photo_exit"], (1, seen(exit_branch)))


if __name__ == "__main__":
    unittest.main()
