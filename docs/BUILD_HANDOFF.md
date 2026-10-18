# Build Handoff — current state

This file records what is true in the repository **now**. When code and any older note disagree, the code wins; fix the note.

- **Baseline:** `main` @ `5b076bd` (18 Oct 2026). This document was written on a branch cut from that commit.
- **Superseded references:** `a309487` (old head of `feature/ch01-scenes-14-30`) and `c4e54dd` (audit baseline quoted by older design notes) are **stale**. Both are ancestors of `main` and predate the Day Three work. Do not use them as a baseline.
- **Tested with:** Ren'Py 8.5.3 (`lint` plus headless playthroughs from the Prologue through Day Two, Day Three, Day Four and Day Five to the temporary end card).

## Build state

| Area | State |
|---|---|
| Prologue | Implemented |
| Chapter 1 Day One | Implemented |
| Chapter 1 Day Two | Implemented end to end; five end states reachable |
| Chapter 1 Day Three | First-pass script, **linked** from Day Two; headless-tested for every lane |
| Chapter 1 Day Four | First-pass script "Recalibration" (`ch01_day4_scenes_01_08.rpy`, `ch01_day4_scenes_09_16.rpy`), **linked** from Day Three; five end routes reachable; all CGs/backgrounds are placeholders |
| Chapter 1 Day Five | First-pass script "The Water" (`ch01_day5_scenes_01_08.rpy`, `ch01_day5_scenes_09_16.rpy`), **linked** from Day Four; five end routes reachable; all CGs/backgrounds are placeholders |
| Day Six | **Not built.** Day Five ends on a temporary end card until `ch01_day6_start` exists |
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

## Day Two -> Day Three -> Day Four

Flow: `ch01_day2_scene_30_finish` (card "CHAPTER ONE — DAY TWO COMPLETE") -> `jump ch01_day3_start` -> Day Three -> `ch01_day3_bedroom` (card "CHAPTER ONE — DAY THREE COMPLETE") -> `jump ch01_day4_start` -> Day Four (title card, `ch01_day_04_started`) -> `ch01_day4_scene_16_finish` -> temporary end card -> `return` (ends the game / back to the main menu). This mirrors the Day One -> Day Two pattern (completion card, `jump`, new day sets its `_started` flag and shows its own title card). There is no day counter or save-point logic in the project; progress is tracked only by story flags (`ch01_day_0N_started` / `ch01_day_0N_complete`; Day Three now sets both, plus the older `ch01_d3_complete`; Day Four sets `ch01_day_04_started` and `ch01_day_04_complete`).

- Day Three keys off the stored `ch01_d2_end_route` and Day Two state, which the link does not touch. The Black Cutout Mini is owned by this point in a normal playthrough (Ryan or Leia bought it in the boutique).
- Day Three file: `game/chapters/ch01/ch01_day3_scenes.rpy` (owned by the Scriptwriter). The link only added the title/completion cards, the `ch01_day_03_*` flags and the final `jump`; story text is unchanged.
- Anything that calls Day Two (`call ch01_day2_start` etc.) now runs on through Day Three and Day Four before returning. QA harnesses that want a Day Two-only run should stop at `ch01_day3_start` (the harness uses a `config.label_overrides` entry for this).

### Day Four now replaces the stub

`ch01_day4_stub.rpy` is deleted. Day Four is the Scriptwriter's first-pass script and is owned by the Scriptwriter (do not edit story text without coordination).

