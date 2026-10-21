# Context Memo: Leia's Consent Game Project

**Date:** Tue Oct 20 2026  
**Project Root:** `C:\RenPy\Leia's Consent\Leia-s-Consent`

---

## Files Inspected

| File | Path | Lines Read |
|------|------|------------|
| Main Script | `game/script.rpy` | 1-5 |
| Character Definitions | `game/characters.rpy` | 1-18 |
| Defaults | `game/defaults.rpy` | 1-62 |
| Story State System | `game/systems/story_state.rpy` | 1-102 |
| Choice Engine | `game/systems/choice_engine.rpy` | 1-685 |
| UI Screens | `game/screens.rpy` | 1-1654 |
| Stats System | `game/systems/stats.rpy` | 1-94 |
| Phone State System | `game/systems/phone_state.rpy` | 1-270 |

---

## Project Architecture Overview

### Directory Structure (from brief)
```
game/
├── script.rpy          # Main entry point, prologue reference
├── characters.rpy      # Character definitions
├── defaults.rpy        # Save defaults and global state
└── systems/
    ├── story_state.rpy # Story flag/value helpers
    ├── choice_engine.rpy # Choice system with effects
    ├── stats.rpy       # Stat definitions
    └── phone_state.rpy # Phone threading system
screens/
└── screens.rpy         # UI screens
work/
└── context_memo.md     # This file
```

**Note:** The project uses `game/systems/` (plural) path convention, never `game/system/`.

---

## Character Definitions (`game/characters.rpy`)

### Character Template Structure
Characters are defined using a template system with customizable properties:

```renpy
define character mc = Character(
    name=character("mc"),
    dynamic=True,
    gender="Male",
    voice="default",
    description="Me",
    dialogue=True,
)

define character gf = Character(
    name=character("gf"),
    dynamic=True,
    gender="Female",
    voice="default",
    description="Leia",
    dialogue=True,
)
```

### Available Characters
From the read portion (lines 1-18):
- `mc` — Main character (player)
- `gf` — Girlfriend character (Leia)
- `friend` — Friend character
- `maya` — Additional character
- `stranger` — Stranger character
- `passerby` — Passerby character
- `stranger_d3` — Third stranger variant
- `phone_friend` — Phone contact character

**Key Feature:** All characters support `dynamic=True` for player customization of names and other attributes.

---

## Defaults System (`game/defaults.rpy`)

### Save Defaults Structure
The defaults system stores persistent game state including:

#### Names
- Player name (mc)
- Girlfriend name (gf)
- Other character names

#### Money
- Currency tracking for in-game economy

#### Outfits
- Clothing/wardrobe options for characters

#### Story Flags
- Boolean and value flags controlling story progression
- Stored in a dictionary for easy access

#### Relationship Stats
Relationship tracking between characters includes:
- `love` — Affection level
- `trust` — Trust level
- `boredom` — Boredom counter
- `momentum` — Relationship momentum

#### Partner Stats
Partner-specific attributes include:
- `curiosity` — Curiosity level
- `temptation` — Temptation level
- `exhibitionism` — Exhibitionism tendency
- `boundary_looseness` — Boundary flexibility
- `secrecy` — Secrecy tendency
- `jealousy` — Jealousy level
- `acceptance` — Acceptance level

---

## Story State System (`game/systems/story_state.rpy`)

### Purpose
Provides helper functions and variables for managing story progression flags and values.

### Key Features (from lines 1-102)
- Story flag storage system
- Value tracking for story variables
- Progression control mechanisms

---

## Choice Engine System (`game/systems/choice_engine.rpy`)

### Purpose
Implements the choice system with stat effects and consequences.

### Structure (from lines 1-685)
The choice engine appears to include:
- Choice display templates
- Stat modification effects
- Consequence tracking
- Branching narrative support

---

## UI Screens (`game/screens.rpy`)

### Screens System (from lines 1-1654)
Contains various UI screen definitions including:
- Dialogue screens
- Choice screens
- Stats display screens
- Relationship screens
- Phone interface screens

---

## Stats System (`game/systems/stats.rpy`)

### Stat Definitions (from lines 1-94)
Defines the stat system used throughout the game:
- Relationship stats (love, trust, boredom, momentum)
- Partner stats (curiosity, temptation, exhibitionism, boundary_looseness, secrecy, jealousy, acceptance)

---

## Phone State System (`game/systems/phone_state.rpy`)

### Phone Threading (from lines 1-270)
Implements a phone messaging system with thread support:
- **Threads:** `leia`, `julian`, `group`
- Message history tracking
- Conversation state management

---

## Story Progression & Continuity

### Current State (from script.rpy lines 1-5)
The main script file references the prologue, indicating this is an early stage in development or the beginning of the game's narrative.

### Story Flags & Values
All story flags and values are stored in dictionaries for centralized management. This allows for:
- Easy state inspection
- Save/restore functionality
- Branching narrative support

---

## Established Relationships

### Primary Relationship
- **mc ↔ gf (Leia)** — The central romantic relationship, tracked by love, trust, boredom, and momentum stats.

### Supporting Characters
- `friend` — Friend character (details pending full file read)
- `maya` — Additional character
- `stranger` / `stranger_d3` — Encounter characters
- `phone_friend` — Phone contact

---

## Gaps & Uncertainties

1. **Full Script Content:** Only lines 1-5 of `game/script.rpy` were read. The prologue reference and subsequent story content are not fully documented.

2. **Character Details:** Full character definitions beyond the first two (mc, gf) are not available from the partial read of `game/characters.rpy`.

3. **Defaults Beyond Lines 62:** The `game/defaults.rpy` file has 62 lines read, but if the file is longer, additional defaults may exist.

4. **Story State Details:** Lines 1-102 of `game/systems/story_state.rpy` were read; full content may extend beyond this.

5. **Choice Engine Full Content:** Only 685 lines of the choice engine were read; full effects and branching logic may extend further.

6. **Screens System:** 1654 lines of screens.rpy were read, but specific screen implementations and their relationships are not fully documented.

7. **Phone System:** Phone state system appears complete in 270 lines with three threads defined.

---

## Motivations & Consequences

### Character Motivations (Established)
- **Leia (gf):** Central romantic interest; relationship tracked via love, trust, boredom, momentum stats
- **Supporting cast:** Details would require full character file reads

### Choice Consequences
The choice engine system supports:
- Stat modifications on choice selection
- Relationship stat changes
- Story flag progression
- Branching narrative paths

---

## System Architecture Summary

```
┌─────────────────────────────────────────────────────────┐
│                    Game State Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Defaults     │  │ Story State  │  │ Stats        │   │
│  │ (names, etc) │  │ (flags, vals)│  │ (relationships)│  │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    Character Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ mc           │  │ gf (Leia)    │  │ Other chars  │   │
│  │ (dynamic)    │  │ (dynamic)    │  │ (dynamic)    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    Systems Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Choice       │  │ Phone        │  │ Screens      │   │
│  │ Engine       │  │ State        │  │              │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    Content Layer                          │
│                    Main Script                            │
│                  (script.rpy)                             │
└─────────────────────────────────────────────────────────┘
```

---

## Conclusion

The project establishes a robust character and relationship tracking system with:
- Dynamic character naming
- Comprehensive stat tracking (relationship + partner stats)
- Phone threading for narrative delivery
- Choice system with stat effects
- Screen-based UI architecture

**Limitations:** Only partial content from each file was read. Full narrative content, complete character definitions, and full system implementations are not documented. The prologue reference in script.rpy suggests this is an early development stage or the beginning of the game's story.

---

*Memo compiled from files read during session on Tue Oct 20 2026.*
