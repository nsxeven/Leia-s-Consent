# Chapter One Scenes 4–6 visual registry.
# Real assets use stable image IDs; only actively referenced missing art stays as a placeholder.

image bg ch01_pool_day = At("images/backgrounds/villa/villa_pool_day.webp", prologue_bg_blur)

image bg ch01_pool_lounge = At("images/backgrounds/chapter 1/ch01_villa_pool_upstairs.webp", prologue_bg_blur)

image cg ch01_sunscreen_white = At("images/cg/ch01/CH1D1_CG_Sunscreen_White_01.webp", prologue_fullscreen)
image cg ch01_sunscreen_blue = At("images/cg/ch01/CH1D1_CG_Sunscreen_Blue_01.webp", prologue_fullscreen)

image cg ch01_pool_hand_pull_white = At("images/cg/ch01/CH1D1_CG_PoolHandPull_White_01.webp", prologue_fullscreen)
image cg ch01_pool_hand_pull_blue = At("images/cg/ch01/CH1D1_CG_PoolHandPull_Blue_01.webp", prologue_fullscreen)

image cg ch01_photo_group = Composite(
    (1920, 1080),
    (0, 0), Solid("#287f9e"),
    (90, 70), Text("CG PLACEHOLDER\nCH01-PHOTO-00 — TRIO HOLIDAY PHOTO", size=52, color="#ffffff"),
)

image cg ch01_photo_awkward_a = At("images/cg/ch01/CH1D1_CG_PoolPhoto_White_01.webp", prologue_fullscreen)
image cg ch01_photo_capture_01_a = At("images/cg/ch01/CH1D1_CG_PoolPhoto_White_01_Capture.webp", prologue_fullscreen)
image cg ch01_photo_capture_02_a = At("images/cg/ch01/CH1D1_CG_PoolPhoto_White_02_Capture.webp", prologue_fullscreen)
image cg ch01_photo_capture_03_a = At("images/cg/ch01/CH1D1_CG_PoolPhoto_White_03_Capture.webp", prologue_fullscreen)

image cg ch01_photo_awkward_b = At("images/cg/ch01/CH1D1_CG_PoolPhoto_Blue_01.webp", prologue_fullscreen)
image cg ch01_photo_capture_01_b = At("images/cg/ch01/CH1D1_CG_PoolPhoto_Blue_01_Capture.webp", prologue_fullscreen)
image cg ch01_photo_capture_02_b = At("images/cg/ch01/CH1D1_CG_PoolPhoto_Blue_02_Capture.webp", prologue_fullscreen)
image cg ch01_photo_capture_03_b = At("images/cg/ch01/CH1D1_CG_PoolPhoto_Blue_03_Capture.webp", prologue_fullscreen)





image cg ch01_towel_call_down = At("images/cg/ch01/CH1D1_CG_TowelCallDown_01.webp", prologue_fullscreen)

image cg ch01_towel_shift = At("images/cg/ch01/CH1D1_CG_TowelShift_01.webp", prologue_fullscreen)

image cg ch01_towel_realization = At("images/cg/ch01/CH1D1_CG_TowelRealization_01.webp", prologue_fullscreen)