- **Files** (`game/chapters/ch01/`): `ch01_day4_scenes_01_08.rpy` (entry `ch01_day4_start`, scenes 1-8), `ch01_day4_scenes_09_16.rpy` (scenes 9-16, end routes), `ch01_day4_choice_registration.rpy` (50 choice ids in `CHOICE_EFFECTS` / `CHOICE_TAGS`, helpers at `init 2`), `ch01_day4_visuals.rpy` (placeholder images).
- **Reads (never recomputes):** `ch01_d3_lane` (copied to `ch01_d4_lane`), `ch01_d3_end_variant`, `ch01_d2_end_route`, `ch01_d2_mall_outfit_source`, `ch01_d3_ntr_repair_effort`, `ch01_d3_maya_dessert`, `ch01_dream_response`, flag `ch01_d3_cutout_secret`. If the Day 3 keys are absent (dev skip), the lane is derived from `ch01_d2_end_route`.
- **Flags:** `ch01_day_04_started`, `ch01_day_04_complete`, `ch01_d4_scene_01_complete` .. `ch01_d4_scene_16_complete` (a scene flag is set when each scene ends), and the branch flags `ch01_d4_club_story_deferred`, `ch01_d4_cutout_disclosed`, `ch01_d4_cutout_partial`, `ch01_d4_exhib_brief_done`, `ch01_d4_exhib_ryan_likes_watching`, `ch01_d4_exhib_tease_done`, `ch01_d4_love_exhib_seed`, `ch01_d4_love_mini_thanks`, `ch01_d4_love_strained`, `ch01_d4_market_honey_bee_callback`, `ch01_d4_maya_real_talk`, `ch01_d4_ntr_boundary_set`, `ch01_d4_ntr_pressed_early`, `ch01_d4_ntr_repaired_curious`, `ch01_d4_ntr_soft_gate`, `ch01_d4_photo_candid_taken`, `ch01_d4_photo_pose_taken`, `ch01_d4_photo_skipped`, `ch01_d4_photo_swap_taken`.
- **End route:** `ch01_d4_end_route` (Day Five must read this and never recompute it) stores one of `love`, `exhibitionism`, `love_repaired`, `ntr_unresolved`, `ntr_confirmed`. `ch01_d4_end_variant` records the sub-variant (`love_slow_dance`, `love_terrace_talk`, `love_open_door`, `exhib_shared_step`, `exhib_ryan_likes_watching`, `exhib_private_optout` (route becomes `love`), `ntr_repaired_thanks` / `_boundary` / `_curious`, `ntr_unresolved`, `ntr_confirmed`). Other values Day Five may use: `ch01_d4_exposure_step` (`none` / `covered_tease` / `brief_reveal`), `ch01_d4_ntr_outcome`, `ch01_d4_ntr_fine_count`, `ch01_d4_photo_style`, `ch01_d4_hook_reply`.
- **Placeholder art (all `Composite` text cards in `ch01_day4_visuals.rpy`, final art replaces the same names):**
  - Backgrounds: `bg ch01_d4_breakfast_terrace`, `bg ch01_d4_market`, `bg ch01_d4_harbor_wall`, `bg ch01_d4_dinner_terrace`, `bg ch01_d4_dusk_path`, `bg ch01_d4_terrace_night`.
  - CGs: `cg ch01_d4_photo_candid`, `cg ch01_d4_photo_pose`, `cg ch01_d4_photo_swap`, `cg ch01_d4_photo_maya_julian`, `cg ch01_d4_love_night_01`, `cg ch01_d4_love_night_02`, `cg ch01_d4_exhib_terrace_01`, `cg ch01_d4_exhib_terrace_02`, `cg ch01_d4_exhib_watching`, `cg ch01_d4_ntr_terrace_talk`.
  - Phone attachment aliases (`ImageReference`): `ch01_d4_photo_candid`, `ch01_d4_photo_pose`, `ch01_d4_photo_maya_julian`.
  - The CG brief for the artist is the Scriptwriter's `07_cg_checklist.md` (Ryan's point of view only; Ryan is never drawn).
- **Day Five** follows: `ch01_day4_scene_16_finish` runs `if renpy.has_label("ch01_day5_start"): jump expression "ch01_day5_start"`, so the temporary Day Four end card is now only reached if Day Five is missing. Since Day Five now exists, the guard may be replaced with a literal `jump ch01_day5_start`.
- Day Four does not change Day Two/Three scripts or any system file. It never calls `purchase_outfit` and never opens the Shop.

### Day Five

`ch01_day5_scenes_01_08.rpy` (entry `ch01_day5_start`, scenes 1-8), `ch01_day5_scenes_09_16.rpy` (scenes 9-16, end routes), `ch01_day5_choice_registration.rpy` (71 choice ids, helpers at `init 2`), `ch01_day5_visuals.rpy` (placeholders). Day Five is the Scriptwriter's first-pass script ("The Water": Julian's family boat, a private cove, no signal). It adds one character, `skipper` ("Captain Ilario"); do not define it twice.

