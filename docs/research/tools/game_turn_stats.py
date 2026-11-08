# Game-side comparison numbers on origin/main (same files and spoken-line rule as tic_scan.py)
import re, subprocess, statistics, collections
G = r"C:/RenPy/Leia's Consent/Leia-s-Consent"
files = ["game/chapters/prologue.rpy", "game/chapters/ch01/ch01_main.rpy", "game/chapters/ch01/ch01_scenes_04_06.rpy",
         "game/chapters/ch01/ch01_scenes_07_13.rpy", "game/chapters/ch01/ch01_scenes_14_30.rpy"]
say = re.compile(r'^\s*(mc|gf|friend|maya|\w+)?\s*"((?:[^"\\]|\\.)*)"')
fill = re.compile(r"\b(uh|um|like|i mean|you know)\b", re.I)
sizes, per, nfill, ncut, nlaugh = [], collections.defaultdict(list), 0, 0, 0
sha = subprocess.run(["git", "-C", G, "rev-parse", "--short", "origin/main"], capture_output=True, text=True).stdout.strip()
for f in files:
    src = subprocess.run(["git", "-C", G, "show", "origin/main:" + f], capture_output=True, text=True, encoding="utf-8").stdout
    for line in src.splitlines():
        m = say.match(line)
        if not m or m.group(1) in (None, "centered", "extend"):
            continue
        t = re.sub(r"\{[^}]*\}", "", m.group(2)).strip()
        n = len(t.split()); sizes.append(n); per[m.group(1)].append(n)
        nfill += len(fill.findall(t)); ncut += t.count("—") + t.count("--") + t.count("...")
print("origin/main", sha, "spoken lines", len(sizes), "median", statistics.median(sizes),
      "<=4: %.1f%%" % (100 * sum(s <= 4 for s in sizes) / len(sizes)),
      ">=15: %.1f%%" % (100 * sum(s >= 15 for s in sizes) / len(sizes)))
print("filler tokens (uh/um/like/I mean/you know):", nfill, "= %.1f per 100 lines" % (100 * nfill / len(sizes)), "| dash/ellipsis marks:", ncut)
for who in ("mc", "gf", "friend", "maya"):
    ws = per.get(who, [])
    if ws:
        print("  %-7s %3d lines avg %.1f median %s  >=15: %.0f%%" % (who, len(ws), sum(ws) / len(ws), statistics.median(ws), 100 * sum(w >= 15 for w in ws) / len(ws)))
