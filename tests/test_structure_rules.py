"""Structure rules that keep the codebase from growing load-order patches again.

Every ALLOW_* set lists what existed when the rules were introduced (main
226101b). Rule for editors: SHRINK, NEVER GROW. When you fold an entry into its
owning file, delete it from the set; the test then keeps it from coming back.
To change a definition, edit the file that owns it; do not add a later file,
a `zz*` filename or a `config.label_overrides` entry.

Days 3-5 story files are out of scope for the clean-up and stay listed in
OUT_OF_SCOPE until their own pass.
"""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))

import lc_rpy_model as m  # noqa: E402
from lc_effective_effects import effective_effects  # noqa: E402

# Definitions that are knowingly duplicated today: shrink, never grow.
ALLOW_DUP = {
    "screen": {
        "choice", "choice_feedback_overlay", "confirm", "file_slots", "game_menu", "history",
        "input", "lc_phone_extra_apps", "lc_phone_settings", "lc_phone_settings_mode",
        "lc_phone_status", "lc_phone_status_row", "lc_phone_status_section", "load", "main_menu",
        "notify", "phone_notification_banner", "phone_notification_overlay", "phone_screen",
        "preferences", "quick_menu", "quick_menu@touch", "save", "say", "skip_indicator",
        "status_choice_tutorial",
    },
    "def": {
        "apply_choice", "clear_choice_feedback", "lc_phone_set_information_mode",
        "lc_review_finish", "lc_review_titles", "phone_add_message", "set_dialogue_theme",
        "set_player_transparency_mode", "set_story_flag", "show_choice_feedback",
    },
    "label": set(),
}

# Load-order patch files (game/-relative): shrink, never grow.
ALLOW_PATCH_FILES = {
    "chapters/ch01/ch01_photo_route_phone_patch.rpy",
    "chapters/ch01/zz_ch01_phone_photo_aliases.rpy",
    "chapters/ch01/zz_ch01_phone_sequence_revision.rpy",
    "chapters/ch01/zz_ch01_scene_13_asleep_revision.rpy",
    "chapters/ch01/zzzz_ch01_day2_polish_revision.rpy",
    "chapters/ch01/zzzz_ch01_scene27_staged_phone.rpy",
    "chapters/ch01/zzzzz_ch01_love_outfit_control.rpy",
    "screens/z_phone_presentation.rpy",
    "screens/zz_choice_screen_developer_scroll.rpy",
    "screens/zz_day1_ui_qol_patch.rpy",
    "screens/zzzz_phone_app_icons_patch.rpy",
    "screens/zzzzzz_phone_ios_presentation.rpy",
    "screens/zzzzzz_phone_wallpaper.rpy",
    "screens/zzzzzzz_phone_hardware_polish.rpy",
    "screens/zzzzzzzz_scrapbook_ui.rpy",
    "systems/zz_phone_presentation_logic.rpy",
    "systems/zz_story_state_flag_getter.rpy",
    "systems/zzz_menu_safe_transparency_patch.rpy",
    "zzzz_ch01_breakfast_presentation.rpy",
}

# Files that may still contain config.label_overrides: shrink, never grow.
ALLOW_OVERRIDES = {
    "chapters/ch01/zzzz_ch01_day2_polish_revision.rpy",
    "chapters/ch01/zzzz_ch01_scene27_staged_phone.rpy",
}

# Days 3-5 belong to their own later pass; their Day 4/5 track-text helpers are
# re-scored in systems/stat_model_v2_later_days.rpy on purpose.
OUT_OF_SCOPE = {"ch01_day3_", "ch01_day4_", "ch01_day5_"}
OUT_OF_SCOPE_DUP = {"def": {"ch01_d4_track_text", "ch01_d5_track_text"}}

PATCH_NAME = re.compile(r"^z+_|_patch\.rpy$")


def game_rel(path):
    return path.relative_to(m.GAME).as_posix()


class StructureRuleTests(unittest.TestCase):
    def test_no_new_duplicate_definitions(self):
        for kind, allowed in ALLOW_DUP.items():
            dups = set(m.duplicates(kind)) - allowed - OUT_OF_SCOPE_DUP.get(kind, set())
            self.assertEqual(dups, set(), f"{kind} defined more than once; edit the owning file instead")

    def test_allow_lists_only_shrink(self):
        """An allow-list entry that is already fixed must be removed from the list."""
        for kind, allowed in ALLOW_DUP.items():
            stale = allowed - set(m.duplicates(kind))
            self.assertEqual(stale, set(), f"remove fixed {kind} entries from ALLOW_DUP")
        present = {game_rel(p) for p in m.rpy_files()}
        self.assertEqual(ALLOW_PATCH_FILES - present, set(), "remove deleted files from ALLOW_PATCH_FILES")

    def test_no_new_patch_files(self):
        patch_files = {game_rel(p) for p in m.rpy_files() if PATCH_NAME.search(p.name)}
        self.assertEqual(patch_files - ALLOW_PATCH_FILES, set(),
                         "no new zz*/ *_patch.rpy files: edit the owning file")

    def test_no_new_label_overrides(self):
        users = {game_rel(p) for p in m.rpy_files() if m.overrides_in_text(m.read(p))}
        self.assertEqual(users - ALLOW_OVERRIDES, set(),
                         "no new config.label_overrides: edit the label itself")
        self.assertEqual(ALLOW_OVERRIDES - users, set(), "remove fixed files from ALLOW_OVERRIDES")

    def test_every_hidden_pov_moment_is_used(self):
        text = "\n".join(p.read_text(encoding="utf-8") for p in m.rpy_files())
        registered = set(re.findall(r"lc_pov_register\(\s*['\"](\w+)", text))
        begun = set(re.findall(r"lc_pov_begin\(\s*['\"](\w+)", text))
        self.assertEqual(registered - begun, set(), "registered Hidden POV moment never begins")
        self.assertEqual(begun - registered, set(), "lc_pov_begin for an unregistered moment")

    def test_every_story_choice_id_is_registered(self):
        effects = effective_effects()
        missing = []
        for path in m.rpy_files():
            if "/chapters/" not in path.as_posix():
                continue
            for cid in re.findall(r"\b(?:apply_choice|format_choice|format_\w*choice)\(\s*['\"](\w+)",
                                  path.read_text(encoding="utf-8")):
                if cid not in effects:
                    missing.append(f"{path.name}: {cid}")
        self.assertEqual(missing, [])

    def test_no_orphan_compiled_scripts(self):
        """Ren'Py still loads a .rpyc whose .rpy was moved or deleted (local builds only)."""
        orphans = [p.relative_to(m.GAME).as_posix() for p in m.GAME.rglob("*.rpyc")
                   if not p.with_suffix(".rpy").exists()]
        self.assertEqual(orphans, [], "delete stale .rpyc files left behind by a move")

    def test_paths_named_in_tests_exist(self):
        """A moved file must take its tests with it, or they silently test nothing."""
        ref = re.compile(r"['\"]((?:game|tests|tools|docs)/[\w./-]+\.(?:rpy|py|md|json))['\"]")
        missing = []
        for test in (ROOT / "tests").glob("*.py"):
            for rel in ref.findall(test.read_text(encoding="utf-8")):
                if not (ROOT / rel).exists():
                    missing.append(f"{test.name}: {rel}")
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
