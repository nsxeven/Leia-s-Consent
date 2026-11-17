# Ryan's thoughts

At the end of a day's review the game offers one of Ryan's thoughts per part of that day (Day
One: daytime, evening, night).
The player keeps one, or keeps nothing. A later day reads the kept thought to tint a few `think`
lines or add one reply option. Keeping a thought never changes stats, and ignoring the offer
plays exactly as before.

Files: `game/python-packages/lc_thoughts.py` (pool, rules), `game/systems/thoughts.rpy` (save
value, hook, API), `game/screens/thoughts_screen.rpy` (the offer page). Tests:
`tests/test_thoughts.py`.

## Player behaviour

- After the scrapbook spread closes (CONTINUE), a second spread opens: "BEFORE I SLEEP" on the
  left page, one handwritten thought card per part of the day on the right. Clicking a card keeps
  it; KEEP NOTHING (where CONTINUE always sits) or Esc keeps nothing. Stray clicks do nothing.
  Keyboard and gamepad focus starts on the first card and moves between the cards and KEEP
  NOTHING (Enter / A picks).
- Only thoughts whose Day beat this save actually saw are offered. A part of the day with no
  seen beat gives no card; a day with nothing to offer shows no page at all.
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
2. In a lane, the lane limits the stats (`LANE_STATS`, in order of preference): Love lane only
   Love/Trust; Love + Exhibitionism prefers Exhibitionism (Temptation never outranks it); NTR
   never Love and prefers Temptation over Exhibitionism. The first listed stat over its tint bar
   (`lc_thoughts.TINT`) that the thought has a variant for wins.
3. With no lane (undecided/strained), the stat furthest over its bar among the stats the thought
   has variants for. Ties follow `STAT_PRIORITY`.
4. Otherwise the base text.

The offer is one card per part of the day (`OFFER_PARTS`), in day order. Within a part it takes
the seen thought this save colours most (`colour_count`: the lane variant plus each stat the lane
allows that is over its bar), so it reflects how this save played the day; equal counts go to
the earlier beat. On Day One this gives Love saves (high Trust) the towel, carry and dream, and
lower-Trust saves the photo shoot, dinner and sofa (the towel when the shoot was stopped).

Every text was checked against the Day One script. The comment above each thought names its
`Source:` label(s) (tested to exist); re-read those scenes when editing either side.

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
   `day`, `requires` (a beat id), `base` and `variants`, with a `# Source: <label>` comment
   naming the scene(s) it was checked against. Give every thought a lane line for the Love lane.
   Write in Ryan's inner voice
   (`docs/characters/ryan.md`, `docs/DIALOGUE_STYLE.md`): plain words, a bit timid, natural
   sentences, no stat or route words, names as `[player_name]` / `[girlfriend_name]` /
   `[friend_name]`.
3. Group the day's thoughts into parts in `OFFER_PARTS` (day order; tested). The review's
   `review_closed` hook then offers the day automatically.

## Day One pool

Parts: daytime (photo shoot, towel), evening (dinner stranger, carry), night (sofa glance, dream).

| Id | Beat (seen when) | Variants |
|---|---|---|
| `d1_photo_shoot` | `ch01_pool_capture_count >= 1` (the shoot was not stopped) | love lane, exhibitionism, temptation |
| `d1_towel` | flag `ch01_scene_06_complete` | love lane, exhibitionism, temptation, trust |
| `d1_dinner_stranger` | flag `ch01_leia_stranger_second_glance` | love lane, exhibitionism, temptation |
| `d1_julian_carry` | value `ch01_carry_response` | love lane, exhibitionism, temptation, trust |
| `d1_sofa_glance` | value `ch01_watching_response` | love lane, exhibitionism, temptation |
| `d1_dream` | flag `ch01_day1_towel_dream_seen` | love lane, exhibitionism, temptation, trust |
