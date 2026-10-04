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
image bg prologue_party_kitchen = At("images/backgrounds/prologue/PRO_kitchen.webp", prologue_bg_blur)
image bg prologue_truthordare = At("images/backgrounds/prologue/PRO_truthordare.webp", prologue_bg_blur)
image bg prologue_packing = At("images/backgrounds/prologue/PRO_bedroom.webp", prologue_bg_blur)

image cg prologue_party_arrival = At("images/cg/prologue/PRO_CG_PartyArrival_01.webp", prologue_fullscreen)

image cg prologue_party_couch = At("images/cg/prologue/PRO_CG_PartyCouch_01.webp", prologue_fullscreen)

image cg prologue_first_kiss_01 = At("images/cg/prologue/PRO_CG_FirstKiss_01.webp", prologue_fullscreen)

image cg prologue_first_kiss_02 = At("images/cg/prologue/PRO_CG_FirstKiss_02.webp", prologue_fullscreen)

image cg prologue_first_kiss_03 = At("images/cg/prologue/PRO_CG_FirstKiss_03.webp", prologue_fullscreen)

image cg prologue_present_stare = At("images/cg/prologue/PRO_CG_PackingBanter_01.webp", prologue_fullscreen)

image cg prologue_packing_banter = At("images/cg/prologue/PRO_CG_PackingBanter_02.webp", prologue_fullscreen)

image cg prologue_departure = At("images/cg/prologue/PRO_CG_Departure_01.webp", prologue_fullscreen)

# --- Standard VN sprite envelope ------------------------------------------
# Sprite edge treatment will be implemented with a Ren'Py 8.5.3-compatible
# displayable composition after visual testing. No fixed screen-space glow is used.

# Entrance transforms. Use these only when a character actually enters the
# composition, not for ordinary expression changes.
transform prologue_sprite_enter_center:
    xalign 0.5
    yalign 1.0
    yoffset 1980
    xysize (760, 900)
    fit "contain"
    alpha 0.0
    yoffset 198
    parallel:
        linear 0.30 alpha 1.0
    parallel:
        easeout 0.30 yoffset 180

transform prologue_sprite_enter_left:
    xalign 0.25
    yalign 1.0
    yoffset 1980
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
    yoffset 1980
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
    yoffset 1980

transform prologue_julian_right:
    xalign 0.82
    yalign 1.0
    yoffset 1980


# --- Two-character Prologue composition ----------------------------------
# Leia owns the left slot. Ryan/Julian own the right slot.
# Ryan's source artwork faces the opposite direction, so the right-slot
# transform mirrors him horizontally to face Leia.
transform prologue_ryan_enter_right:
    xalign 0.82
    yalign 1.0
    yoffset 1980
    xysize (760, 900)
    fit "contain"
    xzoom -1.0
    alpha 0.0
    xoffset 45
    parallel:
        linear 0.30 alpha 1.0
    parallel:
        easeout 0.30 xoffset 0

transform prologue_ryan_right:
    xalign 0.82
    yalign 1.0
    yoffset 1980
    xysize (760, 900)
    fit "contain"
    xzoom -1.0


# --- Canonical dialogue-side contract -------------------------------------
# Leia always owns the RIGHT slot. Other active characters own the LEFT slot.
# Preserve the approved 760x900 dialogue sprite envelope; explicit xpos/xanchor
# makes placement independent of the source canvas width.
transform prologue_leia_enter_right:
    xpos 0.78
    xanchor 0.5
    yalign 1.0
    yoffset 1980
    xysize (760, 900)
    fit "contain"
    xzoom -1.0
    alpha 0.0
    yoffset 198
    parallel:
        linear 0.30 alpha 1.0
    parallel:
        easeout 0.30 yoffset 180

transform prologue_leia_right:
    xpos 0.78
    xanchor 0.5
    yalign 1.0
    yoffset 1980
    xysize (760, 900)
    fit "contain"
    xzoom -1.0

transform prologue_other_enter_left:
    xpos 0.22
    xanchor 0.5
    yalign 1.0
    yoffset 1980
    xysize (760, 900)
    fit "contain"
    xzoom 1.0
    alpha 0.0
    yoffset 198
    parallel:
        linear 0.30 alpha 1.0
    parallel:
        easeout 0.30 yoffset 180

transform prologue_other_left:
    xpos 0.22
    xanchor 0.5
    yalign 1.0
    yoffset 1980
    xysize (760, 900)
    fit "contain"
    xzoom 1.0


transform prologue_other_left:
    xalign 0.18
    yalign 1.0
    yoffset 1980
    xysize (760, 900)
    fit "contain"
    xzoom 1.0
