# Leia's Consent

**Leia's Consent** is an adult (18+) choice-driven visual novel built with [Ren'Py](https://www.renpy.org/). It is a slow burn: every central character is an adult, and the story is about Leia's curiosity and discovery while she and her boyfriend Ryan work out what they are comfortable with together.

> Content warning: this project contains sexual content, nudity and suggestive material. It is intended for adults only.

## Premise and canon defaults

- **Leia** — girlfriend / female lead
- **Ryan** — boyfriend / player POV
- **Julian** — Ryan's friend / outside male influence
- **Maya** — Leia's new friend, introduced on Day Two

Players can rename Leia, Ryan and Julian at the start of a new game. Internal code and asset identifiers stay fixed (`mc`, `gf`, `friend`) so saves and content remain stable.

Route design in one sentence: **Love** = engaged; **Exhibitionism** = outside attention with Ryan included; **NTR pressure** = outside attention increasingly separated from Ryan by disengagement and secrecy. Nothing is hard-locked early; Ryan's choices accumulate into a lane.

## Running the game

1. Install the Ren'Py SDK (the project is developed and was last checked on **Ren'Py 8.5.3**; any recent 8.x SDK should work).
2. Clone this repository and add the folder to the Ren'Py launcher's Projects Directory (the repository root is the project: it contains `game/`).
3. Launch it from the Ren'Py launcher, or from a terminal:
   ```
   /path/to/renpy-sdk/renpy.sh /path/to/Leia-s-Consent          # play
   /path/to/renpy-sdk/renpy.sh /path/to/Leia-s-Consent lint     # static checks
   ```
4. **Start a fresh save** after changing labels or choice logic; old development saves can hold stale story state.

`lint` currently reports one known, expected note: the `init -1500` priority of the start-up guard in `game/systems/dev_source_checks.rpy`, which must run before everything else.

## Project structure

```
game/
  script.rpy            entry point (label start -> prologue_name_setup)
  characters.rpy        Character definitions (mc, gf, friend, maya, stranger, passerby)
  defaults.rpy          save-state defaults (stats, flags, outfits, money)
  chapters/
    prologue/           prologue.rpy, prologue_visuals.rpy
    ch01/               Chapter One: Something Different
      ch01_main.rpy                 Day One scenes 1-3
      day1/                         Day One (file names keep their ch01_ prefix)
        ch01_scenes_04_06.rpy         Day One pool, photography, towel
        ch01_scenes_07_13.rpy         Day One dinner, walk, shop, return
        ch01_scenes_14_30.rpy         Day One night pool, movie night, dream
        ch01_phone_moments.rpy        Day One phone moments, pool-photo route, reply timers
        ch01_scenes_*_visuals.rpy     Day One scene images
      day2/                         Day Two
        ch01_day2_scenes_01_15.rpy    Day Two morning to pool (incl. boutique)
        ch01_day2_scenes_16_30.rpy    Day Two pool accident to the five end states
        ch01_day2_scene_19b_leia_asks_maya.rpy, ch01_day2_visuals.rpy
      ch01_visuals.rpy              Chapter One images shared across days
      ch01_release_demo.rpy         Day One demo gate
      ch01_day3_scenes.rpy          Day Three first pass (linked from Day Two)
      ch01_day4_scenes_01_08.rpy    Day Four 'Recalibration' scenes 1-8 (entry ch01_day4_start)
      ch01_day4_scenes_09_16.rpy    Day Four scenes 9-16, end routes, temporary end card
      ch01_day4_choice_registration.rpy  Day Four choice ids/effects/tags and helpers
      ch01_day5_scenes_01_08.rpy    Day Five 'The Water' scenes 1-8 (entry ch01_day5_start)
      ch01_day5_scenes_09_16.rpy    Day Five scenes 9-16, end routes, temporary end card
      ch01_day5_choice_registration.rpy  Day Five choice ids/effects/tags and helpers
      ch01_day5_visuals.rpy         Day Five placeholder bg/cg images
      *_visuals.rpy                 stable image names (placeholders or real art)
  systems/              one file per game system (choice_engine, stats, story_state, hooks,
                        day review, Hidden POV, phone, gallery, wardrobe, effects ...);
                        each file opens with a header listing its API
  screens/              feature screens (scrapbook UI skin, phone, day review, gallery,
                        status, title screen ...)
  python-packages/      pure-Python logic with unit tests (stat model, chapter registry ...)
  dev/                  developer/QA-only labels and screens (dev_sandbox, story_state_test,
                        systems_vertical_slice, debug/dev menus, screenshot tours); left out
                        of release builds by game/options.rpy
  sprites/              layered character sprites (Leia, Ryan, dinner stranger)
  images/               backgrounds/, cg/, sprites/ (production art)
docs/
  BUILD_HANDOFF.md      current build truth (read this before coding)
  ARCHITECTURE.md       folder layout, load order, rules, how to add a Day or a system
tools/                  asset generators, clean_orphan_rpyc (run after pulls)
tests/                  unittest suite (run by CI on every PR)
```

