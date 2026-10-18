# Build handoff

This note is the current boundary for the Chapter One development build. It does not change story text or art.

## What is linked

A new game starts at `prologue_name_setup`, then `chapter_one_start`.

Day One ends in `ch01_scene_30_end_day_one` and jumps to `ch01_day2_start`.

Day Two ends in `ch01_day2_scene_30_finish`. That label sets `ch01_day_02_complete`, shows the Day Two complete card, and returns. It does not continue the story.

## Day 3 is not linked

`game/chapters/ch01/ch01_day3_scenes.rpy` is in the tree and defines `ch01_day3_start`. No playable label jumps to it. Do not wire Day Three in from the Day Two finish card unless that link is an explicit next task.

## No CG art changed

The Day Two QA pass did not add, replace, or edit CG image files. `game/images/` is untouched. Scene scripts still point at the existing CG names.

## Day Two rules to keep

- After the boutique, scenes 11b and 12 call `has_choice_tag("repair")`. That function must stay defined. It is true when `choice_tag_count` for the tag is greater than zero. Removing it raises `NameError` before the villa pool plan.
- The Love dinner picker in `ch01_day2_scene_21_pre_sunset` must not offer `boutique_cutout_mini`. The Black Cutout Mini is reserved for Day 3.
- Dinner collision: `stranger_casual_dry` walks in from screen-left (`ch01_stranger_walk_in_left`) before the spill CGs. `stranger_casual_wet` is the sprite after those CGs. The later corridor compliment is `passerby`, a separate `Character` from `stranger`.
- `bbc_stranger_casual` is an alias of `stranger_casual_dry`. Do not point it back at `Base_Casual.png` or `Penis_Casual.png`; those files are not in the project.
- Black Cutout Mini source: if Ryan buys it during the boutique shop, `ch01_d2_mall_outfit_source` is `ryan`. Otherwise Leia buys it herself and the source is `leia`.
