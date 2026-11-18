# Chapter One Scenes 4–6 visual registry.
# Explicit flash image avoids an undeclared `white` image at each shutter.
image lc_photo_flash_white = Solid("#ffffff")
# Real assets use stable image IDs; only actively referenced missing art stays as a placeholder.

image bg ch01_pool_day = At("images/backgrounds/villa/villa_pool_day.webp", prologue_bg_blur)

image bg ch01_pool_lounge = At("images/backgrounds/chapter 1/ch01_villa_pool_upstairs.webp", prologue_bg_blur)

image cg ch01_sunscreen_white = At("images/cg/ch01/CH1D1_CG_Sunscreen_White_01.webp", prologue_fullscreen)
image cg ch01_sunscreen_blue = At("images/cg/ch01/CH1D1_CG_Sunscreen_Blue_01.webp", prologue_fullscreen)

image cg ch01_sunscreen_apply_white = At("images/cg/ch01/CH1D1_CG_SunscreenApply_White_01.webp", prologue_fullscreen)
image cg ch01_sunscreen_apply_blue = At("images/cg/ch01/CH1D1_CG_SunscreenApply_Blue_01.webp", prologue_fullscreen)

image cg ch01_pool_hand_pull_white = At("images/cg/ch01/CH1D1_CG_PoolHandPull_White_01.webp", prologue_fullscreen)
image cg ch01_pool_hand_pull_blue = At("images/cg/ch01/CH1D1_CG_PoolHandPull_Blue_01.webp", prologue_fullscreen)

image cg ch01_photo_group_white = At("images/cg/ch01/CH1D1_CG_PoolSelfie_Trio_White.webp", prologue_fullscreen)
image cg ch01_photo_group_blue = At("images/cg/ch01/CH1D1_CG_PoolSelfie_Trio_Blue.webp", prologue_fullscreen)

image cg ch01_photo_awkward_a = At("images/cg/ch01/CH1D1_CG_PoolPhoto_White_01.webp", prologue_fullscreen)
image cg ch01_photo_capture_01_a = At("images/cg/ch01/CH1D1_CG_PoolPhoto_White_01_Capture.webp", prologue_fullscreen)
image cg ch01_photo_capture_02_a = At("images/cg/ch01/CH1D1_CG_PoolPhoto_White_02_Capture.webp", prologue_fullscreen)
image cg ch01_photo_capture_03_a = At("images/cg/ch01/CH1D1_CG_PoolPhoto_White_03_Capture.webp", prologue_fullscreen)
# Capture 4: Julian's unsent favourite, sent late to the Trip Group (scene 27).
image cg ch01_photo_capture_04_a = At("images/cg/ch01/CH1D1_CG_PoolPhoto_White_04_Capture.webp", prologue_fullscreen)

image cg ch01_photo_awkward_b = At("images/cg/ch01/CH1D1_CG_PoolPhoto_Blue_01.webp", prologue_fullscreen)
image cg ch01_photo_capture_01_b = At("images/cg/ch01/CH1D1_CG_PoolPhoto_Blue_01_Capture.webp", prologue_fullscreen)
image cg ch01_photo_capture_02_b = At("images/cg/ch01/CH1D1_CG_PoolPhoto_Blue_02_Capture.webp", prologue_fullscreen)
image cg ch01_photo_capture_03_b = At("images/cg/ch01/CH1D1_CG_PoolPhoto_Blue_03_Capture.webp", prologue_fullscreen)
image cg ch01_photo_capture_04_b = At("images/cg/ch01/CH1D1_CG_PoolPhoto_Blue_04_Capture.webp", prologue_fullscreen)

image cg ch01_towel_call_down = At("images/cg/ch01/CH1D1_CG_TowelCallDown_01.webp", prologue_fullscreen)

image cg ch01_towel_shift_01 = At("images/cg/ch01/CH1D1_CG_TowelShift_01.webp", prologue_fullscreen)
image cg ch01_towel_shift_02 = At("images/cg/ch01/CH1D1_CG_TowelShift_02.webp", prologue_fullscreen)
image cg ch01_towel_shift_03 = At("images/cg/ch01/CH1D1_CG_TowelShift_03.webp", prologue_fullscreen)

# Realization is the balcony reaction beat used on Julian's "I'm looking at the water." line.
image cg ch01_towel_realization = At("images/cg/ch01/CH1D1_CG_TowelRealization_01.webp", prologue_fullscreen)

# Upstairs follow-up conversation after Ryan comes up.
image cg ch01_towel_did_he_see = At("images/cg/ch01/CH1D1_CG_TowelDidHeSee_01.webp", prologue_fullscreen)


