# Build Handoff — current state

This file records what is true in the repository **now**. When code and any older note disagree, the code wins; fix the note.

- **Baseline:** `main` @ `5b076bd` (18 Oct 2026). This document was written on a branch cut from that commit.
- **Superseded references:** `a309487` (old head of `feature/ch01-scenes-14-30`) and `c4e54dd` (audit baseline quoted by older design notes) are **stale**. Both are ancestors of `main` and predate the Day Three work. Do not use them as a baseline.
- **Tested with:** Ren'Py 8.5.3 (`lint` plus headless playthroughs from the Prologue through Day Two, Day Three and the Day Four stub).

## Build state

| Area | State |
|---|---|
| Prologue | Implemented |
| Chapter 1 Day One | Implemented |
| Chapter 1 Day Two | Implemented end to end; five end states reachable |
| Chapter 1 Day Three | First-pass script, **linked** from Day Two; headless-tested for every lane |
| Day Four | **Placeholder stub only** (`ch01_day4_stub.rpy`); no canon yet |
| Gallery | Architecture exists; story-to-gallery mapping is not decided |
| `zz...` cleanup | Paused except where a late override directly conflicts with runtime |

## Day Two end states

`ch01_d2_end_route` stores one of: `love`, `exhibitionism`, `love_repaired`, `mixed_unresolved`, `ntr_confirmed`.

| End state | How it is reached |
|---|---|
| `love` | Love lane bedroom (curtains drawn), or a Love lane with enough shared openness that gets the open-curtain bedroom variant but stays `love` |
| `exhibitionism` | Exhibitionism lane bedroom (curtains open, consensual roleplay), or the NTR-lane pool-suspicion bed choice "It bothered me... and I haven't stopped thinking about it" |
| `love_repaired` | NTR soft gate ("I'm fine." at sunset) plus the dinner wink, then honesty at the final hard gate |
| `mixed_unresolved` | NTR lane with pool suspicion but no soft gate, and the accusatory bed choice |
| `ntr_confirmed` | NTR soft gate plus dinner wink, then accusation or a second "I'm fine." at the hard gate |

Day Three is written to start from the stored `ch01_d2_end_route`.

## Day Two -> Day Three -> Day Four stub

Flow: `ch01_day2_scene_30_finish` (card "CHAPTER ONE — DAY TWO COMPLETE") -> `jump ch01_day3_start` -> Day Three -> `ch01_day3_bedroom` (card "CHAPTER ONE — DAY THREE COMPLETE") -> `jump ch01_day4_start` -> placeholder end card -> `return` (ends the game / back to the main menu). This mirrors the Day One -> Day Two pattern (completion card, `jump`, new day sets its `_started` flag and shows its own title card). There is no day counter or save-point logic in the project; progress is tracked only by story flags (`ch01_day_0N_started` / `ch01_day_0N_complete`; Day Three now sets both, plus the older `ch01_d3_complete`).

- Day Three keys off the stored `ch01_d2_end_route` and Day Two state, which the link does not touch. The Black Cutout Mini is owned by this point in a normal playthrough (Ryan or Leia bought it in the boutique).
- Day Three file: `game/chapters/ch01/ch01_day3_scenes.rpy` (owned by the Scriptwriter). The link only added the title/completion cards, the `ch01_day_03_*` flags and the final `jump`; story text is unchanged.
- Anything that calls Day Two (`call ch01_day2_start` etc.) now runs on through Day Three into the Day Four stub before returning. QA harnesses that want a Day Two-only run should stop at `ch01_day3_start` (the harness uses a `config.label_overrides` entry for this).

### Replacing the Day Four stub

`game/chapters/ch01/ch01_day4_stub.rpy` only shows "End of the current build. Day Four continues in the next update." and returns. It is a placeholder, not story content. To replace it with the Scriptwriter's approved Day Four script: add the real entry label (keep the name `ch01_day4_start`, or change the final `jump` in `ch01_day3_bedroom`), start it with a title card and a `ch01_day_04_started` flag as Day Two/Three do, and delete the stub file.

## Assets

