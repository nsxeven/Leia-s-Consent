# Stat model v2

Approved by darryn on 2026-11-08. Code: `game/python-packages/lc_stat_model.py` (rules, thresholds,
route resolvers, migration, colour meaning). Everything that shows or reads a stat goes through it.

## The five stats

One display name per stat, in every mode and on every screen (choice cards, Status, phone Status,
end-of-day review, tooltips, Route Explorer, debug).

| Stat (id, group) | Meaning | Route it feeds | Lean |
|---|---|---|---|
| **Love** (`love`, relationship) | How close and cared-for she feels with Ryan | Love family | High: Love / Love+Exhib / NTS. Low: NTR |
| **Trust** (`trust`, relationship) | Honesty and agreeing things together | Gates agreed NTS steps and NTR repair | High: NTS steps, repair. Low: NTR |
| **Exhibitionism** (`exhibitionism`, partner) | How much they both enjoy her being seen, with Ryan in on it | Love+Exhib and NTS | High: Love+Exhib / NTS. Low: pure Love |
| **Sharing** (`sharing`, relationship; starts 0) | Agreed openness to someone else joining in (Maya first) | NTS only, never NTR | High: NTS. Low: stays Love+Exhib |
| **Temptation** (`temptation`, relationship) | Drift, secrets and restlessness pulling her away | NTR | High: NTR. Keep low to avoid it |

Old stats: `curiosity` and `acceptance` folded into Exhibitionism; `boredom`, the old `temptation`,
`secrecy` and `boundary_looseness` folded into Temptation; `momentum` and `jealousy` retired. The old
"NTS Tendency" / "NTR Tendency" rows are replaced by one Full-only **Current lean** row
(`lc_current_lean()` in `systems/stats.rpy`), computed by the same functions the route checks call.

## Scoring rule for choices (enforced by `tests/test_choice_scoring.py`)

1. Only the five stats, each in its own group.
2. At most 2 stats per choice (hard gates: 3). Deltas: +-1 ordinary, +-2 strong, +-3 key beat, gates up to +-5.
3. At most one route stat (Exhibitionism, Sharing, Temptation) per choice.
4. Temptation up never sits with any stat going up.
5. Allowed shapes: Love (Love/Trust up); Love+Exhib (Exhibitionism up, optional Love/Trust up);
   NTS (Sharing up, optional Trust up); NTR (Temptation up, optional Love or Trust down; hard gates
   both); Repair (Temptation down + Love or Trust up, only on beats in `REPAIR_CHOICES`);
   Temptation down alone; Neutral (no stats).
6. The Full route tag is derived, never typed: `lc_choice_route_tag(choice_id)` gives Love,
   Love+Exhib, NTS, NTR, Repair, May lead to NTR, Locks NTR, NTR stays open, "Repair, NTR stays
   open" or Neutral, from the effects plus `CHOICE_ROUTE_FLAGS` (the route value the branch writes).
   The Full-mode tag line on choice cards is a later task (LC-F); Developer mode already shows it.

Day 1 effects live in `systems/choice_engine.rpy`, Day 2 in `ch01_day2_scenes_01_15.rpy`. The Day 3-5
registration files are Scriptwriter-owned, so their effects are re-scored in
`systems/stat_model_v2_later_days.rpy` (init 5, the effective definition). A new Day 3-5 choice
needs a v2 entry there (or v2 stats in its own file), or the scoring test fails.
`get_choice_effects()` still folds any old-style tuple at runtime so a stale entry can't crash a save.

## Route thresholds (`lc_stat_model.THRESHOLDS`)

Days 1-2 were scaled from the old numbers (Exhibitionism climbs about 2.2x faster, Temptation about
1.25x) and tuned with `tests/test_route_simulation.py`. Day 3+ lanes still come from stored values.