# Title screen (systems/title_customiser.rpy): this Day's Leia outfits and backgrounds. order= is
#   the menu position shared by every Day (the Prologue and Day One interleave).
# load order: init 1, after the registry (init -1).
init 1 python:
    _d = LC_LEIA_SPRITE_DIR
    _b = "images/backgrounds/"
    lc_title_register_outfit("purple_dress", "Lilac dress", _d + "CH1/Base_PurpleDress.png", _d + "CH1/Chest_PurpleDress.png", "leia_purple_dress", default=True, seen_cgs=("ch01_dress_reveal",), order=10)
    lc_title_register_outfit("blue_bikini", "Blue bikini", _d + "CH1/Base_BlueBikini.png", _d + "CH1/Chest_BlueBikini.png", "leia_blue_bikini", seen_cgs=("ch01_swimsuit_choice_blue", "ch01_sunscreen_blue", "ch01_sunscreen_apply_blue"), order=40)
    lc_title_register_outfit("white_ruffle", "White ruffle", _d + "CH1/Base_WhiteRuffle.png", _d + "CH1/Chest_WhiteRuffle.png", "leia_white_ruffle", seen_cgs=("ch01_swimsuit_choice_white", "ch01_sunscreen_white", "ch01_sunscreen_apply_white"), order=50)
    lc_title_register_outfit("lounge", "Loungewear", _d + "CH1/Base_Lounge.png", _d + "CH1/Chest_Lounge.png", "leia_lounge", seen_cgs=("ch01_movie_cuddle_blanket", "ch01_movie_blanket_hand", "ch01_movie_no_blanket", "ch01_movie_micro_test_glance"), order=60)
    lc_title_register_outfit("towel", "Towel", _d + "CH1/Base_Towel.png", _d + "CH1/Chest_Towel.png", "leia_towel", mature=True, seen_cgs=("ch01_towel_call_down", "ch01_towel_shift_01"), order=70)
    lc_title_register_outfit("purple_dress_wet", "Lilac dress (soaked)", _d + "CH1/Base_PurpleDressWet.png", _d + "CH1/Chest_PurpleDressWet.png", "leia_purple_dress_wet", mature=True, seen_cgs=("ch01_dinner_spill_02", "ch01_dinner_spill_03"), order=80)
    lc_title_register_outfit("purple_dress_no_bra", "Lilac dress (no bra)", _d + "CH1/Base_PurpleDressNoBra.png", _d + "CH1/Chest_PurpleDressNoBra.png", "leia_purple_dress_no_bra", mature=True, seen_cgs=("ch01_dinner_sticky_bra", "ch01_dinner_restroom_return_01"), order=90)

    lc_title_register_background("pool_evening", "Pool, evening", _b + "villa/villa_pool_evening.webp", ("ch01_pool_evening",), default=True, order=10)
    lc_title_register_background("pool_day", "Pool, day", _b + "villa/villa_pool_day.webp", ("ch01_pool_day", "ch01_villa_pool"), order=20)
    lc_title_register_background("pool_lounge", "Upstairs lounge", _b + "chapter 1/ch01_villa_pool_upstairs.webp", ("ch01_pool_lounge",), order=30)
    lc_title_register_background("living_evening", "Living room, evening", _b + "villa/villa_living_evening.webp", ("ch01_villa_living_evening",), order=40)
    lc_title_register_background("living_day", "Living room, day", _b + "villa/villa_living_day.webp", ("ch01_villa_living",), order=50)
    lc_title_register_background("bedroom_evening", "Bedroom, evening", _b + "villa/villa_master_evening.webp", ("ch01_villa_bedroom_evening",), order=60)
    lc_title_register_background("bedroom_day", "Bedroom, day", _b + "villa/villa_master_day.webp", ("ch01_master_bedroom",), order=70)
    lc_title_register_background("entry_evening", "Villa door, evening", _b + "villa/villa_frontdoor_evening.webp", ("ch01_villa_entry_evening",), order=80)
    lc_title_register_background("villa_arrival", "Arrival", _b + "chapter 1/ch01_villa_arrival.webp", ("ch01_villa_exterior",), order=90)
    lc_title_register_background("restaurant", "Restaurant", _b + "chapter 1/ch01_restaurant.webp", ("ch01_restaurant_evening",), order=100)
    lc_title_register_background("bar", "Bar", _b + "chapter 1/ch01_bar.webp", ("ch01_restaurant_bar",), order=110)
