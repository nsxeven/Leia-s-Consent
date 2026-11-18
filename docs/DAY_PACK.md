# Day packs: where every kind of content goes

Every Day of the game (the Prologue, Day 1 ... Day 5) is one **Day pack**: one folder under
`game/chapters/` plus one small Python file under `game/python-packages/lc_days/`. Everything that
belongs to a Day lives in its pack. The engine (`game/systems/`, `game/screens/`, the
`game/python-packages/lc_*.py` modules) holds the machinery every Day uses.

`tests/test_day_packs.py` checks this: every Day has the files below, starts at its start label,
reads the previous Day's end route, stores its own, runs its review, and declares every story key
it sets. It also stops new Day ids from creeping into the engine
(`tests/data/engine_day_ids_allow.json` lists the ones still there, each with a reason; that list
may only get shorter).

## The folders

| Day | Folder | Python file | Start label | End-route key it stores |
|---|---|---|---|---|
| Prologue | `game/chapters/prologue/` | `lc_days/prologue.py` | `prologue_start` | (none) |
| Day 1 | `game/chapters/ch01/day1/` | `lc_days/day1.py` | `chapter_one_start` | `ch01_day1_route_pressure` |
| Day 2 | `game/chapters/ch01/day2/` | `lc_days/day2.py` | `ch01_day2_start` | `ch01_d2_end_route` |
| Day 3 | `game/chapters/ch01/day3/` | `lc_days/day3.py` | `ch01_day3_start` | `ch01_d3_lane` |
| Day 4 | `game/chapters/ch01/day4/` | `lc_days/day4.py` | `ch01_day4_start` | `ch01_d4_end_route` |
| Day 5 | `game/chapters/ch01/day5/` | `lc_days/day5.py` | `ch01_day5_start` | `ch01_d5_end_route` |

File names start with the Day's prefix: `prologue_`, `ch01_day1_` ... `ch01_day5_` (Day 1's scene
files keep their old names, `ch01_main.rpy` and `ch01_scenes_*.rpy`).

## The files in a pack

| File | What goes in it |
|---|---|
| `<prefix>_scenes*.rpy` | the dialogue: one `label` per scene |
| `<prefix>_visuals.rpy` | this Day's `image bg ...` and `image cg ...` lines (and text placeholder cards); the first visuals file also registers the Day's title-screen outfits and backgrounds (`lc_title_register_outfit(..., order=N)`) |
| `<prefix>_registrations.rpy` | choice effects and tags, Full Transparency CG counts, review choice styles and stickers, Day helpers and thresholds, gate formatters (`LC_GATE_FORMATTERS.append(...)`), the Full "Current lean" reader (`lc_hook_add("current_lean", ...)`), and the **story-key ledger** |
| `<prefix>_gallery.rpy` | the Day's Gallery tab, its rows, its CGs that are still placeholders, and the rows the title-screen reel may show (`LC_TITLE_SAFE_GALLERY`) |
| `<prefix>_chapter.rpy` | the title-card line, the end-of-day review row, and the Day's Chapter Select preset (`CHAPTER_SELECT_PRESETS["dayN"]` and the seed functions that mark earlier Days finished, including the Day's **phone history**) |
| `game/python-packages/lc_days/<day>.py` | chapter titles (`CHAPTER`), route thresholds, gate / route-flag / repair choices and route resolvers (`STAT_*`), Ryan's thoughts (`THOUGHT_*`), journal flags and paper exceptions (`UI_*`); the names are listed in `lc_days/__init__.py` |

Every Day uses the same layout: scene files hold only labels, and all of a Day's choice rows,
tags, CG counts, lane helpers and exempt lists sit in its `<prefix>_registrations.rpy`.

## How to add each kind of content

**Dialogue or a new scene.** Add a `label ch01_dayN_scene_NN_<name>:` to the Day's scenes file and
`call` or `jump` it from the scene before. Never rename or delete a label that has shipped: saves
point at labels. Writing style: `docs/DIALOGUE_STYLE.md`.

**A choice and its scoring.** Give every option a stable id and use the same pattern as the
existing Days:

```
    $ d6_hi = format_choice("ch01_d6_beach_hi", "Hi.")
    menu:
        "[d6_hi]":
            $ apply_choice("ch01_d6_beach_hi")
```

Then add the id to the Day's `<prefix>_registrations.rpy`, inside `CHOICE_EFFECTS.update({...})`
(stats, `[("relationship", "love", 1)]`) and `CHOICE_TAGS.update({...})` (behaviour tags). Score it
with the rule in `docs/STAT_MODEL.md`; `tests/test_choice_scoring.py` names any row that breaks it.
Never reuse or rename a choice id.

**A story key (flag or value).** `$ set_story_flag("ch01_dN_<fact>")` or
`$ set_story_value("ch01_dN_<fact>", value)`; read it back with `has_story_flag` /
`get_story_value`. Then add one ledger line at the bottom of the Day's `<prefix>_registrations.rpy`:
`# key ch01_dN_<fact>: read-by <file that reads it>` or
`# key ch01_dN_<fact>: pending <why nothing reads it yet>`. Keys built in code
(`"ch01_dN_seen_" + name`) get one pattern line: `# key ch01_dN_seen_*: pending ...`.
Keys are save data: never rename one.

