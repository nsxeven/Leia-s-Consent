# Chapter One Scenes 14–30 visual placeholders.
# Final generated art should replace these stable names after narrative QA.

image bg ch01_villa_kitchen_night = Composite(
    (1920, 1080),
    (0, 0), Solid("#24252d"),
    (0, 700), Transform(Solid("#625b54"), xysize=(1920, 380)),
    (1180, 130), Transform(Solid("#8a8074"), xysize=(560, 500)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nBG-CH1-18 — VILLA KITCHEN / NIGHT", size=46, color="#ffffff"),
)

image bg ch01_pool_evening = At("images/backgrounds/villa/villa_pool_evening.webp", prologue_bg_blur)
image bg ch01_pool_night = At("images/backgrounds/villa/villa_pool_night.webp", prologue_bg_blur)

# Night pool: Leia at the pool edge, Julian beside her with a whisky.
image cg ch01_night_pool_attention = At("images/cg/ch01/CH1D1_CG_PoolTension_01.webp", prologue_fullscreen)

image bg ch01_villa_bedroom_night = At("images/backgrounds/villa/villa_master_night.webp", prologue_bg_blur)

image cg ch01_movie_cuddle_blanket = At("images/cg/ch01/CH1D1_CG_MovieBlanket_01.webp", prologue_fullscreen)
# Scene 15: Leia settled against Ryan, his hand at her hip under the blanket.
image cg ch01_movie_blanket_hand = At("images/cg/ch01/CH1D1_CG_MovieBlanket_02.webp", prologue_fullscreen)

# Blanket draped over the sofa, Leia smiling at Ryan, Julian mid-movie.
image cg ch01_movie_no_blanket = At("images/cg/ch01/CH1D1_CG_MovieStare_01.webp", prologue_fullscreen)

# Blanket off: Ryan's hand on Leia's backside (01), then the squeeze (02).
image cg ch01_movie_ass_grab_01 = At("images/cg/ch01/CH1D1_CG_MovieAssGrab_01.webp", prologue_fullscreen)
image cg ch01_movie_ass_grab_02 = At("images/cg/ch01/CH1D1_CG_MovieAssGrab_02.webp", prologue_fullscreen)

# Back downstairs after changing: Julian hands Ryan a whisky at the counter.
image cg ch01_villa_night_julian_drink = At("images/cg/ch01/CH1D1_CG_JulianDrink.webp", prologue_fullscreen)

image cg ch01_lounge_micro_test = Composite(
    (1920, 1080),
    (0, 0), Solid("#433746"),
    (90, 70), Text("CG PLACEHOLDER\nCH01-MOVIE-03 — FIRST DELIBERATE MICRO-TEST\nLOUNGE TOP SHIFT / LEIA AWARE / JULIAN UNAWARE", size=50, color="#ffffff"),
)

image ch01_photo_late_favourite = Composite(
    (1080, 1350),
    (0, 0), Solid("#6a7787"),
    (60, 70), Text("PHONE PHOTO PLACEHOLDER\nCH01-PHOTO-LATE-01\nUNSENT POOL FAVOURITE", size=42, color="#ffffff"),
)
# Outfit-specific stable IDs for the eventual final photo. Both temporarily
# share the existing placeholder until the two production files are ready.
# Keep the legacy ID above for existing saved message attachments.
image ch01_photo_late_favourite_white = "ch01_photo_late_favourite"
image ch01_photo_late_favourite_blue = "ch01_photo_late_favourite"


# Day One closing dream. These are temporary composition placeholders; keep the
# stable IDs when replacing them with final CG variants.
image cg ch01_dream_towel_replay = Composite(
    (1920, 1080),
    (0, 0), Solid("#393747"),
    (90, 70), Text("CG PLACEHOLDER\nCH01-DREAM-TOWEL-01 — MEMORY REPLAY\nLEIA UPSTAIRS IN TOWEL / RYAN + JULIAN BELOW", size=50, color="#ffffff"),
)

image cg ch01_dream_towel_shift = Composite(
    (1920, 1080),
    (0, 0), Solid("#493947"),
    (90, 70), Text("CG PLACEHOLDER\nCH01-DREAM-TOWEL-02 — TOWEL SHIFTS\nRYAN TRIES TO WARN HER / NO VOICE", size=50, color="#ffffff"),
)

image cg ch01_dream_towel_curtain = Composite(
    (1920, 1080),
    (0, 0), Solid("#353a47"),
    (90, 70), Text("CG PLACEHOLDER\nCH01-DREAM-TOWEL-03 — SHEER CURTAIN DRAWN\nLEIA THINKS SHE HAS PRIVACY", size=50, color="#ffffff"),
)

image cg ch01_dream_stranger_behind = Composite(
    (1920, 1080),
    (0, 0), Solid("#30323d"),
    (90, 70), Text("CG PLACEHOLDER\nCH01-DREAM-STRANGER-04 — IMPOSSIBLE APPEARANCE\nDINNER STRANGER BEHIND LEIA / BOTH SEEN THROUGH SHEER", size=50, color="#ffffff"),
)

image cg ch01_dream_stranger_look = Composite(
    (1920, 1080),
    (0, 0), Solid("#34313d"),
    (90, 70), Text("CG PLACEHOLDER\nCH01-DREAM-STRANGER-05 — DINNER MEMORY DISTORTED\nLEIA'S GAZE DROPS / SHE DOES NOT LOOK AWAY", size=50, color="#ffffff"),
)

image cg ch01_dream_stranger_reach = Composite(
    (1920, 1080),
    (0, 0), Solid("#2e3039"),
    (90, 70), Text("CG PLACEHOLDER\nCH01-DREAM-STRANGER-06 — DREAM ESCALATION\nLEIA REACHES TOWARD HIM / CUT TO BLACK", size=50, color="#ffffff"),
)

# Waking from the dream: Leia asleep beside Ryan.
image cg ch01_dream_wake_night = At("images/cg/ch01/CH1D1_CG_NightmareWakeUp.webp", prologue_fullscreen)
