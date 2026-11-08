"""Generate Golden Hour glass nine-slices and controls (Pillow). Run from repo root."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parents[1] / 'game/gui/glass'
OUT.mkdir(parents=True, exist_ok=True)


def rounded(name, color, size=(96, 96), radius=20, border=None):
    im = Image.new('RGBA', size)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((1, 1, size[0]-2, size[1]-2), radius=radius, fill=color, outline=border, width=2)
    im.save(OUT / (name+'.png'))


rounded('panel', '#182537db', border='#f5c5688a')
rounded('nav_idle', '#243248ba', size=(80, 60), radius=12, border='#f0a98b3f')
rounded('nav_active', '#704055dc', size=(80, 60), radius=12, border='#ff8fc0')
# A thin Leia-pink active underline carries the selected-tab cue.
active = Image.open(OUT/'nav_active.png')
ImageDraw.Draw(active).rounded_rectangle((10, 54, 70, 58), radius=2, fill='#ff8fc0')
active.save(OUT/'nav_active.png')
rounded('pill_honey', '#f5c568ef', size=(52, 36), radius=12)
rounded('pill_peach', '#f0a98bef', size=(52, 36), radius=12)
rounded('pill_pink', '#ff8fc0ef', size=(52, 36), radius=12)
def bar(name, color, border=None):
    # 30px tall like the thumb: a 24px band centred, transparent 3px above/below,
    # so the thumb sits on the bar's centre line (Frame borders 8/9 keep the gap).
    im = Image.new('RGBA', (24, 30))
    ImageDraw.Draw(im).rounded_rectangle((1, 4, 22, 25), radius=6, fill=color, outline=border, width=2 if border else 0)
    im.save(OUT / (name+'.png'))


bar('bar_track', '#101d30e0', border='#c6a98288')
for name, color in [('honey','#f5c568'), ('amber','#e5b96c'), ('peach','#f0a98b'), ('pink','#ff8fc0')]:
    bar('bar_'+name, color)
rounded('slider_thumb', '#fff1db', size=(30, 30), radius=15, border='#ff8fc0')
for name, color in [('toggle_off','#36465b'), ('toggle_on','#ff8fc0')]:
    rounded(name, color, size=(48, 30), radius=14, border='#f5c568')
for name, bg in [('sound_test','#f5c568'), ('sound_test_hover','#ff8fc0')]:
    im=Image.new('RGBA',(34,34)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((1,1,32,32), radius=9, fill=bg)
    d.polygon(((8,13),(13,13),(19,8),(19,26),(13,21),(8,21)), fill='#283344')
    d.arc((16,9,29,25), -65, 65, fill='#283344', width=2)
    im.save(OUT/(name+'.png'))
# Mute toggle: speaker + sound waves (on) / speaker + cross (muted).
for name, bg, muted in [('mute_off','#36465b',False), ('mute_off_hover','#ff8fc0',False),
                        ('mute_on','#d4636e',True), ('mute_on_hover','#ff8fc0',True)]:
    im=Image.new('RGBA',(34,34)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((1,1,32,32), radius=9, fill=bg, outline='#f5c568', width=2)
    ink = '#fff1db' if not name.endswith('hover') else '#283344'
    d.polygon(((7,13),(11,13),(16,8),(16,26),(11,21),(7,21)), fill=ink)
    if muted:
        d.line((19,12,27,22), fill=ink, width=3); d.line((27,12,19,22), fill=ink, width=3)
    else:
        d.arc((14,10,24,24), -60, 60, fill=ink, width=2); d.arc((15,6,29,28), -60, 60, fill=ink, width=2)
    im.save(OUT/(name+'.png'))
# Status bars (darryn 2026-11-09): one gradient bar per stat, coloured by meaning
# (same colours as the stat icons and the phone Status tints), on a 24px track.
STAT_BARS = {
    "love": ("#FFAACD", "#E86298"),
    "trust": ("#FFDE8C", "#E8AA46"),
    "exhibitionism": ("#FFC4A0", "#E87678"),
    "temptation": ("#EC6E82", "#B22850"),
    "sharing": ("#C8ACEC", "#8C68C8"),
}
def stat_bar(name, top, bot):
    w, h = 24, 24
    t = tuple(int(top[i:i+2], 16) for i in (1, 3, 5)); b = tuple(int(bot[i:i+2], 16) for i in (1, 3, 5))
    g = Image.new('RGBA', (w, h))
    gd = ImageDraw.Draw(g)
    for y in range(h):
        k = y / (h - 1)
        gd.line((0, y, w, y), fill=tuple(int(t[i] + (b[i] - t[i]) * k) for i in range(3)) + (255,))
    m = Image.new('L', (w, h)); ImageDraw.Draw(m).rounded_rectangle((1, 1, w - 2, h - 2), radius=8, fill=255)
    out = Image.new('RGBA', (w, h)); out.paste(g, (0, 0), m)
    ImageDraw.Draw(out).rounded_rectangle((4, 3, w - 5, 9), radius=3, fill=(255, 255, 255, 60))
    out.save(OUT / ('stat_' + name + '.png'))
for _n, (_t, _b) in STAT_BARS.items():
    stat_bar(_n, _t, _b)
rounded('stat_track', '#101d30e0', size=(24, 24), radius=8, border='#c6a98288')
print('generated', len(list(OUT.glob('*.png'))), 'Golden Hour glass assets')
