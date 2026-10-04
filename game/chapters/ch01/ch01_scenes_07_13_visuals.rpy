# Chapter One Scenes 7–13 visual placeholders.
# Final generated art should replace these stable image names.

image bg ch01_villa_entry_day = At("images/backgrounds/villa/villa_frontdoor_day.webp", prologue_bg_blur)
image bg ch01_villa_entry_evening = At("images/backgrounds/villa/villa_frontdoor_evening.webp", prologue_bg_blur)

image bg ch01_car_night = At("images/backgrounds/car/car_night.webp", prologue_bg_blur)

image bg ch01_restaurant_evening = At("images/backgrounds/chapter 1/ch01_restaurant.webp", prologue_bg_blur)

image bg ch01_restaurant_bar = At("images/backgrounds/chapter 1/ch01_bar.webp", prologue_bg_blur)

image bg ch01_island_walk_night = At("images/backgrounds/chapter 1/ch01_roadside.webp", prologue_bg_blur)

image bg ch01_shop_night = At("images/backgrounds/chapter 1/ch01_conveniencestore.webp", prologue_bg_blur)

image bg ch01_villa_night = At("images/backgrounds/villa/villa_frontdoor_night.webp", prologue_bg_blur)

image bg ch01_villa_living_night = At("images/backgrounds/villa/villa_living_night.webp", prologue_bg_blur)

image cg ch01_drive_to_dinner = At("images/cg/ch01/CH1D1_CG_DriveToDinner_01.webp", prologue_fullscreen)
image cg ch01_dinner_arrival = At("images/cg/ch01/CH1D1_CG_DinnerArrival_01.webp", prologue_fullscreen)
image cg ch01_dinner_photo_ask = At("images/cg/ch01/CH1D1_CG_DinnerPhotoAsk_01.webp", prologue_fullscreen)

# Dinner collision production CG sequence:
# 01 = impact / liquid airborne
# 02 = immediate wet-clothes aftermath
# 03 = Leia follows his glance and looks up
# 04 = Leia's second downward glance
image cg ch01_dinner_spill_01 = At("images/cg/ch01/CH1D1_CG_DinnerSpill_01.webp", prologue_fullscreen)
image cg ch01_dinner_spill_02 = At("images/cg/ch01/CH1D1_CG_DinnerSpill_02.webp", prologue_fullscreen)
image cg ch01_dinner_spill_03 = At("images/cg/ch01/CH1D1_CG_DinnerSpill_03.webp", prologue_fullscreen)
image cg ch01_dinner_spill_04 = At("images/cg/ch01/CH1D1_CG_DinnerSpill_04.webp", prologue_fullscreen)

# Backward-compatible alias for older development saves/references.
image cg ch01_dinner_spill = "cg ch01_dinner_spill_01"

image cg ch01_dinner_return_braless = Composite(
    (1920, 1080),
    (0, 0), Solid("#704455"),
    (90, 70), Text("CG PLACEHOLDER\nCH01-DINNER-02 — RETURN FROM RESTROOM\nSAME DRESS / STICKY BRA REMOVED\nPOST-SPILL VISUAL CONTINUITY STATE", size=52, color="#ffffff"),
)

# Placeholder for the later restaurant compliment beat.
# Replace this stable ID with final art; script timing should not change.
image cg ch01_dinner_stranger_compliment = Composite(
    (1920, 1080),
    (0, 0), Solid("#3b2a2f"),
    (90, 70), Text("CG PLACEHOLDER\nCH1D1 — RESTAURANT STRANGER COMPLIMENT\nLEIA POST-SPILL / NO-BRA DRESS STATE\nSTRANGER COMPLIMENTS HER AT THE TABLE", size=52, color="#ffffff"),
)

image cg ch01_trip_catch = Composite(
    (1920, 1080),
    (0, 0), Solid("#36445b"),
    (90, 70), Text("CG PLACEHOLDER\nCH01-WALK-01 — LEIA TRIPS / JULIAN CATCHES HER\nACCIDENTAL CONTACT / BOTH EMBARRASSED", size=52, color="#ffffff"),
)

image cg ch01_drive_back_seating = Composite(
    (1920, 1080),
    (0, 0), Solid("#1d293b"),
    (90, 70), Text("CG PLACEHOLDER\nCH01-DRIVE-02 — RETURN CAR SEATING\nRYAN DRIVING / JULIAN FRONT / LEIA LYING IN REAR", size=52, color="#ffffff"),
)

image cg ch01_julian_carry = Composite(
    (1920, 1080),
    (0, 0), Solid("#31384a"),
    (90, 70), Text("CG PLACEHOLDER\nCH01-CARRY-01 — JULIAN PRINCESS-CARRIES LEIA\nRYAN AHEAD WITH KEYS", size=52, color="#ffffff"),
)

image cg ch01_carry_dress_shift = Composite(
    (1920, 1080),
    (0, 0), Solid("#403747"),
    (90, 70), Text("CG PLACEHOLDER\nCH01-CARRY-02 — DRESS NECKLINE SHIFTS\nJULIAN'S HANDS OCCUPIED / RYAN'S VIEW OBSCURED\nAMBIGUOUS VIEWING ANGLE", size=52, color="#ffffff"),
)


# Dinner stranger — fixed-coordinate production layers.
# Dry is retained for any pre-spill staging; wet is the post-CG state.
layeredimage stranger_casual_dry_layers:
    always "images/sprites/bbc stranger/Base_Casual_Dry.png"
    always "images/sprites/bbc stranger/Chest_Casual.png"
    always "images/sprites/bbc stranger/Penis_Casual_Dry.png"

image stranger_casual_dry = Fixed(lc_sprite_silhouette("stranger_casual_dry_layers"), xysize=(941, 1672))

layeredimage stranger_casual_wet_layers:
    always "images/sprites/bbc stranger/Base_Casual_Wet.png"
    always "images/sprites/bbc stranger/Chest_Casual.png"
    always "images/sprites/bbc stranger/Penis_Casual_Wet.png"

image stranger_casual_wet = Fixed(lc_sprite_silhouette("stranger_casual_wet_layers"), xysize=(941, 1672))
