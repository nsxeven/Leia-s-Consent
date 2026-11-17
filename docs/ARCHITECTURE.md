# Architecture

How the Leia's Consent source is laid out, how it loads, and the rules that keep it
maintainable. This describes the code on `main`; when this file and the code disagree,
the code wins and this file gets fixed. Current build state (what is implemented, what
is placeholder art) lives in `docs/BUILD_HANDOFF.md`.

## Folder layout

| Path | What lives there |
|---|---|
| `game/script.rpy` | entry point: `label start` shows the adult notice first (until accepted), then jumps to the Prologue name setup (`prologue_name_setup`) |
| `game/00_release_build.rpy` | the release switch (`LC_RELEASE`, `python early`); the only file a release branch changes (`docs/BRANCH_AND_RELEASE_POLICY.md`) |
| `game/characters.rpy`, `game/defaults.rpy` | Character objects; save-state defaults (stats, flags, outfits, money) |
| `game/options.rpy`, `game/gui.rpy`, `game/screens.rpy` | Ren'Py project config, GUI variables and the stock screens/styles |
| `game/chapters/prologue/` | the Prologue (`prologue.rpy`) and its images |
| `game/chapters/ch01/` | Chapter One shared files: `ch01_main.rpy` (Day One scenes 1-3, entry `chapter_one_start`), `ch01_visuals.rpy` (images shared across days), `ch01_release_demo.rpy` (Day One demo gate and demo end) |
| `game/chapters/ch01/day1/` | Day One scenes 4-30 and its phone moments, each scene file with a `*_visuals.rpy` partner |
| `game/chapters/ch01/day2/` | Day Two scenes, the scene 19b side file and `ch01_day2_visuals.rpy` |
| `game/chapters/ch01/` (`ch01_day3_*`, `ch01_day4_*`, `ch01_day5_*`) | Days Three to Five: scenes, choice registration and visuals. Scriptwriter-owned; they stay flat in `ch01/` until their own pass |
| `game/systems/` | reusable game systems: one feature per file, no story text |
| `game/screens/` | feature screens (phone, review, gallery, menus, title screen) |
| `game/sprites/` | layered character sprites |
| `game/dev/` | developer/QA-only labels and screens; left out of release builds by `game/options.rpy` |
| `game/python-packages/` | pure-Python modules with no Ren'Py import, unit-tested directly: `lc_stat_model.py` (stats, thresholds, routes), `lc_chapters.py` (chapter registry), `lc_discovery.py` (discovery registry, Moments strip rules), `lc_thoughts.py` (Ryan's thoughts pool and rules), `lc_phone_moments.py` (calls, hesitation typing, leave on read), `lc_notice.py` (Things Ryan noticed: push-in maths, registry checks, found record), `lc_leia_side.py` (Leia's side: errand map cards, visit log, outcomes, +2/day gain cap), `lc_ui_logic.py`, `lc_title_touch.py`, `lc_wallpaper_crop.py` |
| `game/python-packages/` | pure-Python modules with no Ren'Py import, unit-tested directly: `lc_stat_model.py` (stats, thresholds, routes), `lc_chapters.py` (chapter registry), `lc_discovery.py` (discovery registry, Moments strip rules), `lc_thoughts.py` (Ryan's thoughts pool and rules), `lc_phone_moments.py` (calls, hesitation typing, leave on read), `lc_notice.py` (Things Ryan noticed: push-in maths, registry checks, found record), `lc_feed.py` (social-feed app: post registry, release/unlock, seen record), `lc_ui_logic.py`, `lc_title_touch.py`, `lc_wallpaper_crop.py` |
| `tools/` | asset generators (`gen_*.py`) and `tools/clean_orphan_rpyc.py` / `tools/clean_orphan_rpyc.bat` |
| `tools/dev/` | `tools/dev/snapshot_baselines.py` (behaviour pins) and `tools/dev/rpyc_moves.json` (moved-script map) |
| `tests/` | the unittest suite plus its helpers (`tests/lc_rpy_model.py`, `tests/lc_rpy_harness.py`, `tests/lc_save_names.py`, `tests/lc_effective_effects.py`) and baselines in `tests/data/` |
| `docs/` | writer and developer docs (this file, the feature docs listed in the index below) |

Every file in `game/systems/` and `game/screens/` opens with a header block: feature
name, Purpose, Public API (real signatures), Internal helpers, Example, Depends on, Hooks,
Load order, Docs and Tests. Read the header before using a system.

