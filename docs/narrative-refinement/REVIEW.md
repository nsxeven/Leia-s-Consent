# Narrative refinement review

## Scope and status

Branch: `feature/narrative-refinement-days1-5`, based on main `41913f32e216e9b7cfb96ee7fc5a330468857786`.

This is a **targeted non-graphic editorial and continuity pass across Days 1–5**, not a completed full rewrite or a claim that every line of the roughly 40,000-word build has been reviewed. It includes bounded competitor research, source reconciliation, 23 affected scene labels, one dialogue-selection fix, and reproducible state smoke checks. Explicit passages were left unchanged. The original request for exhaustive scene-by-scene refinement remains only partially fulfilled.

No approved event, timeline, asset, choice ID, stored-state key, gallery reference or phone message ID was replaced. No Notion document was edited. No new CG or placeholder implementation is claimed. Ryan and Leia still begin as a loving couple. Maya and Julian retain their independent relationship. Dream anxiety is not treated as proof of events. Shared attention and hidden conduct remain distinct route concepts.

## Canon reconciliation before editing

Authority was reconciled against the checked-out commit rather than assuming every historical Notion page described the current build.

| Evidence | Discrepancy / resolution |
|---|---|
| [Development Hub](https://www.notion.so/3d71b392fa4c8168b2ffd870b23716e8), latest Oct 18 append; repository README and BUILD_HANDOFF | These describe implemented Days 1–5 and the 47-entry gallery. They agree with main. Day 6 was described elsewhere as a local draft and is not included here. |
| [START](https://www.notion.so/3dc1b392fa4c81cb951ae8d3c8fd898e), [canonical index](https://www.notion.so/3dc1b392fa4c812b9219f1a557e9bebc), [handoff](https://www.notion.so/3da1b392fa4c81eabc93c3ecac617bed) | Older descriptions of orphaned Day 3, absent Day 4 or no gallery are stale implementation status, not instructions to remove working content. |
| [Bible](https://www.notion.so/3d91b392fa4c81298853c2d1da978ea0) and [route map](https://www.notion.so/3d91b392fa4c81539526f79651b1cd35) | Character history, adult cast, relationship foundation and approved incidents remain authoritative. Implementation-status remarks need reading alongside newer Hub entries. |
| [Day 1 reference](https://www.notion.so/3dc1b392fa4c816781bdcfedb39720fd), [Day 2 reference](https://www.notion.so/3dc1b392fa4c8190b164c770f65708a8), [Day 3 reference](https://www.notion.so/3dc1b392fa4c81258928dfebb066d392) | Used for route intent and established incidents; no wholesale replacement from older prose. |
| [QA reference](https://www.notion.so/3dc1b392fa4c812e9b3fcf00bf1eac6f) and live art wiring | DinnerSpill01–04, distinct TowelDidHeSee and corrected dry/wet stranger rig already exist in main. Older pending-work notes do not justify recreating assets. Day 2 and Days 4–5 still contain placeholders; Day 3 still contains CG TODOs. |
| [Blueprint](https://www.notion.so/3d71b392fa4c818a8e0ac77b0b250ca3) | Historical UI descriptions differ from later runtime work. No UI/art redesign attempted. |

## Largest narrative weaknesses observed

1. **False or overly specific callbacks undermine player memory.** Examples include Leia and Julian supposedly only knowing each other for two days, a dress being described as her purchase regardless of payer, and a late message assuming the cove was the disclosure location. These are corrected in the affected scenes.
2. **Narration often explains a beat after dialogue already expresses it.** Selected passages now use chairs, gestures, coffee and interrupted speech. This makes friendship and discomfort more immediate without making all characters agreeable.
3. **Some prose exceeds Ryan’s knowledge.** Assertions about what both people rehearsed or whether others were lying were narrowed to what he can observe. A comprehensive viewpoint audit remains outstanding.
4. **Day 3 compresses relationship time.** The Love balcony previously resolved into a generic declaration and kiss. A brief personal exchange now gives the pair shared humor. This does not resolve broader differences in scene depth across all routes.
5. **Dialogue occasionally exposes implementation structure.** Spoken “Day Two” and “Day four” references were replaced where edited. Other meta-language remains editorial debt.
6. **Visual completeness and name customization lag behind script coverage.** Day 3 has sparse background transitions, later scripts contain hardcoded display names, and multiple days use placeholders. These require separate review; this branch does not imply a finished production build.

## Route-state and continuity audit

| Handoff / system | Observed contract | Result / limitation |
|---|---|---|
| Day 2 ending | `love`, `exhibitionism`, `love_repaired`, `mixed_unresolved`, `ntr_confirmed` | Preserved. Chapter-select presets checked. |
| Day 3 lane | Stored Day 2 result maps into Love, exhibitionism or NTR lane | Preserved. Intermediate repair responses affect scenes but do not create a new ending lane in this pass. No exhaustive traversal. |
| Day 4 ending | `love`, `exhibitionism`, `love_repaired`, `ntr_unresolved`, `ntr_confirmed` | Preserved. Day 4 presets check stored Day 2 setup. |
| Day 5 entry | `love_repaired` becomes track `ntr_repaired`; pending ending is stored separately | Actual top-level Ren’Py Python statements checked for each preset. |
| Day 5 resolution | Pending result becomes `ch01_d5_end_route`; completion flag set | All five initial ending resolutions checked. Does not explore every interactive path leading to them. |
| Day 5 dinner | Original repaired track OR currently repaired pending outcome receives the disclosure callback | Fixed predicate: `d5_track == "ntr_repaired" or d5_pending == "love_repaired"`. Seven AST branch cases checked, including repaired-then-setback. |
| Choices / gallery | Literal Chapter One choice IDs must be registered; gallery validator checks its own invariants | Both checks passed. Not proof that every visual exists or every menu consequence is balanced. |
| Phone | Message IDs and operations preserved; two message bodies polished | Actual phone UI interaction not exercised. Day 3’s typo/correction sequence remains plain-text TODO integration. |
| Rollback / saves | No new state variables or data migrations | Interactive rollback and old-save loading not tested. Existing saves paused within edited dialogue may need separate compatibility testing. |

The only non-comment, non-prose control-flow difference is the dinner predicate above; see `control-flow-diff.txt`. No choice outcomes or relationship-stat effects were changed. See `SCENE_LOG.md` for the label inventory and exact editorial decisions.

## Validation

- Ren’Py **8.5.3.26051504** was downloaded and executed locally. Native execution from the workspace failed; extracting the SDK under `/tmp` allowed lint and the no-display test command to run.
- Lint completed with **17 diagnostics, identical to the baseline set**. With `--error-code`, current lint exits 1. This is not a clean lint result.
- Existing diagnostics: five undefined `white` image uses; seven malformed legacy photo-alias references; four out-of-range init priorities; one undeclared `julian` hide tag. Full reports: `lint-baseline.txt` and `lint-current.txt`.
- **32 smoke checks passed**: 18 chapter-select presets, five Day 5 stored ending resolutions, seven dinner callback cases, registered literal choice IDs and gallery validation. See `state-smoke-results.json`.
- Running the same harness on the baseline fails the newly repaired dinner callback: it selects the unrelated hallway memory. See `baseline-regression.json`. This establishes regression sensitivity for the actual fix.
- No visual playthrough, full route traversal, interactive rollback, old-save loading, mobile-layout verification or exhaustive asset-file audit was completed. A dummy-display attempt could not initialize a usable renderer; the successful state tests deliberately use no display.

### Reproducing state checks

Use a disposable copy of the project, copy `tools/narrative_smoke.rpy` into that copy’s `game/zzzz_narrative_smoke.rpy`, and run:

```sh
RENPY_PATH_TO_SAVES=/tmp/lc-narrative-test-saves \
LC_NARRATIVE_TEST_REPORT=/tmp/lc-state-smoke-results.json \
/path/to/renpy-8.5.3-sdk/renpy.sh /path/to/disposable-project narrative_smoke
```

The harness intentionally lives outside `game/` in the source repository so it does not register a command in a shipped build. It executes selected real initialization/finish statements and inspects the actual dinner-menu AST. It is a targeted smoke test, not a substitute for playing all branches.

## Creative approvals and unresolved work

**No major creative event change is proposed in this PR.** The small Love balcony expansion is the only added dialogue beat; it preserves the existing action and timing. Review it for voice along with the other prose edits.

Potential future major work—longer Day 3 relationship scenes, changes to route convergence, or changed consequences—needs a separate concrete proposal against approved canon. It has not been implemented here. The complete scene-by-scene prose pass, interactive continuity testing and remaining competitor reception gaps are unfinished. Research access limits and confidence are documented in `RESEARCH.md`; no inaccessible F95 material or unplayed game is presented as firsthand evidence.
