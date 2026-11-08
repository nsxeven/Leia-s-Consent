# Real-dialogue research: summary for darryn (DRAFT, 2026-11-08)

Branch `research/real-dialogue` (off PR #126 `feature/character-voices` @ 6143412). Not merged.
The game is untouched: only `docs/` changed. `main` at research time: 6eda038.

## What changed and why
1. **The diagnosis got sharper.** I measured four real recorded conversations (Santa Barbara
   Corpus). Real people use *lots* of short lines too: 36-52% of turns are 4 words or fewer. What
   our script is missing is the **long, messy turns**: 11-26% of real turns run 15+ words, ours are
   **1.4%**. We also have almost no fillers (2.3 per 100 lines vs roughly 17-41 in real talk), no
   self-corrections and very little laughter. The one clipped real-world sample we found was
   *edited* reality TV (72% short), so our dialogue reads like an edited show, not like people.
2. **New: `docs/research/REAL_DIALOGUE_LEDGER.md`**, with 59 sourced entries: 17 Reddit threads
   read in the Desktop browser, 14 corpus/conversation-research entries, 16 reality-TV, podcast,
   Gottman and film entries (film as contrast only), 11 personality-research entries, and 1 game
   measurement. Every entry has a URL, access date, what was inspected and its limitations.
3. **New: `docs/research/REAL_SPEECH_PATTERNS.md`**: 16 rule sections, each tied to ledger IDs.
   They cover line-length targets per situation, fillers, self-repair, laughter, how partner
   teasing actually works (running bits, not comebacks), roasting, new friends, drinking games,
   jealousy, "are we okay?", suggesting something new / being watched (consent steps), bedroom
   talk and betrayal confrontations.
4. **Character files** (diff against PR #126): each now has a Big Five + attachment profile with
   reasons, a sentence-length range, real-speech habits with sources, and 10 DRAFT sample lines.
   - Leia: O/E/A high, N mid, anxious-leaning but chooses for herself; 6-20 words, the most talkative of the couple.
   - Ryan: E low-mid, A high, avoidant-leaning under conflict ("I'm fine" = NTR seed); 4-12 words, no deadpan verdicts.
   - Julian: E high, secure-leaning but wants approval; 10-30 words, the longest in the cast.
   - Maya: O/E/A high, N low, secure-leaning; 5-18 words in bursts, interrupts, asks the blunt question.
5. **Towel scene rewrite** (`docs/research/SAMPLE_SCENE_TOWEL.md`): short lines went from 82% to
   **31%**, 6+ runs from 1 to 0, banned phrases from 1 ("Exactly.") to 0. Leia now averages 12.5
   words a line and Ryan 6.4 (before: 3.0 and 2.5).
6. `docs/DIALOGUE_STYLE.md` gains a "Research basis" note and one proposed check: every scene
   has at least one 15+-word spoken line.

## Open questions for you
1. ~~Targets: keep "≤35% short lines" as the hard limit?~~ **Decided (darryn):** no hard limit.
   It just has to feel like real people talking, not LLMs. The numbers only flag scenes for a read-aloud.
2. **Profiles:** do the Big Five / attachment picks match how *you* see them? Especially Ryan as
   avoidant-leaning and Julian as secure (not anxious).
3. **Running bits:** what's Ryan and Leia's real dumb joke from home? The research says that's
   how long-term couples tease, and only you can invent it.
4. ~~Towel scene: too forward?~~ **Approved (darryn):** goes into rewrite pass A as written.
5. Still open from PR #126: Leia's pet name for Ryan, jobs, Maya's age and how she knows Ryan.

## What still needs your human ear
- All sample lines are model-written placeholders. The research tells you the *shape*
  (length, mess, who wins), not the words. Swap in lines only these people would say.
- Humor: whether a joke is actually funny can't be measured.
- Consent beats: the rules give the structure (question first, nerves out loud, a way out, a later
  check-in). How sexy or awkward it should feel is your call.
- Read scenes out loud, ideally with someone else.

## Limits of this research
- Reddit: targeted threads (post + visible comments, top sort), not the full Hot/Top x time-period
  sweep. Self-selected people retelling from memory. Comments about minors excluded.
- SBCSAE: a 4-file sample counted by a script (not checked against audio); "like" counts include non-filler uses.
- Reality TV is edited (frankenbites); film is scripted. Both are used for social beats, not timing.
- Personality sources were mostly abstracts or summaries. The profiles are writing tools, not diagnoses.
- Corpus/media/personality entries were gathered by research subagents. I re-ran the corpus
  measurement (same numbers) and spot-checked five sources and their quotes.

## Next step if you approve
Merge the voice files (PR #126 + this branch), add the dialogue-tic unit test, then do rewrite pass A
(the worst 60-80 exchanges in the Prologue and first hour of Day 1 → v0.1.1).
