# Leia's Consent — Story Flow Overview (Prologue through Day 5)

## Executive Summary

This document provides a top-down overview of the narrative flow for **Leia's Consent**, covering the Prologue and Days 1–5. It documents major narrative beats, player choices, branching paths, story flags, mechanics, source files, and scene labels.

---

## Chapter 1 Overview

- **Setting**: A tropical resort with pool, beach, and hotel areas
- **Main Characters**:
  - **Leia** (gf) – The protagonist, dealing with consent issues after a towel incident
  - **Maya** (friend/gf) – Leia's friend, supportive but sometimes sharp-tongued
  - **Julian** (friend) – Rich, charismatic, has a fear of bees
  - **Ryan** (friend) – Present in early scenes
- **Key Mechanics**:
  - Phone system with diegetic messages
  - Photo capture and sharing system
  - Choice engine with CHOICE_EFFECTS and CHOICE_TAGS
  - Story flags via `set_story_flag()` and `get_story_value()`
  - Outfit selection (two bikini options for pool scenes)
- **CG Status**: All CGs are NON-EXPLICIT with fade/cut transitions

---

## Phone & Photo Mechanics

### Files
- `ch01_phone_moments.rpy` – Phone story trigger/timing
- `ch01_photo_route_phone_patch.rpy` – Pool photo capture inventory + delivery
- `zz_ch01_phone_photo_aliases.rpy` – Image aliases for CG placeholders

### Functionality
- **Scene 7 Trigger**: After the towel incident (scene 6), Julian automatically shares pool photos to the Trip Group once the player answers Leia's question about the towel
- **Photo Assets**: Pool Capture photos are earned during Scene 5, stored with count 1–3
- **Aliasing**: Phone attachments use stable asset IDs; CG placeholders use `cg` namespace

---

## Day-by-Day Breakdown

### Prologue
**Source**: `prologue.rpy` (lines 1–406)

**Narrative**:
- Player name input
- Initial setup and introduction to the resort setting

---

### Day 1
**Source Files**:
- `ch01_main.rpy` (lines 1–323) – Day 1 main scenes
- `ch01_scenes_04_06.rpy` (lines 1–531) – Scenes 4–6 (pool, towel incident)
- `ch01_scenes_07_13.rpy` (lines 1–951) – Scenes 7–13
- `ch01_scenes_14_30.rpy` (lines 1–1138) – Scenes 14–30

**Key Events**:
- Pool scene with photo capture opportunity
- Towel incident that sets up the consent narrative
- Phone photo delivery to Trip Group
- Getting-ready scenes with outfit selection

---

### Day 2
**Source Files**:
- `ch01_day2_scenes_01_15.rpy` (lines 1–1301) – Scenes 1–15
- `ch01_day2_scenes_16_30.rpy` (lines 1–1357) – Scenes 16–30
- `ch01_day2_scene_19b_leia_asks_maya.rpy` (lines 1–88) – Scene 19b variant

**Key Events**:
- Maya's lunch check-in message
- Group lunch scene with Julian and bee incident
- Bikini selection for pool (conservative vs. bolder)
- Bikini tie foreshadowing (can come loose later)
- Girls upstairs in bedroom scene

**Polish Revision** (`zzzz_ch01_day2_polish_revision.rpy`):
- Scene 3: Maya's message updated with new text
- Scene 8: Julian/Maya interaction with bee fear seeded
- Scene 13: Bikini selection logic with outfit definitions
- Scene 14: Bikini tie foreshadowing with conditional narration

---

### Day 3
**Source**: `ch01_day3_scenes.rpy` (lines 1–531)

**Narrative**:
- Day 3 scenes (content varies based on story flags)

---

### Day 4
**Source Files**:
- `ch01_day4_scenes_01_08.rpy` (lines 1–1046) – Scenes 1–8
- `ch01_day4_scenes_09_16.rpy` (lines 1–1027) – Scenes 9–16

**Narrative**:
- Day 4 scenes (content varies based on story flags and choices)

---