## Load order and init priorities

Ren'Py loads `.rpy` files sorted by path (relative to `game/`), then runs all init code
sorted by priority (stable within a priority, so file order only breaks ties). Defaults:
`screen` -500, `image` +500, `define`/`default`/`transform`/`init python` 0, plus a file's
`init offset`. Last definition wins, which is why the project allows only one definition
per name (see Rules). Priorities in use:

| Priority | Used by | Why |
|---|---|---|
| `python early` | `game/00_release_build.rpy` | release values must exist before `game/options.rpy` is evaluated |
| -1500 | `game/systems/dev_source_checks.rpy` | stray-.rpyc guard runs before anything a stale file could break (lint notes it is outside -999..999; that note is expected) |
| -999 | `game/dev/dev_phone_shots.rpy`, `game/dev/dev_scrapbook_preview.rpy` | env-var-gated screenshot modes configure the engine before anything else |
| -100 | `game/systems/lc_hooks.rpy` | hook registry exists before any system registers |
| -50 | `game/systems/lc_hover_fade.rpy` | button cross-fade installed before screens build |
| -40 | `game/systems/lc_audio_scene_lock.rpy` | audio-lock helpers before the audio helpers that call them |
| -10 | `game/systems/lc_chapters.rpy`, `game/systems/lc_fx.rpy` | chapter registry import; audio channel registration |
| -5 | `game/systems/lc_breath.rpy` | Leia's breath channel |
| -2 | `game/systems/gallery_data.rpy`, `game/systems/lc_fx.rpy` | gallery table before `game/systems/gallery.rpy` builds it; audio helpers |
| `init offset = -2` / `-1` | `game/gui.rpy` / `game/screens.rpy` | stock GUI and styles load before the project restyles them at 0 |
| -1 | `game/systems/hidden_pov.rpy`, `game/systems/hidden_pov_chime.rpy`, `game/systems/title_customiser.rpy`, `game/screens/scrapbook_ui.rpy` | registries, tables and an audio channel that init 0 and `init 1` code use |
| -1 | `game/chapters/ch01/day2/ch01_day2_visuals.rpy` | the `lc_placeholder_text` helper (text stand-in cards) that the Day 2-5 visuals files call |
| 0 | most systems and screens | the default |
| 1, 2 | day registration blocks (`CHOICE_EFFECTS.update`, Hidden POV `lc_pov_register`, Day 4/5 helpers at init 2) in `game/chapters/`; `game/chapters/ch01/ch01_release_demo.rpy` (init 1: the demo-build Gallery filter, not a day registration); `game/gui.rpy` font scaling; `game/sprites/julian.rpy` images | after the engine tables and init-0 helpers exist |
| 5 | `game/systems/stat_model_v2_later_days.rpy`, `game/systems/lc_cursor.rpy` | v2 re-scoring after the Day 3-5 registration blocks; cursor after the hover timings |
| 6 | `game/systems/choice_path_tags.rpy` | wraps the gate formatters the day files define |
| 10 | `game/systems/chapter_select.rpy`, `game/systems/love_outfit_control.rpy` | after the story, stats and wardrobe helpers |
| 20, 21 | `game/systems/day_review.rpy`, then `game/systems/lc_tag_collection.rpy` | the tag collection reads the review tables |
| 50 | `game/chapters/ch01/day1/ch01_phone_moments.rpy` | Day One phone helpers |
| 90, 95, 96 | `game/systems/choice_engine.rpy` (feedback block, 90), `game/screens/phone_sweetheart.rpy` (90, 95), `game/screens/phone_wallpaper.rpy` (96) | kept from the old load order so init runs exactly as before |
| 200 | `game/systems/transparency_display.rpy`, `game/systems/full_transparency_route_explorer.rpy` | kept from the old load order |
| 300 | `game/screens/phone_sweetheart.rpy` | the last phone overlay registration |
| 998 | `game/systems/story_state.rpy` (`get_story_flag`) and Day One/Two data adjustments (including `PHONE_THREAD_ORDER` in `game/chapters/ch01/day1/ch01_phone_moments.rpy`) | late data overrides kept from the old load order |
| 999 | `game/systems/hidden_pov.rpy` (validation), `game/systems/notice.rpy` (validation), `game/systems/lc_audio_scene_lock.rpy` (wraps `config.scene`), `game/screens/scrapbook_ui.rpy` (click-to-continue on every Character), `game/screens/phone_call.rpy` (appends `lc_phone_moments_overlay` after the Chapter One phone overlay) | need everything else registered first |

