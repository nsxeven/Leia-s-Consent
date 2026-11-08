# Dialogue style guide — DRAFT for darryn's review (2026-11-08)

Goal: people talk like people, and each character sounds like themself. Read
the character files in `docs/characters/` before writing.

## The problem (measured on main, Prologue + Day 1)
- 55% of spoken lines are 4 words or fewer; 16 runs of 6+ clipped lines in a row.
- All four main characters average 4.2-4.8 words a line: one voice, four names.
- Repeated stock lines: "Exactly." (12), lone "Okay." / "Fine." / "Yeah." (9),
  "Fair." (4), "a beat too long" and friends (5), "There she is", "No grin. No
  comment. No attempt..."
- Player quote (desmosome, F95): "They are all men of few words, acting like they
  are cool as shit... They don't communicate like actual humans."

## Banned or rationed

| Pattern | Rule |
|---|---|
| "There she is." / "There it is." | Banned. |
| "Exactly." / "Noted." / "Fair." / "Touché." as a whole line | Banned. |
| One-word verdict comebacks ("Pervert." "Skill." "Yet.") in a row | Max one per scene. |
| Ping-pong of 6+ lines all ≤ 4 words | Avoid; usually break it with a longer line, an action or a thought (flagged, not failed). |
| Everyone has a witty comeback | No. Someone fails to answer, laughs, misunderstands, changes the subject. |
| "a beat too long", "a fraction too late", "for a beat" | Max once per day. |
| "No X. No Y. No Z." narration fragments | Banned. |
| "Not X. Just Y." | Max once per day. |
| "with the seriousness/expression of somebody who..." | Max once per day. |
| Narration explaining the subtext right after it happened ("That landed harder than I wanted it to.") | Cut; show the reaction instead. |
| Characters naming their emotions perfectly | Rare. People say "I don't know, it was weird" instead. |

## Do this instead
- **Mix lengths.** Real talk is uneven: one rambling line, one short one, an interruption.
- **Imperfect speech**: "I mean", "like", "wait", false starts, trailing "...",
  self-corrections ("I'm not staring. Okay, I'm staring a little.").
- **People don't always win.** The joke can fall flat; someone just laughs; someone says "what?" and means it.
- **Different rhythms per character**: Julian rambles, Maya interrupts, Leia runs
  sentences together when excited, Ryan is plain and a bit awkward.
- **Questions over comebacks**: curious people ask things back.
- **Subtext stays sub**: let the reader catch it.
- **Read it out loud.** If nobody you know would say it, rewrite it.

## Before / after (the lines the player quoted)

Before:
> **Leia:** What? / **Ryan:** Nothing. / **Leia:** You have that face. / **Ryan:** I was just thinking you look good. / **Leia:** I'm wearing a towel. / **Ryan:** Exactly. / **Leia:** Pervert.

After (draft):
> **Leia:** What? Why are you looking at me like that?
> **Ryan:** I'm not— okay, I was. You look really good, that's all.
> **Leia:** I'm literally in a towel. My hair's doing the wet-dog thing.
> **Ryan:** Yeah. Still.
> **Leia:** *(laughing)* You're such a perv. Hand me the other one.

Before:
> **Julian:** She changed her mind and unpacked another suitcase, didn't she? / **Ryan:** Give her a minute. / **Julian:** I've given her twelve.

After (draft):
> **Julian:** Is she still changing? Dude, I've been out here so long I've got a tan line from my sunglasses.
> **Ryan:** She's almost done. I think. She said "two minutes".
> **Julian:** She said "two minutes" before I'd even found the shade.

## Research basis (added 2026-11-08, DRAFT)
Real recorded conversation (Santa Barbara Corpus sample) is 36-52% short turns too, so short
lines aren't the problem on their own. What's missing is the long turns: 11-26% of real turns run
15+ words, against 1.4% in our Prologue + Day 1. Fillers, self-corrections and laughter are also
nearly absent. Sourced rules per situation: `docs/research/REAL_SPEECH_PATTERNS.md`. Evidence:
`docs/research/REAL_DIALOGUE_LEDGER.md`. Worked example: `docs/research/SAMPLE_SCENE_TOWEL.md`.

## The real target (darryn, 2026-11-08)
**It should feel like real people talking, not LLMs talking to each other.** The numbers are
smoke detectors, not targets: no percentage is a hard limit, and a scene that reads like
real talk passes even if a number is off. The read-aloud test decides.

## Automatic check (`tests/test_dialogue_tics.py`)
Run `python tests/test_dialogue_tics.py` to see the flags. It covers Prologue + Day 1; add each new
day's files to its `STORY` list. The 12 banned lines still in the game sit in its `KNOWN` list; rewrite
pass A removes them (lower each count as you go). For each scan, only banned phrases **fail**. Everything else **flags** the
scene for a read-aloud pass:
- fail: a banned phrase appears, or a rationed one goes over its limit;
- flag: a lot of very short lines (for reference, real talk runs about 36-52% at ≤ 4 words;
  Prologue + Day 1 is 55%);
- flag: a run of 6+ clipped lines;
- flag: no line of 15+ words in a scene (real talk has 11-26%; we have 1.4%);
- flag: a character's average line length drifting far outside their file's range
  (Julian longest, then Leia and Maya, Ryan shortest).

## Workflow for every new day
1. darryn's day plan.
2. Scriptwriter drafts with the character files open.
3. Automatic check, then a "read like a human" rewrite of anything flagged.
4. darryn reads the key scenes. Human taste is the final fix; the tools only
   remove the obvious tells.

## Rewrite pass "A" (approved 2026-11-08)
After darryn signs off these files: rewrite the worst 60-80 exchanges in the
Prologue and the first hour of Day 1, ship as v0.1.1. The NTR choice rework in
Day 1 (honest mistakes instead of jerk behavior) goes out together with Day 2.