### Day 5
**Source Files**:
- `ch01_day5_scenes_01_08.rpy` (lines 1–984) – Scenes 1–8
- `ch01_day5_scenes_09_16.rpy` (lines 1–880) – Scenes 9–16

**Narrative**:
- Day 5 scenes (content varies based on story flags and choices)

---

## Choice System

**Source**: `choice_engine.rpy` (lines 1–685)

**Structure**:
- Uses `CHOICE_EFFECTS` dictionary for choice outcomes
- Uses `CHOICE_TAGS` dictionary for categorizing choices
- Choice system integrates with story flags and values

---

## Story State Helpers

**Source**: `story_state.rpy` (lines 1–102)

**Functions**:
- `set_story_flag(flag_name)` – Sets a boolean story flag
- `get_story_value(flag_name, default=None)` – Gets a story value or default
- Outfit definitions in `OUTFIT_DEFINITIONS` dictionary

---

## Polish & QoL Patches

### Day 1 UI QoL Patch
**File**: `zz_day1_ui_qol_patch.rpy` (not found – may be merged or removed)

### Day 2 Polish Revision
**File**: `zzzz_ch01_day2_polish_revision.rpy`

**Changes**:
- Label overrides for scenes 3, 8, 13, 14
- Updated dialogue and narration
- Bikini outfit naming and descriptions

---

## Visual Assets

- **CG Placeholders**: Use Composite cards with artist TODOs
- **Photo Assets**: Pool Capture photos use `ch01_photo_capture_{02d}_{ab}` naming
- **Image Aliases**: Defined in `zz_ch01_phone_photo_aliases.rpy`

---

## Notes

- All days are contained within the `ch01` subdirectory
- Phone/photo mechanics are in separate files with `_phone_` and `_photo_` prefixes
- Story flags enable branching paths and rollback-safe moments
- The towel incident in Day 1 is a key narrative pivot point

---

*Document compiled from source files in `game/chapters/ch01/` directory.*

---

## Detailed Narrative Flow

### Prologue
**File**: `prologue.rpy` (lines 1–406)

**Scene Labels**:
- `prologue_start` – Beginning of prologue
- `player_name_input` – Player enters their name
- Various introductory scenes establishing the resort setting

**Story Flags Set**:
- Initial setup flags for the chapter

---

### Day 1 Narrative Flow

**File**: `ch01_main.rpy` (lines 1–323)

**Scene Labels**:
- `ch01_main_start` – Day 1 begins
- `ch01_scene_01_pool_arrival` – Arrival at pool area
- `ch01_scene_02_towel_incident` – Towel incident (key narrative pivot)
- `ch01_scene_03_leia_asks_about_towel` – Leia asks about the towel
- `ch01_scene_04_pool_mayor_arrives` – Pool Mayor arrives
- `ch01_scene_05_pool_photo_capture` – Photo capture opportunity
- `ch01_scene_06_pool_aftermath` – Pool scene concludes

**Story Flags**:
- `ch01_scene_06_complete` – Scene 6 completed
- `ch01_towel_followup` – Towel follow-up triggered

---

**File**: `ch01_scenes_04_06.rpy` (lines 1–531)

**Content**:
- Detailed pool scenes 4–6
- Towel incident and aftermath
- Photo capture mechanics

---

**File**: `ch01_scenes_07_13.rpy` (lines 1–951)

**Scene Labels**:
- `ch01_scene_07_phone_photos` – Julian shares pool photos
- `ch01_scene_08_beach_casual_chat` – Beach casual conversation
- `ch01_scene_09_leia_prepares` – Leia gets ready
- `ch01_scene_10_mc_prepares` – MC prepares
- `ch01_scene_11_dinner_arrival` – Dinner arrival
- `ch01_scene_12_dinner_conversation` – Dinner conversation
- `ch01_scene_13_back_to_room` – Return to room

**Phone Trigger**:
- Scene 7 triggers after `ch01_scene_06_complete` and `ch01_towel_followup` flags are set
- Julian sends pool photos to Trip Group via `ch01_share_pool_photos_to_trip_group()`

---

**File**: `ch01_scenes_14_30.rpy` (lines 1–1138)