Priorities are chosen for a reason and written next to the block (`# load order: ...`).
Never rename a file to change when it loads; give the block an explicit priority.

## Naming rules

- Files: `snake_case.rpy`. Story files keep their chapter prefix (`ch01_day2_...`) even
  inside a day folder. Systems and screens are named after the feature.
- Project functions, screens, transforms and store variables start with `lc_` (older
  systems use their feature prefix: `phone_`, `gallery_`, `outfit_`, `status_`). Constants
  are `UPPER_CASE`.
- A leading `_` marks an internal helper. Internal helpers that a save or screen may
  reference are not renamed; their file header lists them under Internal instead.
- Story ids (labels, flags, story values, choice ids, message ids, gallery entry ids,
  image tags) are stable once shipped: see Save safety.

## Rules: one definition per name, no patch files

- **No `zz*` / `*_patch.rpy` files.** To change behaviour, edit the file that owns it.
  `tests/test_structure_rules.py` (`test_no_new_patch_files`) fails on a new one.
- **No `config.label_overrides`.** Edit the label itself; an old label name that saves may
  still hold becomes a one-line `jump` in `game/systems/save_compat.rpy`.
  (`test_no_new_label_overrides`)
- **One definition per name.** A screen, label or `def` defined twice is rejected
  (`test_no_new_duplicate_definitions`). `ALLOW_DUP` is empty; the one exception is
  `OUT_OF_SCOPE_DUP = {"def": {"ch01_d4_track_text", "ch01_d5_track_text"}}`: the Day 4/5
  track-text functions live in the Scriptwriter-owned Day 4/5 files and are re-defined by
  `game/systems/stat_model_v2_later_days.rpy` until those days get their own pass.
  Allow-lists may only shrink (`test_allow_lists_only_shrink`).
- **Add behaviour through hooks, not wrappers.** Re-defining another file's function
  (`_orig = f; def f(...)`) is the pattern the hooks replaced. Existing exceptions, kept
  until their own pass: `game/systems/day_review.rpy` wraps `config.show`
  (`lc_review_show`), `game/systems/lc_audio_scene_lock.rpy` wraps `config.scene`,
  `game/systems/choice_path_tags.rpy` wraps the Day 2/4/5 gate formatters, and
  `game/systems/stat_model_v2_later_days.rpy` re-defines the Day 4/5 track-text functions.
  New code uses `lc_hooks` instead.
- **Headers stay true.** Every system/screen file opens with a header
  (`test_system_and_screen_files_open_with_header`); every name its Public API or Internal
  list mentions must be defined in that file (`test_header_api_names_are_defined`), an entry
  written as `name(args)` must show the real parameters (`test_header_signatures_match_code`),
  and every def/class at the top of an `init python` block must be listed under Public API or
  Internal (`test_every_top_level_def_is_documented`). Entries are indented 3 spaces after
  `#`, wrapped meaning text 7; any other indentation fails as ambiguous. Paths
  in headers and in this file must exist (`test_paths_named_in_headers_exist`,
  `test_architecture_doc_paths_exist`).
- Other structure checks in the same file: every Hidden POV registration is used and vice
  versa, every choice id used in a scene is registered, no empty `init python` block, no
  stray compiled scripts, every path a test names exists.

## Hooks

`game/systems/lc_hooks.rpy` (init -100) lets one system react to another without
re-defining it:

- `lc_hook_add(event, fn)` registers `fn` (once) and returns it. Register only at init.
- `lc_hook_run(event, *args, **kw)` calls every registered `fn` in order (exceptions
  propagate; a hook that must never break its caller wraps its own body).
- `lc_hook_filter(event, value, *args)` passes `value` through every `fn` and returns it.

Events in use:

