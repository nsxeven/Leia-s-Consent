# The Trip Group starts without a photograph. The four-person asset is pending:
# images/cg/ch01/CH1D2_CG_GroupSelfie_Four.webp
# The stable image name remains available for future phone/gallery references.
default phone_group_avatar_stage = None
# A separate save field records membership; old saves derive it from the photo flag.
default phone_group_maya_member = False

image phone_avatar_group_four = DynamicDisplayable(phone_group_four_image)

init python:
    PHONE_GROUP_FOUR_ART = "images/cg/ch01/CH1D2_CG_GroupSelfie_Four.webp"
    PHONE_GROUP_EMPTY_ART = "gui/phone/sprite_match/avatar_group_empty.png"
    PHONE_GROUP_MASK = "gui/phone/sprite_match/avatar_group_mask.png"

    def phone_group_four_image(st, at):
        """Stable alias; a dropped-in four-person file replaces the fallback."""
        if renpy.loadable(PHONE_GROUP_FOUR_ART):
            return PHONE_GROUP_FOUR_ART, None
        outfit = get_story_value("ch01_pool_outfit", "pool_conservative")
        suffix = "Blue" if outfit == "pool_bolder" else "White"
        return "images/cg/ch01/CH1D1_CG_PoolSelfie_Trio_{}.webp".format(suffix), None

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
        """A 128px circular photo, or a neutral initials disc before the selfie."""
        stage = phone_group_stage()
        if stage is None:
            return PHONE_GROUP_EMPTY_ART
        outfit = get_story_value("ch01_pool_outfit", "pool_conservative")
        trio = "images/cg/ch01/CH1D1_CG_PoolSelfie_Trio_{}.webp".format(
            "Blue" if outfit == "pool_bolder" else "White")
        photo = "phone_avatar_group_four" if stage == "four" else trio
        return AlphaMask(Transform(photo, xysize=(128, 128), fit="cover"), PHONE_GROUP_MASK)
