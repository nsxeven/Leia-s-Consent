"""Stray compiled scripts: the clean-up tool and the start-up guard (clean-up PR 2c review).

Ren'Py loads a .rpyc even when its .rpy was moved or deleted, and .rpyc files are
git-ignored, so a pull never removes them. A stale copy can crash the game at
load or silently replace a screen.
"""
import contextlib
import importlib.util
import io
import json
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

    # Save continuity (clean-up PR 4): Ren'Py names every statement and keeps those
    # names in the .rpyc next to the .rpy. A save points at statement names, so when
    # a .rpy moves its compiled copy must move with it, or mid-scene saves in that
    # file cannot find their place. The tool moves orphans listed in the rename map.

    def compiled(self, game, rel, text):
        p = game / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def test_moves_a_listed_orphan_to_its_new_path(self):
        game = self.make_game(["chapters/day1/scene.rpy"])
        self.compiled(game, "chapters/scene.rpyc", "old names")
        moved = load_tool().move_orphans(game, {"chapters/scene.rpy": "chapters/day1/scene.rpy"})
        self.assertEqual(moved, [("chapters/scene.rpyc", "chapters/day1/scene.rpyc")])
        self.assertFalse((game / "chapters/scene.rpyc").exists())
        self.assertEqual((game / "chapters/day1/scene.rpyc").read_text(encoding="utf-8"), "old names")

    def test_replaces_a_compile_made_after_the_move(self):
        # Launching before running the tool compiles the moved .rpy with NEW names
        # (Ren'Py writes the .rpyc while loading, before the start-up guard can stop
        # it). The guard then refuses to start the game, so no save can use those new
        # names: the old compiled copy (with the names saves use) must win.
        game = self.make_game(["chapters/day1/scene.rpy"])
        self.compiled(game, "chapters/scene.rpyc", "old names")
        self.compiled(game, "chapters/day1/scene.rpyc", "fresh names")
        moved = load_tool().move_orphans(game, {"chapters/scene.rpy": "chapters/day1/scene.rpy"})
        self.assertEqual(moved, [("chapters/scene.rpyc", "chapters/day1/scene.rpyc")])
        self.assertEqual((game / "chapters/day1/scene.rpyc").read_text(encoding="utf-8"), "old names")
        self.assertEqual(load_tool().find_orphans(game), [])

    def test_unlisted_orphans_and_missing_targets_are_left_for_delete(self):
        game = self.make_game(["script.rpy"])
        self.compiled(game, "gone.rpyc", "x")                 # not in the map
        self.compiled(game, "chapters/scene.rpyc", "x")       # listed, but its new .rpy is absent
        tool = load_tool()
        self.assertEqual(tool.move_orphans(game, {"chapters/scene.rpy": "chapters/day1/scene.rpy"}), [])
        self.assertEqual(tool.delete_orphans(game), ["chapters/scene.rpyc", "gone.rpyc"])

    def test_follows_a_chain_of_moves(self):
        game = self.make_game(["c/scene.rpy"])
        self.compiled(game, "a/scene.rpyc", "old names")
        moved = load_tool().move_orphans(game, {"a/scene.rpy": "b/scene.rpy", "b/scene.rpy": "c/scene.rpy"})
        self.assertEqual(moved, [("a/scene.rpyc", "c/scene.rpyc")])

    def test_main_moves_before_deleting(self):
        root = Path(tempfile.mkdtemp())
        game = root / "game"
        (root / "tools" / "dev").mkdir(parents=True)
        (root / "tools" / "dev" / "rpyc_moves.json").write_text(
            '{"chapters/scene.rpy": "chapters/day1/scene.rpy"}', encoding="utf-8")
        self.compiled(game, "chapters/day1/scene.rpy", "label x:")
        self.compiled(game, "chapters/scene.rpyc", "old names")
        self.compiled(game, "stale.rpyc", "x")
        tool = load_tool()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(tool.main([], root=root), 0)
        self.assertIn("Moved:", out.getvalue())
        self.assertIn("chapters/scene.rpyc -> chapters/day1/scene.rpyc", out.getvalue())
        self.assertIn("Removed:", out.getvalue())
        self.assertEqual((game / "chapters/day1/scene.rpyc").read_text(encoding="utf-8"), "old names")
        self.assertFalse((game / "stale.rpyc").exists())

    def test_committed_rename_map_is_valid(self):
        """Every entry: old .rpy gone, new .rpy present (game/-relative paths)."""
        moves = json.loads((ROOT / "tools" / "dev" / "rpyc_moves.json").read_text(encoding="utf-8"))
        self.assertTrue(moves)
        for old, new in moves.items():
            self.assertTrue(old.endswith(".rpy") and new.endswith(".rpy"), old)
            self.assertFalse((ROOT / "game" / old).exists(), f"{old} still exists")
            final = new
            while final in moves:
                final = moves[final]
            self.assertTrue((ROOT / "game" / final).exists(), f"{old} -> {final} missing")

    def test_startup_guard_is_dev_checkout_only_and_registered(self):
        guard = m.effective("def")["_lc_check_orphan_compiled_scripts"].body
        self.assertIn('"script.rpy"', guard)          # skipped in release builds (no .rpy shipped)
        self.assertIn("clean_orphan_rpyc", guard)     # tells Darryn how to fix it
        text = "\n".join(d.body for d in m.definitions("effect"))
        self.assertIn("_lc_check_orphan_compiled_scripts()", text)


if __name__ == "__main__":
    unittest.main()
