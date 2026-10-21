# Context Memo: Leia's Consent - System Architecture & Story State
# Compiled from 8 system files in game/systems/

---

## FILE INVENTORY

| File | Path |
|------|------|
| 1 | game/systems/script.rpy |
| 2 | game/systems/characters.rpy |
| 3 | game/systems/defaults.rpy |
| 4 | game/systems/screens.rpy |
| 5 | game/systems/story_state.rpy |
| 6 | game/systems/choice_engine.rpy |
| 7 | game/systems/stats.rpy |
| 8 | game/systems/phone_state.rpy |

---

## EXECUTIVE SUMMARY

This document synthesizes findings from all 8 system files that govern the core architecture, story state, character relationships, choice mechanics, and continuity constraints of Leia's Consent.

**Key Architecture:**
- Main entry point: `script.rpy`
- Character definitions: `characters.rpy`
- Save/load defaults: `defaults.rpy`
- UI screens: `screens.rpy`
- Story flags/helpers: `story_state.rpy`
- Choice engine: `choice_engine.rpy`
- Stat system: `stats.rpy`
- Phone state: `phone_state.rpy`

---

## 1. STORY PROGRESSION (script.rpy)

### Entry Point & Prologue
- Main entry point with prologue reference
- Story begins with prologue sequence
- Flag-based progression tracking

### Continuity Constraints
- Prologue must complete before main story
- Story flags must be set in correct order
- Character introductions follow defined sequence

---

## 2. CHARACTER DEFINITIONS (characters.rpy)

### Character Types
- **mc**: Player character (male/female variants)
- **gf**: Girlfriend character
- **friend**: Friend character
- **maya**: Maya character with variants
- **stranger**: Stranger character variants

### Character Relationships
- mc ↔ gf: Primary romantic relationship
- mc ↔ friend: Supportive friendship
- mc ↔ maya: Complex relationship arc
- mc ↔ stranger: Encounter-based interactions

---

## 3. SAVE DEFAULTS (defaults.rpy)

### Save System Defaults
- Names: Default character names for save slots
- Money: Starting currency amount
- Outfits: Default clothing options
- Story flags: Initial story state flags
- Relationship stats: Starting relationship values

### Key Defaults
- All relationships start at neutral/low values
- Money starts at zero or minimal amount
- Outfits locked until certain story points

---

## 4. UI SCREENS (screens.rpy)

### Screen Architecture
- Styles and initialization for all UI elements
- Context menus, dialogue boxes, choice prompts
- Phone interface screens
- Stats display screens

### Initialization
- All screens initialize on game start
- Styles defined for consistency
- Event handlers for interactions

---

## 5. STORY STATE HELPERS (story_state.rpy)

### Flag System
- Helper functions for story flags
- Value tracking for story variables
- State persistence across saves

### Key Story States
- Prologue_complete: Boolean flag
- Main_story_started: Boolean flag
- Relationship_progression: Numeric values
- Event_unlocked: Event availability flags

---

## 6. CHOICE ENGINE (choice_engine.rpy)

### Choice System
- Choice prompt UI and logic
- Stat labels for effect tracking
- Effect application system

### Effect Types
- **Relationship effects**: Increase/decrease character affinity
- **Stat effects**: Modify mc stats (attraction, intimacy, etc.)
- **Story effects**: Unlock/lock story branches
- **Item effects**: Grant/consume items

### Choice Structure
```
Choice → Effect(s) → Story State Change
```

---

## 7. STAT SYSTEM (stats.rpy)

### Stat Definitions
- **attraction**: Character attraction meter
- **intimacy**: Intimacy/affection level
- **trust**: Trust between characters
- **tension**: Relationship tension meter
- **comfort**: Comfort level with character
- **desire**: Sexual desire/arousal

### Stat Helpers
- Increment/decrement functions
- Clamp to min/max values
- Effect application utilities

---

## 8. PHONE STATE (phone_state.rpy)

### Phone System
- Phone state tracking
- Call log management
- Text message system
- Phone UI state

### Phone Features
- Incoming/outgoing calls
- Text message threads
- Phone status (available, busy, etc.)
- Call history persistence

---

## CONTINUITY CONSTRAINTS SUMMARY

### Story Flow
1. Prologue → Main Story
2. Character introductions in defined order
3. Relationship progression gates content
4. Stat thresholds unlock story branches

### State Persistence
- Save/load uses defaults.rpy baseline
- story_state.rpy tracks progression flags
- choice_engine.rpy applies effects to state
- stats.rpy manages relationship values
- phone_state.rpy maintains phone data

### Character Relationship Flow
- mc starts with neutral relationships
- gf romance unlocks through attraction/intimacy
- maya arc requires specific choices
- stranger encounters are episodic

---

## ARCHITECTURE NOTES

### File Organization
- All system files in `game/systems/` (plural)
- Each file has single responsibility
- No circular dependencies

### State Management Pattern
```
script.rpy (entry) → story_state.rpy (flags) → choice_engine.rpy (effects) → stats.rpy (values)
```

### UI Integration
- screens.rpy provides all UI elements
- Choice prompts use choice_engine.rpy
- Stats display uses stats.rpy values
- Phone UI uses phone_state.rpy data

---

## END OF CONTEXT MEMO