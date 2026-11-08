# Real dialogue evidence ledger (DRAFT for darryn, 2026-11-08)

Research only. Built on branch `research/real-dialogue` (off `feature/character-voices` @ 6143412, PR #126). The game was not touched; GitHub `main` at research time: 6eda038.

**Who inspected what.** Reddit (R01-R17) was read by the Hermes coordinator in the Hermes Desktop embedded browser pane (logged-in old.reddit view, read-only: no votes, posts, joins or messages). Corpus/CA (C01-C14), media (M01-M16) and personality (P01-P11) entries were gathered by three research subagents; the coordinator re-ran the SBCSAE measurement script (same numbers) and spot-checked five sources and quotes (Temptation Island and Too Hot to Handle transcripts, Gottman soft start-up, the Where Should We Begin? transcript, and Provine's laughter article). G01 is the coordinator's own count of the game.

**Labels.** *Evidence* = seen in the source. *Inference* = our reading. The `Takeaway` line on every entry is a *Suggestion* for writers. Quotes are kept to 1-2 short lines; everything else is paraphrased. No character is based on an identifiable private person: Reddit and podcast material is used only as aggregate patterns.

**Caveats that apply everywhere.** Reddit is self-selected and retold from memory, not recorded speech. Reality TV is edited (see M08 on frankenbites), so its timing and fluency are not natural speech. Film (M15-M16) is scripted and is a contrast only. The SBCSAE numbers come from a four-file sample counted by a script, not checked against audio.

## Coverage

| Source type | Entries | IDs |
|---|---:|---|
| Reddit | 17 | R01, R02, R03, R04, R05, R06, R07, R08, R09, R10, R11, R12, R13, R14, R15, R16, R17 |
| corpus | 5 | C01, C02, C03, C04, C05 |
| CA research | 9 | C06, C07, C08, C09, C10, C11, C12, C13, C14 |
| reality TV | 8 | M01, M02, M03, M04, M05, M06, M07, M08 |
| podcast | 3 | M09, M10, M11 |
| research (relationships) | 3 | M12, M13, M14 |
| scripted film/TV (contrast) | 2 | M15, M16 |
| personality research | 11 | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11 |
| game measurement | 1 | G01 |
| **Total** | **59** | |

Reddit sample: subscriptions checked first (9 subscribed communities, none about real couples' speech), so all 10 subreddits below were *discovered*: r/AskWomen, r/Hotwife, r/sex, r/nonmonogamy, r/polyamory, r/relationship_advice, r/relationships, r/TwoXChromosomes, r/AskMen, r/AskReddit. Threads were found by web search, then opened and read in the pane (post + visible comment tree, sort=top). **Not done:** the full Hot/Top x Today-to-All-time feed sweep, and r/dating (nothing usable for a 4-year couple). Comments about minors were excluded.

## Index by situation

| Situation | Entries |
|---|---|
| How real conversation works (all situations) | R15, C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C11, C12, C14, M08, M12, M15, P01, P02, P03, P04, P05, P06, P07, G01 |
| Bickering and teasing between partners | R09, R10, C02, C12, C13, M03, M14, P03 |
| Old friends roasting each other | R11, R15, C13, M03, P05, P06 |
| Two women who just met becoming fast friends | R16, C03, C10, M02, M11, M15, P01, P02, P03, P05, P06 |
| Drinking games and drunk talk | R11, R12, R16, C06, P02 |
| Flirting | C11, M02, M11, M15, M16, P05, P07, P08 |
| Jealousy and awkward moments | R04, R06, R07, R13, C09, M01, M02, M04, M05, M07, M16, P07, P08, P09, P10 |
| Suggesting something new in bed / being watched / agreeing on it | R01, R02, R03, R04, R05, M09, M16, P08, P11 |
| The "are we okay?" conversation | R07, R08, R17, C04, C05, C08, C11, M01, M06, M07, M09, M10, M12, M13, P04, P07, P08, P09, P10, P11 |
| Bedroom talk | R01, R03, R06, R09, M09, P08 |
| Confession and betrayal confrontations | R05, R14, R17, C07, C13, C14, M04, M05, M06, M07, M10, M11, M13, M14, P09, P10, P11 |

## How real conversation works (all situations)

### C01 · Santa Barbara Corpus of Spoken American English, parts 1–4

- **Type:** corpus · **Also relevant to:** -
- **Source:** https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english (accessed 2026-11-08)
- **Inspected:** UCSB corpus overview, access and contents/summaries sections (HTML downloaded).
- **Finding (Evidence):** The site offers free TRN transcripts and CHAT versions, audio and timestamps aligned at the intonation-unit level; it describes parts 1–4 as approximately 249,000 words.
- **Takeaway (Suggestion):** Treat natural speech as timed, multi-unit interaction, not alternating polished one-liners.
- **Limitations:** The entire corpus includes noncasual genres; the quantitative entries below use a selected four-file sample.

### C02 · SBCSAE SBC002: Lambada

- **Type:** corpus · **Also relevant to:** teasing
- **Source:** https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC002.trn (accessed 2026-11-08)
- **Inspected:** Full SBC002.trn downloaded and parsed with sbcsae/measure.py. Group conversation about dance and a movie. Speaker turns are contiguous timestamped units with same assigned speaker; counts exclude zero-word turns. Text only, no audio listening.
- **Finding (Evidence):** 645 lexical turns: median 5 words; 48.8% <=4 words, 13.0% >=15 words. 1258 lexical intonation units: median 3.0 words (mean 4.02). Filler tokens/phrases uh 15, um 4, like 73, I mean 33, you know 23; 154 laughter-marked units, 616 overlap-opening marks, 173 cut-off marks.
- **Takeaway (Suggestion):** Let one character sustain a thought across several short intonation units and another answer briefly; vary long and short turns.
- **Limitations:** Exploratory four-file convenience sample, not representative of all US talk. Continuation rows inherit most recent named speaker (can misassign amid overlap); fillers are literal matches, like includes lexical uses; bracket openings are notation marks, not interruptions; @/Hx indicates laughter-marked unit, not laughs; hyphens and double dashes are mechanical cut-off proxies.

### C03 · SBCSAE SBC003: Conceptual Pesticides

- **Type:** corpus · **Also relevant to:** new-friends
- **Source:** https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC003.trn (accessed 2026-11-08)
- **Inspected:** Full SBC003.trn downloaded and parsed with sbcsae/measure.py. Multiparty domestic talk about food and peppers. Speaker turns are contiguous timestamped units with same assigned speaker; counts exclude zero-word turns. Text only, no audio listening.
- **Finding (Evidence):** 746 lexical turns: median 4.0 words; 51.9% <=4 words, 10.7% >=15 words. 1454 lexical intonation units: median 3.0 words (mean 3.39). Filler tokens/phrases uh 13, um 27, like 50, I mean 10, you know 49; 90 laughter-marked units, 557 overlap-opening marks, 138 cut-off marks.
- **Takeaway (Suggestion):** Let one character sustain a thought across several short intonation units and another answer briefly; vary long and short turns.
- **Limitations:** Exploratory four-file convenience sample, not representative of all US talk. Continuation rows inherit most recent named speaker (can misassign amid overlap); fillers are literal matches, like includes lexical uses; bracket openings are notation marks, not interruptions; @/Hx indicates laughter-marked unit, not laughs; hyphens and double dashes are mechanical cut-off proxies.

### C04 · SBCSAE SBC006: Cuz

- **Type:** corpus · **Also relevant to:** are-we-okay
- **Source:** https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC006.trn (accessed 2026-11-08)
- **Inspected:** Full SBC006.trn downloaded and parsed with sbcsae/measure.py. Two speakers exchange family news and stories. Speaker turns are contiguous timestamped units with same assigned speaker; counts exclude zero-word turns. Text only, no audio listening.
- **Finding (Evidence):** 392 lexical turns: median 7.0 words; 35.7% <=4 words, 25.8% >=15 words. 1504 lexical intonation units: median 4.0 words (mean 4.18). Filler tokens/phrases uh 18, um 16, like 51, I mean 7, you know 68; 226 laughter-marked units, 562 overlap-opening marks, 225 cut-off marks.
- **Takeaway (Suggestion):** Let one character sustain a thought across several short intonation units and another answer briefly; vary long and short turns.
- **Limitations:** Exploratory four-file convenience sample, not representative of all US talk. Continuation rows inherit most recent named speaker (can misassign amid overlap); fillers are literal matches, like includes lexical uses; bracket openings are notation marks, not interruptions; @/Hx indicates laughter-marked unit, not laughs; hyphens and double dashes are mechanical cut-off proxies.

### C05 · SBCSAE SBC011: This Retirement Bit

- **Type:** corpus · **Also relevant to:** are-we-okay
- **Source:** https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC011.trn (accessed 2026-11-08)
- **Inspected:** Full SBC011.trn downloaded and parsed with sbcsae/measure.py. Talk about retirement and another person. Speaker turns are contiguous timestamped units with same assigned speaker; counts exclude zero-word turns. Text only, no audio listening.
- **Finding (Evidence):** 381 lexical turns: median 6 words; 42.0% <=4 words, 14.2% >=15 words. 830 lexical intonation units: median 3.0 words (mean 3.85). Filler tokens/phrases uh 25, um 4, like 13, I mean 2, you know 22; 96 laughter-marked units, 356 overlap-opening marks, 168 cut-off marks.
- **Takeaway (Suggestion):** Let one character sustain a thought across several short intonation units and another answer briefly; vary long and short turns.
- **Limitations:** Exploratory four-file convenience sample, not representative of all US talk. Continuation rows inherit most recent named speaker (can misassign amid overlap); fillers are literal matches, like includes lexical uses; bracket openings are notation marks, not interruptions; @/Hx indicates laughter-marked unit, not laughs; hyphens and double dashes are mechanical cut-off proxies.

### C06 · Universals and cultural variation in turn-taking in conversation

- **Type:** CA research · **Also relevant to:** drinking/drunk
- **Source:** https://cognitionandculture.net/wp-content/uploads/pnas.0903616106.pdf (accessed 2026-11-08)
- **Inspected:** Full PNAS article PDF downloaded and text extracted; examined methods and response-time distribution/results.
- **Finding (Evidence):** Across 10 languages, measured responses to questions in informal conversations cluster around very short gaps; the highest frequency of transitions falls between 0 and 200 ms, although average offsets differ culturally.
- **Takeaway (Suggestion):** Let the reply often begin almost at completion, with occasional overlap or a meaningful delay rather than a mechanical pause every time.
- **Limitations:** Measured question–answer transitions, not every turn; PDF font extraction mangles some minus signs and symbols, so no inferred median is quoted.

### C07 · Timing in turn-taking and its implications for processing models of language

- **Type:** CA research · **Also relevant to:** confrontation
- **Source:** https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2015.00731/full (accessed 2026-11-08)
- **Inspected:** Full Frontiers HTML article downloaded and read, especially abstract and timing/planning discussion.
- **Finding (Evidence):** The article describes average interturn gaps around 200 ms, versus speech-production latencies above 600 ms; prospective responders therefore begin planning while they are still listening.
- **Takeaway (Suggestion):** Write replies that latch onto a projected ending, including mistaken anticipation and late course correction.
- **Limitations:** Timing generalization is across analyzed conversational datasets, not a prescription for every emotionally loaded pause.

### C08 · The preference for self-correction in the organization of repair in conversation

- **Type:** CA research · **Also relevant to:** are-we-okay
- **Source:** https://www.cambridge.org/core/journals/language/article/abs/preference-for-selfcorrection-in-the-organization-of-repair-in-conversation/5549B861FDE7180B75FA5C382821875E (accessed 2026-11-08)
- **Inspected:** Cambridge article landing page and abstract downloaded; full paper was access-gated.
- **Finding (Evidence):** The abstract identifies a conversational organization addressing trouble in speaking, hearing and understanding, with a strong empirical skew toward self-repair rather than correction by others.
- **Takeaway (Suggestion):** Let a speaker fix their own phrasing before a listener supplies the polished version.
- **Limitations:** Abstract only; no claim about exact repair rates or detailed sequential mechanisms.

### C09 · Universal principles in the repair of communication problems

- **Type:** CA research · **Also relevant to:** jealousy/awkward
- **Source:** https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0136100 (accessed 2026-11-08)
- **Inspected:** Full PLOS HTML article downloaded; read abstract and frequency/types sections.
- **Finding (Evidence):** Other-initiated repair appears on average about once per 1.4 minutes in the languages sampled; speakers use open, restricted and candidate-understanding requests and favor the most specific usable one.
- **Takeaway (Suggestion):** When something is missed, use a targeted check (the name? this Friday?) rather than a universal Huh? every time.
- **Limitations:** Cross-linguistic conversation sample; 1.4 minutes is an aggregate, not an individual-scene quota.

### C10 · Using uh and um in spontaneous speaking

- **Type:** CA research · **Also relevant to:** new-friends
- **Source:** https://www.columbia.edu/~rmk7/HC/HC_Readings/Clark_Fox.pdf (accessed 2026-11-08)
- **Inspected:** Full Cognition article PDF downloaded and text extracted; read abstract, proposal and reported contrast in following delays.
- **Finding (Evidence):** Their proposal treats uh as announcing a relatively minor expected delay and um a more substantial one; their data show sharper differences in following than preceding delays.
- **Takeaway (Suggestion):** Put a filler where a character is holding the floor while searching or deciding, not evenly across sentences.
- **Limitations:** Interpretation of fillers is a proposed account, not an invariant meaning; PDF text extraction contains minor font/ligature artifacts.

### C11 · Basic meanings of you know and I mean

- **Type:** CA research · **Also relevant to:** flirting, are-we-okay
- **Source:** https://www.maryvillecollege.edu/wp-content/uploads/Faculty/BehavioralSciences/cschrock/Fox-Tree-and-Schrock-2002.pdf (accessed 2026-11-08)
- **Inspected:** Full Journal of Pragmatics article PDF downloaded and text extracted; read abstract and opening discussion.
- **Finding (Evidence):** The article analyzes you know as inviting listener inference and I mean as warning of a coming adjustment; these phrases are not interchangeable filler.
- **Takeaway (Suggestion):** Use you know to enlist shared understanding, and I mean when a speaker revises or qualifies what was just said.
- **Limitations:** The basic-meaning analysis is the authors’ synthesis; individual tokens can have context-sensitive functions.

### C12 · Laughter

- **Type:** CA research · **Also relevant to:** teasing
- **Source:** http://cogweb.ucla.edu/Abstracts/Provine_96.html (accessed 2026-11-08)
- **Inspected:** Full American Scientist article HTML downloaded; read field-observation, punctuation-effect and speaker-versus-audience passages.
- **Finding (Evidence):** In the reported field observations, fewer than 20% of sampled laughs responded to structured jokes or stories; speakers laughed about 46% more often than audiences, and laughter tended to punctuate speech rather than interrupt it mid-phrase.
- **Takeaway (Suggestion):** Let the speaker laugh at their own ordinary remark and allow the listener to respond without a laugh.
- **Limitations:** This is a 1996 popular-science account of fieldwork, not a directly analyzed full 1993 journal article; observation context and definitions matter.

### C14 · Overlapping talk and the organization of turn-taking for conversation

- **Type:** CA research · **Also relevant to:** confrontation
- **Source:** https://www.cambridge.org/core/journals/language-in-society/article/overlapping-talk-and-the-organization-of-turntaking-for-conversation/D12AD4181BEEFB073869BE7C55B07660 (accessed 2026-11-08)
- **Inspected:** Cambridge article landing page and abstract downloaded; full PDF not inspected.
- **Finding (Evidence):** The abstract distinguishes overlapping talk as an interactional phenomenon participants sometimes treat as problematic and resolve through organized practices; simultaneous speech is not automatically equivalent to hostile interruption.
- **Takeaway (Suggestion):** Make overlapping talk context-dependent, and show whether participants yield, persist, or repair the collision.
- **Limitations:** Abstract only; no numerical overlap rate or detailed examples inspected.

### M08 · Frankenbites 101: Reality TV Editing

- **Type:** reality TV · **Also relevant to:** -
- **Source:** https://postaudiotips.beehiiv.com/p/frankenbites-101-reality-tv-editing (accessed 2026-11-08)
- **Inspected:** Audio editor Vanessa Flores's article on assembling interview snippets and altering breath timing, crossfades, stretch and pitch.
- **Finding (Evidence):** The editor describes joining fragments from different parts of an interview into grammatically coherent sentences and manipulating timing and inflection to hide seams; apparent fluency or timing on a reality show therefore cannot be treated as a raw conversational measurement.
- **Takeaway (Suggestion):** Use edited TV for social beats and conflict loops, not for a model of untouched everyday timing.
- **Limitations:** Practitioner article about reality production generally, not proof any particular episode here was frankenbitten.

### P01 · Big Five Personality Traits: The 5-Factor Model of Personality

- **Type:** personality research · **Also relevant to:** new-friends
- **Source:** https://www.simplypsychology.org/big-five-personality.html (accessed 2026-11-08)
- **Inspected:** Browser-rendered overview and trait definitions
- **Finding (Evidence):** O describes openness to novelty; C organization and self-discipline; E sociability and talkativeness; A compassion and cooperation; N negative emotional reactivity. Traits are continua, not four-letter types.
- **Takeaway (Suggestion):** Use high/mid/low as drafting contrasts rather than diagnoses or fixed dialogue rules.
- **Limitations:** Educational synthesis, not a primary experiment.

### P02 · Personality in its natural habitat: Manifestations and implicit folk theories of personality in daily life

- **Type:** personality research · **Also relevant to:** new-friends, drinking/drunk
- **Source:** https://experts.arizona.edu/en/publications/personality-in-its-natural-habitat-manifestations-and-implicit-fo/ (accessed 2026-11-08)
- **Inspected:** University of Arizona publication page and abstract
- **Finding (Evidence):** An EAR sampled ambient sounds from 96 people across two days; Big Five scores related to everyday social interaction, moods, activities, and language, and listeners judged extraversion especially well from the audio. Many manifestations were gender-specific.
- **Takeaway (Suggestion):** Make extraversion audible through social initiative and interactive energy, but do not assert an exact words-per-line effect from this abstract.
- **Limitations:** Abstract does not report individual word-category coefficients or a universal verbosity threshold; short observation window.

### P03 · Using Linguistic Cues for the Automatic Recognition of Personality in Conversation and Text

- **Type:** personality research · **Also relevant to:** teasing, new-friends
- **Source:** https://www.jair.org/index.php/jair/article/view/10520 (accessed 2026-11-08)
- **Inspected:** JAIR article landing page and full abstract; PDF link itself was not text-extractable
- **Finding (Evidence):** Big Five prediction from conversational and written linguistic features exceeded baseline for some traits; ranking models performed best overall, observer ratings were easier to model than self-reports, and optimal features varied by trait.
- **Takeaway (Suggestion):** Differentiate several cues together (turn length, social focus, stance) rather than assigning a single signature word.
- **Limitations:** Abstract gives no robust trait-specific words or effect sizes; prediction is imperfect and context-sensitive.

### P04 · Linguistic styles: language use as an individual difference

- **Type:** personality research · **Also relevant to:** are-we-okay
- **Source:** https://pubmed.ncbi.nlm.nih.gov/10626371/ (accessed 2026-11-08)
- **Inspected:** PubMed abstract
- **Finding (Evidence):** Word-use dimensions showed consistency across multiple writing samples and corresponded modestly with personality measures; linguistic style supplies information beyond story content.
- **Takeaway (Suggestion):** Keep recurring stylistic tendencies across situations, with stress-driven changes rather than a catchphrase per person.
- **Limitations:** Written diaries and assignments, not direct dialogue; authors explicitly describe modest effect sizes.

### P05 · The links between bloggers’ personalities and their use of words

- **Type:** personality research · **Also relevant to:** roasting, flirting, new-friends
- **Source:** https://www.bps.org.uk/research-digest/links-between-bloggers-personalities-and-their-use-words (accessed 2026-11-08)
- **Inspected:** British Psychological Society Research Digest article body
- **Finding (Evidence):** In 694 bloggers, higher neuroticism tracked more negative-emotion words, extraversion more positive-emotion words, agreeableness fewer swear words and more communality words, and conscientiousness more achievement words. Openness associated with more prepositions and formal, longer words rather than the expected intellectual/sensory categories.
- **Takeaway (Suggestion):** Use group/social and positive words for sociable voices; negative appraisal when threatened; allow an agreeable roaster to soften insults.
- **Limitations:** Secondary summary of long-form blog writing; correlations do not dictate single lines, and the sample was predominantly female.

### P06 · Bloggers’ reveal personalities with word choice

- **Type:** personality research · **Also relevant to:** new-friends, roasting
- **Source:** https://www.colorado.edu/asmagazine/2010/12/01/bloggers-reveal-personalities-word-choice (accessed 2026-11-08)
- **Inspected:** University of Colorado article body
- **Finding (Evidence):** The university report describes specific-word associations in bloggers; neuroticism accompanied negative adjectives such as terrible/worse, while extraversion accompanied social-outing terms.
- **Takeaway (Suggestion):** Give worried characters occasional negative appraisal, not a rote trait-word checklist; let extroverts frame events as shared experiences.
- **Limitations:** University news coverage, not the paper; written blog correlations and particular keywords are poor prescriptions for spoken fiction.

### P07 · Romantic love conceptualized as an attachment process

- **Type:** personality research · **Also relevant to:** flirting, jealousy/awkward, are-we-okay
- **Source:** https://pubmed.ncbi.nlm.nih.gov/3572722/ (accessed 2026-11-08)
- **Inspected:** PubMed abstract
- **Finding (Evidence):** Two questionnaire studies extended secure, avoidant, and anxious/ambivalent attachment ideas to adult romantic love; groups differed in romantic experience and relationship models.
- **Takeaway (Suggestion):** Treat attachment as a relational stress tendency, not a complete personality or a predetermined outcome.
- **Limitations:** Original categorical model and self-report design; not evidence that any one line proves an attachment style.

### G01 · Leia's Consent Prologue + Day 1 spoken lines (baseline)

- **Type:** game measurement · **Also relevant to:** -
- **Source:** https://github.com/nsxeven/Leia-s-Consent/tree/6eda038 (accessed 2026-11-08)
- **Inspected:** game/chapters/prologue.rpy and ch01_main / ch01_scenes_04_06 / 07_13 / 14_30 at origin/main 6eda038, counted with scratch/tic_scan.py and scratch/game_turn_stats.py (same spoken-line rule).
- **Finding (Evidence):** 933 spoken lines, median 4 words; 54.8% are 4 words or fewer, only 1.4% are 15+ words; 16 runs of 6+ short lines. Fillers (uh/um/like/I mean/you know): 21 tokens = 2.3 per 100 lines. Ryan 4.6, Leia 4.5, Julian 5.0 words per line on average, each with 1-2% long lines. 'Exactly.' x12.
- **Takeaway (Suggestion):** The gap to real speech is the missing long turns and missing speech mess (fillers, repairs, laughter), more than the share of short lines.
- **Limitations:** A VN line is not exactly a conversational turn (backchannels like 'mhm' are usually cut in scripts); counts use the tic_scan spoken-line regex, which skips narration.

## Bickering and teasing between partners

### R10 · r/AskMen: What little thing do you do to tease/annoy your SO?

- **Type:** Reddit · **Also relevant to:** -
- **Source:** https://old.reddit.com/r/AskMen/comments/7s5kdl/ (accessed 2026-11-08)
- **Inspected:** Top ~30 of 155 comments with replies, sort=top, Desktop pane.
- **Finding (Evidence):** Long-term partner teasing is mostly repeated running bits rather than one-liners: mispronouncing names 'with total confidence, straight faced', giving the same wrong actor name to every question until she 'finally snaps', interrupting her story with 'Go on.', bad accents for an hour. The target's response is mock exasperation; a woman says if he stopped she'd be really upset.
- **Quote:** "......thats gary oldman dear"
- **Takeaway (Suggestion):** Give Ryan and Leia one or two long-running dumb bits; the payoff is the other person's groan, not a counter-quip.
- **Limitations:** 2018 thread; men describing their own teasing (self-flattering); humor threads favor the funniest examples.

### C13 · Jocular mockery, (dis)affiliation and face

- **Type:** CA research · **Also relevant to:** roasting, confrontation
- **Source:** https://research-repository.griffith.edu.au/items/63d55628-9950-5217-a906-b2c0299ba156 (accessed 2026-11-08)
- **Inspected:** Griffith repository record and full abstract downloaded; manuscript listed but not opened.
- **Finding (Evidence):** The abstract treats jocular mockery as an interactional move whose responses can align or disalign with earlier action and index affiliation or disaffiliation as relationships evolve.
- **Takeaway (Suggestion):** After a tease, write the target’s reaction as consequential: play along, resist, or answer seriously; do not guarantee a joke in return.
- **Limitations:** Abstract only; no transcript examples or quantified frequency of reactions inspected.

### M14 · R is for Repair — Gottman Institute

- **Type:** research (relationships) · **Also relevant to:** confrontation
- **Source:** https://www.gottman.com/blog/r-is-for-repair/ (accessed 2026-11-08)
- **Inspected:** Gottman Institute article definition of repair attempts and examples of mutually agreed interruption gestures.
- **Finding (Evidence):** A repair can be any action, even silly, that stops escalation; the article's example is a couple agreeing on a playful physical signal, while warning that an uninvited 'calm down' is unhelpful.
- **Takeaway (Suggestion):** Give the established couple one idiosyncratic, mutually understood de-escalation cue rather than a stock quip.
- **Limitations:** Prescriptive relationship writing with an anecdotal couple example, not a controlled transcript; a cue may fail depending on context.

## Old friends roasting each other

### R15 · r/AskMen: Someone told me that most guys don't just call each other up to chitchat...

- **Type:** Reddit · **Also relevant to:** general
- **Source:** https://old.reddit.com/r/AskMen/comments/1lpj1np/ (accessed 2026-11-08)
- **Inspected:** First ~25 comments with replies of 1,061 (top 200 view), Desktop pane.
- **Finding (Evidence):** Male friends talk around an activity ('we talk when we have something to say'); a call from a long-time best friend implies an emergency, so some open with 'nobody died'; deep talks are 'random and you just end up in one'. One reconstructed call: five inappropriate jokes and twenty minutes complaining about work.
- **Quote:** "We can still have deep conversations, but they're usually random and you just end up in one."
- **Takeaway (Suggestion):** Put Ryan and Julian's serious beats in the middle of doing something (pool, driving, grill), arriving sideways.
- **Limitations:** Gender generalizations that commenters themselves flag; disagreement present.

### M03 · Too Hot to Handle, season 3 episode 3: morning-after rule-breaker banter

- **Type:** reality TV · **Also relevant to:** teasing
- **Source:** https://subslikescript.com/series/Too_Hot_to_Handle-12004280/season-3/episode-3-The_Truth_Hurts (accessed 2026-11-08)
- **Inspected:** Full transcript, opening group breakfast exchange about sleeping arrangements and kissing penalties.
- **Finding (Evidence):** A group turns an evasive answer into escalating concrete questions, repeat-back, a pillow joke and small overlapping echo reactions; confessional explanation is intercut, not part of the breakfast conversation.
- **Quote:** "Where'd it go? / It found some legs and just crawled out."
- **Takeaway (Suggestion):** For group teasing, let several people pursue one small factual detail rather than giving everyone a polished comeback.
- **Limitations:** Edited reality TV; music, narrator, confessionals, and unsignaled speaker changes interrupt the subtitle-like transcript; champagne appears in another episode, but this breakfast does not establish drunkenness.

## Two women who just met becoming fast friends

### R16 · r/AskWomen: What is your favourite personal drunk-girl/s-in-a-club/bar-bathroom story?

- **Type:** Reddit · **Also relevant to:** drinking/drunk
- **Source:** https://old.reddit.com/r/AskWomen/comments/9tmps4/ (accessed 2026-11-08)
- **Inspected:** All 37 comments, sort=top, Desktop pane.
- **Finding (Evidence):** Women who just met bond fast in a set order: a compliment ('how pretty you are'), a shared small thing (same watch, tattoos), then confiding or protecting ('went into friend mode'; a staged 'It's been ages!' to rescue a stranger from a creep). Over-sharing and confident wrong stories are common; one met a lifelong best friend this way.
- **Quote:** "Should I text Jake?" Every girl waiting in line, in unison: "No"
- **Takeaway (Suggestion):** Leia and Maya's friendship: compliment first, a tiny shared thing second, a protective or confiding moment third.
- **Limitations:** 8-year-old anecdote thread, selected for memorable stories.

## Drinking games and drunk talk

### R11 · r/AskReddit: What's the dumbest argument you've ever had with a partner or friend?

- **Type:** Reddit · **Also relevant to:** roasting
- **Source:** https://old.reddit.com/r/AskReddit/comments/1tto156/ (accessed 2026-11-08)
- **Inspected:** All 12 comments, sort=top, Desktop pane.
- **Finding (Evidence):** A drinking-game rule dispute (does no/know count as a rhyme?) split friends into factions and they 'argued for minutes'; the commenter still brings it up as a joke. Trivial-fact fights (concave vs convex) get settled absurdly, and friends mock the loser.
- **Quote:** "Sounds like you lost twice that day"
- **Takeaway (Suggestion):** Drinking games produce rules-lawyering and side arguments that become callbacks later in the trip.
- **Limitations:** Small, recent thread; anecdotes.

### R12 · r/AskReddit: Funniest thing your drunk friend has ever said?

- **Type:** Reddit · **Also relevant to:** -
- **Source:** https://old.reddit.com/r/AskReddit/comments/nmmyl/ (accessed 2026-11-08)
- **Inspected:** Top ~25 comment threads, sort=top; underage/high-school anecdotes excluded.
- **Finding (Evidence):** Drunk talk: name and word retrieval failures that the group repairs together ('You know Sarah?' / 'Sarah?' / '...your girlfriend Sam?' / 'Yeah, that's the one'), requests acted on literally, confident non-sequiturs and loose metaphors. The one crisp sober comeback in the thread is singled out by readers as Churchill-level wit, which shows crisp comebacks stand out because they're rare.
- **Quote:** "Do you mean Sam.. your girlfriend Sam?" / "Yeah, that's the one"
- **Takeaway (Suggestion):** Drunk characters lose words and the group repairs them; reserve one sharp comeback per scene at most.
- **Limitations:** 14-year-old humor thread; heavily selected for funniness.

## Flirting

### M02 · Love Island USA, season 2 episode 20: asking for a one-on-one chat

- **Type:** reality TV · **Also relevant to:** new-friends, jealousy/awkward
- **Source:** https://subslikescript.com/series/Love_Island-8819906/season-2/episode-20-Episode_220 (accessed 2026-11-08)
- **Inspected:** Full episode transcript, Aaron requesting a private conversation with Sher and discussion of other connections.
- **Finding (Evidence):** The invitation happens publicly, includes a joking refusal and reassurance from the current partner, then shifts to banal questions about work and life goals before romantic availability is probed.
- **Quote:** "I WANTED TO TALK TO YOU ONE-ON-ONE. / HOW DO YOU FEEL?"
- **Takeaway (Suggestion):** Start a romantic check-in with logistical permission and ordinary questions rather than an immediate confession.
- **Limitations:** Edited broadcast conversation; all-caps transcript may collapse speakers and omit pauses.

### M11 · Modern Love: Myha'la's Relationship Advice? Get in a Fight

- **Type:** podcast · **Also relevant to:** new-friends, confrontation
- **Source:** https://podcasts.happyscribe.com/modern-love/myha-la-s-relationship-advice-get-in-a-fight (accessed 2026-11-08)
- **Inspected:** HappyScribe transcript, first six minutes of host interview about early messages and attraction; episode introduction to discussion of arguments.
- **Finding (Evidence):** A host asks for a remembered specific question; the guest admits she cannot recall it, then reconstructs feelings and mundane details such as an interview request, timing and a bottle of wine. A recollection of attraction is far messier than a perfect flirt exchange.
- **Quote:** "I couldn't tell you, honestly."
- **Takeaway (Suggestion):** Let a recollection fail on a factual detail and detour through ordinary logistics before returning to emotion.
- **Limitations:** Hosted, edited interview, not the couple talking to each other; automated transcript misrenders names and capitalization.

### M15 · Before Sunrise (1995): train conversation

- **Type:** scripted film/TV (contrast) · **Also relevant to:** new-friends, general
- **Source:** https://www.springfieldspringfield.co.uk/movie_script.php?movie=before-sunrise (accessed 2026-11-08)
- **Inspected:** Film dialogue transcript from train meeting through extended imagined TV-show digression.
- **Finding (Inference):** Questions about language and travel elicit an overlong false start about speaking French, and a mundane trip report unexpectedly expands into an elaborate TV-show idea; the other person interrupts and mocks its premise without ending the connection.
- **Quote:** "It sucked. / What?"
- **Takeaway (Suggestion):** Let one partner take a long, peculiar detour and let the other puncture it with a short, concrete objection.
- **Limitations:** Fully scripted and performed; coherent digression and elegant callbacks are writerly craft, not evidence of everyday frequency.

### M16 · Before Sunrise (1995): Vienna invitation

- **Type:** scripted film/TV (contrast) · **Also relevant to:** consent/new-things, jealousy/awkward
- **Source:** https://www.springfieldspringfield.co.uk/movie_script.php?movie=before-sunrise (accessed 2026-11-08)
- **Inspected:** Film dialogue transcript at the train's Vienna stop, invitation, practical questions and hesitant acceptance.
- **Finding (Inference):** A wish to keep talking meets questions about what they would do and how travel would work; the inviter offers the option of the next train but then gives an improbably complete imagined-future monologue to persuade her.
- **Quote:** "What would we do? / I don't know."
- **Takeaway (Suggestion):** Borrow the uncertain practical follow-up and explicit exit option, not the perfectly structured persuasion speech.
- **Limitations:** Scripted contrast only; not evidence of real-world consent practices or average speech patterns.

### P08 · A Brief Overview of Adult Attachment Theory and Research

- **Type:** personality research · **Also relevant to:** jealousy/awkward, consent/new-things, are-we-okay, bedroom
- **Source:** https://labs.psychology.illinois.edu/~rcfraley/attachment.htm (accessed 2026-11-08)
- **Inspected:** Researcher-authored overview, including adult individual differences and anxiety/avoidance sections
- **Finding (Evidence):** Adult attachment is commonly described on anxiety and avoidance dimensions; anxious people may worry they are not fully loved and react when needs go unmet, while avoidant people may downplay dependence. Responsive partners support exploration.
- **Takeaway (Suggestion):** Distinguish Leia’s reassurance check from her agency in choosing; Ryan’s minimization can coexist with real concern.
- **Limitations:** Overview synthesizes studies; orientations are dimensions and context-dependent, not diagnoses or gender rules.

## Jealousy and awkward moments

### R06 · r/nonmonogamy: Tips for responding to jealous questioning

- **Type:** Reddit · **Also relevant to:** bedroom
- **Source:** https://old.reddit.com/r/nonmonogamy/comments/zviv7c/ (accessed 2026-11-08)
- **Inspected:** Post + ~40 comments and replies, sort=top, Desktop pane.
- **Finding (Evidence):** Jealousy shows up sideways: a comparison question while cuddling, then a flurry of follow-ups. Partners describe naming it ('that was really passive aggressive... what are you actually trying to express?') and the jealous person learning to say the real feeling plainly (insecure about her body). Asked how to help, the jealous partner snaps 'You can answer my questions!'
- **Quote:** "I'll bet you enjoy feeling her breasts more than mine. Do you?"
- **Takeaway (Suggestion):** Write jealousy as an indirect, loaded question first, and the honest version ('I'm feeling self-conscious') only after it's called out.
- **Limitations:** Single couple's situation plus advice; non-monogamous context differs from the game's opening state.

### R07 · r/polyamory: how much of your jealousy do you actually share with your partner?

- **Type:** Reddit · **Also relevant to:** are-we-okay
- **Source:** https://old.reddit.com/r/polyamory/comments/1k12sqs/ (accessed 2026-11-08)
- **Inspected:** Post + OP update + 26 comments, sort=top, Desktop pane.
- **Finding (Evidence):** OP held back insecurities fearing she'd seem 'too needy'; it turned out her partner also wanted to check in but felt insecure too. Commenters process alone first; one sat on a feeling for a month before raising it; jealousy often translates to a plain need ('I wanna do this activity too'); partners notice you 'feeling funky' and ask later.
- **Takeaway (Suggestion):** Hard talks arrive late, after both people have avoided them; the trigger is often small and the ask underneath is concrete.
- **Limitations:** Poly-specific community; self-reports.

### R13 · r/relationships: My boyfriend [23M] is jealous of my male friend [24M]...

- **Type:** Reddit · **Also relevant to:** -
- **Source:** https://old.reddit.com/r/relationships/comments/4dr3d5/ (accessed 2026-11-08)
- **Inspected:** 10 comments, sort=top; OP body removed.
- **Finding (Evidence):** Commenters frame jealousy of a partner's friend as fairness (she had made him drop two female friends); one suggests a plain reassurance in the form 'I am dating you because I want to be dating you'; another sympathizes because of his own past betrayal.
- **Takeaway (Suggestion):** Jealousy arguments quickly become about fairness and past history, not just the present friend.
- **Limitations:** THIN: post removed, 10 comments, 10 years old.

### M01 · Love Island USA, season 2 episode 20: attention after recoupling

- **Type:** reality TV · **Also relevant to:** are-we-okay
- **Source:** https://subslikescript.com/series/Love_Island-8819906/season-2/episode-20-Episode_220 (accessed 2026-11-08)
- **Inspected:** Full episode transcript, opening morning conversation about time together after the recoupling.
- **Finding (Evidence):** A complaint about not getting one-on-one time is rehearsed with a friend first; the speaker simultaneously praises her new partner and asks for attention, while the friend briefly jokes about neediness.
- **Quote:** "BUT LET ME SPEND TIME WITH HIM."
- **Takeaway (Suggestion):** Let a partner test a complaint with a friend and qualify it before saying what they want.
- **Limitations:** Edited reality TV, not spontaneous continuous conversation; transcript has all-caps text, garbled names, and weak speaker attribution.

### M07 · Bachelor in Paradise season 9 episode 6 recap

- **Type:** reality TV · **Also relevant to:** are-we-okay, confrontation
- **Source:** https://deadline.com/2023/11/bachelor-in-paradise-season-9-episode-6-recap-abc-1235591496/ (accessed 2026-11-08)
- **Inspected:** Deadline's episode recap paragraphs describing Kat and Tanner's breakup, plus Jess and Blake's pre-date conversation.
- **Finding (Evidence):** The recap describes a partner naming a specific hurt before the other explains an alternative connection; after separating, each gives the friend group a different face-saving account. Another pair recognizes their own prior wish to explore options while still feeling rejected when the other does it.
- **Takeaway (Suggestion):** Make the public retelling of a disagreement different from the private one, especially when both want to save face.
- **Limitations:** Journalist's paraphrase, not a transcript; edited reality TV; no claims about exact turn length or wording.

### P09 · Conflict in Close Relationships: An Attachment Perspective

- **Type:** personality research · **Also relevant to:** are-we-okay, confrontation
- **Source:** https://experts.umn.edu/en/publications/conflict-in-close-relationships-an-attachment-perspective/ (accessed 2026-11-08)
- **Inspected:** University of Minnesota publication abstract
- **Finding (Evidence):** In videotaped dating-couple problem discussions, more ambivalent participants evaluated the partner/relationship less positively after a major issue; ambivalent women in this sample showed stronger stress and more negative behavior, while more avoidant men appeared less warm and supportive on major issues.
- **Takeaway (Suggestion):** In the bad route, let Leia seek clarity while Ryan’s visible warmth drops; do not transplant sample-specific gender effects into every scene.
- **Limitations:** Abstract only; conditional effects in a particular sample, not proof of exact phrasing.

### P10 · The longitudinal impact of demand and withdrawal during marital conflict

- **Type:** personality research · **Also relevant to:** are-we-okay, confrontation
- **Source:** https://pubmed.ncbi.nlm.nih.gov/7593873/ (accessed 2026-11-08)
- **Inspected:** PubMed abstract
- **Finding (Evidence):** Forty-eight couples completed recorded problem-solving discussions; demandingness and, to a lesser extent, withdrawal correlated with satisfaction, and withdrawal by men plus woman-demand/man-withdraw around woman-identified issues predicted wives’ satisfaction decline over follow-up.
- **Takeaway (Suggestion):** Show the escalating loop rather than treating either person as the sole villain: more questions, then clipped replies and retreat, then further pursuit.
- **Limitations:** Observational associations in married couples; this does not establish causation or universal sex roles.

## Suggesting something new in bed / being watched / agreeing on it

### R01 · r/AskWomen: Your partner wants to try something really weird in bed... How would you want to be approached about it?

- **Type:** Reddit · **Also relevant to:** bedroom
- **Source:** https://old.reddit.com/r/AskWomen/comments/3ddd8i/ (accessed 2026-11-08)
- **Inspected:** Post (author deleted) + all 20 visible comments, sort=top, read in Hermes Desktop embedded pane.
- **Finding (Evidence):** Top answers want it raised outside an intimate moment, as a question about how she feels, with time to think, and with 'no' accepted as final. Suggested openers are small questions ('would you be willing to try X?', 'is there anything you really enjoy?') or a feeler ('Have you ever heard of X?') before admitting the wish.
- **Quote:** "Don't spring it on me in the middle of a sexual moment."
- **Takeaway (Suggestion):** The asker leads with a question and a way out, not a pitch; the listener gets a beat to think rather than answering instantly.
- **Limitations:** 2015 thread, 20 comments, self-selected women on one subreddit; OP deleted.

### R02 · r/Hotwife: How did you bring it up for the first time?

- **Type:** Reddit · **Also relevant to:** -
- **Source:** https://old.reddit.com/r/Hotwife/comments/1fi0aa/ (accessed 2026-11-08)
- **Inspected:** 7 comments, sort=top (post body removed), Desktop pane.
- **Finding (Evidence):** Couples report it starting as a playful 'what's your fantasy' game or fantasy talk while apart; one partner was shy and reluctant at first and warmed up over time. One top comment frames it as needing to 'convince her', which is pressure, not consent.
- **Takeaway (Suggestion):** Let the idea surface as a game or hypothetical first; never write the partner being talked into it.
- **Limitations:** 2013, tiny thread, community of practitioners (survivorship bias); post removed; one comment shows a coercive attitude the game must not copy.

### R03 · r/Hotwife: How did you initially bring up the subject with your wife?

- **Type:** Reddit · **Also relevant to:** bedroom
- **Source:** https://old.reddit.com/r/Hotwife/comments/261ekl/ (accessed 2026-11-08)
- **Inspected:** Post + 7 comments, sort=top, Desktop pane.
- **Finding (Evidence):** A two-step pattern: fantasy talk during sex first, then a separate sober conversation ('post-sex pillow talk') saying he was serious only if she was interested. She was uncertain and worried it was really about him; it helped to frame it as something for the couple and to say he respected her decision. A commenter warns about one-sided phrasing.
- **Quote:** "Telling her "I want to share you" sounds one sided"
- **Takeaway (Suggestion):** Show the heat-of-the-moment fantasy AND the later plain-language follow-up where she can say no; give the listener a worry ('is this about you?') that gets answered.
- **Limitations:** 2014, 7 comments, practitioner community; one commenter recommends raising it mid-arousal, which conflicts with R01.

### R04 · r/sex: How do I tell my partner about my exhibitionism fantasy?

- **Type:** Reddit · **Also relevant to:** jealousy/awkward
- **Source:** https://old.reddit.com/r/sex/comments/1taqcfa/ (accessed 2026-11-08)
- **Inspected:** AutoModerator-preserved post text + 10 comments, sort=top, Desktop pane.
- **Finding (Evidence):** A woman wants to be watched with her partner included and fears he will think she wants to cheat. Advice: say it plainly and completely (half-telling reads as manipulative), make clear it only happens if he wants it too, and watch that he doesn't take over her fantasy as his.
- **Quote:** "I want to do all this with him included."
- **Takeaway (Suggestion):** When Leia raises being watched, give her the fear ('you'll think I want someone else') out loud, and have the plan hinge on both of them agreeing.
- **Limitations:** ~6 months old, 10 comments; post removed by mods (text preserved by bot); advice quality varies.

### R05 · r/sex: My gf's exhibitionism is rising and I need to have a delicate conversation...

- **Type:** Reddit · **Also relevant to:** confrontation
- **Source:** https://old.reddit.com/r/sex/comments/qw3gjv/ (accessed 2026-11-08)
- **Inspected:** Top ~10 comment branches of 254 comments (sort=top) to the practical limit; post body removed.
- **Finding (Evidence):** Top replies: the partner has a voice ('It makes me uncomfortable when you...'); bystanders who did not agree must not be involved; ask which specific part is uncomfortable before setting a boundary; start by validating her excitement, then the limit. The thread drifts into side arguments about law and mailboxes.
- **Quote:** "It makes me uncomfortable when you..."
- **Takeaway (Suggestion):** Consent talk about exhibitionism includes the people who might see; a boundary is said as 'I feel X when Y' after acknowledging what she likes.
- **Limitations:** 4 years old; OP text removed; very large thread only partly read; commenters' legal claims not verified.

## The "are we okay?" conversation

### R08 · r/relationship_advice: Is it normal to 'check in' on your relationship, to periodically ask if everything's okay? (23 MF)

- **Type:** Reddit · **Also relevant to:** -
- **Source:** https://old.reddit.com/r/relationship_advice/comments/ftqj9f/ (accessed 2026-11-08)
- **Inspected:** Post + top ~15 comments with replies of 171, sort=top, Desktop pane.
- **Finding (Evidence):** OP's own words: 'hey, is everything okay with us? is there anything that's bothering you?' and she worries it sounds 'paranoid or nuts'. Replies: the easy answer is 'Yup, still love you.'; asking for what you need ('I could use some extra love today') lands well, while 'Do you really love me though?' sounds like an accusation. Some couples ask 'kinda playfully'.
- **Quote:** "Hey, I could use some extra love today"
- **Takeaway (Suggestion):** 'Are we okay?' is short, hedged and often half-joking; the good answer is brief and warm, not a speech.
- **Limitations:** 2020 thread, self-selected advice-givers; a 2-person relationship snapshot.

### R17 · r/relationship_advice: Is it manipulative to ask "do you hate me?" after an argument?

- **Type:** Reddit · **Also relevant to:** confrontation
- **Source:** https://old.reddit.com/r/relationship_advice/comments/m2wse3/ (accessed 2026-11-08)
- **Inspected:** Post + 3 edits + top ~10 comments of 151, sort=top, Desktop pane.
- **Finding (Evidence):** Reported loop: he ends arguments with 'I need some space', she asks 'do you hate me?', he says the question hurts. He isn't verbal; his small step is 'I appreciate you'. Replies: 'So I'm just a terrible person.' turns the talk onto the asker; 'Are we good?' or a direct request ('Can I hug you?', 'Please, just hold me') works better. Sharp disagreement in the thread.
- **Quote:** "Even just the simple "Are we good?"
- **Takeaway (Suggestion):** After a fight, the reassurance bid is tiny and specific ('Are we good?' / 'Can I hug you?'); the non-verbal partner answers with an action or a three-word line.
- **Limitations:** Married 10 years (older than the game's couple); contested thread, no consensus.

### M12 · Turn Towards Instead of Away — Gottman Institute

- **Type:** research (relationships) · **Also relevant to:** general
- **Source:** https://www.gottman.com/blog/turn-toward-instead-of-away (accessed 2026-11-08)
- **Inspected:** Gottman Institute article definition and examples of bids, turning toward and missing a bid.
- **Finding (Evidence):** A bid for attention may be a smile, wink or request for help rather than a direct relationship check-in; missing it leaves less room for repair than an overt response, according to the article.
- **Takeaway (Suggestion):** Hide an 'are we okay?' question inside a small bid and show whether the other notices it.
- **Limitations:** Research-informed guidance and author interpretation, not a transcript of a particular couple; reported study percentages are not independently audited here.

### P11 · The Four Horsemen: Stonewalling

- **Type:** personality research · **Also relevant to:** confrontation, consent/new-things
- **Source:** https://www.gottman.com/blog/the-four-horsemen-stonewalling/ (accessed 2026-11-08)
- **Inspected:** Gottman Institute article body and suggested antidote
- **Finding (Evidence):** Stonewalling is disengagement during a difficult exchange, often attributed to feeling overwhelmed; the article describes tuning out, turning away, and appearing busy, and recommends a time-out with return to conversation.
- **Takeaway (Suggestion):** Stage Ryan’s “I’m fine” as one avoidant move followed by observable withdrawal; a healthier branch explicitly pauses and comes back.
- **Limitations:** Practitioner explanation, not a standalone experimental estimate; a single brief pause is not necessarily stonewalling.

## Bedroom talk

### R09 · r/TwoXChromosomes: Funny things said during sex by your SO

- **Type:** Reddit · **Also relevant to:** teasing
- **Source:** https://old.reddit.com/r/TwoXChromosomes/comments/3w0b44/ (accessed 2026-11-08)
- **Inspected:** Post + 11 comments, sort=top; one anecdote about a 16-year-old excluded from use.
- **Finding (Evidence):** Real bedroom talk is clumsy and funny: a boyfriend's mid-sex compliment comes out wrong ('Your conditioner is really working'), she says 'What?', he explains badly, they laugh and carry on. Others: private running jokes reused in bed, an embarrassing noise met by silence then a lame deflection, both laughing.
- **Quote:** "And this is why I don't compliment, I'm bad at it."
- **Takeaway (Suggestion):** Let intimate scenes have a flubbed line and a shared laugh that doesn't end the mood.
- **Limitations:** 10-year-old humor thread; skews to memorable mishaps, not typical talk.

### M09 · Where Should We Begin?: Impotent is No Way To Define a Man

- **Type:** podcast · **Also relevant to:** consent/new-things, are-we-okay
- **Source:** https://podcasts.happyscribe.com/where-should-we-begin-with-esther-perel/impotent-is-no-way-to-define-a-man (accessed 2026-11-08)
- **Inspected:** HappyScribe transcript, especially 06:30-13:10 discussion of touch, timing, explicit request and feedback.
- **Finding (Evidence):** The pair distinguish desire for contact from whether this moment is welcome. Under therapist prompting, one asks for a specific touch, then tries lighter pressure, tip-of-finger contact and a simple report that it feels nice; uncertainty about preference is allowed before trying.
- **Quote:** "I think I like it lighter."
- **Takeaway (Suggestion):** For consensual novelty, make preference discovery a sequence of small requests and feedback, not a fluent speech about desire.
- **Limitations:** Anonymized couple in a one-time, edited therapy session; machine transcription may err; avoid identifying or importing personal histories into fiction.

## Confession and betrayal confrontations

### R14 · r/relationship_advice: married 10 years... wife cheating and confronted her

- **Type:** Reddit · **Also relevant to:** -
- **Source:** https://old.reddit.com/r/relationship_advice/comments/2g1hhx/ (accessed 2026-11-08)
- **Inspected:** Post + 2 updates + top comments of 91, sort=top, Desktop pane.
- **Finding (Evidence):** The confrontation runs for days ('talking... and arguing and what not'). The accused partner repeats one denial 'over and over', later minimizes ('we both just fucked up... yada yada'), freezes when caught, and apologizes 'about 1 million times'. The hurt partner fixates on one concrete detail (deleted messages), argues in numbered rhetorical questions, swears, and still says he loves her. Commenters disagree.
- **Quote:** "apologized about 1 million times"
- **Takeaway (Suggestion):** Write betrayal confrontations as loops over one detail, with repeated denials and repeated apologies, spread over more than one scene.
- **Limitations:** One private person's account (used only for aggregate pattern, no identifying details); OP's reporting is one-sided.

### M04 · Too Hot to Handle, season 3 episode 3: group confrontation over conflicting claims

- **Type:** reality TV · **Also relevant to:** jealousy/awkward
- **Source:** https://subslikescript.com/series/Too_Hot_to_Handle-12004280/season-3/episode-3-The_Truth_Hurts (accessed 2026-11-08)
- **Inspected:** Full episode transcript, later rule-break announcement and argument about what was said to two women.
- **Finding (Evidence):** The conflict circles the disputed wording of earlier conversations: accusation, denial, correction, simultaneous interruption, renewed denial. Third parties and replayed footage escalate rather than settle the exchange.
- **Quote:** "I didn't lie about it. I just didn't say nothin'."
- **Takeaway (Suggestion):** When accused, have a character narrow the meaning of one verb and make the others repeat the contested claim.
- **Limitations:** Edited reality TV with producer-controlled revelation and cutaway evidence; no reliable full-conversation timing.

### M05 · Temptation Island, season 1 episode 11: final bonfire breakup

- **Type:** reality TV · **Also relevant to:** jealousy/awkward
- **Source:** https://subslikescript.com/series/Temptation_Island-9174576/season-1/episode-11-Final_Bonfire_-_Part_2 (accessed 2026-11-08)
- **Inspected:** Full episode transcript, final bonfire sequence with a betrayed partner's statement and response.
- **Finding (Evidence):** One partner alternates direct accusation with self-reproach; the other begins with an old endearment, which is rejected twice before the substantive explanation resumes. Hurt does not appear as a neat sequence of setup, rebuttal and resolution.
- **Quote:** "Don't call me that. / Don't call me that."
- **Takeaway (Suggestion):** Let a familiar term of affection become unacceptable in the middle of a rupture, and allow repetition without new information.
- **Limitations:** Heavily edited reality TV; host enforces turn-taking, and previews and confessionals are intercut. Separate hand-segmented 18-turn final-bonfire excerpt in measure_media_turns.py has median 3 words/turn and 13/18 (72.2%) turns of 4 or fewer words; this is not an episode-wide estimate.

### M06 · Temptation Island, season 1 episode 11: host-mediated decisions

- **Type:** reality TV · **Also relevant to:** are-we-okay
- **Source:** https://subslikescript.com/series/Temptation_Island-9174576/season-1/episode-11-Final_Bonfire_-_Part_2 (accessed 2026-11-08)
- **Inspected:** Full transcript, earlier bonfire decision segment with both partners choosing to leave alone.
- **Finding (Evidence):** A speaker cushions the final decision with fillers, respect and residual affection; the host then restates the choice for clarity, forcing a blunt answer after a qualified one.
- **Quote:** "I still respect you. I still love you."
- **Takeaway (Suggestion):** Let an emotionally decisive answer arrive only after hedges and a concrete follow-up question.
- **Limitations:** Edited reality TV; formal host prompts and fixed choice architecture are unlike private couple talk.

### M10 · Modern Love: Un-Marry Me!

- **Type:** podcast · **Also relevant to:** are-we-okay
- **Source:** https://podcasts.happyscribe.com/modern-love/un-marry-me (accessed 2026-11-08)
- **Inspected:** HappyScribe transcript, opening reported domestic nap-time dispute and 05:28-06:39 reported marital conversation.
- **Finding (Evidence):** In the interviewee's recollection, a charged household disagreement starts with a missed routine and an immediate practical objection; later, a relationship-defining announcement provokes repeated attempts to pin down what a new term means, not instant mutual understanding.
- **Quote:** "Detaching? What does that even mean?"
- **Takeaway (Suggestion):** When a partner introduces a new relationship label, let the other ask what it changes in practice.
- **Limitations:** A public person's retrospective account and narrator-mediated podcast, not a recording of the couple's original private exchange; machine transcription.

### M13 · How to Fight Smarter: Soften Your Start-Up — Gottman Institute

- **Type:** research (relationships) · **Also relevant to:** are-we-okay
- **Source:** https://www.gottman.com/blog/softening-startup/ (accessed 2026-11-08)
- **Inspected:** Gottman Institute article contrasting a blame-heavy opening with a specific complaint and request, including guidance after defensiveness.
- **Finding (Evidence):** The examples distinguish describing an observable problem and need from judging a partner's character; even an 'I feel' sentence can function as blame if it smuggles in 'you never.' A reassurance after a defensive response can redirect the discussion.
- **Quote:** "I don't feel heard right now."
- **Takeaway (Suggestion):** Give a conflict opener one observable grievance and a request, and let defensiveness still be possible.
- **Limitations:** Prescriptive examples, not records of naturally occurring talk; good practice should not make every character sound therapeutic.

