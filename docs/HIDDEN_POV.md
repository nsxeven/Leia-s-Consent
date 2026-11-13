# Hidden POV opportunities

Optional views are discoverable, nonmodal cues during ordinary say dialogue, **not** story choices. Ignoring a cue advances the same line and route. Opening one does not grant consent, change stats, send messages, or change the narrative image. The full-screen modal viewer closes onto the very same dialogue interaction.

## Add a moment

1. Define a stable `image cg ...` as usual. If it belongs in the Gallery, add the stable image name to a Gallery row; the Day Two breakfast page remains `d2_breakfast_pov`, `mature=True`.
2. In an init-time registration file, add a row (no custom screen):

   ```renpy
   init 1 python:
       lc_pov_register(
           "unique_moment_id",
           image="cg stable_pov_image",
           source="cg currently_shown_image",
           position=(1310, 420),
           title="Optional view",
           mature=False,
       )
   ```

   `image` is the registered CG (including `cg` tag); `source` is the **exact master-layer image** that hosts the cue, including tag; `position` is the upper-left corner of a fixed 64×64 hitbox at the game's 1920×1080 coordinates. Pick a position on the scene itself, away from say box (y=792 onward), phone at bottom right, and quick menu. `title` labels the viewer; `mature` adds its 18+ badge (and must agree with the Gallery's mature flag). The source image must already be on screen when dialogue begins. Eligibility is deliberately limited to the begin/end hooks, the shown source image, and ordinary say UI; do not put story mutations or side effects in the screen predicate. Put branch-specific begin hooks inside the eligible branch.
3. Immediately after showing the source CG (and before the first eligible say line), write `$ lc_pov_begin("unique_moment_id")`; restore ordinary HUD/UI before dialogue starts. Place `$ lc_pov_end()` after the last eligible line, before the next scene/jump; if an early exit exists, end it there too. The source-image guard and start-interaction callback automatically clear a stale active opportunity when the source leaves the master layer (including scene changes on paths that missed the end hook). A new begin resets that encounter's viewed suppression. Do not tie suppression to permanent `renpy.seen_image`: revisiting a scene on replay offers the cue again.

## Mode and interaction contract

- Normal: a gentle twinkling gold sparkle using `gui/cursor/sparkle_idle.png`; Insight: that sparkle plus a gold `!`; Full: red `!`; Developer: red `!` with the moment id beside it. The global mouse cursor is untouched. The `!` uses the SDK's DejaVu Sans font.
- The hotspot is an overlay above the story image but below the phone, in a fixed 64×64 slot; it is absent when a phone/journal/menu covers the scene, the quick menu is suppressed, no say screen is active, the viewer is open, the encounter was viewed, or the source CG is gone. Hidden-interface mode suppresses ordinary overlays.
- The click handler alone calls SDK `renpy.mark_image_seen(image)` and `renpy.save_persistent()` for the Gallery's existing `renpy.seen_image(("cg", name))` rule. Screen prediction, hover, and rendering do not mark seen. The viewer itself uses `add`, not `scene`/`show` of the CG. This is profile-wide Gallery history; rollback can restore local cue state, **not** undo persistent Gallery history after an actual view.
- `Function(lc_pov_open, id)` shows a modal screen using `renpy.show_screen` without Return, call, jump or changing the master-layer image. Close via button, Escape, game-menu key, or right click. Its full-screen shield consumes other clicks; no clickthrough advances the say line. The click stops active Skip (does not resume it). Auto-forward remains the user's preference: the SDK say behavior consults `config.afm_callback` before advancing, and our chained callback returns False while the viewer is open. Closing resumes normal Auto behavior without changing that preference. The modal blocks skip timers according to SDK `display/behavior.py`'s `ev.modal` path.

## Acceptance checklist (darryn, **not run here**)

- Fresh save: compare Normal, Insight, Full, Developer at the breakfast CG; check pixel placement, hover and supported glyphs, unchanged cursor, and phone HUD access. Ignore the cue and verify the line and phone reply proceed normally; no POV Gallery unlock.
- Click on a line mid-dialogue, including Auto and Skip enabled: verify the underlying line remains, viewer displays correct art, no stray click advances text, Escape/Close return cleanly, phone and Esc menu remain usable afterward. Confirm only the click unlocks the mature Gallery page.
- Save/load and rollback before/after clicking, then revisit/replay the encounter; check per-encounter suppression, persistent Gallery history, and source-image cleanup on transition. Check hidden-interface mode, touch scaling, menus and phone priority.

## Limits

Static lint cannot validate hotspot alignment against final art, focus/key priority, transition frames, save serialization, or live Auto/Skip click behavior. Ren'Py records seen CGs in profile-wide persistent history; it cannot be rolled back with save state. A loaded save from **inside** the removed legacy blocking `call screen lc_breakfast_julian_pov` may need an earlier save; old saves elsewhere keep their stable image/gallery ids. Registration data is init-time and assumes a single active opportunity per scene; begin a new one only after ending the previous one.
