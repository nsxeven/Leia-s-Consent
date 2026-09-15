# Prologue visuals.
# Generated prologue art is kept separate from the later layered wardrobe sprite
# system. Missing present-day art remains explicit placeholders.

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

# --- Generated Leia prologue sprites --------------------------------------
# Keep this tag separate from the layered wardrobe `leia` tag.

image leia_prologue seated_amused01 = "images/sprites/prologue/seated_amused01.png"
image leia_prologue seated_defeated01 = "images/sprites/prologue/seated_defeated01.png"
image leia_prologue seated_defeated02 = "images/sprites/prologue/seated_defeated02.png"
image leia_prologue seated_flustered01 = "images/sprites/prologue/seated_flustered01.png"
image leia_prologue seated_flustered02 = "images/sprites/prologue/seated_flustered02.png"
image leia_prologue seated_laughing01 = "images/sprites/prologue/seated_laughing01.png"
image leia_prologue seated_neutral01 = "images/sprites/prologue/seated_neutral01.png"
image leia_prologue seated_protesting01 = "images/sprites/prologue/seated_protesting01.png"
image leia_prologue standing_excited01 = "images/sprites/prologue/standing_excited01.png"
image leia_prologue standing_interrupted01 = "images/sprites/prologue/standing_interrupted01.png"
image leia_prologue standing_listening01 = "images/sprites/prologue/standing_listening01.png"
image leia_prologue standing_neutral01 = "images/sprites/prologue/standing_neutral01.png"
image leia_prologue standing_shy01 = "images/sprites/prologue/standing_shy01.png"
image leia_prologue standing_surprised01 = "images/sprites/prologue/standing_surprised01.png"
image leia_prologue standing_surprised02 = "images/sprites/prologue/standing_surprised02.png"
image leia_prologue standing_warming01 = "images/sprites/prologue/standing_warming01.png"

# --- Standard VN sprite envelope ------------------------------------------
# Future-proof rule for generated character sprites:
#   * never render taller than 900 px on the 1080p game canvas
#   * never render wider than 760 px
#   * preserve aspect ratio
#   * anchor the sprite to the bottom of the screen
#   * reserve the upper ~100 px as breathing room so hair/head stays on-screen
#
# Because `fit "contain"` only scales down to this envelope, differently-sized
# source PNGs can be dropped in later without hand-tuning zoom for every pose.
# The dialogue box can overlap the lower body, which is normal VN composition.
transform prologue_leia_generated:
    xalign 0.5
    yalign 1.0
    xysize (760, 900)
    fit "contain"

# Optional positions using the same size envelope. These are ready for future
# two-character scenes without changing the sprite scale standard.
transform prologue_leia_generated_left:
    xalign 0.25
    yalign 1.0
    xysize (760, 900)
    fit "contain"

transform prologue_leia_generated_right:
    xalign 0.75
    yalign 1.0
    xysize (760, 900)
    fit "contain"

# --- Temporary Julian sprite ----------------------------------------------

image julian_placeholder = Composite(
    (520, 900),
    (175, 70), Transform(Solid("#d3a98e"), xysize=(165, 165)),
    (150, 225), Transform(Solid("#586273"), xysize=(215, 430)),
    (115, 285), Transform(Solid("#586273"), xysize=(55, 325)),
    (350, 285), Transform(Solid("#586273"), xysize=(55, 325)),
    (170, 645), Transform(Solid("#3e4550"), xysize=(70, 220)),
    (275, 645), Transform(Solid("#3e4550"), xysize=(70, 220)),
    (145, 25), Text("JULIAN\nPLACEHOLDER", size=28, color="#ffffff", text_align=0.5),
)

image julian = "julian_placeholder"

transform prologue_leia_left:
    xalign 0.18
    yalign 1.0

transform prologue_julian_right:
    xalign 0.82
    yalign 1.0
