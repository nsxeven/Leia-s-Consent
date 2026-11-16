"""Behaviour pins for the clean-up: effective definitions must not change.

tests/data/effective_fingerprints.json records, for every screen, function,
class, define/default, transform, image, layeredimage, module-level assignment
and style (per variant), what the copy Ren'Py actually uses looks like; for
every label the parameters + body that really run (label_overrides and
single-`jump` aliases followed); the multiset of init side-effect statements
(overlay registrations, table updates, loops); the overlay registration order;
and the final choice-effects table.

Moving a definition to another file, deleting a dead duplicate or folding a
label override keeps these prints identical. A change that is MEANT to rewrite
an effective body (e.g. folding a load-time wrapper into one function) lists the
name in FOLDED with a reason AND the dotted name of a behaviour test that pins
what the folded code does (see test_behaviour_freeze.py).
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "dev"))
sys.path.insert(0, str(ROOT / "tests"))

from snapshot_baselines import fingerprints  # noqa: E402

# kind -> {name: (reason, "tests.module.Class.test_method")}.
# Clean-up PR 2b folded the four load-time wrapper chains into hooks
# (game/systems/lc_hooks.rpy); each entry names the test that pins the behaviour.
FOLDED = {
    "def": {
        "set_story_flag": ("Chapter Select unlock moved from a wrapper to a story_flag_set hook",
                           "tests.test_behaviour_freeze.StoryFlagHookTests.test_day_two_complete_unlocks_chapter_select"),
        "lc_review_finish": ("tag unlock moved from a wrapper to a review_finished hook",
                             "tests.test_tag_collection.TagCollectionTests.test_finish_unlocks_tags_and_stickers_permanently"),
        "lc_review_titles": ("auto titles now lc_review_auto_titles; equipped tags via a review_titles filter",
                             "tests.test_tag_collection.TagCollectionTests.test_equip_each_slot_separately"),
        "lc_current_titles": ("reads lc_review_auto_titles instead of the removed _lc_tags_orig_review_titles",
                              "tests.test_tag_collection.TagCollectionTests.test_equip_each_slot_separately"),
        "phone_add_message": ("calls the renamed base writer phone_store_message instead of the alias",
                              "tests.test_behaviour_freeze.PhoneAddMessageTests.test_incoming_to_closed_thread_is_unread_and_notifies_once"),
        "phone_deliver_reply_step": ("calls the renamed base writer phone_store_message instead of the alias",
                                     "tests.test_phone_replies.PhoneRepliesTest.test_selected_reply_waits_for_staged_delivery"),
    },
    "assign": {
        "_chapter_select_orig_set_story_flag": ("wrapper alias removed (story_flag_set hook)", "tests.test_behaviour_freeze.StoryFlagHookTests.test_day_two_complete_unlocks_chapter_select"),
        "_lc_tags_orig_review_finish": ("wrapper alias removed (review_finished hook)", "tests.test_tag_collection.TagCollectionTests.test_finish_unlocks_tags_and_stickers_permanently"),
        "_lc_tags_orig_review_titles": ("wrapper alias removed (lc_review_auto_titles)", "tests.test_review_tags.ReviewTagTests.test_protective_run_gets_bodyguard"),
        "_phone_add_message_base": ("wrapper alias removed (base writer is phone_store_message)", "tests.test_behaviour_freeze.PhoneAddMessageTests.test_incoming_to_closed_thread_is_unread_and_notifies_once"),
    },
    "effect": {
        'lc_hook_add("story_flag_set", chapter_select_unlock_after_day_two) #2ca61c8a3dfa527b':
            ("hook registration replacing the set_story_flag wrapper", "tests.test_behaviour_freeze.StoryFlagHookTests.test_day_two_complete_unlocks_chapter_select"),
        'lc_hook_add("review_finished", lc_tags_unlock_finished_day) #4f4bba022f135a3a':
            ("hook registration replacing the lc_review_finish wrapper", "tests.test_tag_collection.TagCollectionTests.test_finish_unlocks_tags_and_stickers_permanently"),
        'lc_hook_add("review_titles", lc_tags_apply) #0ce7aed81f42da81':
            ("hook registration replacing the lc_review_titles wrapper", "tests.test_tag_collection.TagCollectionTests.test_equip_each_slot_separately"),
    },
}

# Kinds where a NEW entry is as suspicious as a missing one.
BOTH_WAYS = ("effect",)


class EffectiveFingerprintTests(unittest.TestCase):
    def test_effective_definitions_unchanged(self):
        baseline = json.loads((ROOT / "tests/data/effective_fingerprints.json").read_text(encoding="utf-8"))
        current = fingerprints()
        problems = []
        for kind, names in baseline.items():
            allowed = FOLDED.get(kind, {})
            now_kind = current.get(kind, {})
            for name, print_ in names.items():
                if name in allowed:
                    continue
                now = now_kind.get(name)
                if now is None:
                    problems.append(f"{kind} {name}: missing")
                elif now != print_:
                    problems.append(f"{kind} {name}: changed")
            if kind in BOTH_WAYS:
                for name in set(now_kind) - set(names) - set(allowed):
                    problems.append(f"{kind} {name}: new")
        self.assertEqual(problems, [], "\n" + "\n".join(problems))

    def test_folded_entries_name_a_behaviour_test(self):
        loader = unittest.TestLoader()
        for kind, names in FOLDED.items():
            for name, (reason, test_name) in names.items():
                self.assertTrue(reason.strip(), f"{kind} {name} needs a reason")
                suite = loader.loadTestsFromName(test_name)
                self.assertGreater(suite.countTestCases(), 0, f"{kind} {name}: {test_name} not found")


if __name__ == "__main__":
    unittest.main()
