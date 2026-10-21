# External Scripting Notes: Ren'Py Menus, Ink, and Route Design

**Access Date:** 2026-10-20  
**Fetch Status:** 3 successful web fetches (status 200 each)  
**Sources:** Ren'Py Menus, inkle's Ink, 8 Weeks Devlog (Itch.io)

---

## 1. Conditional Branching via State (Ren'Py Menus)

**Source:** [Ren'Py Menus Documentation](https://www.renpy.org/doc/html/menus.html)

**Lesson:** Use Python `if-clauses` within menu choices to gate options dynamically based on narrative state. This creates a lightweight, player-facing branching layer that feels organic rather than a rigid flowchart.

**Mechanism:**
- Each choice can have an `if` expression; the choice only appears if true.
- If all options are gated, the entire menu skips—useful for end-game or state-dependent scenes.
- A `set` clause can track which items have been "used," enabling one-time or cumulative choices.

**Creator Insight:** The menu statement can be preceded by a label name, allowing a named "menu block" that groups related decisions. This reduces visual clutter and groups choices thematically.

**Player Impact:** Choices feel responsive to prior actions. A conditional menu can present 3–5 options that narrow as the story progresses, maintaining agency without overwhelming the player.

---

## 2. Markup-First Narrative (Ink)

**Source:** [inklestudios.com/ink/](https://www.inklestudios.com/ink/)

**Lesson:** Treat text as the primary asset, with logic embedded within. This reduces the cognitive load on writers and keeps prose front-and-center, ideal for dialogue-heavy or prose-driven visual novels.

**Mechanism:**
- Text flows naturally; code and logic are inserted between paragraphs or within tags.
- `divert` statements act like hyperlinks, routing narrative to different labels based on player input.
- Variables and conditions live alongside the prose, making state changes feel less mechanical.

**Creator Insight:** Ink is conceived as "middleware"—a narrative engine designed to slot into a game engine. This separation of concerns means the writer focuses on flow, while the engine handles the branching.

**Player Impact:** The narrative breathes; choices interrupt less, and the story feels more like reading than navigating a state machine.

---

## 3. Route Differentiation via Animation and Pacing (8 Weeks Devlog)

**Source:** [8 Weeks Day 20 Devlog](https://fromplutoguy.itch.io/hard-choice/devlog/1659294/day-20-three-routes-one-very-long-day)

**Lesson:** When branching into full "routes," differentiate not just through dialogue but through pacing, animation, and scene rhythm. Route identity becomes a production layer, not just a script layer.

**Mechanism:**
- Build each route as a self-contained sequence with its own emotional cadence.
- Use 50+ animated/video sequences per route to reinforce distinct vibes (spontaneous, confident, emotional).
- Give the player control within scenes (view changes, pace adjustments) to maintain agency even in scripted moments.

**Creator Insight:** A route is not just a label jump; it's a "rhythm, mood, and moment" package. The creator prioritized making each path feel personally tailored, even within a shared narrative structure.

**Player Impact:** Players feel the weight of their choice because the *experience* of the scene shifts, not just the dialogue. This deepens immersion and makes branching feel earned.

---

## 4. Synthesis: Layered Branching for Leia's Consent

**Application:** Combine Ren'Py's stateful menus for early-game decision gates, Ink-like markup for mid-game prose flow, and route-specific animation/pacing for late-game divergence.

**Suggested Structure:**
1. **Early Game:** Use conditional menus to gate relationship options based on flags (`if relationship == "close"`).
2. **Mid Game:** Embed state changes within dialogue blocks to keep prose fluid.
3. **Late Game:** Diverge into route-specific scenes with distinct pacing and visual rhythm.

**Production Note:** For each major route, aim for 15–25 unique animated or styled sequences. This balances production scope with player perception of depth.

---

## 5. Metadata & Access

- **Ren'Py Menus:** https://www.renpy.org/doc/html/menus.html  
- **Inkle's Ink:** https://www.inklestudios.com/ink/  
- **8 Weeks Devlog:** https://fromplutoguy.itch.io/hard-choice/devlog/1659294/day-20-three-routes-one-very-long-day  

**Fetch Timestamp:** 2026-10-20 14:33 UTC  
**Total Characters Fetched:** ~12,500 (3,800–3,900 per source)

---

*Notes compiled for Leia's Consent script review. Distinguishes creator commentary from structural mechanics; focuses on transferable lessons for branching, choice consequences, and production scope.*
