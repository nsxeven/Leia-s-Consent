# Chapter One — Day Two visual placeholders.
# Stable IDs are intentionally separate from final generated assets.


init -1 python:
    def lc_placeholder_text(text, **kwargs):
        """Full-screen stand-in card. {gf}/{mc}/{friend} use the current names."""
        def _card(st, at):
            shown = text
            shown = shown.replace("{gf}'S", girlfriend_name.upper() + "'S")
            shown = shown.replace("{mc}'S", player_name.upper() + "'S")
            shown = shown.replace("{friend}'S", friend_name.upper() + "'S")
            shown = shown.replace("{gf}", girlfriend_name.upper())
            shown = shown.replace("{mc}", player_name.upper())
            shown = shown.replace("{friend}", friend_name.upper())
            return Text(shown, **kwargs), None
        return DynamicDisplayable(_card)

image bg ch01_d2_breakfast = Composite(
    (1920, 1080),
    (0, 0), Solid("#d8c9ad"),
    (0, 610), Transform(Solid("#c59b72"), xysize=(1920, 470)),
    (1020, 90), Transform(Solid("#8cc9d7"), xysize=(760, 450)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY TWO — VILLA BREAKFAST", size=46, color="#352f2b"),
)

image bg ch01_d2_cafe = At("images/backgrounds/chapter 2/ch02_cafe.webp", prologue_bg_blur)

image bg ch01_d2_island_day = Composite(
    (1920, 1080),
    (0, 0), Solid("#86cbd8"),
    (0, 620), Transform(Solid("#d8bd86"), xysize=(1920, 460)),
    (300, 180), Transform(Solid("#f0e2cb"), xysize=(430, 500)),
    (850, 220), Transform(Solid("#e7d7bc"), xysize=(620, 440)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY TWO — ISLAND SHOPS / PHOTO WALK", size=46, color="#ffffff"),
)

image bg ch01_d2_sunset = Composite(
    (1920, 1080),
    (0, 0), Solid("#b06e6e"),
    (0, 260), Transform(Solid("#d79072"), xysize=(1920, 430)),
    (0, 690), Transform(Solid("#4e8191"), xysize=(1920, 390)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY TWO — SUNSET WALK", size=46, color="#ffffff"),
)

image bg ch01_d2_dinner = Composite(
    (1920, 1080),
    (0, 0), Solid("#342c30"),
    (0, 690), Transform(Solid("#755742"), xysize=(1920, 390)),
    (320, 540), Transform(Solid("#9b724f"), xysize=(1280, 220)),
    (90, 70), lc_placeholder_text("BACKGROUND PLACEHOLDER\nDAY TWO — RECTANGULAR DINNER TABLE\n{gf} + MAYA TOGETHER / {mc} + {friend} OPPOSITE", size=44, color="#ffffff"),
)

image bg ch01_d2_game_night = Composite(
    (1920, 1080),
    (0, 0), Solid("#27252e"),
    (0, 760), Transform(Solid("#5d514a"), xysize=(1920, 320)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY TWO — VILLA DRINKS / NEVER HAVE I EVER", size=46, color="#ffffff"),
)

# Day Two morning: Leia asleep (unglamorous sprawl), then waking up (darryn 2026-11-09).
image cg ch01_d2_breakfast_01 = At("images/cg/ch02/CH2D2_CG_Breakfast_01.webp", prologue_fullscreen)
image cg ch01_d2_breakfast_02 = At("images/cg/ch02/CH2D2_CG_Breakfast_02.webp", prologue_fullscreen)
image cg ch01_d2_breakfast_03 = At("images/cg/ch02/CH2D2_CG_Breakfast_03.webp", prologue_fullscreen)
image cg ch01_d2_breakfast_04 = At("images/cg/ch02/CH2D2_CG_Breakfast_04.webp", prologue_fullscreen)
image cg ch01_d2_breakfast_julian_pov = At("images/cg/ch02/CH2D2_CG_BreakfastCloseup_01.webp", prologue_fullscreen)
image cg ch01_d2_leia_sleeping = At("images/cg/ch02/CH2D2_CG_LeiaSleeping_01.webp", prologue_fullscreen)
image cg ch01_d2_leia_waking = At("images/cg/ch02/CH2D2_CG_LeiaSleeping_02.webp", prologue_fullscreen)

# Maya's arrival, first café table exchange, and her new friendship with Leia.
# The later posed walk photograph is a separate image and gallery moment.
image cg ch01_d2_maya_reveal = At("images/cg/ch02/CH2D2_CG_MayaReveal_01.webp", prologue_fullscreen)
image cg ch01_d2_maya_cafe_01 = At("images/cg/ch02/CH2D2_CG_MayaCafe_01.webp", prologue_fullscreen)
image cg ch01_d2_maya_cafe_02 = At("images/cg/ch02/CH2D2_CG_MayaCafe_02.webp", prologue_fullscreen)
image cg ch01_d2_mall_arrival = At("images/cg/ch02/CH2D2_CG_Mall_01.webp", prologue_fullscreen)
image cg ch01_d2_mall_boutique_window = At("images/cg/ch02/CH2D2_CG_Mall_02.webp", prologue_fullscreen)
# Maya holds up a red and a black dress to compare; Leia weighs in.
image cg ch01_d2_shop_dresses = At("images/cg/ch02/CH2D2_CG_Shop_01.webp", prologue_fullscreen)

image cg ch01_d2_photo_leia_maya = Composite(
    (1920, 1080),
    (0, 0), Solid("#6b8fa0"),
    (90, 70), lc_placeholder_text("CG PLACEHOLDER\nDAY TWO PHOTO — {gf} + MAYA\nNEW FRIENDSHIP / RELAXED PAIRING", size=50, color="#ffffff"),
)

image cg ch01_d2_pool_top_accident = Composite(
    (1920, 1080),
    (0, 0), Solid("#277f9f"),
    (90, 70), Text("CG PLACEHOLDER\nDAY TWO POOL — BIKINI-TOP ACCIDENT\nFLOATING TOP / ROUTE-DEPENDENT COMPANY", size=50, color="#ffffff"),
)

image cg ch01_d2_dinner_reach = Composite(
    (1920, 1080),
    (0, 0), Solid("#5a3942"),
    (90, 70), lc_placeholder_text("CG PLACEHOLDER\nDAY TWO DINNER — DELIBERATE REACH\nLOOSE NECKLINE / {mc} + {friend} VIEWING ANGLE", size=50, color="#ffffff"),
)

image cg ch01_d2_julian_underwear_reveal = Composite(
    (1920, 1080),
    (0, 0), Solid("#393744"),
    (90, 70), lc_placeholder_text("CG PLACEHOLDER\nNEVER HAVE I EVER — {friend} DOWN TO UNDERWEAR\nREACTIONS CARRY THE REVEAL", size=50, color="#ffffff"),
)


# Stable Day Two finale CG IDs. Final art can replace these one-for-one.

image cg ch01_d2_love_pool_oral_01 = Composite(
    (1920, 1080),
    (0, 0), Solid("#835d6e"),
    (90, 70), Text("CG PLACEHOLDER\\nDAY TWO FINALE — 1\\nFINAL ART PENDING", size=48, color="#ffffff"),
)

image cg ch01_d2_love_pool_oral_02 = Composite(
    (1920, 1080),
    (0, 0), Solid("#6f5266"),
    (90, 70), Text("CG PLACEHOLDER\\nDAY TWO FINALE — 2\\nFINAL ART PENDING", size=48, color="#ffffff"),
)

image cg ch01_d2_love_bedroom_01 = Composite(
    (1920, 1080),
    (0, 0), Solid("#4a394d"),
    (90, 70), Text("CG PLACEHOLDER\\nDAY TWO FINALE — 3\\nFINAL ART PENDING", size=48, color="#ffffff"),
)

image cg ch01_d2_love_bedroom_02 = Composite(
    (1920, 1080),
    (0, 0), Solid("#3f3344"),
    (90, 70), Text("CG PLACEHOLDER\\nDAY TWO FINALE — 4\\nFINAL ART PENDING", size=48, color="#ffffff"),
)

image cg ch01_d2_exhib_bed_open_01 = Composite(
    (1920, 1080),
    (0, 0), Solid("#51384d"),
    (90, 70), Text("CG PLACEHOLDER\\nDAY TWO FINALE — 5\\nFINAL ART PENDING", size=48, color="#ffffff"),
)

image cg ch01_d2_exhib_bed_open_02 = Composite(
    (1920, 1080),
    (0, 0), Solid("#4b3448"),
    (90, 70), Text("CG PLACEHOLDER\\nDAY TWO FINALE — 6\\nFINAL ART PENDING", size=48, color="#ffffff"),
)

image cg ch01_d2_exhib_bed_open_03 = Composite(
    (1920, 1080),
    (0, 0), Solid("#453041"),
    (90, 70), Text("CG PLACEHOLDER\\nDAY TWO FINALE — 7\\nFINAL ART PENDING", size=48, color="#ffffff"),
)

image cg ch01_d2_exhib_bed_open_04 = Composite(
    (1920, 1080),
    (0, 0), Solid("#3e2c3b"),
    (90, 70), Text("CG PLACEHOLDER\\nDAY TWO FINALE — 8\\nFINAL ART PENDING", size=48, color="#ffffff"),
)

image cg ch01_d2_ntr_dream_strangers = Composite(
    (1920, 1080),
    (0, 0), Solid("#492f3c"),
    (90, 70), Text("CG PLACEHOLDER\\nDAY TWO FINALE — 9\\nFINAL ART PENDING", size=48, color="#ffffff"),
)

image cg ch01_d2_ntr_dream_julian_pool = Composite(
    (1920, 1080),
    (0, 0), Solid("#3d3040"),
    (90, 70), Text("CG PLACEHOLDER\\nDAY TWO FINALE — 10\\nFINAL ART PENDING", size=48, color="#ffffff"),
)

image cg ch01_d2_ntr_dream_nhie = Composite(
    (1920, 1080),
    (0, 0), Solid("#372b37"),
    (90, 70), Text("CG PLACEHOLDER\\nDAY TWO FINALE — 11\\nFINAL ART PENDING", size=48, color="#ffffff"),
)

image cg ch01_d2_ntr_dream_wrong_room = Composite(
    (1920, 1080),
    (0, 0), Solid("#2f2832"),
    (90, 70), Text("CG PLACEHOLDER\\nDAY TWO FINALE — 12\\nFINAL ART PENDING", size=48, color="#ffffff"),
)



image bg ch01_d2_mall = At("images/backgrounds/chapter 2/ch02_mall.webp", prologue_bg_blur)
image bg ch01_d2_boutique = At("images/backgrounds/chapter 2/ch02_clothingstore.webp", prologue_bg_blur)

image cg ch01_d2_boutique_changing_room = Composite(
    (1920, 1080),
    (0, 0), Solid("#765e69"),
    (90, 70), lc_placeholder_text("CG PLACEHOLDER\nDAY TWO BOUTIQUE — MAYA + {gf} CHANGING ROOM\nMAYA RED SLIP DRESS / {gf} BLACK CUTOUT MINI", size=48, color="#ffffff"),
)

image cg ch01_d2_boutique_reveal_ryan = Composite(
    (1920, 1080),
    (0, 0), Solid("#684d5a"),
    (90, 70), lc_placeholder_text("CG PLACEHOLDER\nBOUTIQUE REVEAL — {mc} PRESENT\nCLOSE FRAMING / MAYA SECURING {gf}'S TOP", size=48, color="#ffffff"),
)

image cg ch01_d2_boutique_reveal_julian = Composite(
    (1920, 1080),
    (0, 0), Solid("#5c5964"),
    (90, 70), lc_placeholder_text("CG PLACEHOLDER\nBOUTIQUE REVEAL — {friend} PRESENT\nWIDER FRAMING / PUBLIC BOUTIQUE CONTEXT", size=48, color="#ffffff"),
)

image cg ch01_d2_boutique_slip_ryan = Composite(
    (1920, 1080),
    (0, 0), Solid("#744958"),
    (90, 70), lc_placeholder_text("CG PLACEHOLDER\nBOUTIQUE WARDROBE SLIP — {mc} PRESENT\nCLOSE / {gf} IMMEDIATELY CATCHES ONE FRONT PANEL", size=48, color="#ffffff"),
)

image cg ch01_d2_boutique_slip_julian = Composite(
    (1920, 1080),
    (0, 0), Solid("#504b58"),
    (90, 70), lc_placeholder_text("CG PLACEHOLDER\nBOUTIQUE WARDROBE SLIP — {friend} PRESENT\nWIDE / {friend}'S GAZE LINGERS BEFORE HE CATCHES HIMSELF", size=48, color="#ffffff"),
)

transform ch01_d2_leia_left:
    xalign 0.16
    yalign 1.0
    yoffset lc_sprite_yoffset

transform ch01_d2_maya_center:
    xalign 0.50
    yalign 1.0
    yoffset lc_sprite_yoffset

transform ch01_d2_julian_right:
    xalign 0.84
    yalign 1.0
    yoffset lc_sprite_yoffset

transform ch01_d2_maya_right:
    xalign 0.80
    yalign 1.0
    yoffset lc_sprite_yoffset

transform ch01_d2_julian_left:
    xalign 0.20
    yalign 1.0
    yoffset lc_sprite_yoffset


# Day Two breakfast Hidden POV (folded from the retired root
# zzzz_ch01_breakfast_presentation.rpy in clean-up PR 3): the same stable CG id
# remains mapped to the mature Gallery page. The registry owns only the opt-in cue
# and image scope.
# load order: init 1, kept from that file (lc_pov_register is defined at init 0 in
# systems/hidden_pov.rpy).
init 1 python:
    lc_pov_register(
        "d2_breakfast_julian",
        image="cg ch01_d2_breakfast_julian_pov",
        source="cg ch01_d2_breakfast_02",
        # Sparkle centre: beside and just above Julian's eye, at his temple (darryn 2026-11-15).
        center=(1785, 255),
        title="Julian's POV",
        mature=True,
        # Moments strip on the Day Two review (systems/discovery.rpy).
        day_id="ch01_d2",
        label="Julian, breakfast",
        mood="noticed",
    )
    # Moments strip: the two Day Two doors (systems/discovery.rpy). Marked when a non-neutral
    # answer is picked (Door A fix/watch, Door B nod/lap); the neutral answer plays today's text
    # and leaves the door unopened. No image: both scenes still use placeholder art.
    lc_discovery_register("ch01_d2", "d2_knot_door", "door", "Pool, the knot", "you saw it first")
    lc_discovery_register("ch01_d2", "d2_dare_door", "door", "Game night, the dare", "her eyes on you")

# Things Ryan noticed (systems/notice.rpy, docs/NOTICES.md): two push-in notices on finished
# Day Two morning CGs. The spot is the same on every lane; the captions change by lane (Love
# captions are about Leia). Both feed one extra option in the sunset talk (scene 20).
# load order: init 1, after lc_notice_register (init 0, systems/notice.rpy).
init 1 python:
    lc_notice_register(
        "d2_notice_bed_hand",
        source="cg ch01_d2_leia_sleeping",
        # Eye on her forearm (her hand itself hangs below the dialogue box); the push-in frames
        # the arm and hand, so the captions move to the top spot.
        center=(600, 680),
        focus_rect=(330, 560, 520, 500),
        lines=["Her hand had slipped off the edge of the mattress, palm up, right where I'd been lying a minute ago."],
        lane_lines={
            "love": ["Her hand had found its way over to my side of the bed and stayed there, palm up, right where I'd been.",
                     "Even asleep, [girlfriend_name] goes looking for me. I don't think she even knows she does it."],
            "exhib": ["One arm off the bed, camisole riding up, the duvet somewhere around her knees. Those useless curtains weren't hiding any of it.",
                      "Anyone walking along the sand could have looked straight in. That didn't bother me nearly as much as it should have."],
            "ntr": ["Her hand was hanging off the edge, palm open, toward the side of the bed I'd just left.",
                    "She hadn't stirred when I got up. I couldn't decide if that was sweet, or if I just didn't leave much of a gap anymore."],
        },
        day_id="ch01_d2",
        label="Morning, her hand",
        mood="still reaching",
    )
    lc_notice_register(
        "d2_notice_breakfast_smile",
        source="cg ch01_d2_breakfast_01",
        # Eye beside her hand on her cheek.
        center=(1040, 300),
        focus_rect=(640, 100, 520, 480),
        lines=["Chin propped on her hand, smiling across the table at me while [friend_name] kept talking."],
        lane_lines={
            "love": ["Chin on her hand, smiling right at me like [friend_name] wasn't even at the table.",
                     "That smile's just for me. I've never once had to ask [girlfriend_name] for it."],
            "exhib": ["Her shirt had slid right off one shoulder and [girlfriend_name] hadn't bothered fixing it, with [friend_name] sitting right there.",
                      "She caught me noticing and just smiled wider."],
            "ntr": ["She was smiling at me, chin propped on one hand, coffee in the other.",
                    "Across the table [friend_name] was sitting exactly the same way, with the same smile. I couldn't stop seeing it."],
        },
        day_id="ch01_d2",
        label="Breakfast, her smile",
        mood="across the table",
    )
