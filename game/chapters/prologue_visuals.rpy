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

# Background presentation: a uniform soft blur across the entire background.
# The dialogue UI now supplies its own bezel treatment, so the old simulated
# center-sharp / edge-blur composition is intentionally removed.
transform prologue_bg_blur:
    xysize (1920, 1080)
    fit "cover"
    blur 4.0

image bg prologue_party = At("images/backgrounds/prologue/PRO_party.webp", prologue_bg_blur)

image cg prologue_party_arrival = At("images/cg/prologue/PRO_CG_PartyArrival_01.webp", prologue_fullscreen)

image cg prologue_party_couch = At("images/cg/prologue/PRO_CG_PartyCouch_01.webp", prologue_fullscreen)

image cg prologue_first_kiss_01 = At("images/cg/prologue/PRO_CG_FirstKiss_01.webp", prologue_fullscreen)

image cg prologue_first_kiss_02 = At("images/cg/prologue/PRO_CG_FirstKiss_02.webp", prologue_fullscreen)

image cg prologue_first_kiss_03 = At("images/cg/prologue/PRO_CG_FirstKiss_03.webp", prologue_fullscreen)

image cg prologue_present_stare = At("images/cg/prologue/PRO_CG_PackingBanter_01.webp", prologue_fullscreen)

image cg prologue_packing_banter = At("images/cg/prologue/PRO_CG_PackingBanter_02.webp", prologue_fullscreen)

image cg prologue_departure = At("images/cg/prologue/PRO_CG_Departure_01.webp", prologue_fullscreen)

# --- Standard VN sprite envelope ------------------------------------------
# A displayable-relative shadow/glow follows each sprite's own alpha silhouette.
# Because it is applied to the sprite itself, it automatically follows left,
# center, right, and future multi-character staging rather than using a fixed
# screen-space location.
transform lc_sprite_dark_glow:
    matrixcolor TintMatrix("#ffffff")
    additive 0.0
    shadow (0, 0)
    shadowcolor "#000000b8"
    blur 3.0

# Entrance transforms. Use these only when a character actually enters the
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