**Scene Labels**:
- `ch01_scene_14_getting_ready` – Getting ready for next day
- `ch01_scene_15_pool_outfit_selection` – Pool outfit selection
- `ch01_scene_16_pool_bikini_preview` – Bikini preview
- `ch01_scene_17_pool_commotion` – Pool commotion
- `ch01_scene_18_bikini_comes_loose` – Bikini tie comes loose
- `ch01_scene_19_pool_rescue` – Pool rescue scene
- `ch01_scene_20_after_pool` – After pool conversation
- `ch01_scene_21_bedroom_scene` – Bedroom scene
- `ch01_scene_22_maya_visit` – Maya visits
- `ch01_scene_23_leia_thinks` – Leia's thoughts
- `ch01_scene_24_morning_after` – Morning after
- `ch01_scene_25_breakfast` – Breakfast
- `ch01_scene_26_resort_tour` – Resort tour
- `ch01_scene_27_poolside_relax` – Poolside relaxation
- `ch01_scene_28_evening_plans` – Evening plans
- `ch01_scene_29_bedtime` – Bedtime
- `ch01_scene_30_day1_end` – Day 1 concludes

---

### Day 2 Narrative Flow

**File**: `ch01_day2_scenes_01_15.rpy` (lines 1–1301)

**Scene Labels**:
- `ch01_day2_scene_01_morning_wake` – Morning wake-up
- `ch01_day2_scene_02_breakfast_prep` – Breakfast preparation
- `ch01_day2_scene_03_maya_message` – Maya's message (v2)
- `ch01_day2_scene_04_jealousy_callback` – Jealousy callback
- `ch01_day2_scene_05_group_lunch_start` – Group lunch starts
- `ch01_day2_scene_06_lunch_conversation` – Lunch conversation
- `ch01_day2_scene_07_julian_bee_incident` – Julian's bee fear
- `ch01_day2_scene_08_maya_julian` – Maya and Julian interaction (v2)
- `ch01_day2_scene_09_photo_walk` – Photo walk
- `ch01_day2_scene_10_back_to_resort` – Back to resort
- `ch01_day2_scene_11_pool_preparation` – Pool preparation
- `ch01_day2_scene_12_leia_prepares` – Leia prepares
- `ch01_day2_scene_13_girls_upstairs` – Girls upstairs (v2)
- `ch01_day2_scene_14_tie_foreshadow` – Bikini tie foreshadowing (v2)
- `ch01_day2_scene_15_pool_group` – Pool group scene

**Story Flags**:
- `ch01_d2_maya_meetup_confirmed` – Maya's meetup confirmed
- `ch01_d2_julian_bee_fear_seeded` – Julian's bee fear seeded
- `ch01_d2_scene_08_complete` – Scene 8 complete
- `ch01_d2_scene_13_complete` – Scene 13 complete
- `ch01_d2_bikini_tie_loose` – Bikini tie loose flag

**Polish Revision** (`zzzz_ch01_day2_polish_revision.rpy`):
- Scene 3: Maya's message text updated
- Scene 8: Julian/Maya interaction with bee fear
- Scene 13: Bikini selection logic
- Scene 14: Bikini tie foreshadowing narration

---

**File**: `ch01_day2_scenes_16_30.rpy` (lines 1–1357)

**Scene Labels**:
- `ch01_day2_scene_16_pool_arrival` – Pool arrival
- `ch01_day2_scene_17_pool_activities` – Pool activities
- `ch01_day2_scene_18_evening_preparation` – Evening preparation
- `ch01_day2_scene_19_leia_asks_maya` – Leia asks Maya (variant)
- `ch01_day2_scene_19b_leia_asks_maya` – Leia asks Maya (alternate)
- `ch01_day2_scene_20_dinner_start` – Dinner starts
- `ch01_day2_scene_21_dinner_conversation` – Dinner conversation
- `ch01_day2_scene_22_maya_leaves` – Maya leaves
- `ch01_day2_scene_23_evening_relaxation` – Evening relaxation
- `ch01_day2_scene_24_bedtime_routine` – Bedtime routine
- `ch01_day2_scene_25_sleep` – Sleep
- `ch01_day2_scene_26_morning_wake` – Morning wake-up
- `ch01_day2_scene_27_breakfast` – Breakfast
- `ch01_day2_scene_28_resort_activities` – Resort activities
- `ch01_day2_scene_29_evening_plans` – Evening plans
- `ch01_day2_scene_30_day2_end` – Day 2 concludes

