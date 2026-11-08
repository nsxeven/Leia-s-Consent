# Same rules as tic_scan.py (spoken-line detection, <=4-word count, 6+ runs, tic regexes),
# but scans local .rpy excerpt files given on the command line instead of origin/main files.
# Also flags the banned/rationed phrases listed in docs/DIALOGUE_STYLE.md.
import re, sys, collections

say = re.compile(r'^\s*(mc|gf|friend|maya|\w+)?\s*"((?:[^"\\]|\\.)*)"')
tics = {
    "There she is / There it is": r"\bthere (she|he|it) is\b",
    "Exactly.": r"^exactly[.!]",
    "Fair.": r"^fair( enough)?[.!]",
    "Noted.": r"^noted[.!]",
    "Wow.": r"^wow[.!]",
    "Okay. / Fine. as a full line": r"^(okay|ok|fine|sure|yeah|right|cool)[.!]$",
    "That's ... (verdict line)": r"^that('s| is) (fair|not|a|the|what|why|how)\b",
    "'No X. No Y.' fragments (narration)": r"\bno \w+\. no \w+\.",
    "Not X. Just Y.": r"\bnot \w+[^.]*\. just\b",
    "a beat too long / a fraction": r"\b(a beat|a fraction|half a second|a second too long)\b",
    "somebody/someone who (narration simile)": r"\bwith the (expression|seriousness|confidence|energy|tone) of (somebody|someone)\b",
    # extra banned items from docs/DIALOGUE_STYLE.md
    "Touche. as a whole line": r"^touch[eé][.!]$",
    "Noted./Exactly./Fair. whole line (style guide)": r"^(noted|exactly|fair)[.!]$",
}
for path in sys.argv[1:]:
    spoken, n_short, run, runs6 = 0, 0, 0, 0
    counts, examples = collections.Counter(), collections.defaultdict(list)
    per = collections.defaultdict(list)
    for line in open(path, encoding="utf-8"):
        m = say.match(line)
        if not m:
            continue
        who, text = m.group(1), m.group(2)
        t = re.sub(r"\{[^}]*\}", "", text).strip()
        is_speech = who not in (None, "centered", "extend")
        if is_speech:
            spoken += 1
            words = len(t.split())
            per[who].append(words)
            if words <= 4:
                n_short += 1; run += 1
            else:
                if run >= 6: runs6 += 1
                run = 0
        for k, pat in tics.items():
            if re.search(pat, t, re.I):
                counts[k] += 1
                examples[k].append("%s: %s" % (who or "narr", t[:90]))
    if run >= 6: runs6 += 1
    print("==", path)
    print("spoken lines %d | <=4 words %d = %.0f%% | runs of 6+ short lines %d" % (spoken, n_short, 100.0 * n_short / max(spoken, 1), runs6))
    for who, ws in per.items():
        print("   %-7s lines %2d  avg words %.1f  range %d-%d" % (who, len(ws), sum(ws) / len(ws), min(ws), max(ws)))
    if not counts:
        print("   tics/banned: none")
    for k, v in counts.most_common():
        print("   %2d  %s   e.g. %s" % (v, k, " | ".join(examples[k][:3])))
