# Code Inspection Report: Leia's Consent

## 1. Project Instructions (README.md)

**Start jump point:** `label start` → `jump prologue_name_setup` (script.rpy, line 5)

**Key conventions:**
- Story content lives in chapter files under `game/chapters/`
- Late-override files use `zz_`, `zzzz_`, `zzzzz_` prefixes (alphabetical load order)
- Stable image names used (e.g., `cg ch01_d2_love_bedroom_01`)
- Placeholders are `Composite` images; real art points to same name
- Gallery entries use `gallery_row(...)` in `game/systems/gallery_data.rpy`
- Run `lint` and play affected route from fresh save before PR

**Five end states stored in `ch01_d2_end_route`:**
- `love`, `exhibitionism`, `love_repaired`, `mixed_unresolved`, `ntr_confirmed`

---

## 2. game/script.rpy

**Inspected:** Lines 1–5

```python
label start:
    jump prologue_name_setup
```

**Observation:** Entry point is intentionally minimal; all story lives in chapter files.

---

## 3. game/systems/story_state.rpy

**Inspected:** Lines 1–102

### Story-State Helper Names (Actual)

| Helper | Purpose |
|--------|---------|
| `set_story_flag(flag_id, value=True)` | Set boolean story flag |
| `has_story_flag(flag_id)` | Check if flag is true |
| `clear_story_flag(flag_id)` | Remove flag entirely |
| `set_story_value(key, value)` | Store arbitrary save-specific value |
| `get_story_value(key, default=None)` | Read stored value without creating |
| `has_story_value(key)` | Check if key exists |
| `clear_story_value(key)` | Remove stored value |
| `resolve_story_outcome(key, options, weights=None)` | Resolve RNG once, cache result |
| `story_state_summary()` | Developer snapshot for notifications/tests |
| `debug_reset_story_state()` | Reset flags and resolved outcomes |

---

## 4. game/systems/choice_engine.rpy

**Inspected:** Lines 1–180 (truncated)

### Choice-Flow Observations

**Constants:**
- `CHOICE_MODES = ("normal", "insight", "full", "developer")` (line 7)
- `CHOICE_MODE_LABELS` maps modes to display names (lines 9–14)
- `STAT_LABELS` defines stat display names (lines 16–28)

**Choice Effects Storage:**
- `CHOICE_EFFECTS` dictionary maps stable choice IDs to effect tuples: `(target, stat, value)`
- Examples from lines 31–180:
  - `"dev_encourage_curiosity"`: partner curiosity +5, player acceptance +3, relationship momentum +1
  - `"ch01_outfit_bolder"`: partner curiosity +3, player acceptance +3, relationship trust +1
  - `"ch01_photo_more"`: partner curiosity +2, exhibitionism +3, acceptance +2, momentum +1
  - `"ch01_movie_stop"`: love +1, trust +2
  - `"ch01_movie_subtle"`: love +1, exhibitionism +2, acceptance +2, momentum +1

**Choice ID Naming Convention:**
- Prefix `ch01_` for Chapter 1 choices
- Suffix describes action (e.g., `outfit_bolder`, `photo_support`, `towel_laugh`, `bra_playful`)
- Effects stored as tuples: `(target_type, stat_name, value)`

**Effect Targets:**
- `"partner"`: Leia
- `"player"`: Ryan
- `"relationship"`: Relationship dynamics

---

## 5. Low-Risk Improvement Suggestion

**Suggestion:** Add a `CHOICE_EFFECTS_REGISTRY` function that logs when a new choice effect is registered, including source file and line number. This would help track which chapter files define which effects without requiring grep searches.

**Why low-risk:**
- Does not alter existing behavior
- Can be added as a simple decorator or wrapper around the `CHOICE_EFFECTS` dict
- Helps with code reviews and debugging effect chains

---

## 6. Distinguishing Facts from Assumptions

| Type | Content |
|------|---------|
| **Fact** | `script.rpy` line 5: `jump prologue_name_setup` |
| **Fact** | `story_state.rpy` defines 10 helper functions (lines 4–102) |
| **Fact** | `choice_engine.rpy` uses `CHOICE_EFFECTS` dict with stable IDs (lines 31+) |
| **Fact** | Five end states stored in `ch01_d2_end_route` (README line 75) |
| **Fact** | Late-override files use `zz_` prefix (README line 87) |
| **Assumption** | All choice effects are registered at game start; no runtime registration observed |
| **Assumption** | Effects are not modified after initial assignment |

---

*Report generated: 2026-10-20*
*Word count: ~480*