- **DinnerSpill:** `CH1D1_CG_DinnerSpill_01` to `_04` all exist and are wired in `ch01_scenes_07_13_visuals.rpy` as `cg ch01_dinner_spill_01..04`: 01 impact / liquid airborne, 02 wet aftermath, 03 Leia follows his glance, 04 her second glance. The older id `ch01_dinner_spill` remains as an alias of `_01` for old saves.
- **TowelDidHeSee:** `CH1D1_CG_TowelDidHeSee_01` exists and is registered as `cg ch01_towel_did_he_see`; it is shown at the start of `ch01_scene_07_did_he_see`. The Towel realization CG is not repeated there.
- **Dinner stranger rig:** `Base/Penis_Casual_Dry`, `Base/Penis_Casual_Wet` and a shared `Chest_Casual` share one 941x1672 canvas and are registered as `stranger_casual_dry` and `stranger_casual_wet`. Staging is dry approach from the left, then the collision CG sequence, then wet stranger dialogue, then exit left. The later corridor compliment man is a different person with his own `passerby` speaker and must not reuse these images.
- **Day Two CGs are all placeholders.** Day Two story CGs resolve to `Composite` placeholder images in `ch01_day2_visuals.rpy`, including the **12 finale CGs**: `ch01_d2_love_pool_oral_01/02`, `ch01_d2_love_bedroom_01/02`, `ch01_d2_exhib_bed_open_01..04`, `ch01_d2_ntr_dream_strangers`, `..._julian_pool`, `..._nhie`, `..._wrong_room`. The other Day Two placeholders are the Leia+Maya photo, pool-top accident, dinner reach, Julian underwear reveal, the five boutique CGs and the general Day Two backgrounds.

## Black Cutout Mini

Boutique outfit `boutique_cutout_mini` (cost 280). If Ryan buys it in the Shop, that stands (`ch01_d2_mall_outfit_source == "ryan"`). In every other case, including Ryan declining, being unable to pay, or being absent, Leia buys it herself (`"leia"`). Either way Leia owns it before Day Three. It is reserved for Day Three and is never offered or worn at the Day Two dinner. The Shop only offers it once the boutique scene opens it (`shop_story_flag`).

## Known open items

1. Test Day Two Scenes 19-30 from a fresh save on each route (headless traces of all five end states pass; see below).
2. Replace the 12 finale placeholder CGs and the other Day Two placeholders.
3. Run the unchecked QA & Release checklist (Notion page 08).
4. Decide Gallery mapping for finalized CGs.
5. ~~Link Day Three after Day Two QA.~~ Done: Day Two -> Day Three -> Day Four stub (see above). Remaining: replace the stub with the approved Day Four script.
6. ~~Phone Shop could sell the Black Cutout Mini at any time.~~ Fixed: the outfit carries `shop_story_flag: ch01_d2_boutique_shop_open`, set by the boutique scene just before it opens the Shop for Ryan. Until then the Shop (phone app and full screen) neither lists nor sells it; once owned it is listed as owned.
7. ~~Four Day Two choice ids registered but never used (`ch01_d2_game_reassure`, `ch01_d2_game_tease`, `ch01_d2_game_ignore`, `ch01_d2_sunset_tease`).~~ Removed: Notion canon (05, 07, 07C) has no player menu in the sunset payoff or the Never Have I Ever scenes (25-28) for them to carry; the only sunset menu is connect / partial / ignore_gate. Nothing read them.
8. ~~`mixed_unresolved` did not set `ch01_d2_bedroom_variant`.~~ Fixed: it now sets `pool_suspicion_unresolved` (no bedroom payoff scene plays on that path). Nothing reads the value; Day Three keys off `ch01_d2_end_route`.

## QA notes

- `lint` (Ren'Py 8.5.3) leaves only pre-existing, non-blocking items: `scene white` in Day One scenes 04-06, unused legacy aliases in `zz_ch01_phone_photo_aliases.rpy`, init priorities above 999 in a few late patch files, and a `hide julian` without a prior show in `zzzz_ch01_scene27_staged_phone.rpy`.
- Always test with a fresh save when label or choice logic changed.

## Before starting a coding session

- Fetch `main`, branch from it, and confirm the head.
- Find the **effective** runtime owner of what you change (late `zz...` overrides replace earlier labels and screens).
- Do not resume broad `zz...` cleanup unless explicitly requested.
- Do not edit `ch01_day3_scenes.rpy` or add or replace CG art outside the owners' workflows.
