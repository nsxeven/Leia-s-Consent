"""Build the static Handjet fonts shipped in game/fonts.

Source: Handjet[ELGR,ELSH,wght].ttf from github.com/google/fonts (ofl/handjet),
SIL Open Font License 1.1, no Reserved Font Name.

    python3 tools/fonts/make_handjet_instances.py path/to/Handjet[ELGR,ELSH,wght].ttf

Writes Handjet-SemiBold.ttf (wght 600) and Handjet-ExtraBold.ttf (wght 800) with the
default square single-element pixels. The only glyph edit: the zero's inner bar is
removed (zero = O) because at UI sizes the barred zero reads as an 8 ("18" vs "10").
"""
import sys
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

OUT = Path(__file__).resolve().parents[2] / "game" / "fonts"


def build(src, weight, style):
    font = instancer.instantiateVariableFont(
        TTFont(src), {"wght": weight, "ELGR": 1, "ELSH": 2}, updateFontNames=True
    )
    glyf = font["glyf"]
    zero = glyf["zero"]
    zero.components = [c for c in zero.components if c.glyphName != "pixel"]
    zero.recalcBounds(glyf)
    path = OUT / "Handjet-{}.ttf".format(style)
    font.save(str(path))
    return path


if __name__ == "__main__":
    src = sys.argv[1]
    for weight, style in ((600, "SemiBold"), (800, "ExtraBold")):
        print(build(src, weight, style))
