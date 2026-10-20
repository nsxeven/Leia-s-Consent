# Executed validation

Engine: Ren'Py **8.5.3.26051504**. Baseline main: `41913f32e216e9b7cfb96ee7fc5a330468857786`.

## Ren'Py lint

```sh
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy \
/path/to/renpy-8.5.3-sdk/renpy.sh /path/to/project lint /path/to/lint.txt --error-code
```

Result: **exit 1**, with the same 17 diagnostic lines as baseline. This is not a clean lint result. The diagnostics are five undefined `white` uses in Day 1, seven malformed unused legacy photo aliases, four out-of-range init priorities and one undeclared `julian` hide tag. No new undefined labels, variables or image references were reported by lint. Lint is not a complete variable/route analyzer.

The SDK archive was available locally from the earlier task; it was extracted under `/tmp` with `--no-same-owner`. Temporary directories may be cleared between Work sessions; re-extract before reproducing.

## Parsed-script state tests

Copy the project into a disposable directory and copy `tools/day34_smoke.rpy` to that copy's `game/zzzz_day34_smoke.rpy`. The harness lives outside `game/` in the published source so it is not shipped as an active command.

```sh
RENPY_PATH_TO_SAVES=/tmp/lc-day34-test-saves \
LC_DAY34_REPORT=/path/to/state-tests.json \
/path/to/renpy-8.5.3-sdk/renpy.sh /path/to/disposable-project day34_smoke
```

Recorded result: **114 assertions, 25 traversals, passed**. See `state-tests.json` for every assertion and label/image/menu trace. The harness executes actual compiled Ren'Py Python and traverses the actual AST for conditionals, menus, calls and jumps. Rendering, screen calls and notification feedback are stubbed; menu selections are specified by test scenarios. It therefore checks route/state integration without pretending to be a full playthrough.

Coverage:

- Love and repaired-Love entry, independent Exhibitionism, alternate roleplay and private opt-out.
- All three Day Three NTR effort options, exact search-message order, continued contact/photos and Ryan's ignorance before discovery.
- Covert discovery, monitoring, second meeting, concealed knowledge and the confirmed ending; no automatic NTS.
- Existing unresolved repair, unresolved conflict and deeper NTR endings.
- Voluntary disclosure, exclusive Love repair, mutual NTS discussion, NTS refusal into Love and Exhibitionism, inability to reconcile, and missed-repair cases.
- Negative consent-state checks: curiosity alone does not resolve to NTS; monitoring excludes NTS agreement.
- Four Day 2 boutique witness/purchase combinations, matching slip CG, stare flag and acquisition source.
- Gallery registry, new image registration, seen-state helper locks/unlocks and all literal Chapter One choice IDs registered.
- No Adrian contact thread is introduced into Ryan's normal phone.

## Static checks

`python tools/check_day34_static.py` verifies duplicate labels, protected source/assets and the lint diagnostic comparison when the earlier baseline report is available alongside this checkout. `git diff --check` checks whitespace. See `static-checks.json` for the recorded result.

## Not executed / review gate

No rendered playthrough, screenshot QA, interactive rollback, actual save/load round trip, old-save resume, mobile layout or complete combinatorial route traversal was performed. There is no X server/Xvfb in this environment. New state uses the existing save-local dictionaries and avoids irreversible side effects, but that is architectural evidence, not a passed rollback test.

Review on a fresh save or Chapter Select. A development save paused within a replaced Scene 13 may resume differently. New nightclub-event branches stop after Day Four to prevent contradictions with the unchanged Day Five story. Main must not be merged without review.
