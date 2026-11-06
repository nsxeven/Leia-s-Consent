"""Every audio cue used in the game has a file, and every shipped file is credited."""
import json
import re
import unittest
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / "game"
AUDIO = GAME / "audio"
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
                    if not (AUDIO / kind / (name + ".ogg")).is_file():
                        missing.append("%s/%s (%s)" % (kind, name, path.name))
        self.assertEqual(missing, [])

    def test_every_file_is_in_the_manifest_with_a_licence(self):
        manifest = json.loads((AUDIO / "manifest.json").read_text(encoding="utf-8"))
        entries = manifest if isinstance(manifest, list) else manifest.get("files", manifest)
        text = json.dumps(entries)
        for f in AUDIO.rglob("*.ogg"):
            key = "%s/%s" % (f.parent.name, f.stem)
            self.assertIn(f.stem, text, key + " missing from manifest.json")
        self.assertNotIn("CHECK:", text)
        self.assertTrue((AUDIO / "CREDITS.md").is_file())

    def test_prologue_party_is_chatter_only(self):
        src = (GAME / "chapters" / "prologue.rpy").read_text(encoding="utf-8")
        self.assertIn('lc_amb("crowd")', src)  # darryn's crowd chatter for busy places
        self.assertNotIn("lc_music(", src)  # darryn: no party music

    def test_restaurant_has_chatter_and_soft_music(self):
        src = (GAME / "chapters" / "ch01" / "ch01_scenes_07_13.rpy").read_text(encoding="utf-8")
        self.assertIn('lc_amb("crowd")', src)  # darryn's crowd chatter for busy places
        self.assertIn('lc_music("lounge_piano")', src)
        self.assertIn("lc_music_stop()", src)


if __name__ == "__main__":
    unittest.main()
