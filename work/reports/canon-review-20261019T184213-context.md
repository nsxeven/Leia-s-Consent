# Canon Review Context Memo — 20261019T184213

## Inspected Files & Ranges

| File | Path | Lines Read |
|------|------|------------|
| README.md | `README.md` | 1–60 |
| Entry Point | `game/script.rpy` | 1–5 |
| Prologue | `game/chapters/prologue.rpy` | 1–90 |
| Chapter One Main | `game/chapters/ch01/ch01_main.rpy` | 1–70 |
| Day Three Scenes | `game/chapters/ch01/ch01_day3_scenes.rpy` | 1–130 |
| Story State | `game/systems/story_state.rpy` | 1–65 |
| Choice Engine | `game/systems/choice_engine.rpy` | 1–60 |

## Startup Flow (from inspected text)

1. `script.rpy`: label `start` → `prologue_name_setup`
2. `prologue.rpy`: `prologue_name_setup` collects player/gf/friend names; sets `prologue_started` flag; displays "FOUR YEARS AGO" party scene
3. `ch01_main.rpy`: label `chapter_one_start` sets `ch01_started` flag, enables phone HUD, jumps to scene 01 arrival at jetty
4. `ch01_day3_scenes.rpy`: entry `ch01_day3_start` reads Day Two ending route, sets day 3 lane, exits via `ch01_day4_start`

## Established Character & Story Facts

- **Characters**: Leia (gf), Ryan (mc/player), Julian (friend), Maya (new friend)
- **Premise**: Consent-driven slow burn; all characters are adults
- **Routes**: Love (engaged), Exhibitionism (outside attention with Ryan included), NTR pressure (outside attention increasingly separated from Ryan)
- **State System**: Ren'Py `story_flags` and `story_values` store progression; `resolve_story_outcome` uses rollback-aware RNG for one-time decisions
- **Choice Effects**: Central system in `choice_engine.rpy` defines effects for stats like love, trust, curiosity, exhibitionism, secrecy, etc.
- **Day 3 Logic**: Lane branching based on Day Two ending (`ch01_d2_end_route`); NTR repair effort tracked

## State Constraints

- Phone HUD toggled via `set_phone_hud_enabled()` (False in prologue, True after chapter start)
- Route lane persists across Day Three (`ch01_d3_lane`)
- Save-state defaults in `defaults.rpy` (stats, flags, outfits, money)

## Gaps Due to Partial Inspection

- Full content of each file beyond specified line ranges is unverified
- Remaining chapter files (`ch01_scenes_04_06.rpy`, `ch01_day4_*`, `ch01_day5_*`, etc.) not inspected
- `game/systems/defaults.rpy`, `characters.rpy`, and other system files not read
- `work/` and `tests/` directories are non-canon per brief

## Canon Paths (Narrative Sources)

1. `game/chapters/prologue.rpy`
2. `game/chapters/ch01/ch01_main.rpy`
3. `game/chapters/ch01/ch01_day3_scenes.rpy`

---
*Memo saved to: `work/reports/canon-review-20261019T184213-context.md`*
