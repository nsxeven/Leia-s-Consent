# Leia's Consent: Chapter One, Day Four visual placeholders.
# Stable ids (ch01_d4_*) are intentionally separate from final generated assets.
# Same pattern as ch01_day2_visuals.rpy / ch01_day3_visuals.rpy: Composite text
# cards at 1920x1080. Replace each Composite with the final image once art is approved.
#
# Phone attachments store ids WITHOUT the "cg " prefix (see zz_ch01_phone_photo_aliases.rpy),
# so the photo CGs sent as attachments (candid, pose, maya_julian) have an ImageReference alias at the bottom of this file.
#
# ALL CGs: NON-EXPLICIT. Adults only. Consent reads from expression and body language.
# Intimate beats are implied (cut to card, fade, or cropped composition), never shown.
# EVERY CG is Ryan's point of view with Ryan never visible in frame.

# ---------------------------------------------------------------------------
# Backgrounds
# ---------------------------------------------------------------------------

# BG TODO (artist): sunny terrace, long breakfast table for four, pastel awnings,
# view over the pool toward the sea. Same villa as ch01_d2_breakfast, brighter.
image bg ch01_d4_breakfast_terrace = Composite(
    (1920, 1080),
    (0, 0), Solid("#e6d8bd"),
    (0, 640), Transform(Solid("#c9a47a"), xysize=(1920, 440)),
    (1040, 100), Transform(Solid("#8ed0dc"), xysize=(740, 430)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY FOUR - VILLA TERRACE BREAKFAST", size=46, color="#352f2b"),
)

# BG TODO (artist): open-air island market, striped stalls (honey, sunglasses, spices,
# fabric), narrow lane, morning light. Readable signage for a honey stall.
image bg ch01_d4_market = Composite(
    (1920, 1080),
    (0, 0), Solid("#f0d9a8"),
    (0, 700), Transform(Solid("#b88f62"), xysize=(1920, 380)),
    (160, 180), Transform(Solid("#d8795e"), xysize=(520, 420)),
    (760, 150), Transform(Solid("#e9c15a"), xysize=(480, 450)),
    (1320, 190), Transform(Solid("#6fb2a6"), xysize=(460, 410)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY FOUR - ISLAND MARKET LANE", size=46, color="#352f2b"),
)

# BG TODO (artist): low harbor wall, small fishing boats, late-afternoon light.
image bg ch01_d4_harbor_wall = Composite(
    (1920, 1080),
    (0, 0), Solid("#9fd0dc"),
    (0, 560), Transform(Solid("#4f8da0"), xysize=(1920, 280)),
    (0, 820), Transform(Solid("#c9b895"), xysize=(1920, 260)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY FOUR - HARBOR WALL / LATE AFTERNOON", size=46, color="#ffffff"),
)

# BG TODO (artist): rooftop-terrace restaurant at dusk, string lights, four-top table
# near the rail. Warm, not nightclub-dark. Same family as ch01_d2_dinner.
image bg ch01_d4_dinner_terrace = Composite(
    (1920, 1080),
    (0, 0), Solid("#3a2f3a"),
    (0, 690), Transform(Solid("#7a5a45"), xysize=(1920, 390)),
    (1100, 120), Transform(Solid("#c98a6a"), xysize=(640, 360)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY FOUR - DUSK DINNER TERRACE", size=46, color="#ffffff"),
)

# BG TODO (artist): quiet coastal path back to the villa, blue hour, lanterns just coming on.
image bg ch01_d4_dusk_path = Composite(
    (1920, 1080),
    (0, 0), Solid("#4b4a6e"),
    (0, 260), Transform(Solid("#a0607a"), xysize=(1920, 300)),
    (0, 760), Transform(Solid("#2f3a4a"), xysize=(1920, 320)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY FOUR - DUSK PATH HOME", size=46, color="#ffffff"),
)

# BG TODO (artist): villa upper terrace at night, low railing, beach path visible below,
# a few distant lights. Used by the Exhibitionism and NTR night beats.
image bg ch01_d4_terrace_night = Composite(
    (1920, 1080),
    (0, 0), Solid("#1f2538"),
    (0, 700), Transform(Solid("#3b3f52"), xysize=(1920, 380)),
    (1240, 160), Transform(Solid("#6f86a8"), xysize=(520, 420)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY FOUR - VILLA TERRACE AT NIGHT", size=46, color="#ffffff"),
)

# ---------------------------------------------------------------------------
# CGs (placeholders). Each has an ARTIST TODO.
# STANDARD FOR EVERY DAY FOUR CG: Ryan's point of view. Ryan is NEVER in frame: no body,
# no hands, no reflection, no shadow. The camera is his eye line. (Leia's own hands, hair,
# clothing and expressions carry the shot.) Non-explicit, adults only.
# ---------------------------------------------------------------------------

# CG TODO (artist): Ryan POV. Leia mid-laugh at the market stall, caught off guard, sunlight
# in her hair, tortoiseshell sunglasses pushed up her nose, hairclip visible. Warm, candid,
# eyes just off camera. No Ryan in frame.
image cg ch01_d4_photo_candid = Composite(
    (1920, 1080),
    (0, 0), Solid("#7a5f55"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FOUR PHOTO HUNT - CANDID\nRYAN POV / LEIA MID-LAUGH / MARKET LIGHT / HAIRCLIP\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Ryan POV. Leia posing for the camera at the sunglasses stall, round
# sunglasses pushed low, one eyebrow up, playful and confident, looking straight down the
# lens. Clothing as per her chosen day outfit. No Ryan in frame.
image cg ch01_d4_photo_pose = Composite(
    (1920, 1080),
    (0, 0), Solid("#6e5a73"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FOUR PHOTO HUNT - POSED\nRYAN POV / LEIA + SUNGLASSES / THE EYEBROW\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Ryan POV. Leia has just taken HER shot: she lowers Ryan's phone from her
# eye, grinning, about to turn the screen toward the camera. A pyramid of honey jars on the
# stall counter in the foreground, stall owner grinning behind her. Comic, affectionate.
# Ryan is NOT shown (no hands, no jar in his grip). The joke lives in her expression.
# The photo she took (of Ryan) is described in dialogue only and is never shown, so there is
# no phone attachment alias for this one.
image cg ch01_d4_photo_swap = Composite(
    (1920, 1080),
    (0, 0), Solid("#6a6f55"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FOUR PHOTO HUNT - LEIA'S TURN\nRYAN POV / LEIA LOWERING THE PHONE, GRINNING / HONEY STALL\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Julian's entry for Maya's prompt, shown full-screen as the photo on the
# phone. Maya mid-pose, perfectly framed, a large blurred thumb over one corner of the
# lens. Comic. No Ryan in frame (it is Julian's photograph).
image cg ch01_d4_photo_maya_julian = Composite(
    (1920, 1080),
    (0, 0), Solid("#6f5a4a"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FOUR PHOTO HUNT - JULIAN SHOOTS MAYA\nTHE PHOTO ITSELF / GREAT POSE / THUMB OVER LENS / COMIC\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Ryan POV. Slow dance in soft lamplight. Reused by all three Love options
# (kitchen dance, terrace talk, open door), so keep the background non-specific (warm bokeh). Leia's face and
# shoulders fill the frame, eyes closed, her forehead tipped toward camera, her hands
# resting on the shoulders of the unseen camera-holder (her hands only, nothing of Ryan).
# Lamplight, quiet. Dressed. No nudity.
image cg ch01_d4_love_night_01 = Composite(
    (1920, 1080),
    (0, 0), Solid("#4a3a50"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FOUR LOVE NIGHT - 01\nRYAN POV / SLOW DANCE / LEIA CLOSE, EYES CLOSED / LAMPLIGHT\nNON-EXPLICIT / FINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Ryan POV fade card. Bedroom, curtains drawn, warm lamplight on fabric.
# Only Leia's hand reaching toward the lamp switch, and her shoulder in soft shadow.
# One figure at most. Implied only. Nothing else shown.
image cg ch01_d4_love_night_02 = Composite(
    (1920, 1080),
    (0, 0), Solid("#392f45"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FOUR LOVE NIGHT - 02\nRYAN POV / CURTAINS DRAWN / LEIA'S HAND REACHING FOR THE LAMP\nNON-EXPLICIT / FINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Ryan POV. Leia on the night terrace, cream wrap held closed with both
# hands, one shoulder bare, looking back DOWN THE LENS with a flushed, delighted, slightly
# daring expression. Beach path glow behind her. Covered. This is the 'tease' frame.
# No Ryan in frame.
image cg ch01_d4_exhib_terrace_01 = Composite(
    (1920, 1080),
    (0, 0), Solid("#2f3350"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FOUR EXHIBITION - 01\nRYAN POV / LEIA ON TERRACE / WRAP HELD CLOSED / LOOKING INTO LENS\nCOVERED / FINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Ryan POV, same terrace framing, the wrap open for one beat. BRIEF and
# IMPLIED: crop at the collarbone/shoulder line or hold the wrap edges so the beat reads
# without anatomy being the subject. Her eyes are on the lens (on Ryan), not on anyone
# below. She is laughing at her own nerve. No Ryan in frame. NO explicit anatomy.
image cg ch01_d4_exhib_terrace_02 = Composite(
    (1920, 1080),
    (0, 0), Solid("#3a2f4e"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FOUR EXHIBITION - 02\nRYAN POV / WRAP OPEN FOR ONE BEAT / BRIEF AND IMPLIED / EYES ON LENS\nNON-EXPLICIT / FINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Ryan POV, 'Ryan likes watching' sub-variant. Over Leia's shoulder (her
# back and hair in the foreground, wrap on) at the terrace rail, the lights of the beach path
# below. She is glancing back toward the lens, conspiratorial, deciding. Covered.
# No Ryan in frame.
image cg ch01_d4_exhib_watching = Composite(
    (1920, 1080),
    (0, 0), Solid("#35304a"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FOUR EXHIBITION - RYAN LIKES WATCHING (SUB-VARIANT)\nRYAN POV / LEIA AT THE RAIL, GLANCING BACK / COVERED\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Ryan POV, NTR lane. Night terrace, Leia seated on the low wall looking up
# at the lens, the hairclip open in her hands, eyes serious and a little wet. A visible gap
# of empty wall beside her where Ryan would sit. Quiet, not accusatory. No third person,
# no Ryan in frame.
image cg ch01_d4_ntr_terrace_talk = Composite(
    (1920, 1080),
    (0, 0), Solid("#2a2f45"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FOUR NTR LANE - THE TALK\nRYAN POV / LEIA ON THE WALL, HAIRCLIP OPEN / EMPTY SPACE BESIDE HER\nNON-EXPLICIT / FINAL ART PENDING", size=48, color="#ffffff"),
)

# ---------------------------------------------------------------------------
# Phone attachment aliases (no "cg " prefix, same convention as Day 1 photos)
# ---------------------------------------------------------------------------

image ch01_d4_photo_candid = ImageReference("cg ch01_d4_photo_candid")
image ch01_d4_photo_pose = ImageReference("cg ch01_d4_photo_pose")
image ch01_d4_photo_maya_julian = ImageReference("cg ch01_d4_photo_maya_julian")
