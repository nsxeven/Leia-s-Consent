# Prologue pack - Gallery rows (the Prologue tab).
#
# One gallery_row(...) per scene sequence; pages are the stable `cg <name>` images in display
#   order. Unlocks follow the CGs the player has seen. API and rules: systems/gallery_data.rpy;
#   guide: docs/DAY_PACK.md. Never rename a shipped entry id or an image name.
# Load order: init -2 (systems/gallery_data.rpy defines the helpers at init -3 and orders the
#   tabs and rows by Day at init -1).

init -2 python:

    gallery_tab("prologue", "Prologue", "prologue", 0, accent="#6f617f")

    gallery_row("pro_party_meet", "prologue", "The party",
        "The party where Ryan first notices Leia.",
        [("prologue_party_arrival", "Arrival"), ("prologue_party_couch", "On the couch")])
    gallery_row("pro_first_kiss", "prologue", "First kiss",
        "Their first kiss, a moment at a time.",
        [("prologue_first_kiss_01", "Moment 1"), ("prologue_first_kiss_02", "Moment 2"), ("prologue_first_kiss_03", "Moment 3")])
    gallery_row("pro_four_years_on", "prologue", "Four years on",
        "Four years later, packing for the trip.",
        [("prologue_present_stare", "The stare"), ("prologue_packing_banter", "Packing")])
    gallery_row("pro_departure", "prologue", "Departure",
        "Setting off for the villa.",
        ["prologue_departure"])


# Title screen reel (systems/title_screen.rpy): this Day's rows that may show by default.
# load order: init 1, after the reel's table (init 0).
init 1 python:
    LC_TITLE_SAFE_GALLERY = LC_TITLE_SAFE_GALLERY + (
        "pro_party_meet", "pro_first_kiss", "pro_four_years_on", "pro_departure",
    )
