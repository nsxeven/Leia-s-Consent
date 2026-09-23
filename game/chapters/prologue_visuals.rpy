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

# Background presentation: always cover the 16:9 viewport, even when the source
# image is not exactly 1920x1080. A subtle center-sharp / edge-soft treatment is
# created by layering a blurred cover image beneath a slightly inset sharp copy.
transform prologue_bg_cover:
    xysize (1920, 1080)
    fit "cover"

transform prologue_bg_edge_blur:
    xysize (1920, 1080)
    fit "cover"
    blur 7.0

transform prologue_bg_center_sharp:
    xalign 0.5
    yalign 0.5
    xysize (1860, 1046)
    fit "cover"

image bg prologue_party = Composite(
    (1920, 1080),
    (0, 0), At("images/backgrounds/prologue/PRO_party.webp", prologue_bg_edge_blur),
    (30, 17), At("images/backgrounds/prologue/PRO_party.webp", prologue_bg_center_sharp),
)

image cg prologue_party_arrival:
    "images/cg/prologue/PRO_CG_PartyArrival_01.webp"
    at prologue_fullscreen

image cg prologue_party_couch:
    "images/cg/prologue/PRO_CG_PartyCouch_01.webp"
    at prologue_fullscreen

image cg prologue_first_kiss_01:
    "images/cg/prologue/PRO_CG_FirstKiss_01.webp"
    at prologue_fullscreen

image cg prologue_first_kiss_02:
    "images/cg/prologue/PRO_CG_FirstKiss_02.webp"
    at prologue_fullscreen

image cg prologue_first_kiss_03:
    "images/cg/prologue/PRO_CG_FirstKiss_03.webp"
    at prologue_fullscreen

image cg prologue_present_stare:
    "images/cg/prologue/PRO_CG_PackingBanter_01.webp"
    at prologue_fullscreen

image cg prologue_packing_banter:
    "images/cg/prologue/PRO_CG_PackingBanter_02.webp"
    at prologue_fullscreen

image cg prologue_departure:
    "images/cg/prologue/PRO_CG_Departure_01.webp"
    at prologue_fullscreen

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
