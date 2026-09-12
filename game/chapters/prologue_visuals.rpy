# Prologue visual placeholders.
# Replace these displayables with final ComfyUI-generated assets using the same image names.
# Narrative beats use full-screen CGs; choices deliberately switch back to backgrounds + sprites.

# --- Backgrounds used during interactive / decision moments -----------------

image bg prologue_party = Composite(
    (1920, 1080),
    (0, 0), Solid("#2a2034"),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nCOLLEGE PARTY — FOUR YEARS AGO", size=46, color="#ffffff"),
)

image bg prologue_packing = Composite(
    (1920, 1080),
    (0, 0), Solid("#2b2528"),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nRYAN + LEIA'S BEDROOM — PRESENT DAY", size=46, color="#ffffff"),
)

# --- Full-screen story CG placeholders --------------------------------------

image cg prologue_party_arrival = Composite(
    (1920, 1080),
    (0, 0), Solid("#342641"),
    (90, 70), Text("CG P01\nPARTY ARRIVAL — RYAN NOTICES LEIA", size=52, color="#ffffff"),
)

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

# --- Temporary Julian sprite for decisions ---------------------------------

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