**CG files.** Day N's CGs go in `game/images/cg/ch0N/`, named `CH<N>D<N>_CG_<Moment>_<NN>.webp`:
Day 1 is `game/images/cg/ch01/CH1D1_CG_DriveToDinner_01.webp`, Day 2 is
`game/images/cg/ch02/CH2D2_CG_Breakfast_01.webp`, and Prologue CGs are
`game/images/cg/prologue/PRO_CG_<Moment>_<NN>.webp`. Close-ups add `Closeup` to the moment:
`CH2D2_CG_BreakfastCloseup_01.webp`. The image NAME keeps the story ids, `ch01_dN_<moment>_<nn>`
(chapter folder `ch0N` on disk, `ch01_dN_` in code). Declare it in the Day's `<prefix>_visuals.rpy`:
`image cg ch01_d2_breakfast_01 = At("images/cg/ch02/CH2D2_CG_Breakfast_01.webp", prologue_fullscreen)`
and show it in the scene with `show cg ch01_d2_breakfast_01`. (Day 1's older names have no `d1`,
for example `ch01_drive_to_dinner`; never rename a shipped image name.) When a CG replaces a text placeholder,
swap the `Composite(...)` line for the `At(...)` line (keep the image name) and remove the name from
`GALLERY_PLACEHOLDER_IMAGES.update([...])` in the Day's `<prefix>_gallery.rpy`.

**Backgrounds.** A place only one Day uses goes in `game/images/backgrounds/chapter N/ch0N_<place>.webp`
(Day 2: `backgrounds/chapter 2/ch02_cafe.webp`). Shared villa rooms go in
`game/images/backgrounds/villa/villa_<room>_<day|evening|night>.webp`. Declare it in the visuals file
with the blur transform:
`image bg ch01_d2_cafe = At("images/backgrounds/chapter 2/ch02_cafe.webp", prologue_bg_blur)`.

**Sprites and outfits.** Character art goes in `game/images/sprites/<character>/`; each character's
sprite definitions are in `game/sprites/<character>.rpy`. Placing sprites in scenes:
`docs/SPRITE_STAGING.md` (`$ cast_add(leia="towel")` and friends). Outfits are wardrobe data in
`game/systems/wardrobe_logic.rpy`.

**A Gallery row.** In the Day's `<prefix>_gallery.rpy`:
`gallery_row("dN_<moment>", "ch01_dN", "Title", "One line.", [("ch01_dN_<moment>_01", "Page"), ...])`.
Pages are `cg` image names in display order. A row unlocks when the player has seen its CGs.

**Hidden POV, things Ryan noticed, phone moments, the feed, Leia's side.** Register them from the
Day's files in an `init 1 python:` block with the Day's id (`"ch01_dN"`): `lc_pov_register(...)`
(`docs/HIDDEN_POV.md`), `lc_notice_register(...)` (`docs/NOTICES.md`),
`lc_phone_moment_register(...)` (`docs/PHONE_MOMENTS.md`), `lc_feed_register(...)` (`docs/FEED.md`),
`lc_leia_register_places(...)` / `lc_leia_register_choices(...)` (`docs/LEIA_SIDE.md`). Day 2's
examples are in its visuals, feed and errand files.

**Chapter titles.** Edit `CHAPTER` in `game/python-packages/lc_days/<day>.py`. Title cards, the day
review, Chapter Select, save names and the Gallery all read it.

**Phone history for Chapter Select.** When Chapter Select starts a later Day, the phone must already
hold what the earlier Days sent. Each Day's `<prefix>_chapter.rpy` has a `..._select_phone()`
function, called from that Day's "finished" seed, that lists the Day's texts in play order:

```
chapter_select_phone("group", "julian", "ch01_d6_beach_plan", "Beach at noon. Bring snacks.")
chapter_select_phone_reply("ch01_d6_beach_reply", "yes")          # a reply card, already answered
chapter_select_phone_group("four", maya_member=True)               # Trip Group picture / Maya
```

Copy the message id, thread, sender and text exactly from the story's `phone_add_message(...)` (same
`display_time` when the story pins the clock). Where the Day branches, pick what the preset implies
(its stored route values) or the reply card's default, and say which in a comment. Messages arrive
read, with no banners. `tests/test_chapter_select_phone.py` fails when a seeded text no longer
matches the story, when the story gains a text no preset seeds (seed it, or list it in
`NOT_SEEDED` with the reason), and when a preset's phone differs from its expected table.

## A new Day

```
python tools/new_day.py 6            # shows what it would create
python tools/new_day.py 6 --write    # creates the Day 6 pack
```

It writes the folder (start label, registrations, gallery, visuals and chapter files),
`lc_days/day6.py` and a test stub, and never overwrites a file. It then prints the last steps: add
`"day6"` to `DAY_MODULES` (`lc_days/__init__.py`) and to `CHAPTER_ORDER` (`lc_chapters.py`), add the
Day to `DAY_PACKS` in `tests/test_day_packs.py`, and make Day 5's last scene jump to
`ch01_day6_start`.

## Before you push

1. Close the game.
2. Run the unit tests: `PYTHONPATH=game/python-packages python -m unittest discover -s tests -q`
3. Run lint (Ren'Py launcher: Check Script (Lint)) and fix anything new.
4. Commit, push and open a PR; CI runs the same tests.

## After you pull

When files move, old compiled `.rpyc` files stay behind and can break loading saves. After a pull
that moves files: close the game, pull, then double-click `tools/clean_orphan_rpyc.bat`. Every move
is listed in `tools/dev/rpyc_moves.json`, so the tool carries the compiled files over to the new
paths and saves keep loading.
