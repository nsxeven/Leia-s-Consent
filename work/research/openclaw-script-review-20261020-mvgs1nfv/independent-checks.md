# Independent checks on the prologue notes

The OpenClaw critique is a draft, not a verified review. Direct source inspection found:
- prologue.rpy has 406 physical lines, NOT 418. Its claimed coverage 1-418 and several approximate scene ranges are inaccurate.
- Name setup: 5-24. Flashback label begins at 27; FOUR YEARS AGO appears at 33.
- First-impression choices: approximately 90-112. Ryan explicitly makes room for Leia's voice at 115-128. This should temper any blanket claim that he never acts.
- Kitchen beat: approximately 130-183; the easy silence is at 151, and the party calls them back at 170.
- Truth or Dare begins around 188. Julian's dare is at 235. Leia initiates the kiss at 265; the room cheers at 267. Consent/agency critique should inspect the surrounding actual dialogue rather than infer coercion from one phrase.
- Present-day transition at 285; packing begins 294. Phone notifications occur at 313-330, and dialogue establishes Julian downstairs at 340-343. A proposal that Julian speaks face-to-face before departure would add staging, not repair an established missing technical feature.
- Departure choices: 351-377. Transition to chapter one: 393-406.
- No mother/sister/ownership-contract plot from the earlier bot hallucination belongs in this report.

Use these corrected ranges for synthesis. Do not reproduce inaccurate original coverage claims. Treat narrative interpretations as editorial opinions, not verified defects. README's later-day status is documentation evidence only until those files are actually inspected.

## Corrections to structure-notes.md
- ch01_main.rpy has 323 physical lines, not 130. A claimed 1-130 read does not cover scenes 1-3; scene 3 begins at 146. Do not repeat that false coverage.
- Scene 1 begins at 12; scene 2 at 64; scene 3 at 146. Outfit branches set values at 181-213 and converge at 222. The curtain CG and action at 245-253 are in the common flow after the branches. There is no demonstrated missing curtain trigger in the inspected source; remove that bug claim.
- ch01_day2_start already exists at line 267 of game/chapters/ch01/ch01_day2_scenes_01_15.rpy. Day 3-5 entry labels are documented in README. Do not propose adding labels on the false premise they are missing.
- ch01_scene_01_complete at 58 records one scene; ch01_scenes_01_03_complete at 320 records three scenes, not all of Day 1. Their redundancy has not been established. Do not recommend deleting/consolidating them without checking consumers.
- The full repository usage of ch01_outfit_stance was not inspected, so it cannot be called unused or inconsistently used.
- Helper definitions in defaults.rpy were not inspected. Do not assert it defines set_story_value/get_story_value.
- These are reasons to use a continuity/choice audit as a planned follow-up, not evidence of confirmed bugs. Omit unsupported technical repair recommendations from the final plan.

## Corrections to external-notes.md
- The 8 WEEKS creator reports 58 sequences TOTAL across three routes: 19, 20, and 19. The draft's "50+ per route" claim is false. Remove it.
- There is no evidence-based quota of 15-25 sequences for Leia's Consent. Remove that invented production recommendation. Scope art to available time and current placeholder workload.
- Player impact statements are design hypotheses, not measured player feedback or consensus. Label them accordingly.
- Ink's landing page supports text-first authoring and preview tooling; it does not establish that migrating this existing RenPy game would help. Do not recommend a new engine/toolchain or assert detailed Ink behavior not covered by the fetched excerpt.
- The Hard Choice source URL now redirects to the renamed 8 WEEKS page at https://fromplutoguy.itch.io/8-weeks/devlog/1659294/day-20-three-routes-one-very-long-day . Cite the current title. Transfer only non-graphic lessons about distinct emotional rhythms and budgeting route scope.

## Tool-record coverage correction
The exported prologue session proves successful reads of lines 1-100, 101-200, 201-300 and 301-400 only. The file actually ends at 406. Thus OpenClaw did NOT itself read through EOF; its original complete-read claim is false. Independent direct inspection covered the final transition at 401-406. Attribute that tail check to Codex and report model coverage as 1-400, not a full source read. This distinction must remain explicit in the final report.
