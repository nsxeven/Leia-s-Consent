"""darryn rule (2026-11-08): everything is built on main; releases are extracted
from main by changing only game/00_release_build.rpy."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8").replace("\r\n", "\n")


class ReleaseFromMainTests(unittest.TestCase):

    def test_switch_file_defines_profiles(self):
        src = read("game/00_release_build.rpy")
        self.assertIn("python early:", src)  # must run before options.rpy loads
        self.assertRegex(src, r'\n    LC_RELEASE = (None|"[a-z0-9-]+")\n')
        self.assertRegex(src, r'\n    LC_RELEASE_VERSION = "[^"]+"\n')
        for profile in ("None:", '"day1-demo":'):
            self.assertIn(profile, src)
        names = sorted(p.name for p in GAME.glob("*.rpy"))
        self.assertEqual(names[0], "00_release_build.rpy")

    def test_main_is_the_full_developer_build(self):
        # On main the switch is off. A release branch sets the two lines on
        # purpose, so this check skips there.
        src = read("game/00_release_build.rpy")
        if "\n    LC_RELEASE = None\n" not in src:
            self.skipTest("release branch: switch is set on purpose")
        self.assertIn('\n    LC_RELEASE_VERSION = "dev-main"\n', src)

    def test_release_settings_come_from_the_switch(self):
        opts = read("game/options.rpy")
        for line in ('define config.name = LC_RELEASE_INFO["title"]',
                     'define config.version = LC_RELEASE_VERSION',
                     'define build.name = LC_RELEASE_INFO["build_name"]',
                     'define config.save_directory = LC_RELEASE_INFO["save_directory"]'):
            self.assertIn(line, opts)
        self.assertIn("Lewd sounds by Shinlalala", opts)  # CC BY-SA credit on every build
        self.assertIn('define LC_DAY1_DEMO_BUILD = (LC_RELEASE == "day1-demo")',
                      read("game/chapters/ch01/ch01_release_demo.rpy"))
        self.assertIn('if LC_IS_RELEASE else "always"', read("game/systems/chapter_select.rpy"))

    def test_dev_exclusions_precede_joiplay_and_rpy_is_not_blanket_excluded(self):
        opts = read("game/options.rpy")
        self.assertLess(opts.index("if LC_IS_RELEASE:"), opts.index("build.classify('game/**.rpy', 'joiplay')"))
        self.assertNotRegex(opts, r"build\.classify\('game/\*\*\.rpy', None\)")

    def test_no_hardcoded_release_values_elsewhere(self):
        for path in GAME.rglob("*.rpy"):
            if "tl" in path.parts or path.name == "00_release_build.rpy":
                continue
            src = path.read_text(encoding="utf-8")
            self.assertNotRegex(src, r'define LC_DAY1_DEMO_BUILD = (True|False)', path.name)
            self.assertNotRegex(src, r'define config\.version = "', path.name)


if __name__ == "__main__":
    unittest.main()