| Event | Emitted by | Listener |
|---|---|---|
| `story_flag_set` (flag_id, value) | `set_story_flag` in `game/systems/story_state.rpy` | `game/systems/chapter_select.rpy` unlocks Chapter Select after Day Two |
| `review_finished` (day_id) | `lc_review_finish` in `game/systems/day_review.rpy` | `game/systems/lc_tag_collection.rpy` unlocks the day's tags and stickers; `game/systems/discovery.rpy` marks the day cleared on the profile (Moments strip); `game/systems/leia_side.rpy` clears a Leia segment a scene forgot to end |
| `review_titles` (filter over the (ryan, leia) titles) | `lc_review_titles` in `game/systems/day_review.rpy` | `game/systems/lc_tag_collection.rpy` swaps in equipped tags |
| `review_closed` (day_id) | `label lc_day_review` in `game/systems/day_review.rpy`, after the spread closes | `game/systems/thoughts.rpy` offers Ryan's thoughts (may show a screen) |
| `phone_reply_chosen` (thread_id, prompt_id, option, unopened=bool) | `phone_choose_reply` in `game/systems/phone_presentation_logic.rpy` | `game/systems/phone_moments.rpy` records a leave-on-read receipt and marks a registered phone moment found |
| `choice_effects` (filter over a choice's effects, choice_id) | `lc_choice_effective_effects` in `game/systems/choice_engine.rpy` (used by `apply_choice`, the caption formatter and the toast) | `game/systems/leia_side.rpy` cuts Leia-side gains to her +2 a day |
| `choice_applied` (choice_id, effects) | `apply_choice` in `game/systems/choice_engine.rpy`, after the stats moved | `game/systems/leia_side.rpy` records the applied gain in the day's cap ledger |
| `discovery_strip` (filter over the Moments strip items, day_id) | `lc_discovery_strip` in `game/systems/discovery.rpy` | `game/systems/leia_side.rpy` drops a day's errand moments while that save has no visit that day |

Hooks are registered at init only, so they never enter a save. Tests:
`tests/test_lc_hooks.py`.

## Save safety

Saves refer to labels, store variables and story keys by name, and to the current line by
statement identity. So:

- Never rename a label, store variable (`default`), story flag or value key, choice id,
  phone `message_id`, gallery entry id or image tag. `tests/test_save_names.py` checks
  every name in `tests/data/save_names_baseline.json` still exists.
- When a scene's label must change, keep the old name in `game/systems/save_compat.rpy`
  as a one-line `jump` to the new one, with a comment saying which saves need it.
- Moving a `.rpy` file: add `"old/path.rpy": "new/path.rpy"` (relative to `game/`) to
  `tools/dev/rpyc_moves.json`. Ren'Py keeps statement names in the `.rpyc` beside the
  `.rpy`; `tools/clean_orphan_rpyc.py` moves the old `.rpyc` to the new path so mid-scene
  saves keep their place, then deletes stray `.rpyc` files.
- After every pull that moves or deletes scripts: close the game, then double-click
  `tools/clean_orphan_rpyc.bat` (or `python tools/clean_orphan_rpyc.py`; `--check` only
  lists). In a source checkout `game/systems/dev_source_checks.rpy` stops start-up with the
  list if you forget. Release builds are installed into a fresh folder, never over an old one.
- New stats or values that old saves lack must have a `default` and, where needed, an
  after-load migration (see `lc_migrate_stats_v2` in `game/systems/stats.rpy`).

## Adding a new Day

Day One and Day Two are the reference; Day Five shows how the last day of the build hands
over. For Day N the internal ids stay `ch01_*`: story flags `ch01_day_0N_started` /
`ch01_day_0N_complete`, review day id `ch01_dN`, chapter id `dayN`, story keys `ch01_dN_*`.
Work through the steps in order; each names the file that owns the table.

1. **Files.** Create a day folder next to `game/chapters/ch01/day2/` (for example
   day6 for Day Six) with the scene files (`ch01_dayN_scenes_01_15.rpy`, ...) and a
   `ch01_dayN_visuals.rpy` with the stable image names. Text placeholders are fine until
   art lands: `lc_placeholder_text(...)` (defined at init -1 in
   `game/chapters/ch01/day2/ch01_day2_visuals.rpy`) draws the stand-in card.
2. **Chapter registry.** Add the day to `CHAPTERS` and `CHAPTER_ORDER` in
   `game/python-packages/lc_chapters.py` (number, words, `review_day` = `ch01_dN`, neutral
   title, route titles including `repair`; darryn picks the titles from drafted options). If
   the day has a "likes watching" exhibition beat, add its variant story key to
   `NTS_VARIANT_KEYS` there. Add `define lc_chapter_card_dayN = lc_chapters.card_text("dayN")`
   in `game/systems/lc_chapters.rpy` (plus `lc_chapter_complete_card_dayN` if the day shows a
   "Chapter N complete" end card).

   **2b. The other per-day tables** (nothing fails loudly when one is missed):
   - `DAY_FLAGS` in `game/python-packages/lc_ui_logic.py`: add
     `(N, "ch01_day_0N_started", "ch01_day_0N_complete")` at the top. The journal's
     "DAY N" heading (`story_day_number`, shown by `game/screens/scrapbook_ui.rpy`) reads it.
   - `GALLERY_TAB_ACCENTS` in `game/systems/gallery.rpy`: the tab's tint (cosmetic; a
     missing tab falls back to the Prologue colour).
   - `tests/test_lc_chapters.py` (`test_registry_is_complete`) asserts `CHAPTER_ORDER`
     exactly: add the new id there.
   - `game/systems/choice_path_tags.rpy` (init 6) wraps only `format_day2_risk_choice`,
     `format_day4_gate_choice` and `format_day5_gate_choice`. A new gate formatter
     (`format_dayN_*_choice`) must join that list, or its cards get no path stamp in Full mode.
   - The previous last day ends with a runtime hand-off instead of a jump: Day Five's
     `label ch01_day5_scene_16_finish` in `game/chapters/ch01/ch01_day5_scenes_09_16.rpy`
     has an `if renpy.has_label("ch01_day6_start"): jump expression "ch01_day6_start"` block
     and a temporary "Current development build ends here" card, marked "replace with the
     literal jump". Replace both with `jump ch01_dayN_start` (Days 3-5 are
     Scriptwriter-owned: needs darryn's go-ahead) and give the new last day the same block
     for Day N+1.
   - `_lc_review_humanize` in `game/systems/day_review.rpy` strips the `ch01_d1_` ...
     `ch01_d6_` prefixes from choice ids that have no readable caption; from Day Seven on,
     add the day's prefix.
