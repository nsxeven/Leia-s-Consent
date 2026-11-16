"""Parser cases from the PR #215 review, on synthetic source (no real file names)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lc_rpy_model as m  # noqa: E402


def parse(text):
    return m.parse_text(text, "synthetic.rpy", 0)


def kinds(defs):
    return [(d.kind, d.name) for d in defs]


class ParserCaseTests(unittest.TestCase):
    def test_init_side_effects_are_captured(self):
        defs = parse(
            "init python:\n"
            "    def f():\n"
            "        return 1\n"
            "    if \"x\" not in config.overlay_screens:\n"
            "        config.overlay_screens.append(\"x\")\n"
            "    OUTFITS[\"a\"][\"name\"] = \"A\"\n"
            "    TABLE.update({\"k\": 1})\n"
            "    for c in (a, b):\n"
            "        c.who_style = \"x\"\n")
        effects = [d for d in defs if d.kind == "effect"]
        self.assertEqual(len(effects), 4)
        self.assertIn("config.overlay_screens.append(\"x\")", effects[0].body)

    def test_style_variants_are_separate(self):
        defs = parse("style box:\n    xsize 338\n\nstyle box:\n    variant \"small\"\n    xsize 600\n")
        self.assertEqual(kinds(defs), [("style", "box"), ("style", "box@small")])

    def test_screen_variant_list(self):
        defs = parse("screen s():\n    variant [\"small\", \"tablet\"]\n    null\n")
        self.assertEqual(kinds(defs), [("screen", "s@small,tablet")])

    def test_triple_quoted_text_with_apostrophes_and_brackets(self):
        defs = parse(
            "define gui.about = _p(\"\"\"\n"
            "It's (not) [really] a bracket test.\n"
            "All characters are adults.\n"
            "\"\"\")\n"
            "define after = 1\n")
        self.assertEqual(kinds(defs), [("define", "gui.about"), ("define", "after")])
        self.assertIn("All characters are adults.", defs[0].body)

    def test_layeredimage_is_a_definition(self):
        defs = parse("layeredimage julian_party_layers:\n    always \"base.png\"\n")
        self.assertEqual(kinds(defs), [("layeredimage", "julian_party_layers")])
        self.assertEqual(defs[0].priority, 0)

    def test_bom_first_line_statement(self):
        defs = parse("\ufeffdefine first = 1\n")
        self.assertEqual(kinds(defs), [("define", "first")])

    def test_commented_override_is_not_live(self):
        text = ("init python:\n"
                "    # config.label_overrides[\"a\"] = \"a_old\"\n"
                "    config.label_overrides[\"b\"] = \"b_v2\"\n")
        self.assertEqual(m.overrides_in_text(text), {"b": "b_v2"})


if __name__ == "__main__":
    unittest.main()
