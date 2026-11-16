# Source-checkout checks - stop start-up when stray compiled scripts are present
#
# Purpose: Ren'Py loads a .rpyc even after its .rpy was moved or deleted (they are git-ignored),
#   which can crash at load or silently replace a screen. In a source checkout only (game/script.rpy
#   present) this stops the game with the list and the fix: close the game, run
#   tools/clean_orphan_rpyc.bat (moves .rpyc per tools/dev/rpyc_moves.json so saves keep their
#   place, then deletes the rest). Builds without .rpy sources skip it; JoiPlay builds ship the .rpy
#   files, so it runs there too, harmlessly (a fresh install has no strays).
#
# Public API: none - it runs by itself at start-up
#
# Internal (helpers for this file and its screens; do not call from scenes): _lc_check_orphan_compiled_scripts
#
# Example:
#   python tools/clean_orphan_rpyc.py --check     (list strays without changing anything)
#
# Depends on: config.gamedir and os only
# Hooks: none
# Load order: init -1500 (see below): earliest, so it reports before any code a stale .rpyc could
#   break
# Docs: docs/ARCHITECTURE.md   Tests: tests/test_orphan_rpyc.py

# load order: as early as possible (init -1500), so it runs before any init code a
# stale .rpyc could break (e.g. a duplicate Hidden POV registration at init 1).
# It only needs config.gamedir and os.
init -1500 python:

    def _lc_check_orphan_compiled_scripts():
        import os
        gamedir = config.gamedir
        if not os.path.exists(os.path.join(gamedir, "script.rpy")):
            return None
        orphans = []
        for root, dirs, files in os.walk(gamedir):
            if root == gamedir:
                dirs[:] = [d for d in dirs if d not in ("saves", "cache")]
            for name in files:
                if not name.endswith(".rpyc"):
                    continue
                source = os.path.join(root, name[:-1])
                ren_py = os.path.join(root, name[:-5] + "_ren.py")
                if not os.path.exists(source) and not os.path.exists(ren_py):
                    orphans.append(os.path.relpath(os.path.join(root, name), gamedir).replace("\\", "/"))
        # A Force Recompile renames a moved script's old .rpyc to .rpyc.bak; that backup
        # still holds the statement names saves use, so the tool must put it back first.
        moves_path = os.path.join(config.basedir, "tools", "dev", "rpyc_moves.json")
        if os.path.exists(moves_path):
            import json
            with open(moves_path, "r", encoding="utf-8") as handle:
                moves = json.load(handle)
            for old in moves:
                bak = os.path.join(gamedir, old[:-4] + ".rpyc.bak")
                if os.path.exists(bak) and not os.path.exists(os.path.join(gamedir, old)):
                    orphans.append(old[:-4] + ".rpyc.bak")
        if orphans:
            raise Exception(
                "Stale compiled script files were found (their .rpy was moved or deleted):\n  "
                + "\n  ".join(sorted(orphans))
                + "\nClose the game and double-click tools/clean_orphan_rpyc.bat "
                "(or run: python tools/clean_orphan_rpyc.py), then start again.")
        return None

    _lc_check_orphan_compiled_scripts()
