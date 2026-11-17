# Things Ryan noticed (push-in notices)

A notice is a small detail that is already in a CG and that Ryan can stop on. While the CG is
on screen, a small **eye** cue sits on it (a sibling of the Hidden POV sparkle, with its own
art). Clicking it pushes the camera in on the detail and shows one or two of Ryan's thoughts
about it in the dialogue-box spot. Another click eases back to the same line. Notices are
optional and never block anything: ignoring the eye plays exactly as before, and noticing never
changes stats. A later talk can offer an extra, normally scored option when a notice was made.

All characters are adults. Captions use `[player_name]`, `[girlfriend_name]` and `[friend_name]`
(never the default names), US spelling, and Ryan's inner voice (they render in italics).

## Add a notice

1. Pick a detail in a **finished** CG (a file-backed `image cg ...`, never a placeholder
   Composite). Use a spot that is the same on every lane; only the captions change by lane.
2. Register it in the day's visuals file, in an `init 1 python:` block:

   ```renpy
   init 1 python:
       lc_notice_register(
           "d2_notice_bed_hand",
           source="cg ch01_d2_leia_sleeping",   # the master-layer CG that hosts the cue
           center=(600, 680),                    # eye centre, 1920x1080 coordinates
           focus_rect=(300, 380, 600, 660),      # what the push-in frames (x, y, w, h)
           # zoom=1.35,                          # 1.0 < zoom <= 1.4 (CGs are 1920x1080)
           lines=["Base caption (no lane / mixed)."],
           lane_lines={"love": ["...", "..."], "exhib": ["..."], "ntr": ["..."]},
           # closeup="cg some_existing_closeup", # cut to an existing close-up render instead
           day_id="ch01_d2", label="Morning, her hand", mood="still reaching",
       )
   ```

   | Option | Meaning |
   |---|---|
   | `source` | The exact master-layer image that hosts the cue (with the `cg` tag). |
   | `center` | Eye centre. The click area is a square around it: 120 px desktop, 160 px touch (`LC_NOTICE_HITBOX`, `LC_NOTICE_HITBOX_TOUCH`, same as Hidden POV). |
   | `focus_rect` | The part of the CG the push-in frames. The zoom is lowered automatically if the rect would not fit the visible window. |
   | `zoom` | Push-in zoom, default 1.35, at most 1.4 (`lc_notice.MAX_ZOOM`); more would blur a 1920x1080 CG. |
   | `lines` | 1-2 captions shown when no lane caption applies. Required. |
   | `lane_lines` | Optional `{"love" / "exhib" / "ntr": [1-2 captions]}`. The lane comes from the stats-model lean (`lc_current_lean`: `love`, `love_exhib`, `ntr`); other leans use `lines`. **Love captions are about Leia** and stay warm. |
   | `closeup` | Optional existing close-up render: the viewer fades to it (over the push-in) instead of only zooming. |
   | `day_id`, `label`, `mood` | Optional: also registers a `notice` discovery on that day's Moments strip (`docs/HIDDEN_POV.md`, "Seen record and Moments strip"). The label also titles the Status pin; keep route words out of it. |

3. In the scene, right after the `scene cg ...` / `with ...` that shows the source CG, add
   `$ lc_notice_begin("d2_notice_bed_hand")`; add `$ lc_notice_end()` after the last line it
   should be available on, before the next `scene`. A scene change also ends it automatically.
   Notices and Hidden POVs have separate scopes, so a CG can host one of each.
4. To pay it off later, check the save-local record: `lc_noticed("id")` or
   `lc_noticed_any("id1", "id2")`. Offer an **extra option** in an existing talk (registered and
   scored like any choice, `tests/test_choice_scoring.py` + `tests/test_choice_path_tags.py`),
   next to a plain no-stat option that plays the old text.

## Registration check (init 999)

`lc_notice_validate_all()` runs after every registration and the Hidden POV registry. It
reports, and in developer builds (including lint) raises on: an undefined `source`/`closeup`;
a cue hit area off screen or over reserved UI (`LC_POV_RESERVED_RECTS`: the dialogue box and
everything under it, y >= 792, and the phone banner); a cue overlapping a Hidden POV cue or
another notice **on the same CG**; a `focus_rect` outside the frame; a zoom outside 1.0-1.4; a
caption that types a default name or is longer than 150 characters. Rules:
`game/python-packages/lc_notice.py`.

## Behaviour

- **Cue.** Immersive/Insight: a cream eye that blinks now and then over the warm Hidden POV
  glow. Full/Developer: a honey disc with a white eye (Developer adds the notice id). Hover and
  keyboard/gamepad focus show the pink hover state with a small spring. It shows only when the
  source CG is on the master layer, the say screen is up, and no phone, journal, menu, Hidden
  POV viewer or hidden-interface mode covers the scene; once per encounter. Alt text:
  "Something you noticed: <label>".
- **Viewer.** Modal, zorder 630 (above the phone banner). The CG pushes in (`LC_NOTICE_IN`,
  0.9 s ease) and the captions fade up in the dialogue-box spot. A click anywhere, Esc, right
  click, Space/Enter or the Back button eases back (`LC_NOTICE_OUT`, 0.45 s) and closes onto
  the same line: nothing advances the dialogue, and Auto waits while it is open. Skipping or
  reduced motion (Screen shake or Transitions off) makes the push-in and the ease back instant.
  Opening stops Skip.
- **Record.** Only the click writes `lc_noticed_record` (save-local `{notice_id: caption lane
  seen}`, a new dict each time, so rollback undoes it and a repeat click changes nothing) and
  marks the `notice` discovery. Old saves and Chapter Select starts read as nothing noticed.
- **Status pins.** The phone Status app shows a "Things I noticed" card once something was
  noticed: one fixed-height row of pins (a crop of the noticed detail, the label and the first
  caption Ryan saw), scrolling sideways when there are more.

## Day Two instances

| Notice | CG | Spot |
|---|---|---|
| `d2_notice_bed_hand` | `cg ch01_d2_leia_sleeping` (scene 1) | her hand reaching to Ryan's side of the bed |
| `d2_notice_breakfast_smile` | `cg ch01_d2_breakfast_01` (scene 2) | her smile across the breakfast table |

Either one offers **"Tell her what you noticed this morning."** (`ch01_d2_sunset_noticed`,
Love +1, Trust +1) after the sunset talk in `ch01_day2_scene_20_dinner_outfit`, on the shared
tail every lane reaches, except after the "I'm fine" soft gate. "Keep it to yourself." plays the
old text. Leia's answer follows the sunset lane (Love: warm). Stored as story value
`ch01_d2_sunset_noticed`.

## Limits

Static tests and lint cannot check the eye's placement against the art, the feel of the
push-in, or live Auto/Skip input; those need a play check.
