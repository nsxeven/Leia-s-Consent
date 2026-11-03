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
# Lights still on: arriving home and the movie setup, up to "Press play".
image bg ch01_villa_living_evening = At("images/backgrounds/villa/villa_living_evening.webp", prologue_bg_blur)

image cg ch01_drive_to_dinner = At("images/cg/ch01/CH1D1_CG_DriveToDinner_01.webp", prologue_fullscreen)
# Scene 7: Leia steps out of the bathroom in her dinner dress.
image cg ch01_dress_reveal = At("images/cg/ch01/CH1D1_LilacDressReveal_01.webp", prologue_fullscreen)
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

# Production restroom-return sequence (corridor compliment → closer to table).
image cg ch01_dinner_restroom_return_01 = At("images/cg/ch01/CH1D1_CG_DinnerRestroomReturn_01.webp", prologue_fullscreen)
image cg ch01_dinner_restroom_return_02 = At("images/cg/ch01/CH1D1_CG_DinnerRestroomReturn_02.webp", prologue_fullscreen)

# Compatibility aliases for older saves / references.
image cg ch01_dinner_return_braless = "cg ch01_dinner_restroom_return_01"
image cg ch01_dinner_stranger_compliment = "cg ch01_dinner_restroom_return_01"

# Dinner: Leia leans in to tell Ryan her sticky bra is giving up.
image cg ch01_dinner_sticky_bra = At("images/cg/ch01/CH1D1_CG_StickyBraConfession_01.webp", prologue_fullscreen)

# Walk to the shop: 01 = Leia leans in on Ryan's arm (Julian ahead),
# then Maya's incoming call on Ryan's phone.
image cg ch01_walk_back_01 = At("images/cg/ch01/CH1D1_CG_StreetWalkBack_01.webp", prologue_fullscreen)
image cg ch01_walk_back_call = At("images/cg/ch01/CH1D1_CG_StreetWalkBack_02.webp", prologue_fullscreen)

# Actual Day 1 fall sequence. Preserve 01 -> 02 -> 03 ordering and Ryan POV.
image cg ch01_trip_catch = At("images/cg/ch01/CH1D1_CG_StreetWalkFall_01.webp", prologue_fullscreen)
image cg ch01_trip_catch_followup = At("images/cg/ch01/CH1D1_CG_StreetWalkFall_02.webp", prologue_fullscreen)
image cg ch01_trip_catch_aftermath = At("images/cg/ch01/CH1D1_CG_StreetWalkFall_03.webp", prologue_fullscreen)

# Drive back to the villa: Leia lying in the back seat.
image cg ch01_drive_back_seating = At("images/cg/ch01/CH1D1_CG_DriveToVilla_01.webp", prologue_fullscreen)

# Carry from the car: 01 = Julian lifts Leia out, 02 = walking her to the door
# (dress still in place), 03 = the dress slips, from Julian's view.
image cg ch01_julian_carry = At("images/cg/ch01/CH1D1_CG_Carry_01.webp", prologue_fullscreen)
image cg ch01_carry_walk = At("images/cg/ch01/CH1D1_CG_Carry_02.webp", prologue_fullscreen)
image cg ch01_carry_dress_shift = At("images/cg/ch01/CH1D1_CG_Carry_03.webp", prologue_fullscreen)

# Set down on the villa sofa, Leia drifts straight back to sleep.
image cg ch01_sofa_half_asleep_night = At("images/cg/ch01/CH1D1_CG_HalfAsleep_01.webp", prologue_fullscreen)


# Dinner stranger — fixed-coordinate production layers.
# All five PNGs share one 941x1672 canvas, so dry and wet swap in place with no
# re-registration offset. Dry is the pre-spill state (approach from screen-left);
# wet is the post-CG state (collision aftermath, apology, exit left).
#
# The later corridor/table compliment man is a DIFFERENT person. He has no sprite
# and must never reuse these two images; his lines use the separate `passerby`
# Character (see characters.rpy).
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


# Dinner collision staging.
# The pair remain unusually close after the impact, then ease back to the
# canonical dialogue slots when Ryan calls Leia's name.
# Pre-collision approach: the dry stranger walks in from off-screen LEFT and stops
# on the same slot the wet sprite uses after the spill CG, so the swap is seamless.
transform ch01_stranger_approach_left:
    xpos -0.28
    xanchor 0.5
    yalign 1.0
    yoffset lc_sprite_yoffset
    xysize (760, 900)
    fit "contain"
    xzoom 1.0
    ease 1.0 xpos 0.45

transform ch01_stranger_collision_close:
    xpos 0.45
    xanchor 0.5
    yalign 1.0
    yoffset lc_sprite_yoffset
    xysize (760, 900)
    fit "contain"
    xzoom 1.0

transform ch01_leia_collision_close:
    xpos 0.55
    xanchor 0.5
    yalign 1.0
    yoffset lc_sprite_yoffset
    xysize (760, 900)
    fit "contain"
    xzoom -1.0

transform ch01_stranger_collision_reset:
    xpos 0.45
    xanchor 0.5
    yalign 1.0
    yoffset lc_sprite_yoffset
    xysize (760, 900)
    fit "contain"
    xzoom 1.0
    ease 0.65 xpos 0.22

transform ch01_leia_collision_reset:
    xpos 0.55
    xanchor 0.5
    yalign 1.0
    yoffset lc_sprite_yoffset
    xysize (760, 900)
    fit "contain"
    xzoom -1.0
    ease 0.65 xpos 0.78

transform ch01_stranger_exit_left:
    xpos 0.22
    xanchor 0.5
    yalign 1.0
    yoffset lc_sprite_yoffset
    xysize (760, 900)
    fit "contain"
    xzoom 1.0
    pause 1.0
    ease 0.85 xpos -0.28
    linear 0.15 alpha 0.0
