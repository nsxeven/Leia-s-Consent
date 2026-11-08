"""Game-wide smooth hover (darryn 2026-11-08): no instant snaps."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = (ROOT / "game/systems/lc_hover_fade.rpy").read_text(encoding="utf-8")
UI = (ROOT / "game/screens/zzzzzzzz_scrapbook_ui.rpy").read_text(encoding="utf-8")


def block(src, head):
    return src.split(head, 1)[1].split("\ntransform ", 1)[0].split("\nscreen ", 1)[0]


class SmoothHoverTests(unittest.TestCase):

    def test_hook_crossfades_background_foreground_and_image(self):
        self.assertIn("Button.set_style_prefix = set_style_prefix", HOOK)
        self.assertIn("Button.render = render", HOOK)
        self.assertIn("_lc_hover_fade_installed", HOOK)   # reload-safe
        self.assertIn("_lc_rendered", HOOK)               # no fade on first show
        for name in ("background", "foreground", "child"):
            self.assertIn("self.style.%s" % name, HOOK)
        self.assertRegex(HOOK, r"define LC_HOVER_IN = 0\.1\d")
        self.assertRegex(HOOK, r"define LC_HOVER_OUT = 0\.2\d")

    def test_shared_hover_transforms_ease(self):
        for head in ("transform lc_keycap_state:", "transform lc_lift:", "transform lc_tab_slide:",
                     "transform lc_tab_out:", "transform lc_choice_slide:", "transform lc_only_hover:"):
            body = block(UI, head)
            events = re.findall(r"on [\w, ]+:\n((?:        .*\n)+)", body + "\n")
            self.assertTrue(events, head)
            for ev in events:
                self.assertIn("easein LC_HOVER_", ev, head)

    def test_hud_badge_eases(self):
        hud = (ROOT / "game/screens/z_phone_presentation.rpy").read_text(encoding="utf-8")
        self.assertNotIn("861 if hud_hovered", hud)
        self.assertIn("at lc_badge_lift(hud_hovered)", hud)


    def test_no_rollback_tracked_objects_in_render_path(self):
        # Store `object`/`list` are revertable; creating them per frame crashed (#168).
        self.assertIn("class _LCStyleProxy(python_object):", HOOK)
        self.assertNotIn("object.__setattr__", HOOK)
        self.assertNotIn("__slots__", HOOK)
        self.assertIn("self._lc_fade = python_list(", HOOK)
        body = HOOK.split("        def render(self, width, height, st, at):\n            self._lc_rendered", 1)[1]
        self.assertLess(body.index("try:"), body.index("_LCStyleProxy(real"))


    def test_crossfade_is_a_true_dissolve(self):
        # Two opaque arts must never go see-through mid-hover (#184).
        self.assertIn('rv.add_shader("renpy.dissolve")', HOOK)
        self.assertIn("rv.operation = renpy.display.render.DISSOLVE", HOOK)
        self.assertIn("rv.operation_alpha = True", HOOK)


if __name__ == "__main__":
    unittest.main()
