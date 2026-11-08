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
rounded('bar_track', '#101d30e0', size=(24, 24), radius=6, border='#c6a98288')
for name, color in [('honey','#f5c568'), ('amber','#e5b96c'), ('peach','#f0a98b'), ('pink','#ff8fc0')]:
    rounded('bar_'+name, color, size=(24, 24), radius=6)
rounded('slider_thumb', '#fff1db', size=(30, 30), radius=15, border='#ff8fc0')
for name, color in [('toggle_off','#36465b'), ('toggle_on','#ff8fc0')]:
    rounded(name, color, size=(48, 30), radius=14, border='#f5c568')
for name, bg in [('sound_test','#f5c568'), ('sound_test_hover','#ff8fc0')]:
    im=Image.new('RGBA',(34,34)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((1,1,32,32), radius=9, fill=bg)
    d.polygon(((8,13),(13,13),(19,8),(19,26),(13,21),(8,21)), fill='#283344')
    d.arc((16,9,29,25), -65, 65, fill='#283344', width=2)
    im.save(OUT/(name+'.png'))
print('generated', len(list(OUT.glob('*.png'))), 'Golden Hour glass assets')