3. **Start label.** Follow `label ch01_day2_start` in
   `game/chapters/ch01/day2/ch01_day2_scenes_01_15.rpy`:
   `$ lc_review_begin("ch01_dN")` (it also names new saves after the chapter),
   `$ set_story_flag("ch01_day_0N_started")`, initial story values (read the previous day's
   stored values with a fallback for Chapter Select and older saves, as
   `label ch01_day5_start` does), then `scene black` / `with fade` /
   `centered "[lc_chapter_card_dayN]"`.
4. **Finish label.** Follow `label ch01_day2_scene_30_finish` in
   `game/chapters/ch01/day2/ch01_day2_scenes_16_30.rpy`: store the day's end route as a
   story value first (Day Two: `ch01_d2_end_route`; Day Five clamps it to the allowed keys in
   `label ch01_day5_scene_16_finish`), then `$ set_story_flag("ch01_day_0N_complete")`,
   `scene black` / `with fade`, `call lc_day_review("ch01_dN") from lc_review_return_ch01_dN`,
   then the hand-off to the next day (step 2b).
5. **Day review.** Add the day to `LC_REVIEW_DAYS` (label, chapter, `route_key` = the end
   route value), `LC_REVIEW_NIGHT` and `LC_REVIEW_TICKET` in `game/systems/day_review.rpy`.
   Day-specific route overrides go in `lc_review_route`. Every new route key needs an entry
   in `LC_REVIEW_ROUTES` and in `ROUTE_FAMILY` in `lc_chapters.py`
   (`tests/test_lc_chapters.py` checks the pair), in `LC_REVIEW_DIARY` (keyed by route, or by
   `(day_id, route)` for a day-specific pair of lines) and a branch in
   `lc_character_titles`; both are keyed by route and fall back to generic text otherwise.
   Map the day's choice ids to a style in `LC_CHOICE_STYLE` (unmapped days keep the
   route-based titles) and add `LC_MOMENT_STICKERS` rules if the day has sticker moments.
6. **Choices.** Register every choice id in an `init 1 python:` block with
   `CHOICE_EFFECTS.update({...})` and `CHOICE_TAGS.update({...})` (see the top of
   `game/chapters/ch01/day2/ch01_day2_scenes_01_15.rpy`), score them by the rules in
   `docs/STAT_MODEL.md`, and use them in menus as
   `$ x_text = format_choice("id", "Caption")` + `"[x_text]":` + `$ apply_choice("id")`.
   `tests/test_choice_scoring.py`, `tests/test_choice_path_tags.py` and
   `test_every_story_choice_id_is_registered` check them. Add `LC_CHOICE_CG_COUNT` rows in
   `game/systems/choice_path_tags.rpy` for menus that unlock different CG counts, and wrap any
   new gate formatter (step 2b).
