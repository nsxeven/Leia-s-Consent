# Leia's Consent — Git branch and distribution policy

Updated: 2026-10-21

## Authoritative branch roles

| Branch | Purpose | Chapter/day access | Release role |
| --- | --- | --- | --- |
| `main` | **Canonical working development branch**. All currently implemented story days, active systems, development CGs and upcoming approved changes go here. | Unrestricted: the Day One demo gate is off; Chapter Select is available immediately. | **Not** a public build. |
| `release/prologue-day1-demo-v0.1.0` | Versioned Prologue + Day One demo snapshot from the merged build. | Day One finishes at a demo end card. Days 2–5 are runtime-gated. Chapter Select is hidden. | Staging branch only until assets, full QA and packaging pass. |
| `release/prologue-day1-demo-polish` | Historical working branch for merged PR #25. | Earlier (pre-art) demo branch state. | **Legacy only**. Do not package from this branch. |
| `feature/*` | Unmerged experimental/feature work, including PRs #22, #23 and #24. | Depends on the task. | Not automatically part of `main` or a release. |

## Versioned release-branch convention

- New builds are developed on `main`; never implement the current main development progression directly into a versioned release branch.
- When a demo or release is approved, create a **new** release branch from a specifically recorded `main` SHA, e.g. `release/ch01-day2-demo-v0.2.0` or `release/ch01-full-v1.0.0`.
- Apply release-specific restrictions, menu options, age notices, version numbers and distribution exclusions **only to that release branch**.
- Release branches are preserved as versioned snapshots; subsequent bugfix releases get a new branch or a clearly identified patch-version branch.
- New CG art and story improvements pushed to `main` **do not automatically enter** older demo snapshots. Deliberately port only approved fixes and record their origins.
- Do not merge release-only flags/configuration backwards into `main`. In particular, preserve `LC_DAY1_DEMO_BUILD = False` and `CHAPTER_SELECT_RULE = "always"` on `main`.
- Do not merge feature PRs #22–24 merely to reconcile branches; review, test and approve their story changes first.

## Important branch-specific settings

| Setting | `main` | Day One demo |
| --- | --- | --- |
| `LC_DAY1_DEMO_BUILD` | `False` | `True` |
| `CHAPTER_SELECT_RULE` | `"always"` | `"developer_or_unlocked"` (also hidden by demo gate) |
| Game title | `Leia's Consent` | `Leia's Consent — Day One Demo` |
| `config.version` | `dev-main` | `0.1.0-demo.1` |
| `build.name` | `LeiasConsentDev` | `LeiasConsentDayOneDemo` |
| `config.save_directory` | `LeiasConsent-1789068362` (existing dev saves) | `LeiasConsent-DayOneDemo-1789068362` |

The demo save directory is intentionally separate, preventing public-demo saves from overwriting or appearing alongside full development saves. Release save migration can be planned separately if needed.

## Daily local development workflow

```powershell
git status
git fetch origin
git switch main
git pull --ff-only origin main
```

If local changes prevent switching or fast-forwarding, preserve or commit them first; do not force-reset or discard work.

To review the demo snapshot separately:

```powershell
git fetch origin
git switch release/prologue-day1-demo-v0.1.0
git pull --ff-only origin release/prologue-day1-demo-v0.1.0
```

Return to `main` before working on new canon, scripts, CGs or systems.

## Demo packaging warning

The current Day One demo branch **runtime-gates** unfinished later days, but because it is a snapshot of the full source tree, it still contains later-day scripts/assets. Before public packaging, inspect the Ren'Py build manifest and archive contents to ensure unlaunched story content isn't distributed if that matters for spoilers or size.

## Required QA before a public release

Replace outstanding placeholder art; run Ren'Py 8.5.3 lint; test complete Prologue + Day One routes, chapter selector on `main`, demo end gating on the release branch, save/load/rollback, Phone, Gallery, and default/customized character names. Build and inspect the actual distribution. Git history synchronization alone is **not** release approval.
