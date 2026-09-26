# Chapter One Scenes 7–13 visual placeholders.
# Final generated art should replace these stable image names.

image bg ch01_villa_entry_evening = At("images/backgrounds/villa/villa_frontdoor_evening.webp", prologue_bg_blur)

image bg ch01_car_night = At("images/backgrounds/car/car_night.webp", prologue_bg_blur)

image bg ch01_restaurant_evening = Composite(
    (1920, 1080),
    (0, 0), Solid("#3a2730"),
    (0, 610), Transform(Solid("#6c4d3f"), xysize=(1920, 470)),
    (260, 180), Transform(Solid("#c99663"), xysize=(1400, 80)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nBG-CH1-12 — ISLAND RESTAURANT / DINNER", size=46, color="#ffffff"),
)

image bg ch01_restaurant_bar = Composite(
    (1920, 1080),
    (0, 0), Solid("#2d2432"),
    (0, 650), Transform(Solid("#5c3d45"), xysize=(1920, 430)),
    (1180, 160), Transform(Solid("#87596d"), xysize=(620, 430)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nBG-CH1-13 — RESTAURANT BAR / LATE EVENING", size=46, color="#ffffff"),
)

image bg ch01_island_walk_night = Composite(
    (1920, 1080),
    (0, 0), Solid("#111c2a"),
    (0, 720), Transform(Solid("#5f5d61"), xysize=(1920, 360)),
    (200, 110), Transform(Solid("#dab66f"), xysize=(30, 610)),
    (1540, 110), Transform(Solid("#dab66f"), xysize=(30, 610)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nBG-CH1-14 — ISLAND WALK / NIGHT", size=46, color="#ffffff"),
)

image bg ch01_shop_night = At("images/backgrounds/chapter 1/ch01_conveniencestore.webp", prologue_bg_blur)

image bg ch01_villa_night = At("images/backgrounds/villa/villa_frontdoor_night.webp", prologue_bg_blur)

image bg ch01_villa_living_night = At("images/backgrounds/villa/villa_living_night.webp", prologue_bg_blur)

image cg ch01_drive_to_dinner = Composite(
    (1920, 1080),
    (0, 0), Solid("#243146"),
    (90, 70), Text("CG PLACEHOLDER\nCH01-DRIVE-01 — BASELINE CAR SEATING\nRYAN DRIVING / LEIA FRONT PASSENGER / JULIAN REAR", size=52, color="#ffffff"),
)

image cg ch01_dinner_spill = Composite(
    (1920, 1080),
    (0, 0), Solid("#744b57"),
    (90, 70), Text("CG PLACEHOLDER\nCH01-DINNER-01 — STRANGER COLLISION\nBOTH OUTFITS WET / LEIA DRESS + STICKY BRA COMPROMISED", size=52, color="#ffffff"),
)

image cg ch01_dinner_return_braless = Composite(
    (1920, 1080),
    (0, 0), Solid("#704455"),
    (90, 70), Text("CG PLACEHOLDER\nCH01-DINNER-02 — RETURN FROM RESTROOM\nSAME DRESS / STICKY BRA REMOVED\nPOST-SPILL VISUAL CONTINUITY STATE", size=52, color="#ffffff"),
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
