# Hidden POV opportunities

Optional views are discoverable, nonmodal cues during ordinary say dialogue, **not** story choices. Ignoring a cue advances the same line and route. Opening one does not change stats, send messages, or change the narrative image. The full-screen modal viewer closes onto the very same dialogue interaction.

## Add a moment

1. Define a stable `image cg ...` as usual. If it belongs in the Gallery, add the stable image name to a Gallery row; the Day Two breakfast page remains `d2_breakfast_pov`, `mature=True`.
2. In an init-time registration file (`init 1 python` or later), add a row (no custom screen):

   ```renpy
   init 1 python:
       lc_pov_register(
           "unique_moment_id",
           image="cg stable_pov_image",
           source="cg currently_shown_image",
           center=(1340, 450),      # sparkle centre, 1920x1080 coordinates
           title="Optional view",
           # mature=...             # omit: copied from the Gallery row
           # gallery_id="row_id"    # only if the image is in several rows
           # sfx=False              # opt out of the soft chime
       )
   ```

   | Option | Meaning |
   |---|---|
   | `image` | The registered POV CG, including the `cg` tag. |
   | `source` | The **exact master-layer image** that hosts the cue, including tag. It must already be on screen when dialogue begins. |
   | `center=(x, y)` | Where the sparkle sits. The click/tap area is a square centred there: **120 px** on desktop, **160 px** on touch builds (`LC_POV_HITBOX`, `LC_POV_HITBOX_TOUCH`). Preferred for new moments. |
   | `position=(x, y)` | Legacy form: the upper-left of the old 64x64 slot. The centre is `position + 32`, so old registrations keep their sparkle in the same spot. Pass exactly one of `center` / `position`. |
   | `title` | Viewer label and the hotspot's screen-reader text ("Hidden moment: <title>"). Canonical names are customised. |
   | `mature` | Adds the viewer's 18+ badge. Leave it out and it is copied from the Gallery row that lists `image`; if you pass it, it must agree with that row. |
   | `gallery_id` | Only needed when the image appears in more than one Gallery row. |
   | `sfx` | Default `True`: play the soft sparkle chime once when the cue first appears in an encounter. |

3. Immediately after showing the source CG (and before the first eligible say line), write `$ lc_pov_begin("unique_moment_id")`; restore ordinary HUD/UI before dialogue starts. Place `$ lc_pov_end()` after the last eligible line, before the next scene/jump; if an early exit exists, end it there too. The source-image guard and start-interaction callback automatically clear a stale active opportunity when the source leaves the master layer (including scene changes on paths that missed the end hook). A new begin resets that encounter's viewed suppression. Do not tie suppression to permanent `renpy.seen_image`: revisiting a scene on replay offers the cue again.
4. Lint (or just launch) the game. The registration check below tells you if anything is off.

Eligibility is deliberately limited to the begin/end hooks, the shown source image, and ordinary say UI; do not put story mutations or side effects in the screen predicate. Put branch-specific begin hooks inside the eligible branch.

## Registration check (init 999)

After every registration file and the Gallery tables load, `lc_pov_validate_all()` checks each moment:

- `image` and `source` are defined images (`renpy.has_image`).
- The largest (touch, 160 px) hit area stays on the 1920x1080 screen and clear of reserved UI: the dialogue box and everything below it (y >= 792, which also covers the phone HUD and quick menu) and the phone notification banner at the top centre (x 610-1310, y 0-116). See `LC_POV_RESERVED_RECTS`.
- `mature` agrees with the Gallery row (or is filled in from it), and `gallery_id` names a real row.

In developer builds (`config.developer`, which includes lint) any problem raises one exception listing every issue. Release builds only log the problems (`log.txt` / stdout) and keep running.

## One cue at a time

Only one opportunity is active at once. Calling `lc_pov_begin` while another is still active logs a warning (and shows a notify in developer builds), ends the previous one cleanly, then starts the new one. Fix the script by adding the missing `lc_pov_end()`.

## Mode and interaction contract

