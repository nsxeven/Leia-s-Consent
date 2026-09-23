# Prologue visuals.
# Generated prologue art is kept separate from the later layered wardrobe sprite
# system. Missing present-day art remains explicit placeholders.

# --- Standard VN transitions ----------------------------------------------
# Use short crossfades for expression/pose replacement so generated sprites do
# not snap between different silhouettes. Longer transitions are reserved for
# major posture changes and entrances/exits.
define sprite_change = Dissolve(0.18)
define sprite_pose_change = Dissolve(0.28)
define sprite_enter_exit = Dissolve(0.30)

# --- Full-screen generated visuals -----------------------------------------

transform prologue_fullscreen:
    xysize (1920, 1080)
    fit "cover"

image bg prologue_party:
    "images/backgrounds/prologue/party01.webp"
    xysize (1920, 1080)
    fit "cover"

image cg prologue_party_arrival:
    "images/cg/prologue/party_leiafriends01.webp"
    xysize (1920, 1080)
    fit "cover"

# Present-day bedroom background has not been generated yet.
image bg prologue_packing = Composite(
    (1920, 1080),
    (0, 0), Solid("#2b2528"),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nRYAN + LEIA'S BEDROOM — PRESENT DAY", size=46, color="#ffffff"),
)

# --- Missing full-screen story CG placeholders -----------------------------

image cg prologue_first_kiss = Composite(
    (1920, 1080),
    (0, 0), Solid("#583847"),
    (90, 70), Text("CG P06\nFIRST KISS", size=52, color="#ffffff"),
)

image cg prologue_present_stare = Composite(
    (1920, 1080),
    (0, 0), Solid("#403639"),
    (90, 70), Text("CG P07\nPRESENT DAY — RYAN STARING AT LEIA WHILE PACKING", size=52, color="#ffffff"),
)

image cg prologue_packing_banter = Composite(
    (1920, 1080),
    (0, 0), Solid("#463a3d"),
    (90, 70), Text("CG P08\nPACKING BANTER — SUITCASES + OUTFITS", size=52, color="#ffffff"),
)

image cg prologue_departure = Composite(
    (1920, 1080),
    (0, 0), Solid("#322d34"),
    (90, 70), Text("CG P09\nLEAVING FOR THE AIRPORT — THREE-PERSON TRIP BEGINS", size=52, color="#ffffff"),
)

# --- Standard VN sprite envelope ------------------------------------------\n# Entrance transforms. Use these only when a character actually enters the
# composition, not for ordinary expression changes.
transform prologue_sprite_enter_center:
    xalign 0.5
    yalign 1.0
    xysize (760, 900)
    fit "contain"
    alpha 0.0
    yoffset 18
    parallel:
        linear 0.30 alpha 1.0
    parallel:
        easeout 0.30 yoffset 0

transform prologue_sprite_enter_left:
    xalign 0.25
    yalign 1.0
    xysize (760, 900)
    fit "contain"
    alpha 0.0
    xoffset -45
    parallel:
        linear 0.30 alpha 1.0
    parallel:
        easeout 0.30 xoffset 0

transform prologue_sprite_enter_right:
    xalign 0.75
    yalign 1.0
    xysize (760, 900)
    fit "contain"
    alpha 0.0
    xoffset 45
    parallel:
        linear 0.30 alpha 1.0
    parallel:
        easeout 0.30 xoffset 0

# Julian intentionally has no temporary sprite fallback. Final Julian sprite
# assets will be introduced only after they are approved.

transform prologue_leia_left:
    xalign 0.18
    yalign 1.0

transform prologue_julian_right:
    xalign 0.82
    yalign 1.0