## Implemented content

| Chapter | Status |
|---|---|
| Prologue | Implemented |
| Chapter 1, Day 1 | Implemented (resort baseline, swimsuit/towel, pool photography, dinner stranger and spill, accidental Julian catch, movie night, closing dream) |
| Chapter 1, Day 2 | Implemented end to end: Maya, boutique/Shop, villa pool, sunset, dinner, Never Have I Ever, bedroom. Resolves to one of **five end states** stored in `ch01_d2_end_route`: `love`, `exhibitionism`, `love_repaired`, `mixed_unresolved`, `ntr_confirmed` |
| Chapter 1, Day 3 | A first-pass script in `ch01_day3_scenes.rpy` (entry label `ch01_day3_start`), linked from the end of Day 2 and headless-tested for the Love, Exhibitionism and NTR lanes |
| Chapter 1, Day 4 | First-pass script in `ch01_day4_scenes_*.rpy` (entry `ch01_day4_start`), linked from the end of Day 3 and headless-tested for all five end routes (`love`, `exhibitionism`, `love_repaired`, `ntr_unresolved`, `ntr_confirmed`, stored in `ch01_d4_end_route`). All Day 4 CGs and backgrounds are placeholders (`ch01_day4_visuals.rpy`) |
| Chapter 1, Day 5 | First-pass script "The Water" in `ch01_day5_scenes_*.rpy` (entry `ch01_day5_start`), linked from the end of Day 4 (which jumps to it when the label exists) and headless-tested for all five Day 4 end routes. Ends in five routes stored in `ch01_d5_end_route` (`love`, `exhibitionism`, `love_repaired`, `ntr_unresolved`, `ntr_confirmed`). All Day 5 CGs and backgrounds are placeholders (`ch01_day5_visuals.rpy`) |
| Gallery | 47 entries (Prologue 4, Day 1 17, Day 2 9, Day 3 1, Day 4 5, Day 5 11), one per scene sequence with variant pages; unlocks follow the CGs the player has actually seen; open it from **Gallery** in the main menu or game menu. Placeholder CGs show with an "ART PENDING" badge; mature scenes are masked in the grid. Replay is not built yet |
| Day 6+ | Not built. Day 5 ends on a temporary "Current development build ends here" card until `ch01_day6_start` exists |

All Day Two story CGs and all Day Four and Day Five CGs/backgrounds are still placeholders pending final art (including the 12 Day Two finale CGs). See [docs/BUILD_HANDOFF.md](docs/BUILD_HANDOFF.md) for the exact current state.

## Contributing

- **Branch from `main`** for every change (for example `feature/<short-topic>`), keep commits small with clear messages, and open a pull request. Do not push directly to `main`.
- **One definition per name.** Every label, screen and function is defined once, in the file that owns it. Change behaviour there; never add a `zz*` / `*_patch.rpy` file or a `config.label_overrides` entry (the structure tests reject them). Layout, load order, save-safety rules and how to add a Day or a system: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).
- **After pulling** a change that moves or deletes scripts, close the game and run `tools/clean_orphan_rpyc.bat` (or `python tools/clean_orphan_rpyc.py`) so stale compiled files are moved or removed.
- **Stable image names.** Story code refers to stable names (for example `cg ch01_d2_love_bedroom_01`). Placeholders are `Composite` images; when real art arrives, point the same name at the file instead of renaming it in the script.
- **Art ownership.** Do not add or replace CG art as part of a code change; art is delivered separately.
- **Day Three script.** `ch01_day3_scenes.rpy` is owned by the Scriptwriter. Do not edit it without coordination. The Day 2 -> Day 3 -> Day 4 link is in place. Day Four (`ch01_day4_*`) and Day Five (`ch01_day5_*`) are also Scriptwriter-owned; coordinate before editing them.
- **Gallery entries.** Add a scene's CGs to the gallery with one `gallery_row(...)` in `game/systems/gallery_data.rpy` (plus a tab row for a new day). Unlocks follow the CGs the player has seen, so no unlock lines go in story files. See the Gallery section of the handoff doc.
- Run `lint` and play the affected route from a fresh save before opening a PR.
