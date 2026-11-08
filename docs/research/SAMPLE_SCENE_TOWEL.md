# Sample scene: Day 1 towel scene, before and after (DRAFT for darryn, 2026-11-08)

**Not applied to the game.** `game/` is unchanged on this branch. Source:
`game/chapters/ch01/ch01_main.rpy` lines 229-262 on `main` @ 6eda038 (the towel exchange is
lines 243-259). Staging (`scene`, `cast`, `face`, `lc_sfx`, cinematic mode) and the narration
lines are kept as they are; only the spoken lines and one narration line change. Names stay
as Ren'Py tags in the real file (`gf` = [girlfriend_name], `mc` = [player_name]).

## Before (main @ 6eda038)

```renpy
    gf "Wait. I'm definitely closing these first."
    $ lc_sfx("curtain")
    "She caught one of the light curtains and pulled it across the window."
    ...
    gf "...Seriously?"
    mc "What?"
    gf "These barely cover anything."

    "The thin fabric softened the view more than it actually blocked it."
    "I looked at the curtain, then at the towel wrapped around her."
    "{i}That barely covers anything either.{/i}"

    gf "What?"
    mc "Nothing."
    gf "You have that face."
    mc "I was just thinking you look good."
    gf "I'm wearing a towel."
    mc "Exactly."
    $ face("leia", "smile")
    gf "Pervert."

    $ lc_sfx("door_close")
    "She was smiling when she turned back toward the bathroom."
```

## After (DRAFT — darryn to rewrite)

```renpy
    gf "Wait, wait. I'm closing these first. I'm not giving the whole beach a free show."
    $ lc_sfx("curtain")
    "She caught one of the light curtains and pulled it across the window."
    ...
    gf "...Okay, seriously?"
    mc "What?"
    gf "These are, like, see-through. What's even the point of a curtain you can see through?"
    mc "I think they're more of a... I mean, decorative? For the vibe?"
    gf "For the vibe. Great. Thank you, that's super helpful."

    "The thin fabric softened the view more than it actually blocked it."
    "I looked at the curtain, then at the towel wrapped around her."
    "{i}That barely covers anything either.{/i}"

    gf "What? Why are you looking at me like that?"
    mc "I'm not— okay, I was. Sorry. You just look really good, that's all."
    gf "I'm literally in a towel. My hair's dripping all over the floor, I look like a drowned cat."
    mc "Yeah. Still."
    $ face("leia", "smile")
    "She laughed and pulled the towel tighter, though she didn't look like she minded."
    gf "Oh my God, you're such a perv. Okay, I'm going to go put this on before you get any ideas."
    gf "Turn around. Or don't, whatever, it's not like you haven't seen it."
    mc "Turning. I'm turning. Mostly."

    $ lc_sfx("door_close")
    "She was smiling when she turned back toward the bathroom."
```

Full excerpt files: `towel_before.rpy` / `towel_after.rpy` (copied into this folder).

## Measured with the tic scan

Same spoken-line rule and tic regexes as `scratch/tic_scan.py`, run on the excerpt files by
`scratch/tic_scan_file.py`, which also checks the banned list in `docs/DIALOGUE_STYLE.md`:

| | Before | After |
|---|---:|---:|
| Spoken lines | 11 | 13 |
| Lines ≤4 words | 9 (**82%**) | 4 (**31%**) |
| Runs of 6+ short lines | 1 | 0 |
| Lines of 15+ words | 0 | 4 |
| Leia average words / range | 3.0 / 1-6 | 12.5 / 2-20 |
| Ryan average words / range | 2.5 / 1-7 | 6.4 / 1-13 |
| Banned phrases | "Exactly." x1 | none |

Raw output (after):
```
spoken lines 13 | <=4 words 4 = 31% | runs of 6+ short lines 0
   gf      lines  8  avg words 12.5  range 2-20
   mc      lines  5  avg words 6.4  range 1-13
   tics/banned: none
```

## What changed and why (rule → ledger)

- **Real long turns from Leia**, chained from short pieces ("These are, like, see-through.
  What's even the point...") [Patterns §0-1; C02-C05, G01].
- **A real clarification exchange**: "...Okay, seriously?" / "What?" gets answered [§3; C09].
- **Ryan's comeback is gone.** He gets caught, corrects himself ("I'm not— okay, I was"), and
  says something plain [§3, §6; C08, C13, R10]. His one "good" line is just "Yeah. Still.",
  which is honest rather than witty.
- **Leia laughs instead of delivering a verdict.** "Pervert." becomes laughter plus a longer,
  warm tease, and the scene's one short reaction stays affectionate [§5-6; C12, R09].
- **Filler where she's thinking** ("like", "I mean" before Ryan's correction) [§2; C10, C11].
- **Light foreshadowing of the being-watched thread** ("the whole beach a free show") in her
  own words, playful and her choice [§12; R04]. darryn's call whether that's too early.
- **Distinct rhythms.** Leia averages 12.5 words a line and Ryan 6.4. Before, they were 3.0 and 2.5.

## Still needs a human ear
- "I look like a drowned cat" and "For the vibe" are model-written; swap in something only
  Leia would say.
- Whether "it's not like you haven't seen it" is too forward for Day 1 morning Leia.
- Whether Ryan should get "Yeah. Still." or something clumsier.
