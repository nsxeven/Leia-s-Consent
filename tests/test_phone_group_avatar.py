"""Save-safe Trip Group avatar stages and membership."""
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "game/systems/phone_group_avatar.rpy").read_text(encoding="utf-8")


class TripGroupAvatarTest(unittest.TestCase):
    def setUp(self):
        self.flags = set()
        self.values = {}
        self.store = SimpleNamespace(phone_group_avatar_stage=None, phone_group_maya_member=False)
        self.available = set()
        self.env = {
            "renpy": SimpleNamespace(store=self.store, loadable=lambda path: path in self.available),
            "has_story_flag": lambda flag: flag in self.flags,
            "get_story_value": lambda key, default=None: self.values.get(key, default),
            "Transform": lambda name, **kwargs: (name, kwargs),
            "AlphaMask": lambda photo, mask: (photo, mask),
        }
        block = textwrap.dedent(SOURCE.split("init python:\n", 1)[1])
        exec(compile(block, "phone_group_avatar.rpy", "exec"), self.env)

    def test_prologue_has_no_photo_or_maya(self):
        self.assertIsNone(self.env["phone_group_stage"]())
        self.assertEqual(self.env["phone_group_avatar"](), self.env["PHONE_GROUP_EMPTY_ART"])
        self.assertEqual(self.env["phone_group_members"](), ("player", "leia", "julian"))

    def test_trio_outfit_variants_and_circular_mask(self):
        self.store.phone_group_avatar_stage = "trio"
        for outfit, expected in (("pool_conservative", "White"), ("pool_bolder", "Blue")):
            self.values["ch01_pool_outfit"] = outfit
            photo, mask = self.env["phone_group_avatar"]()
            self.assertTrue(photo[0].endswith("Trio_{}.webp".format(expected)))
            self.assertEqual(photo[1], {"xysize": (128, 128), "fit": "cover"})
            self.assertEqual(mask, self.env["PHONE_GROUP_MASK"])

    def test_four_falls_back_to_outfit_trio_until_art_exists(self):
        self.store.phone_group_avatar_stage = "four"
        self.store.phone_group_maya_member = True
        self.values["ch01_pool_outfit"] = "pool_bolder"
        self.assertEqual(self.env["phone_group_avatar"]()[0][0], "phone_avatar_group_four")
        self.assertTrue(self.env["phone_group_four_image"](0, 0)[0].endswith("Trio_Blue.webp"))
        self.assertIn("maya", self.env["phone_group_members"]())
        self.available.add(self.env["PHONE_GROUP_FOUR_ART"])
        self.assertEqual(self.env["phone_group_four_image"](0, 0)[0], self.env["PHONE_GROUP_FOUR_ART"])

    def test_old_saves_derive_stage_and_members_from_flags(self):
        self.flags.add("ch01_scene_05_complete")
        self.assertEqual(self.env["phone_group_stage"](), "trio")
        self.flags.add("ch01_d2_photo_group")
        self.assertEqual(self.env["phone_group_stage"](), "four")
        self.assertIn("maya", self.env["phone_group_members"]())
        self.store.phone_group_avatar_stage = "trio"
        self.assertEqual(self.env["phone_group_stage"](), "trio")

    def test_story_changes_and_both_effective_screen_locations(self):
        one = (ROOT / "game/chapters/ch01/ch01_scenes_04_06.rpy").read_text(encoding="utf-8")
        two = (ROOT / "game/chapters/ch01/ch01_day2_scenes_01_15.rpy").read_text(encoding="utf-8")
        screen = (ROOT / "game/screens/zzzzzz_phone_ios_presentation.rpy").read_text(encoding="utf-8")
        self.assertLess(one.index("phone_group_avatar_stage = \"trio\""), one.index("ch01_scene_05_complete"))
        self.assertLess(two.index("phone_group_maya_member = True"), two.index("ch01_d2_photo_group"))
        self.assertEqual(screen.count("add phone_group_avatar():"), 2)
        self.assertNotIn('add "gui/phone/sprite_match/avatar_group.png":', screen)


if __name__ == "__main__":
    unittest.main()
