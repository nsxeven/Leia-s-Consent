"""Every audio cue used in the game has a file, and every shipped file is credited."""
import json
import re
import unittest
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / "game"
AUDIO = GAME / "audio"
SFX_FOLDERS = ("sfx", "voice/leia", "voice/ryan", "lewd")
PATTERNS = {
    "sfx": re.compile(r'lc_sfx\(\s*"([a-z0-9_]+)"'),
    "amb": re.compile(r'lc_amb\(\s*"([a-z0-9_]+)"'),
    "music": re.compile(r'lc_music\(\s*"([a-z0-9_]+)"'),
    "ui": re.compile(r'(?:lc_ui_(?:play|sound)\(\s*|Function\(\s*lc_ui_(?:play|sound)\s*,\s*)"([a-z0-9_]+)"'),
}


class DemoAudioTests(unittest.TestCase):

    def test_every_cue_has_a_file(self):
        missing = []
        for path in GAME.rglob("*.rpy"):
            if "tl" in path.parts or path.name == "lc_fx.rpy":
                continue
            src = path.read_text(encoding="utf-8")
            for kind, pat in PATTERNS.items():
                for name in pat.findall(src):
                    # lc_sfx() also searches the VOICE and LEWD folders (lc_fx.LC_SFX_SEARCH).
                    kinds = SFX_FOLDERS if kind == "sfx" else (kind,)
                    if not any((AUDIO / k / (name + ".ogg")).is_file() for k in kinds):
                        missing.append("%s/%s (%s)" % (kind, name, path.name))
        self.assertEqual(missing, [])

    def test_folders_match_sliders(self):
        """darryn: vocal clips in voice/, intimate foley in lewd/ (own LEWD slider)."""
        sfx = {f.stem for f in (AUDIO / "sfx").glob("*.ogg")}
        self.assertFalse([s for s in sfx if s.startswith("leia_")], "Leia vocals belong in voice/leia/")
        self.assertFalse([s for s in sfx if re.match(r"(cum_in|cum_out|plapdry|plapwet|pullout|stroke|wet)\d\d$", s)],
                         "Shinlalala pack belongs in lewd/")
        self.assertEqual(len(list((AUDIO / "lewd").glob("*.ogg"))), 61)
        fx = (GAME / "systems" / "lc_fx.rpy").read_text(encoding="utf-8")
        for kind in SFX_FOLDERS:
            self.assertIn('("%s", ' % kind, fx)
        self.assertIn('mixer="lewd"', fx)
        ui = (GAME / "screens" / "zzzzzzzz_scrapbook_ui.rpy").read_text(encoding="utf-8")
        self.assertIn('Preference("mixer lewd volume")', ui)

    def test_every_file_is_in_the_manifest_with_a_licence(self):
        manifest = json.loads((AUDIO / "manifest.json").read_text(encoding="utf-8"))
        entries = manifest if isinstance(manifest, list) else manifest.get("files", manifest)
        text = json.dumps(entries)
        for f in AUDIO.rglob("*.ogg"):
            key = "%s/%s" % (f.parent.name, f.stem)
            self.assertIn(f.stem, text, key + " missing from manifest.json")
        self.assertNotIn("CHECK:", text)
        self.assertTrue((AUDIO / "CREDITS.md").is_file())

    def test_prologue_party_is_chatter_with_muffled_music(self):
        src = (GAME / "chapters" / "prologue.rpy").read_text(encoding="utf-8")
        self.assertIn('lc_amb("crowd")', src)  # darryn's crowd chatter for busy places
        self.assertIn('lc_bgm("party")', src)  # BGM plan: faint muffled party pop under it

    def test_restaurant_has_chatter_and_soft_music(self):
        src = (GAME / "chapters" / "ch01" / "ch01_scenes_07_13.rpy").read_text(encoding="utf-8")
        self.assertIn('lc_amb("restaurant")', src)  # darryn's restaurant recording
        self.assertIn('lc_bgm("lounge_piano")', src)  # restaurant and bar


if __name__ == "__main__":
    unittest.main()
