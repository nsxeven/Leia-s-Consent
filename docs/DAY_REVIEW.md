# Daily review and character titles

Implemented against main `c920dd9c1acb91d03c3301f370bc2dd967fe9915` (Ren'Py 8.5.3).

## Player behaviour

Days 1–5 now call one reusable review before handing off to the next day or the existing demo ending. The review uses only the current save's recorded day, not the persistent gallery's unlocked images. Up to five moments are selected across the day; each moment uses the latest variant actually shown. Cards fade/drop in with a small tilt, can be revealed immediately, and can be animated or static. Dream cards are labelled.

The existing Information Transparency setting controls detail:

- Immersive: story summary, photographs and optional character titles; no numbers or route label.
- Insight: qualitative changes in player-facing stats and current direction.
- Full / Developer: exact net stat changes and expandable actual choice effects after clamping. Direct story/debug adjustments contribute to totals but are not fabricated as choices.

Gameplay Settings adds animation, Story/Genre/Off titles, brief sprite badges (off by default), and Day One dream Full/Summary/Ask controls. Status shows the titles and can reopen the latest completed review. The summary option skips only the Day One dream presentation; all three waking responses and their consequences remain shared. It does not disable NTR elsewhere.

## Add a future day

1. Add its stable ID, display label and authoritative end-route story key to `LC_REVIEW_DAYS` in `game/systems/day_review.rpy`. Keep registry order chronological. Do not rename shipped IDs.
2. At the start of the day, before choices or stat changes:

   ```renpy
   $ lc_review_begin("ch01_d6")
   ```

3. After the ending has stored its route, before the next-day jump:

   ```renpy
   call lc_day_review("ch01_d6") from lc_review_return_ch01_d6
   ```

4. Register its CG moments under the same day ID in `GALLERY_TABS` / `GALLERY_TABLE`. Use stable image names; replacing placeholder art with final art needs no recap code change. Normal `scene cg ...` and `show cg ...` statements are captured automatically. A day without CGs still has its text review. Calls using `renpy.show` directly bypass the statement callback; explicitly call `lc_review_record_image("cg image_name")` after showing such a story image. Never call it for gallery/prediction/unseen images.
5. If adding an end-route value, add its display label and Ryan-safe summary to `LC_REVIEW_ROUTES`. Unknown route values currently fall back to Mixed. Author summaries using only information Ryan knows.

`lc_review_begin` does not reset an unfinished active day's baseline on repeated entry. `lc_review_finish` freezes the completed record once; reopening it cannot collect new photographs or future title facts. Chapter Select resets review history along with its existing reset flow. Old saves that reach a day ending without a captured start get a partial recap rather than invented stat changes. Full tracking starts on the following day.

## Title milestones

Story titles follow completed-day direction. Genre titles are optional presentation; they never alter gameplay. Existing ambiguous `ntr_confirmed` / `ntr_seeded` route flags do **not** prove infidelity or Ryan's knowledge.

Explicit milestone API for future authored events:

```renpy
# Only when the event has actually happened and is known to Ryan:
$ lc_title_fact("sharing_agreed")
$ lc_title_fact("sharing_happened")
```

Supported facts: `sharing_agreed`, `sharing_happened`, `betrayal_known`, `humiliation_agreed`, `married`, `repair_chosen`, `separated`. A fact can be cleared with `lc_title_fact("repair_chosen", False)` when the story changes. Separation and repair take priority; clear obsolete facts deliberately.

- Love: Devoted Boyfriend / Affectionate Partner.
- Shared attention: Knowing Accomplice / Enjoying the Attention.
- Shared curiosity: Curious Partner / Testing the Waters.
- Unresolved pressure: Uneasy Observer / Growing Distant.
- Confirmed sharing plus agreement: Sharing Partner / Adventurous Partner; Genre: Stag / Shared Girlfriend (Hotwife requires marriage).
- Known betrayal: Betrayed Boyfriend / Unfaithful Lover; Genre: Cuckold / Cheating Girlfriend. Beta Cuck additionally requires the explicit humiliation-agreement milestone.
- Repair / separation have their own story titles.

Advanced milestone titles are available to future scripts but are not retroactively asserted from existing ambiguous route flags or dreams. Above-sprite badges are brief, use the existing left/right staging, and appear only while the corresponding character is shown. Ryan's title remains available in Status when he has no on-screen sprite.

## Validation and release handoff

All 19 logic tests passed. Run `python3 -m unittest discover -s tests -v`. These tests execute the production Python block with engine boundaries stubbed. Snapshot copying is tested; that is not an engine rollback test.

Ren'Py lint was compared with the unchanged source baseline: 383 diagnostic lines in each, no newly introduced diagnostic lines after normalizing line numbers. This source-only checkout does not contain the project's image, font or audio binaries, so this is not a clean media-complete release lint.

The isolated rendered smoke test did not complete reliably in the available environment. Visual layout, engine save/load and engine rollback are **not verified**. The implementation is delivered in a draft PR for this reason.

Before shipping a demo, run with the complete assets and check:

- End each of Days 1–5; confirm the next-day/demo handoff and restored phone/quick-menu state.
- Compare Immersive, Insight and Full; expand choice details and scroll long recaps.
- See the animated five-card layout; reveal immediately; turn animation off; reopen from Status.
- Save/load during a day and at the recap; roll back across a choice/CG/day boundary and change branch. No discarded-branch cards should remain.
- Load an older mid-day save and confirm the partial-recap notice.
- Test Day One Full and Summary with each waking response: identical stats/story flags, but unseen dream CGs absent from that run's recap.
- Finish the outstanding CGs, preserve their stable image names, and then package the demo from the chosen release source. This change creates no release package and does not merge unrelated narrative PRs.
