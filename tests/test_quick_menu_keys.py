"""Quick menu keys are opaque; only unavailable actions dim (darryn 2026-11-08)."""
import unittest
from pathlib import Path

SRC = (Path(__file__).resolve().parents[1] / "game" / "screens" / "zzzzzzzz_scrapbook_ui.rpy")


class QuickMenuKeycapTests(unittest.TestCase):

    def setUp(self):
        self.src = SRC.read_text(encoding="utf-8")

    def block(self, start):
        i = self.src.index(start)
        j = self.src.find("\ntransform ", i + 1)
        return self.src[i:j]

    def test_keycaps_use_state_transform_not_cg_ghost(self):
        self.assertIn("        at lc_keycap_state\n", self.src)
        self.assertNotIn("at (lc_cg_key if ghost else lc_lift)", self.src)
        self.assertNotIn("$ ghost = lc_cg_on_screen()", self.src)

    def test_only_insensitive_states_are_dimmed(self):
        body = self.block("transform lc_keycap_state:")
        for state in ("idle", "hover", "selected_idle", "selected_hover"):
            chunk = body.split("on %s:" % state, 1)[1].split("on ", 1)[0]
            self.assertIn("alpha 1.0", chunk, state)
        for state in ("insensitive", "selected_insensitive"):
            chunk = body.split("on %s:" % state, 1)[1].split("on ", 1)[0]
            self.assertIn("alpha 0.4", chunk, state)

    def test_skip_uses_engine_skip_action(self):
        # Skip() is insensitive on unseen text, which is what dims it.
        self.assertIn('use lc_keycap_button("SKIP", Skip(),', self.src)


if __name__ == "__main__":
    unittest.main()
