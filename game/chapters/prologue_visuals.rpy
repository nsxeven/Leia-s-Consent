# Prologue visuals.
# Available generated art is wired directly here. Missing CGs/backgrounds remain
# explicit placeholders so the current build stays playable while art production continues.

# --- Generated backgrounds -------------------------------------------------

image bg prologue_party = "images/backgrounds/prologue/party01.webp"

# Present-day bedroom background has not been generated yet.
image bg prologue_packing = Composite(
    (1920, 1080),
    (0, 0), Solid("#2b2528"),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nRYAN + LEIA'S BEDROOM — PRESENT DAY", size=46, color="#ffffff"),
)

# --- Generated CGs ---------------------------------------------------------

# Current party CG: Leia with her friends before Ryan properly joins the group.
image cg prologue_party_arrival = "images/cg/prologue/party_leiafriends01.webp"

# --- Missing full-screen story CG placeholders -----------------------------

image cg prologue_leia_nerdy = Composite(
    (1920, 1080),
    (0, 0), Solid("#3a2c48"),
    (90, 70), Text("CG P02\nLEIA'S NERDY EXPLANATION", size=52, color="#ffffff"),
)

image cg prologue_group_warmup = Composite(
    (1920, 1080),
    (0, 0), Solid("#40304d"),
    (90, 70), Text("CG P03\nGROUP WARMS UP — RYAN MAKES SPACE FOR LEIA", size=52, color="#ffffff"),
)

image cg prologue_truth_reveal = Composite(
    (1920, 1080),
    (0, 0), Solid("#493249"),
    (90, 70), Text("CG P04\nTRUTH — LEIA POINTS AT RYAN", size=52, color="#ffffff"),
)

image cg prologue_before_kiss = Composite(
    (1920, 1080),
    (0, 0), Solid("#513342"),
    (90, 70), Text("CG P05\nDARE — THE MOMENT BEFORE THE KISS", size=52, color="#ffffff"),
)

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
# These are complete transparent sprites, separate from the later layered
# wardrobe sprite system. The `leia` tag means any new Leia sprite replaces
# the previous one automatically and `hide leia` continues to work.

image leia prologue seated_amused01 = "images/sprites/prologue/seated_amused01.png"
image leia prologue seated_defeated01 = "images/sprites/prologue/seated_defeated01.png"
image leia prologue seated_defeated02 = "images/sprites/prologue/seated_defeated02.png"
image leia prologue seated_flustered01 = "images/sprites/prologue/seated_flustered01.png"
image leia prologue seated_flustered02 = "images/sprites/prologue/seated_flustered02.png"
image leia prologue seated_laughing01 = "images/sprites/prologue/seated_laughing01.png"
image leia prologue seated_neutral01 = "images/sprites/prologue/seated_neutral01.png"
image leia prologue seated_protesting01 = "images/sprites/prologue/seated_protesting01.png"
image leia prologue standing_excited01 = "images/sprites/prologue/standing_excited01.png"
image leia prologue standing_interrupted01 = "images/sprites/prologue/standing_interrupted01.png"
image leia prologue standing_listening01 = "images/sprites/prologue/standing_listening01.png"
image leia prologue standing_neutral01 = "images/sprites/prologue/standing_neutral01.png"
image leia prologue standing_shy01 = "images/sprites/prologue/standing_shy01.png"
image leia prologue standing_surprised01 = "images/sprites/prologue/standing_surprised01.png"
image leia prologue standing_surprised02 = "images/sprites/prologue/standing_surprised02.png"
image leia prologue standing_warming01 = "images/sprites/prologue/standing_warming01.png"

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

transform prologue_leia_center:
    xalign 0.50
    yalign 1.0

transform prologue_julian_right:
    xalign 0.82
    yalign 1.0
