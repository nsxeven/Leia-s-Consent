# Builds docs/research/REAL_DIALOGUE_LEDGER.md from the four scratch ledgers + the game measurement entry.
import json, pathlib, sys
S = pathlib.Path(r"C:/Users/darry/AppData/Local/hermes/profiles/darryn/cache/scratch")
OUT = pathlib.Path(sys.argv[1])
entries = []
entries += json.loads((S / "ledger_reddit.json").read_text(encoding="utf-8"))
entries += json.loads((S / "ledger_corpus.json").read_text(encoding="utf-8"))
entries += json.loads((S / "ledger_media.json").read_text(encoding="utf-8"))
entries += json.loads((S / "ledger_personality.json").read_text(encoding="utf-8"))["entries"]
entries.append({
    "id": "G01", "source_type": "game measurement", "situations": ["general"],
    "title": "Leia's Consent Prologue + Day 1 spoken lines (baseline)",
    "url": "https://github.com/nsxeven/Leia-s-Consent/tree/6eda038",
    "accessed": "2026-11-08",
    "inspected": "game/chapters/prologue.rpy and ch01_main / ch01_scenes_04_06 / 07_13 / 14_30 at origin/main 6eda038, counted with scratch/tic_scan.py and scratch/game_turn_stats.py (same spoken-line rule).",
    "finding": "933 spoken lines, median 4 words; 54.8% are 4 words or fewer, only 1.4% are 15+ words; 16 runs of 6+ short lines. Fillers (uh/um/like/I mean/you know): 21 tokens = 2.3 per 100 lines. Ryan 4.6, Leia 4.5, Julian 5.0 words per line on average, each with 1-2% long lines. 'Exactly.' x12.",
    "quote": "", "label": "Evidence",
    "writer_takeaway": "The gap to real speech is the missing long turns and missing speech mess (fillers, repairs, laughter), more than the share of short lines.",
    "limitations": "A VN line is not exactly a conversational turn (backchannels like 'mhm' are usually cut in scripts); counts use the tic_scan spoken-line regex, which skips narration."})

ORDER = ["general", "teasing", "roasting", "new-friends", "drinking/drunk", "flirting", "jealousy/awkward",
         "consent/new-things", "are-we-okay", "bedroom", "confrontation"]
NAMES = {"general": "How real conversation works (all situations)", "teasing": "Bickering and teasing between partners",
         "roasting": "Old friends roasting each other", "new-friends": "Two women who just met becoming fast friends",
         "drinking/drunk": "Drinking games and drunk talk", "flirting": "Flirting",
         "jealousy/awkward": "Jealousy and awkward moments",
         "consent/new-things": "Suggesting something new in bed / being watched / agreeing on it",
         "are-we-okay": "The \"are we okay?\" conversation", "bedroom": "Bedroom talk",
         "confrontation": "Confession and betrayal confrontations"}
ids = [e["id"] for e in entries]
assert len(ids) == len(set(ids)), "duplicate ids"
types = {}
for e in entries:
    types.setdefault(e["source_type"], []).append(e["id"])
L = []
L.append("# Real dialogue evidence ledger (DRAFT for darryn, 2026-11-08)\n")
L.append("Research only. Built on branch `research/real-dialogue` (off `feature/character-voices` @ 6143412, PR #126). "
         "The game was not touched; GitHub `main` at research time: 6eda038.\n")
L.append("**Who inspected what.** Reddit (R01-R17) was read by the Hermes coordinator in the Hermes Desktop embedded browser pane "
         "(logged-in old.reddit view, read-only: no votes, posts, joins or messages). Corpus/CA (C01-C14), media (M01-M16) and personality "
         "(P01-P11) entries were gathered by three research subagents; the coordinator re-ran the SBCSAE measurement script "
         "(same numbers) and spot-checked five sources and quotes (Temptation Island and Too Hot to Handle transcripts, Gottman "
         "soft start-up, the Where Should We Begin? transcript, and Provine's laughter article). G01 is the coordinator's own count of the game.\n")
L.append("**Labels.** *Evidence* = seen in the source. *Inference* = our reading. The `Takeaway` line on every entry is a *Suggestion* for writers. "
         "Quotes are kept to 1-2 short lines; everything else is paraphrased. No character is based on an identifiable private person: "
         "Reddit and podcast material is used only as aggregate patterns.\n")
L.append("**Caveats that apply everywhere.** Reddit is self-selected and retold from memory, not recorded speech. Reality TV is edited "
         "(see M08 on frankenbites), so its timing and fluency are not natural speech. Film (M15-M16) is scripted and is a contrast only. "
         "The SBCSAE numbers come from a four-file sample counted by a script, not checked against audio.\n")
L.append("## Coverage\n")
L.append("| Source type | Entries | IDs |\n|---|---:|---|")
for t, v in types.items():
    L.append("| %s | %d | %s |" % (t, len(v), ", ".join(v)))
L.append("| **Total** | **%d** | |\n" % len(entries))
L.append("Reddit sample: subscriptions checked first (9 subscribed communities, none about real couples' speech), so all 10 subreddits below were "
         "*discovered*: r/AskWomen, r/Hotwife, r/sex, r/nonmonogamy, r/polyamory, r/relationship_advice, r/relationships, r/TwoXChromosomes, "
         "r/AskMen, r/AskReddit. Threads were found by web search, then opened and read in the pane (post + visible comment tree, "
         "sort=top). **Not done:** the full Hot/Top x Today-to-All-time feed sweep, and r/dating (nothing usable for a 4-year couple). "
         "Comments about minors were excluded.\n")
L.append("## Index by situation\n")
L.append("| Situation | Entries |\n|---|---|")
for s in ORDER:
    L.append("| %s | %s |" % (NAMES[s], ", ".join(e["id"] for e in entries if s in e["situations"])))
L.append("")
for s in ORDER:
    group = [e for e in entries if e["situations"][0] == s]
    if not group:
        continue
    L.append("## %s\n" % NAMES[s])
    for e in group:
        L.append("### %s · %s\n" % (e["id"], e["title"]))
        L.append("- **Type:** %s · **Also relevant to:** %s" % (e["source_type"], ", ".join(e["situations"][1:]) or "-"))
        L.append("- **Source:** %s (accessed %s)" % (e["url"], e["accessed"]))
        L.append("- **Inspected:** %s" % e["inspected"])
        L.append("- **Finding (%s):** %s" % (e["label"], e["finding"]))
        if e.get("quote"):
            L.append("- **Quote:** \"%s\"" % e["quote"].replace("\n", " / ").strip('"'))
        L.append("- **Takeaway (Suggestion):** %s" % e["writer_takeaway"])
        L.append("- **Limitations:** %s\n" % e["limitations"])
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
print("entries", len(entries), "types", {k: len(v) for k, v in types.items()})
