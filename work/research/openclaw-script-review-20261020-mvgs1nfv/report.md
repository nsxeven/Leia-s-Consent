UNVERIFIED MODEL DRAFT - contains rejected recommendations. Read reviewed-plan.md and independent-checks.md instead.

# Editorial Research Plan: Leia's Consent

**Advisory Status:** Synthesis (Post-Correction)  
**Scope:** Prologue narrative flow, Day 1–5 structural scaffolding, and route differentiation. Assumes 32K label overflow was resolved via segmented reads.

**Premise:** A consent-driven slow burn across five days where adult characters negotiate boundaries. The prologue compresses their first meeting into a single night, establishing Ryan's observant reactivity, Leia's strategic quiet, and Julian's catalytic presence.

---

## Five Prioritized Editorial Proposals

### 1. Temper Ryan's Internal Voice (Prologue, Lines 65–140)
**Evidence:** Independent-checks notes name setup at 5–24 and flashback at 27–33.  
**Rationale:** Ryan narrates his own observations ("I noticed [girlfriend_name] before I ever spoke to her"), competing with Leia's more natural delivery.  
**Effort:** Low (2–3 line swaps)  
**Acceptance Criterion:** Dialogue or action replaces at least one explanatory narration; kitchen silence remains the emotional anchor.

### 2. Extend the Kitchen Beat (Prologue, Lines 151–183)
**Evidence:** Kitchen beat identified at 151, party calls them back at 170.  
**Rationale:** The "quiet pocket" risks feeling like a single block before Truth or Dare escalates.  
**Effort:** Low (1–2 shared physical actions)  
**Acceptance Criterion:** A mirror gesture or shared object interaction precedes the party's return.

### 3. Sharpen Julian's Entrance (Prologue, Lines 301–343)
**Evidence:** Present-day transition at 285; packing begins 294; phone notifications at 313–330; Julian downstairs dialogue at 340–343.  
**Rationale:** Julian is the catalyst but feels reported through narration and UI.  
**Effort:** Medium (one direct line before phone UI)  
**Acceptance Criterion:** Julian speaks face-to-face before the first notification interrupts.

### 4. Standardize Day Labels (Day 1–5 Scripts)
**Evidence:** Structure-notes documented `ch01_day2_start` at line 267 of Day 2 script; Day 3–5 entry labels exist in README but lack consistent naming.  
**Rationale:** Inconsistent labels hinder navigation and testing.  
**Effort:** Medium (add `ch01_dayX_start` to Days 3–5)  
**Acceptance Criterion:** All Day 2–5 scripts begin with matching `ch01_dayX_start` labels.

### 5. Consolidate Scene Flags (Day 1, Lines 181–222)
**Evidence:** `ch01_scene_01_complete` at 58 and `ch01_scenes_01_03_complete` at 320 record different scene counts.  
**Rationale:** Redundancy creates cognitive load and potential continuity gaps.  
**Effort:** Low (unify to `ch01_day1_complete`)  
**Acceptance Criterion:** A single flag signals Day 1's full arc; consumers updated accordingly.

---

## Three Ordered Drafting Tasks

1. **Prologue Polish (Lines 1–406):** Apply proposals 1–3 to tighten character voice and Julian's presence. Verify the curtain trigger at 245–253 functions across all outfit branches.
2. **Day 1 Label Audit (Lines 12–222):** Standardize entry labels and unify scene flags. Confirm `ch01_outfit_stance` is read consistently in dialogue.
3. **Route Differentiation Test:** Run Love, Exhibitionism, and NTR-pressure branches to validate pacing and visible choice consequences.

---

## Route Distinction Table (README-Based)

| Route | Emotional Core | Key Choice Moment | Production Note |
|-------|----------------|-------------------|-----------------|
| **Love** | Mutual discovery, patient negotiation | Outfit choice: bolder vs. familiar | Balanced animation, natural pacing |
| **Exhibitionism** | Performative confidence, public gaze | Curtain moment: private-to-public shift | Higher animation count, tighter cuts |
| **NTR-Pressure** | Reactive tension, timing anxiety | Truth or Dare escalation | Faster dialogue, more reactive beats |

---

## Research Lessons (Primary Sources)

1. **Ren'Py Menus:** Conditional branching via Python `if-clauses` gates options dynamically, creating organic decision gates without rigid flowcharts.
2. **Inkle's Ink:** Markup-first narrative embeds logic within prose, reducing writer cognitive load and making state changes feel less mechanical.
3. **8 Weeks Devlog:** Route identity emerges from pacing and rhythm, not just dialogue—each path feels like a "rhythm, mood, and moment" package.

**Sources:**
- Ren'Py Menus: https://www.renpy.org/doc/html/menus.html
- Inkle's Ink: https://www.inklestudios.com/ink/
- 8 Weeks Day 20: https://fromplutoguy.itch.io/8-weeks/devlog/1659294/day-20-three-routes-one-very-long-day

---

## Explicit Exclusions & Limitations

- **Narrative Depth:** Day 2–5 content is documented structure only; narrative inspection assumed complete in original drafts.
- **Line Count Precision:** Prologue's 406 physical lines corrected from earlier 418 claim; coverage now 1–400 with tail check at 401–406.
- **Animation Quotas:** Removed "50+ per route" invention; scaled to available time and placeholder workload.
- **Flag Usage:** `ch01_outfit_stance` and helper definitions not fully audited; treated as "likely used" rather than confirmed.
- **Curtain Trigger:** No demonstrated missing trigger in inspected source; bug claim removed.
- **32K Overflow:** First combined run exceeded 32K; smaller segmented passes used for this synthesis.
- **Model Draft Accuracy:** Original OpenClaw drafts contained inaccurate references; independent corrections applied to ground this editorial starting point.

---

*Report generated 2026-10-20. Synthesis of four saved research files, weighted toward independent-checks.md as the authority.*
