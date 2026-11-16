# Source-checkout safety checks (developer machines only).
#
# Stray compiled scripts: Ren'Py loads a .rpyc even after its .rpy was moved or
# deleted, and .rpyc files are git-ignored, so a pull that moves script files
# leaves stale copies behind. A stale copy can silently replace a screen (e.g. an
# old choice menu) or crash the game at load. This check stops the game with a
# clear message instead. It only runs in a source checkout (game/script.rpy is
# present); release builds ship no .rpy files, so it is skipped there.
# Fix: close the game, double-click tools/clean_orphan_rpyc.bat
# (or run: python tools/clean_orphan_rpyc.py). Tests: tests/test_orphan_rpyc.py.

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
        if orphans:
            raise Exception(
                "Stale compiled script files were found (their .rpy was moved or deleted):\n  "
                + "\n  ".join(sorted(orphans))
                + "\nClose the game and double-click tools/clean_orphan_rpyc.bat "
                "(or run: python tools/clean_orphan_rpyc.py), then start again.")
        return None

    _lc_check_orphan_compiled_scripts()