- **Reads (never recomputes):** `ch01_d4_end_route` (the only route input; mapped to a track `love` / `exhibitionism` / `ntr_repaired` / `ntr_unresolved` / `ntr_confirmed`), plus `ch01_d4_lane`, `ch01_d4_hook_reply`, `ch01_d4_exposure_step`, `ch01_d4_exhib_variant`, `ch01_d4_photo_style`, `ch01_d4_end_variant`, `ch01_d4_dusk_outfit_id`, `ch01_d4_ntr_react`, flags `ch01_d4_love_exhib_seed`, `ch01_d4_exhib_ryan_likes_watching`, `ch01_d4_cutout_disclosed`, `ch01_d4_club_story_deferred`, and Day 2/3 `ch01_d2_mall_outfit_source`, `ch01_d2_pool_outfit`. If `ch01_d4_end_route` is absent (dev skip) it falls back from the stored lane.
- **Flags:** `ch01_day_05_started`, `ch01_day_05_complete`, `ch01_d5_scene_01_complete` .. `ch01_d5_scene_16_complete`, and the branch flags `ch01_d5_bee_rescued`, `ch01_d5_clip_rescued_by_julian`, `ch01_d5_clip_rescued_by_ryan`, `ch01_d5_club_disclosed`, `ch01_d5_dare_offered`, `ch01_d5_eaves_announced`, `ch01_d5_eaves_listened`, `ch01_d5_exhib_comfortable_done`, `ch01_d5_exhib_ryan_likes_watching`, `ch01_d5_exhib_tease_done`, `ch01_d5_julian_looked_after`, `ch01_d5_julian_thanked`, `ch01_d5_love_cove_done`, `ch01_d5_love_strained`, `ch01_d5_maya_confided_early`, `ch01_d5_ntr_boundary_set`, `ch01_d5_ntr_curious`, `ch01_d5_ntr_pressed`, `ch01_d5_ntr_reopened`, `ch01_d5_ntr_repaired_by_disclosure`, `ch01_d5_overheard_club`, `ch01_d5_pass_signal`, `ch01_d5_phone_in_bag`, `ch01_d5_privacy_breach`, `ch01_d5_rope_bracelets`, `ch01_d5_wardrobe_friction`.
- **End route:** `ch01_d5_end_route` (Day Six must read this and never recompute it) stores one of `love`, `exhibitionism`, `love_repaired`, `ntr_unresolved`, `ntr_confirmed`. `ch01_d5_end_variant` records the sub-variant (`love_bracelets`, `exhib_shared_step`, `exhib_ryan_likes_watching`, `exhib_private_optout` (route becomes `love`), `ntr_repaired_thanks` / `_boundary` / `_curious`, `ntr_unresolved`, `ntr_unresolved_reopened`, `ntr_confirmed`). Also stored for Day Six: `ch01_d5_exposure_step` (`none` / `ties_loosened` / `comfortable`), `ch01_d5_leia_call`, `ch01_d5_secret_traded`, `ch01_d5_photo_group`, `ch01_d5_private_photo`, `ch01_d5_ntr_react`, `ch01_d5_ntr_outcome`, `ch01_d5_bunk`, `ch01_d5_invite_reply`.
- **Placeholder art (all `Composite` text cards in `ch01_day5_visuals.rpy`, final art replaces the same names):**
  - Backgrounds (12): `bg ch01_d5_pier_morning`, `bg ch01_d5_boat_deck`, `bg ch01_d5_boat_foredeck`, `bg ch01_d5_boat_stern`, `bg ch01_d5_reef_surface`, `bg ch01_d5_cove_beach`, `bg ch01_d5_cove_rock`, `bg ch01_d5_boat_sunset`, `bg ch01_d5_galley`, `bg ch01_d5_boat_cabin`, `bg ch01_d5_boat_deck_night`, `bg ch01_d5_dawn_pier`.
  - CGs (16): `cg ch01_d5_snorkel_surface`, `cg ch01_d5_cove_lunch_bee`, `cg ch01_d5_photo_three`, `cg ch01_d5_love_cove_swim`, `cg ch01_d5_love_cove_secret`, `cg ch01_d5_exhib_cove_01`, `cg ch01_d5_exhib_cove_02`, `cg ch01_d5_exhib_cove_watching`, `cg ch01_d5_ntr_cove_talk`, `cg ch01_d5_ntr_deck_alone`, `cg ch01_d5_sunset_deck`, `cg ch01_d5_love_night_01`, `cg ch01_d5_exhib_night_01`, `cg ch01_d5_ntr_night_01`, `cg ch01_d5_photo_private`, `cg ch01_d5_invitation`.
  - Phone attachment aliases (`ImageReference`): `ch01_d5_photo_three`, `ch01_d5_photo_love_cove`, `ch01_d5_photo_private`.