| Check | Old | v2 |
|---|---|---|
| Day 1 `ntr_seeded` | 3+ nonchalant tags and (boredom >= 15 or love <= 48) | Temptation >= 17 |
| Day 1 `nts_seeded` (shown as "Exhibition seeded") | nts_score >= ntr_score + 5 and curiosity >= 24 | Exhibitionism >= 30 (and not NTR-seeded) |
| Day 1 Love bedtime | mixed, love >= 54, trust >= 54, nonchalant < 2 | mixed, Love >= 54, Trust >= 54, Temptation <= 12 |
| Day 2 lane `ntr_risk` | seed + boredom >= 15 + (Day 2 nonchalant or love <= 48) + attentive <= nonchalant + 2 | Temptation >= 18 with a Day 1 NTR seed, or >= 20 without |
| Day 2 lane `exhibitionism` | exh >= 22, curiosity >= 24, acceptance >= 15, Day 2 `open` tag | Exhibitionism >= 36, gained some today, Temptation < 18 |
| Day 2 Love+Exhib bedroom blend | love lane, exh >= 20, acceptance >= 15, `open` tag | love lane, Exhibitionism >= 28, gained some today |
| Her own call, Day 1 | 14; 18 / 26; curiosity 25; boredom 16 | 19; 28 / 45; Exhibitionism 21; Temptation 17 |
| Photo confidence (Day 1) | curiosity + acceptance (+5 bolder) >= 38 | Exhibitionism (+3 bolder) >= 14 |
| Her own call, Day 2 | 18 / 26; 18; pool outfit exh 22 or curiosity 27 | 28 / 45; 28; Exhibitionism 36 |
| Day 4 brief reveal / Day 5 bolder swim, comfortable, comfortable after brief | 26 / 24, 34, 30 | 45 / 41, 63, 54 |
| Love-route swimwear | 50 | 63 |
| Wardrobe wear paths | curiosity/exh, love/trust/acc/cur, boredom/temptation/boundary | Exhibitionism 36/32; Love + Trust + Exhibitionism 19/23; Temptation 20/30 |

No route check reads the hidden behaviour tags (`nonchalant`, `open`, `attentive`) any more; they
stay for day-review titles and a few flavour lines.

## Day 2 `mixed_unresolved` -> Day 3

`mixed_unresolved` now starts Day 3 as a **strained Love track with one more chance**
(`ch01_day3_scenes.rpy`): lane `love`, `ch01_d3_strained_love = True`, a strained opening. At the
club the couple gets the same three answers as the NTR night; "You can enjoy yourself. I'll get a
drink." spends the chance and moves the rest of Day 3 (and `ch01_d3_lane`) to `ntr`. Talking it out
records the day as a repair in the review. `ch01_d2_end_route` is never rewritten.

## Colours (by meaning, `systems/stat_delta_colours.rpy`)

Love/Trust up and Temptation down: soft green (`LC_DELTA_UP`). Love/Trust down and Temptation up:
soft red (`LC_DELTA_DOWN`). Exhibitionism: pink, Sharing: purple, either direction (they are a
direction, not good or bad). Same meanings on the choice cards and the review chips/numbers.

## Save migration

`lc_migrate_stats_v2` runs from `config.after_load_callbacks`. A save is converted once when it still
has old keys (`boredom`, `curiosity`, ...):

- Love = love; Trust = trust; Sharing = 0
- Exhibitionism = 10 + (exhibitionism - 10) + ((curiosity - 20) + (acceptance - 10)) / 2
- Temptation = boredom + max(0, temptation - 10) + max(0, secrecy - 5) + max(0, boundary_looseness - 10)
- Every value clamped to 0-100. The old values are kept in `lc_legacy_stats` for one release.
- Day-review snapshots and choice deltas are converted the same way.
- A save made mid-Day-2 stores the old resolver's lane in `ch01_d2_lane_migrated`; the Day 2
  resolver honours it until Day 2 completes, so loading can't flip the lane.
- Story values, flags, choice history, lanes and end states are never touched.