7. **Hidden POV.** Register each moment in the day's visuals file in an `init 1 python:`
   block with `lc_pov_register(...)` and bracket its lines with `lc_pov_begin` /
   `lc_pov_end` (`docs/HIDDEN_POV.md`; Day Two's breakfast is the example). Pass
   `day_id="ch01_dN"`, `label=` and `mood=` to put it on the day's Moments strip; other
   optional moments register with `lc_discovery_register(...)` (`game/systems/discovery.rpy`).
   Push-in notices (Things Ryan noticed) follow the same pattern with `lc_notice_register` /
   `lc_notice_begin` / `lc_notice_end` (`docs/NOTICES.md`).
8. **Phone.** Deliver texts with `phone_add_message(...)` and a stable `message_id`. A new
   contact needs its thread id in the `PHONE_THREAD_ORDER` tuple assigned at init 998 in
   `game/chapters/ch01/day1/ch01_phone_moments.rpy` (it overwrites the
   `game/systems/phone_state.rpy` default, so editing only the default does nothing). A
   contact whose name the player can rename also needs a case in `phone_thread_label` /
   `phone_sender_label` (`game/systems/phone_state.rpy`). Old saves get missing threads on
   demand. Incoming calls, hesitating replies and "leave it on read" are in
   `docs/PHONE_MOMENTS.md`; pass them to the Moments strip with `lc_phone_moment_register(...)`.
9. **Sprites and gallery.** Stage sprites with `cast(...)` / `face(...)`
   (`docs/SPRITE_STAGING.md`). Add a `GALLERY_TABS` row (`("ch01_dN", "Day N", "ch01", N)`)
   and `gallery_row(...)` entries in `game/systems/gallery_data.rpy`, and list text-placeholder
   CGs in `GALLERY_PLACEHOLDER_IMAGES`; no unlock lines go in story files. The day review
   only shows a CG as a photo when it is a page of a gallery entry on the day's tab.
10. **Chapter Select (optional).** Add the day to `CH01_SELECT_DAYS` and seed it in
    `chapter_select_apply` in `game/systems/chapter_select.rpy` (mark the earlier days
    complete, store the values the start label reads, return `"ch01_dayN_start"`). Add an
    `elif _cs_entry == "ch01_dayN_start": jump ch01_dayN_start` branch in
    `label ch01_chapter_select_entry` (its `else` jumps to `ch01_day4_start`). If the day has
    its own route presets, add them in `game/systems/chapter_select.rpy` and pick them in
    `game/screens/chapter_select_screen.rpy` (`cs_routes` and the preset heading).
11. **Tests, baselines and docs.** When the day's writing pass lands, add its story files to
    the `STORY` list in `tests/test_typed_names.py` and the `MIGRATED` list in
    `tests/test_cast_staging.py`. A new day adds init side effects and changes pinned tables,
    so `tests/test_effective_fingerprints.py` fails until you re-run
    `python tools/dev/snapshot_baselines.py` (which also adds the new save names); check that
    only the day's names changed and say so in the PR. Update `docs/BUILD_HANDOFF.md`.

## Adding a feature system

1. Create one file in `game/systems/` (logic) and, if it has UI, one in `game/screens/`.
   Pure logic that can be tested without Ren'Py goes in a module in
   `game/python-packages/` with its own unit tests.
2. Start each file with the header block (copy one from an existing system, e.g.
   `game/systems/lc_hooks.rpy`): Purpose, Public API with real signatures, Internal,
   Example, Depends on, Hooks, Load order, Docs, Tests. The structure tests check it.
3. To react to another system, register a hook (`lc_hook_add`) or add a hook point to
   the owning function; never re-define another file's function or screen.
4. Use the default init priority unless the feature needs another; if it does, say why
   in a `# load order:` comment and in the header.
5. Store player data in `default` variables (save) or `persistent` (profile); never keep
   displayables in saved state. Register hooks, callbacks and overlays at init only.
6. Add tests in `tests/` and, for a user-facing feature, a doc in `docs/`. Add the
   feature to the index below.

## Testing and proof

- Unit tests (pure Python, no Ren'Py needed), from the repository root:
  `PYTHONPATH=game/python-packages python -m unittest discover -s tests -q`
  (Pillow is needed by the UI-art tests). CI runs the same suite on every pull request and
  push to `main` (`.github/workflows/tests.yml`).
- Lint with the Ren'Py SDK: `renpy.sh <project> lint`. The only expected note is the
  `init -1500` priority of the start-up guard.
- **Behaviour pins.** `tests/test_effective_fingerprints.py` compares a fingerprint of
  every effective screen, function, class, define, default, transform, image, label and
  init side effect with `tests/data/effective_fingerprints.json`; `tests/lc_rpy_model.py`
  picks the definition Ren'Py would use. A change that is meant to alter a body lists the
  name in `FOLDED` (with a reason and a behaviour test) while it is proved, then re-runs
  `python tools/dev/snapshot_baselines.py` and empties `FOLDED` in the same PR
  (`test_folded_is_empty_when_merged`). Re-baseline only after the test shows exactly the
  intended names changed.
- `tests/test_behaviour_freeze.py` (with `tests/lc_rpy_harness.py`, which runs named init
  code with stubs) pins what the folded functions do; phone delivery, the day review and
  the tag collection are pinned by their own tests.
- `tests/test_route_simulation.py` plays representative Day 1-2 choice sequences through
  the effective choice effects and the same route resolvers the story calls.

## Feature index

| Feature | File(s) | Doc | Tests |
|---|---|---|---|
| Sprite staging | `game/systems/cast_staging.rpy`, `game/systems/dialogue_staging.rpy` | `docs/SPRITE_STAGING.md` | `tests/test_cast_staging.py` |
| Choices and effects | `game/systems/choice_engine.rpy`, `game/systems/stat_model_v2_later_days.rpy` | `docs/STAT_MODEL.md` | `tests/test_choice_scoring.py` |
| Choice path / CG stamps | `game/systems/choice_path_tags.rpy` | `docs/STAT_MODEL.md` | `tests/test_choice_path_tags.py`, `tests/test_choice_cg_stamp.py` |
| Stats | `game/systems/stats.rpy`, `game/python-packages/lc_stat_model.py` | `docs/STAT_MODEL.md` | `tests/test_stat_model.py`, `tests/test_stat_runtime.py` |
| Stat colours | `game/systems/stat_delta_colours.rpy` | `docs/STAT_MODEL.md` | `tests/test_stat_delta_colours.py` |
| Stat tooltips | `game/systems/stat_tooltips.rpy`, `game/screens/stat_tooltip_screen.rpy` | `docs/STAT_MODEL.md` | `tests/test_stat_tooltips.py` |
| Status | `game/systems/status_display.rpy`, `game/screens/status_screen.rpy` | `docs/STAT_MODEL.md` | `tests/test_status_two_page.py`, `tests/test_status_colours.py` |
| Transparency modes | `game/systems/transparency_display.rpy`, `game/screens/player_settings_screen.rpy`, `game/screens/choice_mode_screen.rpy` | `docs/STAT_MODEL.md` | `tests/test_glass_menu.py` |
| Route explorer | `game/systems/full_transparency_route_explorer.rpy`, `game/screens/route_explorer_screen.rpy` | `docs/STAT_MODEL.md` | `tests/test_stat_runtime.py` |
| Story state | `game/systems/story_state.rpy` | this file | `tests/test_behaviour_freeze.py` |
| Hooks | `game/systems/lc_hooks.rpy` | this file | `tests/test_lc_hooks.py` |
| Save compatibility | `game/systems/save_compat.rpy`, `game/systems/dev_source_checks.rpy`, `tools/clean_orphan_rpyc.py` | this file | `tests/test_save_names.py`, `tests/test_orphan_rpyc.py` |
| Chapters | `game/systems/lc_chapters.rpy`, `game/python-packages/lc_chapters.py` | this file | `tests/test_lc_chapters.py` |
| Chapter Select | `game/systems/chapter_select.rpy`, `game/screens/chapter_select_screen.rpy` | this file | `tests/test_lc_chapters.py` |
| Day review | `game/systems/day_review.rpy`, `game/screens/day_review_screen.rpy` | `docs/DAY_REVIEW.md` | `tests/test_day_review.py`, `tests/test_review_sfx.py` |
| Tags and stickers | `game/systems/lc_tag_collection.rpy`, `game/screens/tag_collection_screen.rpy` | `docs/DAY_REVIEW.md` | `tests/test_tag_collection.py`, `tests/test_review_tags.py` |
| Hidden POV | `game/systems/hidden_pov.rpy`, `game/systems/hidden_pov_chime.rpy` | `docs/HIDDEN_POV.md` | `tests/test_hidden_pov.py` |
| Discoveries and Moments strip | `game/systems/discovery.rpy`, `game/python-packages/lc_discovery.py`, `game/screens/day_review_screen.rpy` (`lc_review_moments`) | `docs/HIDDEN_POV.md` | `tests/test_discovery.py` |
| Ryan's thoughts | `game/systems/thoughts.rpy`, `game/python-packages/lc_thoughts.py`, `game/screens/thoughts_screen.rpy` | `docs/THOUGHTS.md` | `tests/test_thoughts.py` |
| Things Ryan noticed | `game/systems/notice.rpy`, `game/python-packages/lc_notice.py`, `game/screens/notice_screen.rpy`, `game/screens/phone_sweetheart.rpy` (Status pins) | `docs/NOTICES.md` | `tests/test_notice.py` |
| Leia's side (errand map, visit log, outcomes, +2/day cap) | `game/systems/leia_side.rpy`, `game/python-packages/lc_leia_side.py`, `game/screens/leia_map_screen.rpy`, `game/dev/dev_leia_side.rpy` (demo) | `docs/LEIA_SIDE.md` | `tests/test_leia_side.py` |
| Feed app (social feed on the phone) | `game/systems/feed.rpy`, `game/python-packages/lc_feed.py`, `game/screens/phone_feed.rpy`, `game/chapters/ch01/day2/ch01_day2_feed.rpy` (Day Two posts) | `docs/FEED.md` | `tests/test_feed.py` |
| Phone moments (calls, hesitation typing, leave on read) | `game/systems/phone_moments.rpy`, `game/python-packages/lc_phone_moments.py`, `game/screens/phone_call.rpy`, `game/dev/dev_phone_moments.rpy` (demo) | `docs/PHONE_MOMENTS.md` | `tests/test_phone_moments.py` |
| Gallery | `game/systems/gallery.rpy`, `game/systems/gallery_data.rpy`, `game/screens/gallery_screen.rpy` | `docs/BUILD_HANDOFF.md` | `tests/test_gallery_flags.py` |
| Phone data | `game/systems/phone_state.rpy`, `game/systems/phone_presentation_logic.rpy`, `game/systems/phone_group_avatar.rpy` | this file | `tests/test_phone_replies.py`, `tests/test_phone_read_state.py`, `tests/test_phone_group_avatar.py` |
| Phone UI | `game/screens/phone_sweetheart.rpy`, `game/screens/phone_hud.rpy`, `game/screens/phone_screen.rpy`, `game/screens/phone_input_blocker.rpy`, `game/screens/phone_wallpaper.rpy`, `game/screens/gameplay_toasts.rpy` | this file | `tests/test_phone_layout.py`, `tests/test_phone_back_navigation.py`, `tests/test_phone_wallpaper.py` |
| Wardrobe, shop, economy | `game/systems/wardrobe_logic.rpy`, `game/systems/outfits_data.rpy`, `game/systems/outfit_display.rpy`, `game/systems/love_outfit_control.rpy`, `game/systems/economy.rpy`, `game/screens/wardrobe_screen.rpy`, `game/screens/shop_screen.rpy` | this file | `tests/test_shop_coming_soon.py` |
| Effects and audio | `game/systems/lc_fx.rpy`, `game/systems/lc_audio_scene_lock.rpy`, `game/systems/lc_breath.rpy`, `game/systems/lc_typing_sounds.rpy` | this file | `tests/test_lc_fx.py`, `tests/test_bgm.py`, `tests/test_audio_scene_lock.py`, `tests/test_breaths.py`, `tests/test_typing_sounds.py` |
| UI skin and stock screens | `game/screens/scrapbook_ui.rpy`, `game/screens.rpy`, `game/screens/common_scroll.rpy` | `docs/DIALOGUE_STYLE.md` | `tests/test_scrapbook_ui.py`, `tests/test_glass_menu.py`, `tests/test_text_styles.py` |
| Hover fade and cursor | `game/systems/lc_hover_fade.rpy`, `game/systems/lc_cursor.rpy` | this file | `tests/test_smooth_hover.py`, `tests/test_cursor.py` |
| Title screen | `game/systems/title_screen.rpy`, `game/systems/title_customiser.rpy`, `game/systems/lc_title_touch.rpy`, `game/screens/title_screen.rpy`, `game/screens/title_customiser.rpy` | `docs/TITLE_SCREEN.md` | `tests/test_title_screen.py`, `tests/test_title_customiser.py`, `tests/test_title_leia_touch.py` |
| Release switch | `game/00_release_build.rpy`, `game/options.rpy` | `docs/BRANCH_AND_RELEASE_POLICY.md`, `docs/RELEASE_JOIPLAY.md` | `tests/test_release_from_main.py` |
