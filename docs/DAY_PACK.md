# Day packs: where every kind of content goes

Every Day of the game (the Prologue, Day 1 ... Day 5) is one **Day pack**: one folder under
`game/chapters/` plus one pure-Python module under `game/python-packages/lc_days/`. The
engine (`game/systems/`, `game/screens/`, the `game/python-packages/` modules) holds no Day
content; `tests/test_day_packs.py` keeps it that way.

This guide is being written as the packs are built (modular backend branch); the full version
lands with `tools/new_day.py`.