- Normal: a warm glow with a gently twinkling gold sparkle (`gui/pov/glow_idle.svg` + `gui/cursor/sparkle_idle.png`). Insight: that sparkle plus a gold `!`. Full: a red circular button with a white `!` (`gui/pov/bang_idle.svg`: 62 px game-red `#d6334a` disc, darker rim, soft shadow; the `!` is drawn as shapes so it is exactly centred) with a soft pulse ring while idle. Developer: the same button with the moment id beside it. The global mouse cursor is untouched. Insight's small gold `!` uses the SDK's DejaVu Sans font.
- Hover/focus is clearly different from idle: the pink hover sparkle, a brighter pink glow (`gui/pov/glow_hover.svg`) and a small springy scale pulse; the Full/Developer button turns a lighter red (`gui/pov/bang_hover.svg`), gains a white ring highlight and springs up to 110%, and its idle pulse ring stops. Ren'Py buttons have no pressed style state, so there is no separate pressed art; the viewer opens on click. Hovering plays the usual UI tick. All art is centred inside the fixed hit square, so scaling never moves the button or reflows dialogue. Art is cached per state so a screen refresh never restarts the animation.
- Reduced motion: there is no dedicated preference, so the cue goes static (fixed glow, no twinkle, pulse ring or spring) when the player turns off **Screen shake** or **Transitions** in Preferences (`lc_pov_reduce_motion()`).
- Sound: a soft, project-made two-note chime (`LC_POV_CUE_AUDIO`: an OGG embedded in `systems/hidden_pov_chime.rpy` and played via `AudioData`, generated by `tools/gen_pov_cue_assets.py`, credited in `audio/CREDITS.md`) plays once per encounter when the cue first appears, on the UI channel (SFX slider). It is skipped while skipping, and `sfx=False` turns it off per moment.
- Screen readers: the hotspot's alt text is "Hidden moment: <title>"; the viewer's close button reads "Close hidden moment".
- The hotspot is an overlay above the story image but below the phone; it is absent when a phone/journal/menu covers the scene, the quick menu is suppressed, no say screen is active, the viewer is open, the encounter was viewed, or the source CG is gone. Hidden-interface mode suppresses ordinary overlays.
- The click handler alone calls SDK `renpy.mark_image_seen(image)` and `renpy.save_persistent()` for the Gallery's existing `renpy.seen_image(("cg", name))` rule. Screen prediction, hover, and rendering do not mark seen. The viewer itself uses `add`, not `scene`/`show` of the CG. This is profile-wide Gallery history; rollback can restore local cue state, **not** undo persistent Gallery history after an actual view.
- `Function(lc_pov_open, id)` shows a modal screen using `renpy.show_screen` without Return, call, jump or changing the master-layer image. The viewer sits at zorder 630, above the phone notification banner (620), so a toast can never cover the art. Close via button, Escape, game-menu key, or right click. Its full-screen shield consumes other clicks; no clickthrough advances the say line. The click stops active Skip (does not resume it). Auto-forward remains the user's preference: the SDK say behavior consults `config.afm_callback` before advancing, and our chained callback returns False while the viewer is open. Closing resumes normal Auto behavior without changing that preference. The modal blocks skip timers according to SDK `display/behavior.py`'s `ev.modal` path.
- Gallery: a locked row that a Hidden POV unlocks shows a spoiler-free "HIDDEN MOMENT / look for the sparkle" card instead of the plain LOCKED card, and its locked description/notify say the same (`gallery_is_hidden_pov`). No title or art is revealed.

## Acceptance checklist (darryn, **not run here**)

- Fresh save: compare Normal, Insight, Full, Developer at the breakfast CG; check pixel placement, hover and supported glyphs, unchanged cursor, and phone HUD access. Ignore the cue and verify the line and phone reply proceed normally; no POV Gallery unlock.
- Click on a line mid-dialogue, including Auto and Skip enabled: verify the underlying line remains, viewer displays correct art, no stray click advances text, Escape/Close return cleanly, phone and Esc menu remain usable afterward. Confirm only the click unlocks the mature Gallery page.
- Save/load and rollback before/after clicking, then revisit/replay the encounter; check per-encounter suppression, persistent Gallery history, and source-image cleanup on transition. Check hidden-interface mode, touch scaling, menus and phone priority.

## Limits

Static lint cannot validate hotspot alignment against final art, focus/key priority, transition frames, save serialization, or live Auto/Skip click behavior. Ren'Py records seen CGs in profile-wide persistent history; it cannot be rolled back with save state. Saves made **inside** the removed legacy blocking `call screen lc_breakfast_julian_pov` (builds of 2026-11-10 to 11-14) still name that screen, so `game/systems/save_compat.rpy` keeps a stub `screen lc_breakfast_julian_pov()` that draws nothing and immediately returns `None` (the old "keep reading" result). If Ren'Py cannot find the old statement after the script change it rolls back to the nearest earlier point instead; an earlier save always works. Old saves elsewhere keep their stable image/gallery ids. Registration data is init-time and assumes a single active opportunity per scene (see *One cue at a time*). The cue term in player-facing copy is **sparkle**.
