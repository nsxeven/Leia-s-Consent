"""Tidy compiled Ren'Py scripts after a pull: move or delete stray .rpyc files.

Why: Ren'Py still loads a .rpyc after its .rpy was moved or deleted, and .rpyc
files are git-ignored, so pulling a change that moves or deletes script files
leaves the old compiled copy behind. That copy can crash the game at load
("appears twice") or silently replace a screen with an old version.

Saves: Ren'Py names every script statement and keeps those names in the .rpyc
beside the .rpy (it reuses them whenever the .rpy is recompiled). A save records
where you are by statement name. If a .rpy moves but its .rpyc does not, every
statement in it gets a new name and a save made inside that file cannot find its
place. So, before deleting, this tool MOVES the old .rpyc of every script listed
in tools/dev/rpyc_moves.json (old game/-relative .rpy path -> new path) to the new
path, replacing a .rpyc compiled there in the meantime (the start-up guard in
game/systems/dev_source_checks.rpy stops the game while the orphan exists, so no
save can use that newer compile's names). Then it deletes the remaining orphans.

Use (from the game's root folder, with the game closed):
    python tools/clean_orphan_rpyc.py          # moves/deletes them and lists what it did
    python tools/clean_orphan_rpyc.py --check  # only lists them
or double-click tools/clean_orphan_rpyc.bat.

Never touches game/saves or game/cache. The Ren'Py launcher's "Force Recompile"
does NOT fix this: it renames orphans to .rpyc.bak and gives moved scripts new
statement names. This tool also moves a listed .rpyc.bak into place, so running it
after a Force Recompile still keeps saves. Run one Force Recompile AFTER this tool
if you want error messages to show the new file paths (names are kept).
When you move a .rpy in a PR, add "old path": "new path" to rpyc_moves.json.
"""
import json
import os
import sys
from pathlib import Path

SKIP_DIRS = {"saves", "cache"}
MOVES_FILE = Path("tools") / "dev" / "rpyc_moves.json"


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


def load_moves(root):
    path = Path(root) / MOVES_FILE
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def move_target(game_dir, orphan, moves):
    """New game/-relative .rpyc path for `orphan`, or None (not listed / new .rpy absent)."""
    source = orphan[:-1]  # .rpyc -> .rpy
    seen = set()
    while source in moves and source not in seen:
        seen.add(source)
        source = moves[source]
    if not seen or not (Path(game_dir) / source).exists():
        return None
    return source + "c"


def find_backups(game_dir, moves):
    """Listed `<old>.rpyc.bak` files whose moved .rpy exists.

    The launcher's Force Recompile (`renpy.exe <proj> compile`) renames an orphan .rpyc
    to .rpyc.bak and compiles the moved .rpy with NEW statement names. The backup still
    has the names saves use, so it is moved into place like an orphan .rpyc. Unlisted
    .bak files are Ren'Py's own business and are left alone.
    """
    game_dir = Path(game_dir)
    out = []
    for bak in game_dir.rglob("*.rpyc.bak"):
        rel = bak.relative_to(game_dir).as_posix()
        if rel.split("/", 1)[0] in SKIP_DIRS or (game_dir / rel[:-5]).exists():
            continue
        if move_target(game_dir, rel[:-4], moves):
            out.append(rel)
    return sorted(out)


def move_orphans(game_dir, moves):
    """Move each listed orphan .rpyc (or its Force-Recompile .bak) next to its moved .rpy.

    Returns [(old, new)]. An orphan .rpyc wins over a .bak of the same script.
    """
    moved = []
    for rel in find_orphans(game_dir):
        target = move_target(game_dir, rel, moves)
        if target is None:
            continue
        os.replace(Path(game_dir) / rel, Path(game_dir) / target)
        moved.append((rel, target))
    done = {new for _old, new in moved}
    for rel in find_backups(game_dir, moves):
        target = move_target(game_dir, rel[:-4], moves)
        if target in done:
            continue
        os.replace(Path(game_dir) / rel, Path(game_dir) / target)
        moved.append((rel, target))
    return moved


def delete_orphans(game_dir):
    removed = find_orphans(game_dir)
    for rel in removed:
        (Path(game_dir) / rel).unlink()
    return removed


def main(argv, root=None):
    root = Path(root) if root else Path(__file__).resolve().parents[1]
    game_dir = root / "game"
    moves = load_moves(root)
    if "--check" in argv:
        found = find_orphans(game_dir) + find_backups(game_dir, moves)
        lines = []
        for rel in found:
            target = move_target(game_dir, rel[:-4] if rel.endswith(".bak") else rel, moves)
            lines.append(rel + (" (will move to " + target + ")" if target else ""))
        print("\n".join(lines) if lines else "No stray .rpyc files.")
        return 1 if found else 0
    moved = move_orphans(game_dir, moves)
    removed = delete_orphans(game_dir)
    if moved:
        print("Moved:\n  " + "\n  ".join(old + " -> " + new for old, new in moved))
    if removed:
        print("Removed:\n  " + "\n  ".join(removed))
    if not moved and not removed:
        print("No stray .rpyc files.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
