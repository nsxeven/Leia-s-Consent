"""Descriptive counts from four UCSB SBCSAE TRN files; not turn-transition timing.
Rows beginning with numeric timestamps are intonation units. An explicit NAME: begins
a speaker turn; unlabeled rows inherit the most recent explicit name. A turn is a
maximal contiguous run of rows assigned to one name. Lexical tokenization excludes
transcription event codes, unintelligible X, and symbol-only marks. Bracket openers
are overlap-notation counts, not unique interruptions. @ runs count laughter-marked
rows, not individual laughs. Truncations count token-final hyphens plus -- cutoffs.
"""
import re, json, statistics, pathlib, collections
root=pathlib.Path(__file__).parent
files=['SBC002.trn','SBC003.trn','SBC006.trn','SBC011.trn']
row=re.compile(r'^\s*\d+(?:\.\d+)?\s+\d+(?:\.\d+)?\t([^\t]*)\t(.*)$')
name=re.compile(r'^\s*([A-Z][A-Z0-9_ -]{1,24}):\s*$')
token=re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*(?:-[A-Za-z]+)*")
fillers=['uh','um','like','i mean','you know']
def lexical(s):
 s=re.sub(r'\([^)]*\)',' ',s) # event notation such as (H), (Hx), (TSK)
 s=re.sub(r'<[^>]*>',' ',s) if False else s
 s=re.sub(r'\bX{1,}\b',' ',s)
 s=re.sub(r'\[[0-9]*|[0-9]*\]',' ',s)
 return [w.lower() for w in token.findall(s)]
def analyze(path):
 lines=path.read_text(encoding='utf-8-sig',errors='replace').splitlines()
 units=[];turns=[];prev=None; fillers_count=collections.Counter();laugh=overlap=trunc=0
 for line in lines:
  m=row.match(line)
  if not m:continue
  tag,txt=m.groups(); nm=name.match(tag)
  if nm: speaker=nm.group(1).strip()
  elif prev:speaker=prev
  else:continue
  if not turns or speaker!=prev:turns.append([speaker,0])
  prev=speaker
  words=lexical(txt); turns[-1][1]+=len(words)
  if words:units.append(len(words))
  for w in ('uh','um','like'):fillers_count[w]+=words.count(w)
  for phrase in ('i mean','you know'):
   fillers_count[phrase]+=sum(words[i:i+2]==phrase.split() for i in range(len(words)-1))
  laugh+=bool(re.search(r'@|\(Hx\)|\(laugh',txt,re.I))
  overlap+=len(re.findall(r'\[(?!\d*\])',txt))
  trunc+=len(re.findall(r'\b[A-Za-z]+-(?![A-Za-z])|(?<!-)--(?!-)',txt))
 sizes=[t[1] for t in turns if t[1]>0]
 return dict(id=path.stem,parsed_speaker_turns=len(turns),lexical_turns=len(sizes),median_words_per_turn=statistics.median(sizes),percent_turns_le_4=round(100*sum(n<=4 for n in sizes)/len(sizes),1),percent_turns_ge_15=round(100*sum(n>=15 for n in sizes)/len(sizes),1),lexical_intonation_units=len(units),median_words_per_intonation_unit=statistics.median(units),mean_words_per_intonation_unit=round(statistics.mean(units),2),fillers=dict(fillers_count),laughter_marked_units=laugh,overlap_opening_markers=overlap,truncated_words_or_double_dash_cutoffs=trunc)
results=[analyze(root/f) for f in files]
(root/'measurements.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
