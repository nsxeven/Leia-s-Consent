# Leia's Consent — Git branch and distribution policy

Updated: 2026-11-08 (release-from-main rule)

## Authoritative branch roles

| Branch | Purpose | Chapter/day access | Release role |
| --- | --- | --- | --- |
| `main` | **Canonical working development branch**. All currently implemented story days, active systems, development CGs and upcoming approved changes go here. | Unrestricted: the Day One demo gate is off; Chapter Select is available immediately. | **Not** a public build. |
| `release/prologue-day1-demo-v0.1.0` | Versioned Prologue + Day One demo snapshot from the merged build. | Day One finishes at a demo end card. Days 2–5 are runtime-gated. Chapter Select is hidden. | Staging branch only until assets, full QA and packaging pass. |
| `release/prologue-day1-demo-polish` | Historical working branch for merged PR #25. | Earlier (pre-art) demo branch state. | **Legacy only**. Do not package from this branch. |
| `feature/*` | Unmerged experimental/feature work, including PRs #22, #23 and #24. | Depends on the task. | Not automatically part of `main` or a release. |

## THE RULE: build on main, extract releases from main (darryn, 2026-11-08)

1. **Everything is built on `main`**: story, art, audio, UI, fixes, credits, and the
   release machinery itself (demo gate, end card, About text, build exclusions).
   Nothing is ever developed or fixed on a release branch.
2. **A release is extracted from `main`** and differs from it in exactly one file:
   `game/00_release_build.rpy`. Two lines change:
   ```renpy
   LC_RELEASE = "day1-demo"      # main: None
   LC_RELEASE_VERSION = "0.1.1"  # main: "dev-main"
   ```
   Every release difference (demo gate, title, version, build name, save folder,
   About heading, hidden Developer/Route Explorer options, chapter select, dev/QA
   files left out of the zips) keys off those values.
3. Steps: `git fetch` → `git worktree add -b release/<name>-v<version> <dir> origin/main`
   → edit the two lines → tests → commit "Release <name> v<version> from main <sha>"
   → push the branch → compile + distribute pc/mac/joiplay + web_build from that
   worktree → audit the zips.
   Check: `git diff origin/main release/<...> --stat` shows only `game/00_release_build.rpy`.
4. Need something different in a release? Build it on `main` behind
   `LC_RELEASE`/`LC_IS_RELEASE` (or a new profile in `LC_RELEASE_PROFILES`), merge it,
   then re-extract. Never cherry-pick or hand-edit other files on a release branch.
5. Release branches are frozen records of what shipped. A fix = fix on `main`, then
   extract a new patch version (v0.1.1 → v0.1.2).
6. `tests/test_release_from_main.py` checks main's switch is off and every release
   setting comes from the switch.

Release branches before `release/day1-demo-v0.1.1` (`v1.0.0`, `day1-demo-v0.1.0`,
`prologue-day1-demo-*`) used cherry-picked release-only commits; they are historical.

## Version numbers (darryn, 2026-11-08)

Public builds use **`v0.<day>.<patch>`** until the game is complete:

| Build | Version |
| --- | --- |
| Prologue + Day One demo (public since 2026-11-06) | `v0.1.0` (bug-fix re-uploads: `v0.1.1`, `v0.1.2` ...) |
| Build that ends after Day Two | `v0.2.0` |
| Days Three / Four / Five | `v0.3.0` / `v0.4.0` / `v0.5.0` |
| Completed game | `v1.x.x` |

- The second number is always the last playable day. The third number is for re-uploads of the same day (fixes only).
- `config.version` on the release branch is the bare number (`"0.1.0"`); the zips, the F95 thread title, the F95 opening post, the itch upload names and Patreon posts all quote the same `v0.1.0`.
- `main` keeps `config.version = "dev-main"`; it is never a public build.
- The first public upload was labelled `1.0.0` (release branch `release/prologue-day1-demo-v1.0.0`, `8e1fadf`); it is the same content as `v0.1.0`. The older internal snapshots `release/prologue-day1-demo-v0.1.0` and `release/prologue-day1-demo-v0.2.0` predate the public demo and are not the public v0.1.0 / v0.2.0; the public v0.1.0 lives on `release/day1-demo-v0.1.0`, and Day Two should use a new name such as `release/day2-v0.2.0`.

## Release profiles (set in `game/00_release_build.rpy`)

| Setting | `main` (`LC_RELEASE = None`) | Day One demo (`"day1-demo"`) |
| --- | --- | --- |
| `LC_DAY1_DEMO_BUILD` | `False` | `True` (derived) |
| `CHAPTER_SELECT_RULE` | `"always"` | `"developer_or_unlocked"` (derived) |
| Game title | `Leia's Consent` | `Leia's Consent — Day One Demo` |
| `config.version` | `dev-main` | `LC_RELEASE_VERSION`, e.g. `0.1.1` |
| `build.name` | `LeiasConsentDev` | `LeiasConsent-Day1Demo` |
| `config.save_directory` | `LeiasConsent-1789068362` (existing dev saves) | `LeiasConsent-DayOneDemo-1789068362` |
| Developer mode / Route Explorer in settings | shown | hidden unless `config.developer` |
| dev/QA scripts in zips | shipped | left out |

The demo save directory is intentionally separate, preventing public-demo saves from overwriting or appearing alongside full development saves. Never change an existing profile's save folder.

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
