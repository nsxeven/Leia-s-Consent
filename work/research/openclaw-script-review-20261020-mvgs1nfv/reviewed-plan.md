# Leia's Consent - reviewed initial improvement plan

**Authorship/status:** OpenClaw's qwen35-9b-abliterated:latest generated the working drafts and external research. Codex checked selected claims against source and curated this plan. The model drafts, including report.md and model-report-unverified.md, are **unverified brainstorming**, not implementation briefs.

## Coverage

Focus: prologue, opening resort scenes, and README's documented Day 1-5 structure. This is not a complete Day 1-5 narrative or technical audit. The first combined run exceeded 32K context; smaller prologue, structure, external-research and synthesis sessions followed.

Tool records confirm reads of README.md, prologue.rpy and ch01_main.rpy. The first prologue critique read 1-400 but falsely claimed 418 lines; the file has 406. Codex checked the final transition and key scene locations. A later structure session also read the prologue. Several model citations were inaccurate; consult independent-checks.md for corrections rather than trusting the original coverage claims.

The real opening shows Ryan meeting Leia at a university party four years earlier, making space for her in the conversation, sharing a quiet kitchen exchange, and participating in Truth or Dare before their first kiss. Present-day packing sets up the holiday with Julian. The earlier bot's ownership-contract story is not canon.

## Five prioritized proposals

### 1. Build a choice-and-consequence ledger
**Evidence:** Prologue first-impression choices around 90-112 and departure choices at 351-377. In game/chapters/ch01/ch01_main.rpy, outfit branches set values at 181-213 and converge at 222.
**Proposal:** Map each choice to its immediate response, state change and later callback. Distinguish flavor from consequential decisions.
**Benefit:** Clarifies intended reactivity without assuming every flavor choice needs a route effect.
**Effort:** Medium.
**Acceptance:** Every opening choice has a source-backed ledger row. Later callbacks stay unverified until actual consumers are read. No flag deletion.

### 2. Tighten repetition while preserving Ryan's attentiveness
**Evidence:** game/chapters/prologue.rpy:37-89 establishes his initial impression; 115-128 shows him actively including Leia.
**Proposal:** Identify up to three narration lines that repeat visible action or dialogue; draft optional trims.
**Benefit:** Sharper viewpoint without turning the model's subjective opinion into a claim that Ryan never acts.
**Effort:** Low.
**Acceptance:** Each candidate includes original text, proposed replacement/deletion, location and editorial reason. Keep the current script as the baseline.

### 3. Compare one alternative kitchen transition
**Evidence:** prologue.rpy:130-183; the easy silence is at 151 and the party calls them back at 170.
**Proposal:** Draft one brief shared-action beat before returning to the group.
**Benefit:** May strengthen the contrast between private connection and public attention without expanding every scene.
**Effort:** Low.
**Acceptance:** One compact alternative with a clear emotional purpose; retain it only if it adds information or useful rhythm.

### 4. Define distinct emotional promises for each route
**Evidence:** README.md's route-design paragraph. The opening outfit decision is an early shared choice, not proof that a route is locked.
**Proposal:** Make a one-page route guide, then inspect later source before assigning existing scenes to it.

| Route | Established distinction | Planning question |
|---|---|---|
| Love | Ryan stays engaged | How does the couple's connection develop? |
| Exhibitionism | Outside attention with Ryan included | How is shared participation made clear? |
| NTR pressure | Outside attention increasingly separated from Ryan through disengagement and secrecy | Where does emotional distance become observable? |

**Benefit:** Differentiation through relationships and consequences.
**Effort:** Medium.
**Acceptance:** Each route has an emotional objective and one proposed callback. Existing callbacks require citations; additions remain proposals.

### 5. Budget editorial changes against existing staging
**Evidence:** prologue.rpy:313-343 places Julian downstairs through phone notifications and dialogue. ch01_main.rpy:245-253 already contains the curtain CG and action in common branch flow. README documents placeholder art.
**Proposal:** Prefer changes using existing assets. A face-to-face Julian scene would require new staging, not repair an established missing feature.
**Benefit:** Prevents small prose revisions becoming unplanned art/engineering work.
**Effort:** Low for an inventory.
**Acceptance:** List writing, art, state and staging needs for every change. No arbitrary animation quota.

## External research

OpenClaw recorded web-fetch activity; Codex independently opened these primary sources:
- [RenPy menus](https://www.renpy.org/doc/html/menus.html): supports conditional choices and continuation after menu blocks. Transfer: document relevant state and rejoin behavior; do not assume the current game lacks it.
- [inkle's ink overview](https://www.inklestudios.com/ink/): describes text-first authoring and interactive preview tooling. Transfer the flow-review practice, not an engine migration.
- [8 WEEKS creator devlog](https://fromplutoguy.itch.io/8-weeks/devlog/1659294/day-20-three-routes-one-very-long-day): discusses distinct emotional rhythms and production costs across routes. Its 58 sequences are TOTAL across three routes, not 50+ per route.

These are creator/documentation sources, not evidence of player consensus or sales. This small reference set is not comprehensive NTR-market research. Player-impact predictions remain hypotheses.

## Three ordered drafting tasks

1. **Source map:** Read the remaining Day 1-5 narrative and relevant overrides in small passes. Save a coverage table and choice ledger; trace active labels and consumers before proposing technical changes.
2. **Prologue alternatives:** Draft at most three non-canon micro-revisions for proposals 2-3. Save original/revised comparisons for approval.
3. **Route callback plan:** Propose one emotionally distinct callback per route, with prerequisites, shared rejoin and production requirements. Implementation is separate.

## Rejected claims and limits

Do not add supposedly missing day labels: ch01_day2_start already exists at day2_scenes_01_15.rpy:267; later entries are documented. Do not merge scene-level and multi-scene flags without tracing consumers. Do not claim ch01_outfit_stance is unused without searching the repository.

The model repeated inaccurate references and unsupported fixes even after correction. Treat its output as brainstorming requiring review, not autonomous code-review evidence. No runtime testing, full canon audit, measured player-response claim, or game-source edits were performed.
