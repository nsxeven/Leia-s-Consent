# Leia's Consent

Development repository for **Leia's Consent**, a choice-driven Ren'Py visual novel.

## Canon character defaults

- Leia — girlfriend / female lead
- Ryan — boyfriend / player POV
- Julian — friend / outside male influence

Players can rename all three at the start of a new game. Internal code and asset identifiers stay fixed.

## Playable path

Open this directory in the Ren'Py launcher and start a new game.

- `label start` runs the prologue, then Chapter One.
- Day One plays through `ch01_scene_30_end_day_one` and jumps to `ch01_day2_start`.
- Day Two plays through `ch01_day2_scene_30_finish`, shows the Day Two complete card, and returns.

Day Three is not linked. `game/chapters/ch01/ch01_day3_scenes.rpy` defines `ch01_day3_start`, and nothing in the playable path jumps there.

No CG art was changed for the current Day Two QA pass. Image files under `game/images/` are unchanged.

## Development stack

- Ren'Py
- Visual Studio Code
- Git / GitHub Desktop
- ComfyUI

See `docs/BUILD_HANDOFF.md` for the current build boundary and the Day Two rules this tree relies on.
