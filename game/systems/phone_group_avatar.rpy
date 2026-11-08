# The Trip Group starts without a photograph. The four-person asset is pending:
# images/cg/ch01/CH1D2_CG_GroupSelfie_Four.webp
# Generate its circular PNG with tools/gen_phone_group_avatars.py once it lands.
default phone_group_avatar_stage = None
# A separate save field records membership; old saves derive it from the photo flag.
default phone_group_maya_member = False

image phone_avatar_group_four = DynamicDisplayable(phone_group_four_image)

init python:
    PHONE_GROUP_FOUR_ART = "images/cg/ch01/CH1D2_CG_GroupSelfie_Four.webp"
    PHONE_GROUP_FOUR_AVATAR = "gui/phone/sprite_match/avatar_group_four.png"
    PHONE_GROUP_TRIO_AVATARS = {
        "White": "gui/phone/sprite_match/avatar_group_trio_white.png",
        "Blue": "gui/phone/sprite_match/avatar_group_trio_blue.png",
    }
    PHONE_GROUP_EMPTY_ART = "gui/phone/sprite_match/avatar_group_empty.png"

    def phone_group_trio_avatar():
        outfit = get_story_value("ch01_pool_outfit", "pool_conservative")
        return PHONE_GROUP_TRIO_AVATARS["Blue" if outfit == "pool_bolder" else "White"]

    def phone_group_four_image(st, at):
        """Stable image alias with a circular fallback until the four-person PNG exists."""
        if renpy.loadable(PHONE_GROUP_FOUR_AVATAR):
            return PHONE_GROUP_FOUR_AVATAR, None
        return phone_group_trio_avatar(), None

    def phone_group_stage():
        """Recover pre-feature saves from their story progress without changing them."""
        stage = renpy.store.phone_group_avatar_stage
        if stage in ("trio", "four"):
            return stage
        if has_story_flag("ch01_d2_photo_group"):
            return "four"
        if has_story_flag("ch01_scene_05_complete"):
            return "trio"
        return None

    def phone_group_members():
        members = ("player", "leia", "julian")
        if renpy.store.phone_group_maya_member or has_story_flag("ch01_d2_photo_group"):
            return members + ("maya",)
        return members

    def phone_group_avatar():
        """A pre-rendered circular portrait, or the neutral pre-selfie disc."""
        stage = phone_group_stage()
        if stage is None:
            return PHONE_GROUP_EMPTY_ART
        if stage == "four" and renpy.loadable(PHONE_GROUP_FOUR_AVATAR):
            return PHONE_GROUP_FOUR_AVATAR
        return phone_group_trio_avatar()