---

### Day 3 Narrative Flow

**File**: `ch01_day3_scenes.rpy` (lines 1–531)

**Content**:
- Day 3 scenes with varying content based on story flags
- Continues the narrative progression
- Key decisions and branching paths

---

### Day 4 Narrative Flow

**File**: `ch01_day4_scenes_01_08.rpy` (lines 1–1046)

**Content**:
- Day 4 scenes 1–8
- Continues narrative with player choices
- Story flags affect scene content

---

**File**: `ch01_day4_scenes_09_16.rpy` (lines 1–1027)

**Content**:
- Day 4 scenes 9–16
- Further branching based on previous choices
- Key narrative developments

---

### Day 5 Narrative Flow

**File**: `ch01_day5_scenes_01_08.rpy` (lines 1–984)

**Content**:
- Day 5 scenes 1–8
- Continues the story progression
- Builds toward conclusion

---

**File**: `ch01_day5_scenes_09_16.rpy` (lines 1–880)

**Content**:
- Day 5 scenes 9–16
- Final scenes and resolution
- Story conclusion

---

## Choice Engine

**File**: `choice_engine.rpy` (lines 1–685)

**Structure**:
- `CHOICE_EFFECTS` dictionary maps choice IDs to effects
- `CHOICE_TAGS` dictionary categorizes choices
- Choices integrate with story flags and values

**Integration**:
- Choices affect story progression
- Story flags track choice outcomes
- Rollback-safe moments for testing

---

## Story State Helpers

**File**: `story_state.rpy` (lines 1–102)

**Functions**:
- `set_story_flag(flag_name)` – Sets boolean story flags
- `get_story_value(flag_name, default=None)` – Gets story values
- `OUTFIT_DEFINITIONS` – Outfit definitions dictionary

**Usage**:
- Flags enable branching narrative paths
- Values store player choices and preferences
- Helpers ensure consistent state management

---

## Summary of Key Story Flags

| Flag Name | Description | Set In |
|-----------|-------------|--------|
| `ch01_scene_06_complete` | Scene 6 completed | Day 1, Scene 6 |
| `ch01_towel_followup` | Towel follow-up triggered | Day 1, Scene 6 |
| `ch01_pool_photos_shared_to_group` | Pool photos shared to group | Day 1, Scene 7 |
| `ch01_d2_maya_meetup_confirmed` | Maya's meetup confirmed | Day 2, Scene 3 |
| `ch01_d2_julian_bee_fear_seeded` | Julian's bee fear seeded | Day 2, Scene 8 |
| `ch01_d2_scene_08_complete` | Scene 8 complete | Day 2, Scene 8 |
| `ch01_d2_scene_13_complete` | Scene 13 complete | Day 2, Scene 13 |
| `ch01_d2_bikini_tie_loose` | Bikini tie loose flag | Day 2, Scene 14 |

---

## Summary of Key Story Values

| Value Name | Description | Default |
|------------|-------------|---------|
| `ch01_pool_outfit` | Pool outfit selection | `pool_conservative` |
| `ch01_pool_capture_count` | Pool capture count | `1` |
| `ch01_pool_phone_solo_photo_count` | Pool phone solo photo count | Derived |
| `ch01_pool_phone_attachment_count` | Pool phone attachment count | Derived |
| `ch01_d2_pool_outfit` | Day 2 pool outfit | Derived |

---

## Conclusion

This overview documents the narrative flow of Leia's Consent from Prologue through Day 5, including:
- All major source files and their line ranges
- Key scene labels and branching points
- Story flags and values used for state management
- Phone and photo mechanics
- Polish revisions and QoL patches

The document serves as a reference for understanding the game's structure and narrative progression.

---
*Last updated: 2026-10-20*
