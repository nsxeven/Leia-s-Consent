"""Delete stray compiled Ren'Py scripts (.rpyc whose .rpy is gone).

Why: Ren'Py still loads a .rpyc after its .rpy was moved or deleted, and .rpyc
files are git-ignored, so pulling a change that moves or deletes script files
leaves the old compiled copy behind. That copy can crash the game at load
("appears twice") or silently replace a screen with an old version.

Use (from the game's root folder, with the game closed):
    python tools/clean_orphan_rpyc.py          # deletes them and lists what it removed
    python tools/clean_orphan_rpyc.py --check  # only lists them
or double-click tools/clean_orphan_rpyc.bat.

Never touches game/saves or game/cache. Note: the Ren'Py launcher's
"Force Recompile" keeps orphan .rpyc files, so it does not fix this.
"""
import sys
from pathlib import Path

SKIP_DIRS = {"saves", "cache"}


def find_orphans(game_dir):
    game_dir = Path(game_dir)
    out = []
    for rpyc in game_dir.rglob("*.rpyc"):
        rel = rpyc.relative_to(game_dir)
        if rel.parts and rel.parts[0] in SKIP_DIRS:
            continue
        source = rpyc.with_suffix(".rpy")
        ren_py = rpyc.with_name(rpyc.stem + "_ren.py")
        if not source.exists() and not ren_py.exists():
            out.append(rel.as_posix())
    return sorted(out)


def delete_orphans(game_dir):
    removed = find_orphans(game_dir)
    for rel in removed:
        (Path(game_dir) / rel).unlink()
    return removed


def main(argv):
    game_dir = Path(__file__).resolve().parents[1] / "game"
    if "--check" in argv:
        found = find_orphans(game_dir)
        print("\n".join(found) if found else "No stray .rpyc files.")
        return 1 if found else 0
    removed = delete_orphans(game_dir)
    print("Removed:\n  " + "\n  ".join(removed) if removed else "No stray .rpyc files.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
