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

# --- Dialogue staging -----------------------------------------------------
# Canonical positions (Leia always RIGHT, others LEFT, face inward) now live in
# game/systems/dialogue_staging.rpy so every chapter reuses the same contract.
# Legacy prologue_* transform names remain available as aliases.
