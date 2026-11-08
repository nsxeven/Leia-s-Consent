# Real speech patterns: sourced rules for Leia's Consent (DRAFT for darryn, 2026-11-08)

Every rule cites entries in `docs/research/REAL_DIALOGUE_LEDGER.md` (IDs in brackets).
Each item is labeled: **Evidence** (what the sources show), **Inference** (our reading
of it), **Rule** (a Suggestion for writers; nothing here is canon until darryn approves).
These rules sit on top of `docs/DIALOGUE_STYLE.md` and don't replace it.

## 0. The headline finding (it changes the diagnosis a little)

**Evidence.** In four real recorded conversations (Santa Barbara Corpus), **36-52% of turns
are 4 words or fewer**, so real people say plenty of short things. What the game is missing
is the *long* turns: **11-26% of real turns run 15+ words, against 1.4% in the game**. The
game has a median of 4 words a line and 54.8% short lines [C02-C05, G01].

| | Turns ≤4 words | Turns ≥15 words | Median words/turn | Fillers per 100 turns* | Laughter-marked units per 100 turns | Cut-offs per 100 turns |
|---|---:|---:|---:|---:|---:|---:|
| SBC002 group chat [C02] | 48.8% | 13.0% | 5 | 22.9 | 23.9 | 26.8 |
| SBC003 domestic talk [C03] | 51.9% | 10.7% | 4 | 20.0 | 12.1 | 18.5 |
| SBC006 two people swapping family stories [C04] | 35.7% | 25.8% | 7 | 40.8 | 57.7 | 57.4 |
| SBC011 two people on retirement [C05] | 42.0% | 14.2% | 6 | 17.3 | 25.2 | 44.1 |
| **Game, Prologue + Day 1 @ 6eda038** [G01] | **54.8%** | **1.4%** | **4** | **2.3** | n/a (narration) | low (38 dash/ellipsis marks in 933 lines) |
| Edited reality TV, Temptation Island bonfire excerpt (18 turns) [M05] | 72.2% | - | 3 | - | - | - |

\*uh, um, like, I mean, you know; "like" includes non-filler uses, so this is an upper bound.

**Inference.** The game doesn't read like people talking. It reads like an *edited* show:
the one clipped sample we measured was edited reality TV [M05, M08]. Editors cut the
"um, so, like, wait" and keep the punchline. Our scripts are doing the same cut by hand.

**Rule.** Don't just make lines longer. Give every scene some long, messy turns (one
person actually explaining, telling, rambling), and keep the short reactions around them.

---

## 1. Line length by situation

**Evidence.** Talk where one person tells something runs long (SBC006: median 7 words,
26% long turns), while multi-party back-and-forth runs short (SBC003: median 4) [C02-C05].
Long turns are built from short pieces: intonation units have a median of 3-4 words [C02-C05].
Hard conversations open with short, hedged bids [R08, R17, M12] and only then get to the
long explanation [M06, R14].

**Rule.** Targets per scene, as a share of spoken lines (Inference from the above, tuned for a VN,
where scripts drop the "mhm"/"yeah" backchannels a recording keeps):

| Situation | ≤4-word lines | 15+-word lines | Notes |
|---|---:|---:|---|
| Partner teasing, quick banter | 30-40% | ≥5% | Short is fine here, but someone has to tell a whole sentence's worth of story. |
| Old friends roasting | 30-40% | ≥10% | Julian's long turns live here [R15]. |
| New friends (Leia + Maya) | 20-30% | ≥15% | Compliments, then stories and questions [R16, M02]. |
| Drinking games / drunk | 25-35% | ≥15% | Rambles plus word-finding repairs [R12]. |
| Jealousy, awkward moments | 35-45% | ≥10% | Short, loaded questions first, then one long outburst or explanation [R06]. |
| "Are we okay?" | 30-40% | ≥15% | Short opener, long answer [R08, R17]. |
| Suggesting something new / being watched | 20-30% | ≥20% | The asker over-explains; the listener asks questions [R01, R03, R04]. |
| Bedroom | 40-55% | ≥5% | The one place where short is natural, but include a flubbed line or a request [R09, M09]. |
| Confrontation / confession | 30-45% | ≥15% | Long justifications, short repeated denials [R14, M04, M05]. |
| **Any scene (hard limits)** | **≤35% outside bedroom scenes** | **≥1 line** | No run of 6+ short lines (DIALOGUE_STYLE.md). |