- **Day Six is not built.** `ch01_day5_scene_16_finish` ends with `if renpy.has_label("ch01_day6_start"): jump expression "ch01_day6_start"`, otherwise the temporary "Current development build ends here" card and `return`. When Day Six lands (entry label exactly `ch01_day6_start`), replace that block with a literal `jump ch01_day6_start`.
- Day Five does not change Day Two/Three/Four scripts (apart from one narration wording tweak in Day Four scene 13) or any system file; it never calls `purchase_outfit` and never opens the Shop.

## Chapter Select (skip to Day 2 / Day 3 / Day 4 / Day 5)

- Files: `game/systems/chapter_select.rpy` (rule, presets, `chapter_select_apply`, entry label `ch01_chapter_select_entry`), `game/screens/chapter_select_screen.rpy`, a "Chapter Select" button in `navigation` (`screens.rpy`, main menu only), and two persistent defaults in `defaults.rpy`.
- It starts a **new game** with a preset of the earlier state, then jumps to the normal entry label (`ch01_day2_start`, `ch01_day3_start`, `ch01_day4_start` or `ch01_day5_start`). No story scene was changed. Day 3/4 presets store each of the five Day Two end states consistently (end route, lane values, soft gate / wink / confirmed flags, bedroom variant, Black Cutout Mini owned with source `leia`, Day One/Two complete flags, phone unlocked). Day 2 presets only seed a lane (stats, Day One pressure, one history id); the real lane still follows the choices made.
- **Unlock rule:** `define CHAPTER_SELECT_RULE` at the top of `chapter_select.rpy`. Values: `"always"`, `"developer"` (`config.developer`), `"unlocked"` (`persistent.ch01_chapter_select_unlocked`), `"developer_or_unlocked"` (default), `"never"`. The persistent flag is set the first time `ch01_day_02_complete` is set (a wrapper around `set_story_flag`, so the Day 2 scene file is untouched). Flip the rule to change who sees the button.
- When you change what a day reads, update the preset table in the same file. The preset marks the save with `chapter_select_used` / `chapter_select_preset`.
- The Day Four preset also stores what `ch01_day4_start` reads from Day Three: `ch01_d3_lane`, `ch01_d3_end_variant`, and for the NTR lane `ch01_d3_ntr_repair_effort` (`enjoy`, Day Three's default), `ch01_d3_maya_dessert` (`chocolate`) and the flag `ch01_d3_cutout_secret`. Day Four then derives everything else itself; it enters with the Black Cutout Mini and the resort dinner dress owned (not `d2_loose_low_cut`) and handles that.
- The **Day Five** preset is keyed by the five Day Four end routes (`love`, `exhibitionism`, `love_repaired`, `ntr_unresolved`, `ntr_confirmed`). It seeds the Day Two/Three state of the lane that leads there (Day Two end `love`, `exhibitionism`, `ntr_confirmed` for `love_repaired` and `ntr_confirmed`, `mixed_unresolved` for `ntr_unresolved`), then the Day Four state `ch01_day5_start` reads: `ch01_d4_end_route`, `ch01_d4_lane`, `ch01_d4_end_variant`, `ch01_d4_exposure_step`, `ch01_d4_exhib_variant`, `ch01_d4_photo_style`, dusk/day outfit ids and sources, `ch01_d4_hook_reply`, `ch01_d4_ntr_react`, `ch01_d4_disclosure_when`, plus matching `ch01_d4_*` flags and stats, and `ch01_d2_pool_outfit=pool_conservative`. The choices recorded are a typical playthrough of each route (the table `CH01_SELECT_DAY5_PRESETS` in `chapter_select.rpy`): Love = slow dance, candid photo, dinner dress; Exhibition = shared step, `brief_reveal`, posed photo, Black Cutout Mini at dusk, Exhibitionism 38; Love (repaired) = disclosed at the harbor wall, reacted `thanks`; NTR unresolved = accused at the night gate; NTR confirmed = three "I'm fine." picks.
- Names are not asked (defaults Ryan / Leia / Julian); use Start for the full flow.

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
5. ~~Link Day Three after Day Two QA.~~ Done: Day Two -> Day Three -> Day Four (see above). Day Five is linked too. Remaining: Day Six (`ch01_day6_start`) and replacing the Day Four and Day Five placeholder CGs/backgrounds.
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
