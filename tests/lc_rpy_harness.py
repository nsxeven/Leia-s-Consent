"""Execute named Ren'Py `init python` definitions without Ren'Py.

load(names, env) runs every top-level def/class/assignment whose name is in
`names`, in the order Ren'Py would run them (see lc_rpy_model), inside `env`.
A wrapper chain such as

    _orig = set_story_flag          # assignment
    def set_story_flag(...): ...    # wrapper calling _orig

therefore behaves exactly as in game, and the test keeps working after the
chain is folded into one function in another file: names that no longer exist
are simply skipped. Supply everything else the code touches as stubs in env.
"""
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lc_rpy_model as m  # noqa: E402


def load(names, env):
    wanted = set(names)
    chain = sorted((d for d in m.all_definitions()
                    if d.kind in ("def", "class", "assign") and d.name in wanted),
                   key=lambda d: d.order)
    for d in chain:
        exec(compile(d.body + "\n", f"{d.relpath}:{d.line}", "exec"), env)
    return env


def files_defining(anchors):
    """Files (repo-relative) that define any of the anchor function/class names."""
    wanted = set(anchors)
    return {d.relpath for d in m.all_definitions() if d.kind in ("def", "class") and d.name in wanted}


def load_blocks(anchors, env):
    """Exec every whole `init python` block of the files that define the anchor
    names, in Ren'Py order, exactly as the game runs them. Tests name a function
    they care about instead of a file path, so they survive a file being merged
    into another or moved to a new folder."""
    files = files_defining(anchors)
    if not files:
        raise LookupError(f"no file defines any of {sorted(anchors)}")
    for d in m.in_run_order(("pyblock",)):
        if d.relpath in files:
            body = textwrap.dedent("\n".join(d.body.split("\n")[1:]))
            exec(compile(body + "\n", f"{d.relpath}:{d.line}", "exec"), env)
    return env
