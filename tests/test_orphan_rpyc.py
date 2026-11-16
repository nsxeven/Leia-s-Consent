"""Stray compiled scripts: the clean-up tool and the start-up guard (clean-up PR 2c review).

Ren'Py loads a .rpyc even when its .rpy was moved or deleted, and .rpyc files are
git-ignored, so a pull never removes them. A stale copy can crash the game at
load or silently replace a screen.
"""
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
import lc_rpy_model as m  # noqa: E402


def load_tool():
    spec = importlib.util.spec_from_file_location("clean_orphan_rpyc", ROOT / "tools" / "clean_orphan_rpyc.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class OrphanRpycTests(unittest.TestCase):
    def make_game(self, files):
        tmp = Path(tempfile.mkdtemp())
        for rel in files:
            p = tmp / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("x", encoding="utf-8")
        return tmp

    def test_finds_only_orphans(self):
        game = self.make_game([
            "script.rpy", "script.rpyc",                      # paired
            "screens/old_zz.rpyc",                            # orphan
            "systems/feature_ren.py", "systems/feature.rpyc",  # paired with _ren.py
            "saves/1-1.save", "cache/bytecode.rpyb", "cache/x.rpyc",  # ignored folders
        ])
        self.assertEqual(load_tool().find_orphans(game), ["screens/old_zz.rpyc"])

    def test_delete_removes_them(self):
        game = self.make_game(["script.rpy", "a/stale.rpyc"])
        tool = load_tool()
        self.assertEqual(tool.delete_orphans(game), ["a/stale.rpyc"])
        self.assertFalse((game / "a/stale.rpyc").exists())
        self.assertTrue((game / "script.rpy").exists())

    def test_startup_guard_is_dev_checkout_only_and_registered(self):
        guard = m.effective("def")["_lc_check_orphan_compiled_scripts"].body
        self.assertIn('"script.rpy"', guard)          # skipped in release builds (no .rpy shipped)
        self.assertIn("clean_orphan_rpyc", guard)     # tells Darryn how to fix it
        text = "\n".join(d.body for d in m.definitions("effect"))
        self.assertIn("_lc_check_orphan_compiled_scripts()", text)


if __name__ == "__main__":
    unittest.main()
