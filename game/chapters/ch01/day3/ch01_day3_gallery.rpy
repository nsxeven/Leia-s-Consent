# Day Three pack - Gallery rows (the Day 3 tab).
#
# One gallery_row(...) per scene sequence; pages are the stable `cg <name>` images in display
#   order. Unlocks follow the CGs the player has seen. API and rules: systems/gallery_data.rpy;
#   guide: docs/DAY_PACK.md. Never rename a shipped entry id or an image name.
# Load order: init -2 (systems/gallery_data.rpy defines the helpers at init -3 and orders the
#   tabs and rows by Day at init -1).

init -2 python:

    gallery_tab("ch01_d3", "Day 3", "ch01", 3, accent="#7c6258")

    # CGs that are still text placeholders (final art pending): remove a name when its art lands.
    GALLERY_PLACEHOLDER_IMAGES.update([
        "ch01_d3_cutout_stranger",
    ])

    gallery_row("d3_cutout_stranger", "ch01_d3", "The cutout stand",
        "Leia chooses to stay in the novelty cutout stand on the beach path.",
        ["ch01_d3_cutout_stranger"],
        route="NTR lane (Leia chose it)")