Write a long line as a chain of short pieces ("I mean, it was fine, and then he said the
thing, and I just—") rather than one polished sentence [C02-C05, C10].

## 2. Fillers and discourse markers

**Evidence.** Fillers show up at roughly 17-41 per 100 turns in the SBCSAE sample, against
2.3 in the game [C02-C05, G01]. "Uh" signals a short delay and "um" a longer one [C10]. "I mean"
warns that a correction is coming, and "you know" invites the listener to fill in the gap [C11].
They are not interchangeable.

**Rule.** About 1 line in 5-8 carries a filler or discourse marker, placed where the speaker is
*searching or deciding*, never sprinkled evenly. Use "I mean" right before a self-correction and
"you know?" when asking for agreement. Spread them by character (see the character files): Leia
uses "like" and "okay but", Ryan uses "I mean" and "I don't know", Julian uses "okay, hear me
out", Maya uses "wait, no" and "because".

## 3. Repair: people fix their own sentences

**Evidence.** Talk strongly prefers *self*-repair: speakers fix their own trouble before
someone else does [C08]. Cut-off words and restarts show up at 18-57 per 100 turns in the sample
[C02-C05]. Listeners ask what someone meant about once every 1.4 minutes, and they use the most
specific check they can ("Sarah?", "the name?") [C09, R12].

**Rule.** Each short scene gets at least one self-correction or cut-off ("I'm not— okay, I
was.") and, about once a scene, a real clarification question ("Wait, what?" that's
actually answered). Drunk scenes double that [R12].

## 4. Timing and interruption

**Evidence.** Replies usually start within about 200 ms, so people plan their answer while the
other person is still talking [C06, C07]. Overlap is often cooperative, not a fight [C14].

**Rule.** Let characters finish each other's sentences, guess wrong, and get corrected. Use the
"—" cut-off for Maya's interruptions and Leia's excited run-ons. When an interruption is hostile,
show it (someone says "let me finish").

## 5. Laughter

**Evidence.** Fewer than 20% of the laughs in Provine's field sample followed anything like a
joke, and speakers laughed about 46% more than their listeners [C12]. In the corpus,
laughter-marked units run at 12-58 per 100 turns [C02-C05]. In bed, laughter breaks the mood
and the couple carries on [R09].

**Rule.** Laughter follows ordinary lines, and the speaker often laughs at their own line.
Show it in narration or `{i}(laughing){/i}`, not with "haha". Not every joke lands: sometimes
the listener just says "what?" [R09].

## 6. Teasing between partners

**Evidence.** Long-term partners tease with *running bits* repeated over years (the same wrong
actor name, deliberate mispronunciations, bad accents), and the target answers with mock
exasperation rather than a comeback [R10]. A tease can get a play-along answer, pushback, or a
completely serious one; the reply matters [C13]. In group teasing, everyone chases one small
detail [M03].

**Rule.** Give Ryan and Leia one or two dumb running bits from home that come back across the
trip. **Allow at most one crisp comeback per scene**. Other replies should be a groan, a laugh,
a literal answer, a serious answer, or a change of subject [R10, R12, C13].

## 7. Old friends roasting (Ryan + Julian, Ryan + Maya)

**Evidence.** Male friends talk around an activity and only "when we have something to say".
Deep talks are "random and you just end up in one" [R15]. Friend groups keep old arguments
alive as jokes [R11]. A crisp, perfect roast stands out precisely because it's rare [R12].

**Rule.** Put Ryan and Julian's serious beats in the middle of doing something (pool, car,
grill), arriving sideways and leaving fast. Their roasts lean on shared history ("remember the
thing in sophomore year") more than clever wording.

## 8. Two women who just met (Leia + Maya)

**Evidence.** Fast female bonding goes compliment → a small thing in common (same watch,
tattoos) → confiding or protecting ("friend mode") [R16]. Early conversation passes through
plain questions about work and life before anything personal [M02].

**Rule.** Leia and Maya's first scene follows that order. Maya asks real questions, and Leia
over-shares a little, then checks whether that was too much.

## 9. Drinking games and drunk talk

**Evidence.** Drinking games produce rules arguments and factions ("argued for minutes") that
become running jokes [R11]. Drunk speech loses names and words, and the group repairs them
together. It also takes requests literally and wanders into odd metaphors [R12]. A drunk
honest blurt is a well-known move (character drafts; no ledger source, so it stays an Inference).

**Rule.** Never Have I Ever needs at least one dispute over whether something "counts", one
name or word someone can't find that the group fills in, and one person going on too long.

## 10. Jealousy and awkward moments

**Evidence.** Jealousy comes out sideways first, as a loaded comparison question, and the honest
version ("I'm feeling self-conscious") only comes once someone calls it out [R06]. People sit on
it for days or longer, afraid of seeming needy [R07]. It turns into an argument about fairness
and history [R13]. People rehearse the complaint with a friend before raising it [M01].

**Rule.** Write the jealous line as a question with a hook ("So is she, like, really funny, or...?").
Let it get answered literally before anyone addresses the real feeling. Let Maya or Julian hear
the complaint before Ryan or Leia does.

## 11. The "are we okay?" conversation

**Evidence.** Real check-ins are short, hedged and often half-joking ("hey, is everything okay
with us?"), and the good answer is brief and warm ("Yup, still love you.") [R08]. Asking for the
need ("I could use some extra love today", "Can I hug you?", "Are we good?") lands better than
fishing ("Do you hate me?", "So I'm just a terrible person.") [R08, R17]. Bids are often
nonverbal, and what matters is whether the partner notices [M12]. The anxious-pursue /
avoidant-withdraw loop ("I need some space" → "do you hate me?") is well documented [R17, P10,
P11, P09].

**Rule.** Open with five words or fewer and a hedge. The reply is either a short, warm "yeah,
we're good, come here" (Love route) or "I'm fine, just tired" followed by visibly turning away
(NTR seed, [P11]). A long talk can follow, but it starts small.

## 12. Suggesting something new in bed, being watched, agreeing on it (consent)

**Evidence.** Women in R01 want it raised outside the moment, as a question, with time to think
and "no" respected. In practice couples often float it as fantasy talk first, then hold a separate
sober conversation ("I was serious, if you're into it") [R03]. Whoever has the wish voices their
fear ("you'll think I want to cheat") and frames it as something for both of them [R04, R03].
Phrasing matters: "I want to share you" sounds one-sided [R03]. When others could see, the people
watching have to be OK with it too [R05]. Preferences get found through small requests and feedback
("I think I like it lighter") [M09]. A partner being "convinced" is pressure, not consent [R02].

**Rule.** Every new-thing scene has: (1) a question rather than a pitch, (2) the asker's own
nerves spoken out loud, (3) a clear way out ("we don't have to, I just wanted to say it"),
(4) the listener asking at least one practical question, (5) a later check-in in plain words.
No one talks anyone into anything. In exhibition beats, keep bystanders as people who chose to
be there or can't actually see.

## 13. Bedroom talk

**Evidence.** Real couples flub compliments, laugh at noises and use private in-jokes in bed [R09].
They ask for specific things and report how it feels in plain words [M09].

**Rule.** Fewer porn-script lines and more small requests ("slower", "like that?", "wait,
hang on, my hair"), one honest laugh, and a check-in that sounds like a person ("you okay?"
rather than a formal consent question).

## 14. Confession and betrayal confrontations

**Evidence.** Real confrontations run over days and loop around one concrete detail (deleted
messages), with the same denial "over and over" and apologies "about 1 million times" [R14]. The
accused narrows the meaning of one word ("I didn't lie, I just didn't say nothing") [M04]. A pet
name gets rejected ("Don't call me that." twice) [M05]. A decisive answer comes only after hedges
[M06]. Each side tells friends a different version [M07].

**Rule.** Spread a betrayal across at least two scenes. Within a scene, let the hurt person
repeat themselves and fixate on one detail, and let the other person argue about what a word
means. A familiar endearment becomes a weapon. No neat speeches that resolve it.

## 15. What real people do that AI dialogue doesn't (and the reverse)

| Real people [sources] | Typical AI / current-game dialogue [G01, F95 feedback] |
|---|---|
| Mix very short reactions with long, wandering turns [C02-C05] | Uniform 3-6-word lines (median 4, 1.4% long) |
| Start over, fix words, lose names [C08, C09, R12] | Every sentence comes out finished and correct |
| Fillers where they're thinking, "I mean" before a correction [C10, C11] | Almost no fillers (2.3 per 100 lines) |
| Laugh at their own ordinary lines [C12] | Laughter only after a punchline, or "smirks" |
| Answer a tease literally, seriously, or with a groan [C13, R10] | Everyone has a comeback ("Exactly." "Pervert.") |
| Bring up hard things late, sideways, after avoiding them [R07, R06] | Characters name their feelings precisely and right away |
| Ask practical questions about a new idea ("what would we even do?") [M16, R01] | The listener agrees or quips immediately |
| Repeat themselves when hurt [R14, M05] | Every line adds new information |
| Keep running bits and old arguments going for years [R10, R11] | Fresh one-off wit in every scene |
| The reverse problem: real talk is full of dead air, "mhm" and repetition that would bore a reader [C02-C05] | A script should keep *some* of the AI's economy. Cut backchannels, keep the mess that carries character. |

## 16. Personality changes how people talk (keep it consistent)

**Evidence.** Word-use style is a stable individual difference [P04]. Extraversion is easy to
hear in everyday talk [P02] and goes with social, positive words. Neuroticism goes with
negative-emotion words, and agreeableness with fewer swear words and more "we" talk [P05, P06].
These effects are modest, though, and no single word is a fingerprint [P03, P04].

**Rule.** Each character file sets a line-length range and 3-5 habits. Under stress the habit
gets stronger (Julian talks more, Ryan less, Leia faster and more questions, Maya blunter); it
doesn't switch to someone else's habit.

## How to check a scene

1. `python <scratch>/tic_scan_file.py <scene excerpt>.rpy`: the share of ≤4-word lines,
   6+ runs, banned phrases and per-speaker averages.
2. Count 15+-word lines by eye or with the same script's per-speaker range (aim for at least 1).
3. Read it out loud with someone else. If you wouldn't say it, rewrite it.
