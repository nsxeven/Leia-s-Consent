# Leia's Consent: Chapter One, Day Five visual placeholders.
# Stable ids (ch01_d5_*) are intentionally separate from final generated assets.
# Same pattern as ch01_day4_visuals.rpy: Composite text cards at 1920x1080. Replace each
# Composite with the final image once art is approved (keep the image name).
#
# STANDARD FOR EVERY DAY FIVE CG: Ryan's point of view. Ryan is NEVER in frame: no body, no hands,
# no reflection, no shadow. The camera is his eye line. (Leia's own hands, hair, clothing and
# expressions carry the shot.) Non-explicit, adults only. Intimate beats are implied (fade
# card, hand at a lantern, wrap held, cropped composition), never shown.
#
# Phone attachments store ids WITHOUT the "cg " prefix (see zz_ch01_phone_photo_aliases.rpy), so the
# attached photos (three, love_cove, private) have ImageReference aliases at the bottom of this file.

# ---------------------------------------------------------------------------
# Backgrounds
# ---------------------------------------------------------------------------

# BG TODO (artist): a working pier at seven in the morning, fishing boats, coiled rope, a white sailboat with a blue stripe and the name REASONABLE DOUBT on the stern, soft early light.
image bg ch01_d5_pier_morning = Composite(
    (1920, 1080),
    (0, 0), Solid("#cfdde6"),
    (0, 600), Transform(Solid("#6f8fa0"), xysize=(1920, 280)),
    (0, 840), Transform(Solid("#d9c9a8"), xysize=(1920, 240)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY FIVE - PIER MORNING", size=46, color="#352f2b"),
)

# BG TODO (artist): sailboat cockpit and deck in bright morning sun, cushioned bench, a tote bag and dry bags, open sea beyond the rail.
image bg ch01_d5_boat_deck = Composite(
    (1920, 1080),
    (0, 0), Solid("#8ed0dc"),
    (0, 600), Transform(Solid("#4f8da0"), xysize=(1920, 280)),
    (0, 840), Transform(Solid("#e8dcc0"), xysize=(1920, 240)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY FIVE - BOAT DECK", size=46, color="#352f2b"),
)

# BG TODO (artist): shaded foredeck under a folded pale sail, warm planks, a hat on a cushion, sea glare beyond.
image bg ch01_d5_boat_foredeck = Composite(
    (1920, 1080),
    (0, 0), Solid("#b5d6df"),
    (0, 600), Transform(Solid("#5a8fa0"), xysize=(1920, 280)),
    (0, 840), Transform(Solid("#d9c19a"), xysize=(1920, 240)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY FIVE - BOAT FOREDECK", size=46, color="#352f2b"),
)

# BG TODO (artist): stern of the sailboat, transom bench, wake foaming behind, midday light.
image bg ch01_d5_boat_stern = Composite(
    (1920, 1080),
    (0, 0), Solid("#9bcbd8"),
    (0, 600), Transform(Solid("#3f7f92"), xysize=(1920, 280)),
    (0, 840), Transform(Solid("#e5d4b0"), xysize=(1920, 240)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY FIVE - BOAT STERN", size=46, color="#352f2b"),
)

# BG TODO (artist): sea surface over a shallow reef, glittering turquoise, boat hull and swim ladder at the edge, snorkel gear on the platform.
image bg ch01_d5_reef_surface = Composite(
    (1920, 1080),
    (0, 0), Solid("#7fd0d8"),
    (0, 600), Transform(Solid("#2f9aa8"), xysize=(1920, 280)),
    (0, 840), Transform(Solid("#c9e8e0"), xysize=(1920, 240)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY FIVE - REEF SURFACE", size=46, color="#ffffff"),
)

# BG TODO (artist): small white-sand cove closed in by pale rocks, one fig tree, the sailboat anchored in the glassy water, picnic basket on a cloth.
image bg ch01_d5_cove_beach = Composite(
    (1920, 1080),
    (0, 0), Solid("#a8dfe0"),
    (0, 600), Transform(Solid("#3fa0b0"), xysize=(1920, 280)),
    (0, 840), Transform(Solid("#f0e2c0"), xysize=(1920, 240)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY FIVE - COVE BEACH", size=46, color="#352f2b"),
)

# BG TODO (artist): a second, smaller secluded cove behind warm flat rocks, clear green water, no other people, no boat in sight.
image bg ch01_d5_cove_rock = Composite(
    (1920, 1080),
    (0, 0), Solid("#a8dfd0"),
    (0, 600), Transform(Solid("#2f9a95"), xysize=(1920, 280)),
    (0, 840), Transform(Solid("#d9c9a5"), xysize=(1920, 240)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY FIVE - COVE ROCK", size=46, color="#ffffff"),
)

# BG TODO (artist): sailboat stern at sunset, amber and rose light, rail, calm sea, anchor set offshore.
image bg ch01_d5_boat_sunset = Composite(
    (1920, 1080),
    (0, 0), Solid("#e8a870"),
    (0, 600), Transform(Solid("#a05a70"), xysize=(1920, 280)),
    (0, 840), Transform(Solid("#5a3a4a"), xysize=(1920, 240)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY FIVE - BOAT SUNSET", size=46, color="#ffffff"),
)

# BG TODO (artist): small sailboat galley and saloon interior, a folding table set for four with grilled fish and lanterns, warm wood.
image bg ch01_d5_galley = Composite(
    (1920, 1080),
    (0, 0), Solid("#3a2f3a"),
    (0, 600), Transform(Solid("#7a5a45"), xysize=(1920, 280)),
    (0, 840), Transform(Solid("#c98a6a"), xysize=(1920, 240)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY FIVE - GALLEY", size=46, color="#ffffff"),
)

# BG TODO (artist): forward cabin of the sailboat at night, double bunk, a small lantern giving gold light, curved wooden hull.
image bg ch01_d5_boat_cabin = Composite(
    (1920, 1080),
    (0, 0), Solid("#2a2438"),
    (0, 600), Transform(Solid("#5a4030"), xysize=(1920, 280)),
    (0, 840), Transform(Solid("#c9a060"), xysize=(1920, 240)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY FIVE - BOAT CABIN", size=46, color="#ffffff"),
)

# BG TODO (artist): sailboat deck at night, a quilt of cushions and blankets, anchor light on the water, huge stars.
image bg ch01_d5_boat_deck_night = Composite(
    (1920, 1080),
    (0, 0), Solid("#10162a"),
    (0, 600), Transform(Solid("#26304a"), xysize=(1920, 280)),
    (0, 840), Transform(Solid("#6f86a8"), xysize=(1920, 240)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY FIVE - BOAT DECK NIGHT", size=46, color="#ffffff"),
)

# BG TODO (artist): the same pier at dawn after a gray run home, mist, a weathered post beside a blue fishing boat, a ribbon of gold on the horizon.
image bg ch01_d5_dawn_pier = Composite(
    (1920, 1080),
    (0, 0), Solid("#9aa8b5"),
    (0, 600), Transform(Solid("#c9b890"), xysize=(1920, 280)),
    (0, 840), Transform(Solid("#d8a860"), xysize=(1920, 240)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY FIVE - DAWN PIER", size=46, color="#ffffff"),
)

# ---------------------------------------------------------------------------
# CGs (placeholders). Each has an ARTIST TODO. All Ryan POV, Ryan never in frame.
# ---------------------------------------------------------------------------

# CG TODO (artist): Ryan POV, a few feet away in the water: Leia surfacing, mask pushed up on her hair, seawater on her lashes, laughing, the boat's hull behind her. No Ryan in frame (no arms, no snorkel, no shadow). Ryan POV; Ryan is never visible.
image cg ch01_d5_snorkel_surface = Composite(
    (1920, 1080),
    (0, 0), Solid("#2f9aa8"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FIVE - SNORKEL SURFACE\nRYAN POV / NO RYAN IN FRAME\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Comic. Ryan POV: Julian frozen with a drumstick in one fist and a bee on the lid of the honey jar in front of him; Maya off to the side losing it with laughter. Ryan POV; Ryan is never visible.
image cg ch01_d5_cove_lunch_bee = Composite(
    (1920, 1080),
    (0, 0), Solid("#c0a060"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FIVE - COVE LUNCH BEE\nRYAN POV / NO RYAN IN FRAME\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): The photo itself, full screen: Julian pale beside Leia, Maya triumphant, all three squinting into the light, the cove behind them. Used also as a phone attachment (alias ch01_d5_photo_three). Ryan POV; Ryan is never visible.
image cg ch01_d5_photo_three = Composite(
    (1920, 1080),
    (0, 0), Solid("#b8a080"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FIVE - PHOTO THREE\nRYAN POV / NO RYAN IN FRAME\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Ryan POV, treading water in clear green: Leia close, forehead tipped toward the lens, her hands resting on the shoulders of the unseen camera-holder (her hands only, nothing of Ryan drawn). Ryan POV; Ryan is never visible.
image cg ch01_d5_love_cove_swim = Composite(
    (1920, 1080),
    (0, 0), Solid("#3fa0b0"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FIVE - LOVE COVE SWIM\nRYAN POV / NO RYAN IN FRAME\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Ryan POV: Leia on a warm rock, knees up, chin on her arm, sun on her wet hair, looking up with a soft, whole, listening expression. Also the phone attachment 'ch01_d5_photo_love_cove'. Ryan POV; Ryan is never visible.
image cg ch01_d5_love_cove_secret = Composite(
    (1920, 1080),
    (0, 0), Solid("#c9a878"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FIVE - LOVE COVE SECRET\nRYAN POV / NO RYAN IN FRAME\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Ryan POV: Leia lying on her front on a warm rock, swimsuit ties undone and her arms folded under her chin, head turned toward the lens, delighted at her own nerve. COVERED / implied; crop so nothing explicit reads. Ryan POV; Ryan is never visible.
image cg ch01_d5_exhib_cove_01 = Composite(
    (1920, 1080),
    (0, 0), Solid("#a8885a"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FIVE - EXHIB COVE 01\nRYAN POV / NO RYAN IN FRAME\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Ryan POV: Leia sitting on the rock in the sun, top folded beside her, arms loosely crossed, face tipped up, eyes on the lens, laughing at herself. COMFORTABLE and IMPLIED: crop at the collarbone, shoulders and face only. Nothing explicit. Ryan POV; Ryan is never visible.
image cg ch01_d5_exhib_cove_02 = Composite(
    (1920, 1080),
    (0, 0), Solid("#a8885a"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FIVE - EXHIB COVE 02\nRYAN POV / NO RYAN IN FRAME\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Ryan POV over Leia's shoulder (her back and hair in the foreground, covered): far down the cove Maya holds a paperback up like a screen, Julian stares at the horizon. Sub-variant 'Ryan likes watching'. Ryan POV; Ryan is never visible.
image cg ch01_d5_exhib_cove_watching = Composite(
    (1920, 1080),
    (0, 0), Solid("#8a7a5a"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FIVE - EXHIB COVE WATCHING\nRYAN POV / NO RYAN IN FRAME\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Ryan POV: Leia seated on the rock, knees drawn up, the hairclip open in both hands, serious and a little wet-eyed, looking up at the lens. Visible empty rock beside her where Ryan sits. No third person. Ryan POV; Ryan is never visible.
image cg ch01_d5_ntr_cove_talk = Composite(
    (1920, 1080),
    (0, 0), Solid("#5a6a60"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FIVE - NTR COVE TALK\nRYAN POV / NO RYAN IN FRAME\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Ryan POV: Leia's back to the camera at the stern rail, the hairclip clasped in one hand, the horizon in front of her. A strip of empty rail beside her. No third person. Ryan POV; Ryan is never visible.
image cg ch01_d5_ntr_deck_alone = Composite(
    (1920, 1080),
    (0, 0), Solid("#7a5a6a"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FIVE - NTR DECK ALONE\nRYAN POV / NO RYAN IN FRAME\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Ryan POV down the length of the deck: Leia leaning on the stern rail, the last of the sunset across her face, looking back at the lens. Warm, quiet. Ryan POV; Ryan is never visible.
image cg ch01_d5_sunset_deck = Composite(
    (1920, 1080),
    (0, 0), Solid("#c98a60"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FIVE - SUNSET DECK\nRYAN POV / NO RYAN IN FRAME\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Ryan POV fade card: cabin or deck at night, Leia's hand turning the lantern down to a coin of gold, a pale rope bracelet on her wrist. One figure only. Implied. Ryan POV; Ryan is never visible.
image cg ch01_d5_love_night_01 = Composite(
    (1920, 1080),
    (0, 0), Solid("#4a3a50"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FIVE - LOVE NIGHT 01\nRYAN POV / NO RYAN IN FRAME\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Ryan POV: Leia on the deck cushions under a blanket drawn to her chin, stars overhead, eyes on the lens, delighted and a little daring. Covered. One figure only. Ryan POV; Ryan is never visible.
image cg ch01_d5_exhib_night_01 = Composite(
    (1920, 1080),
    (0, 0), Solid("#2a2f48"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FIVE - EXHIB NIGHT 01\nRYAN POV / NO RYAN IN FRAME\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Ryan POV fade card: Leia's hand setting the open hairclip on a shelf beside a lantern, soft gold light. One figure only, no third person. Quiet. Ryan POV; Ryan is never visible.
image cg ch01_d5_ntr_night_01 = Composite(
    (1920, 1080),
    (0, 0), Solid("#3a3048"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FIVE - NTR NIGHT 01\nRYAN POV / NO RYAN IN FRAME\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): The photo Leia sends for Ryan alone: Leia at the cove, laughing, framed by HER call (face only, or cropped at the shoulders). Not explicit. Phone attachment alias ch01_d5_photo_private. Ryan POV; Ryan is never visible.
image cg ch01_d5_photo_private = Composite(
    (1920, 1080),
    (0, 0), Solid("#a09078"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FIVE - PHOTO PRIVATE\nRYAN POV / NO RYAN IN FRAME\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# CG TODO (artist): Close-up of the printed invitation pinned to a weathered post with a brass tack: THE NIGHT OF THE LANTERNS. A second line in a different, looser hand varies by track (see 07_cg_checklist.md). A prop shot, no people. Ryan POV; Ryan is never visible.
image cg ch01_d5_invitation = Composite(
    (1920, 1080),
    (0, 0), Solid("#c8b890"),
    (90, 70), Text("CG PLACEHOLDER\nDAY FIVE - INVITATION\nRYAN POV / NO RYAN IN FRAME\nFINAL ART PENDING", size=48, color="#ffffff"),
)

# ---------------------------------------------------------------------------
# Phone attachment aliases (no "cg " prefix, same convention as Day 1 and Day 4 photos)
# ---------------------------------------------------------------------------

image ch01_d5_photo_three = ImageReference("cg ch01_d5_photo_three")
image ch01_d5_photo_love_cove = ImageReference("cg ch01_d5_love_cove_secret")
image ch01_d5_photo_private = ImageReference("cg ch01_d5_photo_private")
