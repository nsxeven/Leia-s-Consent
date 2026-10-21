# OpenClaw Script Review: Leia's Consent Structure Notes
**Date:** 2026-10-20  
**Source:** README.md + `game/chapters/ch01/ch01_main.rpy`

---

## Documented Day 1–5 Architecture

The README outlines a **five-day arc** built on a "consent-driven slow burn" premise, where every central character is an adult and the story tracks Leia's curiosity and discovery as she and Ryan work out their boundaries together.

| Day | Script Location | Entry Label | End Route Flag |
|-----|----------------|-------------|----------------|
| Prologue | `chapters/prologue.rpy` | `prologue_name_setup` → `prologue_start` | `prologue_complete` |
| Day 1 | `ch01/ch01_main.rpy` | `chapter_one_start` | `ch01_scenes_01_03_complete` |
| Day 2 | `ch01/ch01_day2_scenes_01_15.rpy` | — | `ch01_d2_end_route` |
| Day 3 | `ch01/ch01_day3_scenes.rpy` | `ch01_day3_start` | — |
| Day 4 | `ch01/ch01_day4_scenes_01_08.rpy` | `ch01_day4_start` | `ch01_d4_end_route` |
| Day 5 | `ch01/ch01_day5_scenes_01_08.rpy` | `ch01_day5_start` | `ch01_d5_end_route` |

---

## Opening Scenes: Pacing, Agency, Branching (Scenes 1–3)

**Scene 1: Arrival** — Establishes the resort's "seamless" luxury and Leia's photo-obsession. Julian's arrival is treated as a given; Leia's agency is passive (waiting for the moment to pose).

**Scene 2: The Villa** — Geography is mapped: master bedroom with ocean-facing glass, Julian's adjacent room, and the private pool below. Leia's skepticism ("This is a small country") frames her as the grounded counterpoint to Julian's performative hosting.

**Scene 3: Outfit Choice** — The first major branching moment. Leia presents two swimsuits: the familiar "usual one" and a bolder new option. Three player choices determine:
- `ch01_pool_outfit` (bolder, conservative, or neutral)
- `ch01_outfit_stance` (encouraging, neutral, or protective)

This choice ripples into Day 2's pool accident and the five end states. The scene ends with Leia in a towel, closing the bedroom curtains—a deliberate privacy boundary before the pool's public gaze.

---

## Four Prioritized Proposals

1. **Standardize Day Labels** — Day 2–5 scripts lack consistent entry labels. Add `ch01_day2_start`, `ch01_day3_start`, etc., to mirror Day 1's clarity and improve navigation.

2. **Consolidate Scene Flags** — `ch01_scene_01_complete` and `ch01_scenes_01_03_complete` are redundant. Use a unified `ch01_day1_complete` flag to signal Day 1's full arc.

3. **Explicit Outfit State** — The `ch01_outfit_stance` flag is set but not always read. Either use it consistently in dialogue or prune it to reduce cognitive load.

4. **Curtain Closure Consistency** — Scene 3's curtain moment is cinematic but not always triggered. Ensure the `ch01_bedroom_window` CG path is stable across all outfit branches.

---

## Dependencies & Exclusions

**Dependencies:**
- `game/defaults.rpy` for `set_story_value` and `get_story_value`
- `game/systems/outfits_data.rpy` for `grant_story_outfit`
- `game/chapters/prologue.rpy` for the `prologue_complete` flag
- `ch01/ch01_day2_scenes_01_15.rpy` for the Day 2 pool accident

**Exclusions (Not Inspected):**
- `ch01/ch01_day4_choice_registration.rpy` — likely helper logic
- `ch01/ch01_day5_visuals.rpy` — placeholder art
- `game/screens/zz*` — late-override overlays
- `game/chapters/ch01/ch01_scenes_07_13.rpy` — Day 1 dinner/walk/shop (untested)

---

## Evidence

- **README.md:** Lines 1–75 (Premise, Running, Project Structure, Implemented Content)
- **Prologue:** Lines 1–240 (`prologue_name_setup` through `chapter_one_start`)
- **Day 1 Main:** Lines 1–130 (`chapter_one_start` through `ch01_scene_04_pool_arrival`)

**Status:** Planning phase only. No game execution performed.
