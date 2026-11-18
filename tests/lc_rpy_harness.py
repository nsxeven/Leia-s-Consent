"""Execute named Ren'Py `init python` definitions without Ren'Py.

load(names, env) runs every top-level def/class/assignment whose name is in
`names`, in the order Ren'Py would run them (see lc_rpy_model), inside `env`.
A wrapper chain such as

    _orig = set_story_flag          # assignment
    def set_story_flag(...): ...    # wrapper calling _orig

therefore behaves exactly as in game, and the test keeps working after the
chain is folded into one function in another file: names that no longer exist
are simply skipped. Supply everything else the code touches as stubs in env.

Hooks (game/systems/lc_hooks.rpy): a top-level `lc_hook_add("event", fn)`
registration is run too when `fn` is one of the loaded names, so a folded
wrapper that became a named hook still runs in the same order. Ren'Py's
python_dict/python_list default to dict/list when the env has no stub.
"""
import re
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lc_rpy_model as m  # noqa: E402


_HOOK_ADD = re.compile(r"^lc_hook_add\(\s*['\"]\w+['\"]\s*,\s*(\w+)\s*\)$")


# Tables the Day packs fill at init (their engine owners create them at an earlier priority). A
# test that loads a Day pack without the owning system gets an empty stand-in; when the owner is
# loaded too, its own (empty) table replaces the stand-in first, as in game.
DAY_PACK_TABLES = {
    "CHOICE_EFFECTS": dict, "CHOICE_TAGS": dict, "LC_CHOICE_CG_COUNT": dict,
    "LC_CHOICE_STYLE": dict, "LC_MOMENT_STICKERS": tuple, "LC_REVIEW_DAYS": dict,
    "CHAPTER_SELECT_PRESETS": dict, "LC_REVIEW_NIGHT": dict, "LC_REVIEW_TICKET": dict,
    "LC_GATE_FORMATTERS": list, "LC_TITLE_SAFE_GALLERY": tuple,
}


def _store_builtins(env):
    env.setdefault("python_dict", dict)
    env.setdefault("python_list", list)
    env.setdefault("_", lambda s: s)  # Ren'Py's translation marker
    for name, kind in DAY_PACK_TABLES.items():
        env.setdefault(name, kind())


def day_pack_files(*days):
    """Repo-relative paths of the registrations and chapter files of the named Day packs
    ("prologue", "day1" ... "day5"; see DAY_PACKS in tests/test_day_packs.py)."""
    import test_day_packs as packs
    out = set()
    for pack in packs.DAY_PACKS:
        if pack["day"] in days:
            for suffix in ("_registrations.rpy", "_chapter.rpy"):
                path = m.GAME / pack["folder"] / (pack["prefix"] + suffix)
                if path.exists():
                    out.add(m.relpath(path))
    return out


def _registers_loaded_hook(d, wanted):
    mo = d.kind == "effect" and _HOOK_ADD.match(d.body)
    return bool(mo) and mo.group(1) in wanted


def load(names, env):
    wanted = set(names)
    _store_builtins(env)
    chain = sorted((d for d in m.all_definitions()
                    if (d.kind in ("def", "class", "assign") and d.name in wanted)
                    or _registers_loaded_hook(d, wanted)),
                   key=lambda d: d.order)
    for d in chain:
        exec(compile(d.body + "\n", f"{d.relpath}:{d.line}", "exec"), env)
    return env


def files_defining(anchors):
    """Files (repo-relative) that define any of the anchor function/class names."""
    wanted = set(anchors)
    return {d.relpath for d in m.all_definitions() if d.kind in ("def", "class") and d.name in wanted}


def load_blocks(anchors, env, packs=()):
    """Exec every whole `init python` block of the files that define the anchor
    names, in Ren'Py order, exactly as the game runs them. Tests name a function
    they care about instead of a file path, so they survive a file being merged
    into another or moved to a new folder. The hook API file is always included:
    like Ren'Py itself, every system may call it. `packs` (Day names such as "day1") adds
    the registrations and chapter files of those Day packs, so their table rows load too."""
    # Every Day's *_chapter.rpy registers its review row and title card, like in game.
    files = files_defining(anchors) | day_pack_files(*packs) | {
        m.relpath(p) for p in sorted((m.GAME / "chapters").rglob("*_chapter.rpy"))}
    if not files:
        raise LookupError(f"no file defines any of {sorted(anchors)}")
    files |= files_defining(["lc_hook_add"])
    _store_builtins(env)
    for d in m.in_run_order(("pyblock",)):
        if d.relpath in files:
            body = textwrap.dedent("\n".join(d.body.split("\n")[1:]))
            exec(compile(body + "\n", f"{d.relpath}:{d.line}", "exec"), env)
    return env
