# Ryan's thoughts

At the end of a day's review the game may offer up to three of Ryan's thoughts from that day.
The player keeps one, or keeps nothing. A later day reads the kept thought to tint a few `think`
lines or add one reply option. Keeping a thought never changes stats, and ignoring the offer
plays exactly as before.

Files: `game/python-packages/lc_thoughts.py` (pool, rules), `game/systems/thoughts.rpy` (save
value, hook, API), `game/screens/thoughts_screen.rpy` (the offer page). Tests:
`tests/test_thoughts.py`.

## Player behaviour

- After the scrapbook spread closes (CONTINUE), a second spread opens: "BEFORE I SLEEP" on the
  left page, up to three handwritten thought cards on the right. Clicking a card keeps it;
  KEEP NOTHING (where CONTINUE always sits) or Esc keeps nothing. Stray clicks do nothing.
- Only thoughts whose Day beat this save actually saw are offered. A day with nothing to offer
  shows no page at all.
- Insight and Full stamp each card with what tints it (for example TEMPTATION, or LOVE for the
  Love lane). Immersive shows only the words; the texts never name a stat or route.
- The answer is stored once per save and day. Rolling back past the offer and replaying shows
  it again (the stored answer rolls back with the store). Old saves, Chapter Select starts and
  saves that never reached the offer read as "nothing kept".
- The Day One demo build (`LC_DAY1_DEMO_BUILD`) never shows the offer.
- Today only Day One has a pool (six thoughts). Day Two lines that use the kept thought are
  written with the Day Two rewrite.

## How a thought resolves

Each thought has a base text and variants keyed by a lane (`love_lane`, `exhib_lane`,
`ntr_lane`) or a stat (`love`, `trust`, `exhibitionism`, `sharing`, `temptation`). The text is
resolved every time it is shown, so a kept thought evolves with the save:

1. Lane first: `lc_thought_lane()` maps `lc_current_lean()` (`love` / `love_exhib` / `ntr`) to a
   lane key. If the thought has a variant for that lane, it wins.
2. Otherwise the stat furthest over its tint bar (`lc_thoughts.TINT`), among the stats the
   thought has variants for. Ties follow `STAT_PRIORITY`.
3. Otherwise the base text.

The offer prefers thoughts that a lane or stat tints right now (they reflect how this save
played the day), then the day's order, and shows the picked ones in the day's order.

## Using a kept thought on a later day

```renpy
# A tinted think line (None when nothing was kept: write a neutral line in the else).
if lc_thought_kept("ch01_d1") == "d1_dream":
    $ lc_d2_dream_line = lc_thought_line("ch01_d1")   # resolved now, names filled in
    think "[lc_d2_dream_line]"
else:
    think "..."
```

- `lc_thought_kept(day_id)`: the kept thought id, or None.
- `lc_thought_line(day_id)`: its text for the current stats and lane, with the player's names
  filled in (interpolate it through a plain store variable, as above), or None.
- An extra reply option that depends on a kept thought is a normal scored choice: register it
  and pass the scoring and path-tag tests like any other.

## Adding a day's thoughts

1. Add the beats to `BEATS` in `lc_thoughts.py`: `("flag", id)`, `("value_set", key)` or
   `("value_min", key, n)`, read from story flags and values the day already sets.
2. Add each thought to `THOUGHTS` and `THOUGHT_ORDER` (ids are save data: never rename one):
   `day`, `requires` (a beat id), `base` and `variants`. Write in Ryan's inner voice
   (`docs/characters/ryan.md`, `docs/DIALOGUE_STYLE.md`): plain words, a bit timid, natural
   sentences, no stat or route words, names as `[player_name]` / `[girlfriend_name]` /
   `[friend_name]`.
3. Nothing else: the review's `review_closed` hook offers the day automatically.

## Day One pool

| Id | Beat (seen when) | Variants |
|---|---|---|
| `d1_photo_shoot` | `ch01_pool_capture_count >= 1` (the shoot was not stopped) | love lane, exhibitionism, temptation |
| `d1_towel` | flag `ch01_scene_06_complete` | exhibitionism, temptation, trust |
| `d1_dinner_stranger` | flag `ch01_leia_stranger_second_glance` | love lane, exhibitionism, temptation |
| `d1_julian_carry` | value `ch01_carry_response` | exhibitionism, temptation, trust |
| `d1_sofa_glance` | value `ch01_watching_response` | love lane, exhibitionism, temptation |
| `d1_dream` | flag `ch01_day1_towel_dream_seen` | love lane, exhibitionism, temptation, trust |
