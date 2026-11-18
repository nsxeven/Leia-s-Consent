"""tools/new_day.py: dry run writes nothing, --write creates a pack that keeps the Day contract,
existing files are never overwritten. Runs on a temp dir, never on the real game."""
import importlib.util
import io
import re
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("new_day", ROOT / "tools" / "new_day.py")
new_day = importlib.util.module_from_spec(spec)
spec.loader.exec_module(new_day)


class NewDayTests(unittest.TestCase):
    def run_tool(self, root, *args):
        out = io.StringIO()
        code = new_day.main(list(args), root=root, out=out)
        return code, out.getvalue()

    def test_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, text = self.run_tool(tmp, "6")
            self.assertEqual(code, 0)
            self.assertIn("would create game/chapters/ch01/day6/ch01_day6_registrations.rpy", text)
            self.assertEqual(list(Path(tmp).rglob("*")), [])

    def test_write_creates_a_pack_that_keeps_the_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, _text = self.run_tool(tmp, "6", "--write")
            self.assertEqual(code, 0)
            folder = Path(tmp) / "game" / "chapters" / "ch01" / "day6"
            for suffix in ("_scenes.rpy", "_visuals.rpy", "_registrations.rpy", "_gallery.rpy", "_chapter.rpy"):
                self.assertTrue((folder / ("ch01_day6" + suffix)).exists(), suffix)
            pack = "\n".join(p.read_text(encoding="utf-8") for p in sorted(folder.glob("*.rpy")))
            self.assertRegex(pack, r"(?m)^label ch01_day6_start:")
            self.assertRegex(pack, r'get_story_value\("ch01_d5_end_route"')
            self.assertRegex(pack, r'set_story_value\("ch01_d6_end_route"')
            for needed in (r'lc_review_begin\("ch01_d6"', r'call lc_day_review\("ch01_d6"', r'LC_REVIEW_DAYS\["ch01_d6"\]',
                           r'gallery_tab\("ch01_d6"', r'define lc_chapter_card_day6 = '):
                self.assertRegex(pack, needed)
            # every key the stub sets is in its ledger
            ledger = set(re.findall(r"(?m)^# key (\w+):", pack))
            for key in re.findall(r'set_story_(?:value|flag)\("(\w+)"', pack):
                self.assertIn(key, ledger)
            module = Path(tmp) / "game" / "python-packages" / "lc_days" / "day6.py"
            env = {}
            exec(compile(module.read_text(encoding="utf-8"), str(module), "exec"), env)
            self.assertEqual(env["CHAPTER"]["day"], 6)
            self.assertTrue((Path(tmp) / "tests" / "test_ch01_day6.py").exists())
            self.assertIn(b"\r\n", (folder / "ch01_day6_scenes.rpy").read_bytes())

    def test_never_overwrites(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self.run_tool(tmp, "6", "--write")[0], 0)
            code, text = self.run_tool(tmp, "6", "--write")
            self.assertEqual(code, 1)
            self.assertIn("refusing", text)

    def test_existing_days_are_refused_on_the_real_tree(self):
        code, text = self.run_tool(ROOT, "5")
        self.assertEqual(code, 1)
        self.assertIn("ch01_day5_registrations.rpy", text)


if __name__ == "__main__":
    unittest.main()
