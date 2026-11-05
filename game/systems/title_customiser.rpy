# Title-screen customiser (PR 2, darryn 2026-11-06): background, Leia's outfit and
# expression for the main menu, plus the slower title-only breathing rig.
#
# Unlock rule: an option unlocks forever once it has been SEEN in any playthrough
# (Ren'Py's persistent seen-image record), so no story-script changes are needed.
# The default background/outfit are always available.
#
# Content rule: options with mature=True only appear when the player has switched
# the title screen to "all unlocked" (persistent.lc_title_all_memories).
#
# Adding outfits later (new story outfits, shop outfits or a patron's custom
# outfit pack): call lc_title_register_outfit(...) from an `init 1 python:` block.
# Base/chest paths follow the existing Leia rig (941 x 1672 canvas; Hair.png and
# the expression faces are shared). See docs/TITLE_SCREEN.md.

default persistent.lc_title_bg = "pool_evening"
default persistent.lc_title_outfit = "purple_dress"
default persistent.lc_title_expression = "smile"
# Sprite tags the cast system has shown (it shows under slot tags, so Ren'Py's own
# seen-image record never sees e.g. "leia_blue_bikini"). Filled by cast_staging.
default persistent.lc_title_seen_sprites = set()

# One breath = inhale + pause + exhale + pause. The in-game rig uses 0.65 s phases;
# the title screen breathes slower (darryn 2026-11-06).
define LC_TITLE_BREATH = 1.0
define LC_TITLE_BREATH_PAUSE = 0.15

transform lc_title_chest_breathe:
    xzoom 1.0
    xoffset 0
    block:
        parallel:
            ease LC_TITLE_BREATH xzoom 1.04
        parallel:
            ease LC_TITLE_BREATH xoffset -18
        pause LC_TITLE_BREATH_PAUSE
        parallel:
            ease LC_TITLE_BREATH xzoom 1.0
        parallel:
            ease LC_TITLE_BREATH xoffset 0
        pause LC_TITLE_BREATH_PAUSE
        repeat

# Logo: a light sheen sweeps across every ~7 s (masked to the letters).
transform lc_title_logo_sheen:
    subpixel True
    xpos -260
    pause 2.2
    block:
        ease 1.5 xpos 1120
        pause 5.5
        xpos -260
        repeat

transform lc_title_hair_idle:
    yoffset 0
    block:
        ease LC_TITLE_BREATH yoffset 5
        pause LC_TITLE_BREATH_PAUSE
        ease LC_TITLE_BREATH yoffset 0
        pause LC_TITLE_BREATH_PAUSE
        repeat

init -1 python:

    LC_LEIA_SPRITE_DIR = "images/sprites/leia/"

    LC_TITLE_EXPRESSIONS = [
        # (id, label, image, mature)
        ("smile", "Smile", LC_LEIA_SPRITE_DIR + "expressions/Smile.png", False),
        ("neutral", "Neutral", "leia_expression_neutral_blink", False),
        ("shy", "Shy", LC_LEIA_SPRITE_DIR + "expressions/Shy.png", False),
        ("pout", "Pout", LC_LEIA_SPRITE_DIR + "expressions/Pout.png", False),
        ("flustered", "Flustered", LC_LEIA_SPRITE_DIR + "expressions/Flustered.png", False),
        ("skeptical", "Skeptical", LC_LEIA_SPRITE_DIR + "expressions/Skeptical.png", False),
        ("angry", "Angry", LC_LEIA_SPRITE_DIR + "expressions/Angry.png", False),
        ("ahegao", "Ahegao", LC_LEIA_SPRITE_DIR + "expressions/Ahegao.png", True),
    ]

    LC_TITLE_OUTFITS = []
    LC_TITLE_BACKGROUNDS = []

    def lc_title_register_outfit(outfit_id, label, base, chest, seen_tag=None, mature=False,
                                 default=False, always_unlocked=False, credit=None, hair=None, seen_cgs=()):
        """Add (or replace) a title-screen outfit.

        base/chest: image paths on the 941 x 1672 Leia canvas.
        seen_tag:   the in-game sprite tag (e.g. "leia_blue_bikini"); the outfit unlocks
                    once any image with this tag has been shown in any playthrough.
        seen_cgs:   CG names (without "cg ") that show Leia in this outfit; seeing any of
                    them also unlocks it (covers playthroughs from before this feature).
        always_unlocked: for outfits that are owned outright (e.g. a patron's pack).
        credit:     optional line shown under the sprite, e.g. "Outfit made for <name>".
        """
        global LC_TITLE_OUTFITS
        LC_TITLE_OUTFITS = [o for o in LC_TITLE_OUTFITS if o["id"] != outfit_id]
        LC_TITLE_OUTFITS.append(dict(
            id=outfit_id, label=label, base=base, chest=chest, hair=hair or (LC_LEIA_SPRITE_DIR + "Hair.png"),
            seen_tag=seen_tag, mature=bool(mature), default=bool(default),
            always_unlocked=bool(always_unlocked), credit=credit, seen_cgs=tuple(seen_cgs),
        ))

    def lc_title_register_background(bg_id, label, path, seen_tags=(), mature=False, default=False):
        """Add (or replace) a title-screen background; unlocks once any `bg <tag>` in seen_tags was shown."""
        global LC_TITLE_BACKGROUNDS
        LC_TITLE_BACKGROUNDS = [b for b in LC_TITLE_BACKGROUNDS if b["id"] != bg_id]
        LC_TITLE_BACKGROUNDS.append(dict(id=bg_id, label=label, path=path, seen_tags=tuple(seen_tags),
                                         mature=bool(mature), default=bool(default)))

    _d = LC_LEIA_SPRITE_DIR
    lc_title_register_outfit("purple_dress", "Lilac dress", _d + "CH1/Base_PurpleDress.png", _d + "CH1/Chest_PurpleDress.png", "leia_purple_dress", default=True, seen_cgs=("ch01_dress_reveal",))
    lc_title_register_outfit("casual", "Travel casual", _d + "PRO/Base_Casual.png", _d + "PRO/Chest_Casual.png", "leia_casual", seen_cgs=("prologue_departure", "ch01_villa_arrival"))
    lc_title_register_outfit("prologue_party", "The party", _d + "PRO/Base_PrologueParty.png", _d + "PRO/Chest_PrologueParty.png", "leia_prologue_party", seen_cgs=("prologue_party_arrival", "prologue_party_couch"))
    lc_title_register_outfit("blue_bikini", "Blue bikini", _d + "CH1/Base_BlueBikini.png", _d + "CH1/Chest_BlueBikini.png", "leia_blue_bikini", seen_cgs=("ch01_swimsuit_choice_blue", "ch01_sunscreen_blue", "ch01_sunscreen_apply_blue"))
    lc_title_register_outfit("white_ruffle", "White ruffle", _d + "CH1/Base_WhiteRuffle.png", _d + "CH1/Chest_WhiteRuffle.png", "leia_white_ruffle", seen_cgs=("ch01_swimsuit_choice_white", "ch01_sunscreen_white", "ch01_sunscreen_apply_white"))
    lc_title_register_outfit("lounge", "Loungewear", _d + "CH1/Base_Lounge.png", _d + "CH1/Chest_Lounge.png", "leia_lounge", seen_cgs=("ch01_movie_cuddle_blanket", "ch01_movie_blanket_hand", "ch01_movie_no_blanket", "ch01_movie_micro_test_glance"))
    lc_title_register_outfit("towel", "Towel", _d + "CH1/Base_Towel.png", _d + "CH1/Chest_Towel.png", "leia_towel", mature=True, seen_cgs=("ch01_towel_call_down", "ch01_towel_shift_01"))
    lc_title_register_outfit("purple_dress_wet", "Lilac dress (soaked)", _d + "CH1/Base_PurpleDressWet.png", _d + "CH1/Chest_PurpleDressWet.png", "leia_purple_dress_wet", mature=True, seen_cgs=("ch01_dinner_spill_02", "ch01_dinner_spill_03"))
    lc_title_register_outfit("purple_dress_no_bra", "Lilac dress (no bra)", _d + "CH1/Base_PurpleDressNoBra.png", _d + "CH1/Chest_PurpleDressNoBra.png", "leia_purple_dress_no_bra", mature=True, seen_cgs=("ch01_dinner_sticky_bra", "ch01_dinner_restroom_return_01"))

    _b = "images/backgrounds/"
    lc_title_register_background("pool_evening", "Pool, evening", _b + "villa/villa_pool_evening.webp", ("ch01_pool_evening",), default=True)
    lc_title_register_background("pool_day", "Pool, day", _b + "villa/villa_pool_day.webp", ("ch01_pool_day", "ch01_villa_pool"))
    lc_title_register_background("pool_lounge", "Upstairs lounge", _b + "chapter 1/ch01_villa_pool_upstairs.webp", ("ch01_pool_lounge",))
    lc_title_register_background("living_evening", "Living room, evening", _b + "villa/villa_living_evening.webp", ("ch01_villa_living_evening",))
    lc_title_register_background("living_day", "Living room, day", _b + "villa/villa_living_day.webp", ("ch01_villa_living",))
    lc_title_register_background("bedroom_evening", "Bedroom, evening", _b + "villa/villa_master_evening.webp", ("ch01_villa_bedroom_evening",))
    lc_title_register_background("bedroom_day", "Bedroom, day", _b + "villa/villa_master_day.webp", ("ch01_master_bedroom",))
    lc_title_register_background("entry_evening", "Villa door, evening", _b + "villa/villa_frontdoor_evening.webp", ("ch01_villa_entry_evening",))
    lc_title_register_background("villa_arrival", "Arrival", _b + "chapter 1/ch01_villa_arrival.webp", ("ch01_villa_exterior",))
    lc_title_register_background("restaurant", "Restaurant", _b + "chapter 1/ch01_restaurant.webp", ("ch01_restaurant_evening",))
    lc_title_register_background("bar", "Bar", _b + "chapter 1/ch01_bar.webp", ("ch01_restaurant_bar",))
    lc_title_register_background("prologue_party", "The party", _b + "prologue/PRO_party.webp", ("prologue_party",))
    lc_title_register_background("prologue_bedroom", "Packing night", _b + "prologue/PRO_bedroom.webp", ("prologue_packing",))

init python:

    # Title-screen UI state (store dict so nested screens can all read/set it).
    lc_title_ui = {"editing": False, "tab": "background", "extras": False}

    _lc_title_seen_cache = {"n": -1, "tags": set()}

    def lc_title_seen_tags():
        """Image tags ever shown on this profile (cached by the size of the seen record)."""
        seen = getattr(persistent, "_seen_images", None) or {}
        if len(seen) != _lc_title_seen_cache["n"]:
            _lc_title_seen_cache["n"] = len(seen)
            _lc_title_seen_cache["tags"] = set(k[0] for k in seen if k)
        return _lc_title_seen_cache["tags"]

    def lc_title_show_mature():
        return bool(persistent.lc_title_all_memories)

    # ------------------------------------------------------------------ outfits
    def lc_title_outfit(outfit_id):
        for o in LC_TITLE_OUTFITS:
            if o["id"] == outfit_id:
                return o
        return None

    def lc_title_note_sprite(tag):
        """Called by the cast system whenever it shows a sprite (unlocks title outfits)."""
        seen = persistent.lc_title_seen_sprites
        if seen is None:
            seen = persistent.lc_title_seen_sprites = set()
        if tag and tag not in seen:
            seen.add(tag)

    def lc_title_outfit_unlocked(o):
        if o["default"] or o["always_unlocked"]:
            return True
        if o["seen_tag"] and (o["seen_tag"] in lc_title_seen_tags() or o["seen_tag"] in (persistent.lc_title_seen_sprites or ())):
            return True
        return any(renpy.seen_image(("cg", c)) for c in o["seen_cgs"])

    def lc_title_outfit_options():
        return [o for o in LC_TITLE_OUTFITS if lc_title_show_mature() or not o["mature"]]

    def lc_title_current_outfit():
        o = lc_title_outfit(persistent.lc_title_outfit)
        if o is None or not lc_title_outfit_unlocked(o) or (o["mature"] and not lc_title_show_mature()):
            o = next(x for x in LC_TITLE_OUTFITS if x["default"])
        return o

    # -------------------------------------------------------------- expressions
    def lc_title_expression_options():
        return [e for e in LC_TITLE_EXPRESSIONS if lc_title_show_mature() or not e[3]]

    def lc_title_current_expression():
        for e in lc_title_expression_options():
            if e[0] == persistent.lc_title_expression:
                return e
        return LC_TITLE_EXPRESSIONS[0]

    # -------------------------------------------------------------- backgrounds
    def lc_title_background(bg_id):
        for b in LC_TITLE_BACKGROUNDS:
            if b["id"] == bg_id:
                return b
        return None

    def lc_title_background_unlocked(b):
        tags = lc_title_seen_tags()
        if b["default"]:
            return True
        if "bg" not in tags:
            return False
        return any(renpy.seen_image(("bg", t)) for t in b["seen_tags"])

    def lc_title_background_options():
        return [b for b in LC_TITLE_BACKGROUNDS if lc_title_show_mature() or not b["mature"]]

    def lc_title_current_background():
        b = lc_title_background(persistent.lc_title_bg)
        if b is None or not lc_title_background_unlocked(b) or (b["mature"] and not lc_title_show_mature()):
            b = next(x for x in LC_TITLE_BACKGROUNDS if x["default"])
        return b

    # ------------------------------------------------------------- displayables
    def lc_title_bg_image(b):
        return Transform(b["path"], fit="cover", xysize=(1920, 1080))

    def lc_title_bg_thumb(b, w=196, h=110):
        return Transform(b["path"], fit="cover", xysize=(w, h))

    def lc_title_leia_rig(o, expression):
        """Animated Leia for the title screen (slower, in-sync body/chest/hair breathing)."""
        face = expression[2]
        rig = Fixed(
            o["base"],
            At(o["chest"], lc_title_chest_breathe),
            face,
            At(o["hair"], lc_title_hair_idle),
            xysize=(941, 1672),
        )
        return Fixed(lc_sprite_silhouette(rig), xysize=(941, 1672))

    def lc_title_outfit_thumb(o, locked=False):
        still = Fixed(o["base"], o["chest"], LC_LEIA_SPRITE_DIR + "expressions/Smile.png", o["hair"], xysize=(941, 1672))
        crop = Transform(still, crop=(190, 30, 560, 680), zoom=0.25)
        if locked:
            return Transform(crop, matrixcolor=BrightnessMatrix(-1.0), alpha=0.45)
        return crop

    def lc_title_face_thumb(o, expression):
        face = (LC_LEIA_SPRITE_DIR + "expressions/Neutral01.png") if expression[0] == "neutral" else expression[2]
        still = Fixed(o["base"], o["chest"], face, o["hair"], xysize=(941, 1672))
        return Transform(still, crop=(300, 40, 340, 300), zoom=0.41)

    # Cached so screen redraws (hover etc.) keep the same displayable and the
    # breathing/drift animations never restart.
    _lc_title_disp_cache = {}

    def lc_title_cached(key, make):
        d = _lc_title_disp_cache.get(key)
        if d is None:
            if len(_lc_title_disp_cache) > 24:
                _lc_title_disp_cache.clear()
            d = _lc_title_disp_cache[key] = make()
        return d

    def lc_title_bg_now():
        b = lc_title_current_background()
        return lc_title_cached(("bg", b["id"]), lambda: lc_title_bg_image(b))

    def lc_title_leia_now():
        o = lc_title_current_outfit()
        e = lc_title_current_expression()
        return lc_title_cached(("leia", o["id"], e[0]), lambda: lc_title_leia_rig(o, e))

    def lc_title_logo():
        def make():
            w, h = 1100, 169
            sweep = Fixed(At("gui/title/logo_sheen.png", lc_title_logo_sheen), xysize=(w, h))
            return Fixed("gui/title/logo_line.png", AlphaMask(sweep, "gui/title/logo_line.png"), xysize=(w, h))
        return lc_title_cached(("logo",), make)

    def lc_title_pick(kind, option_id):
        setattr(persistent, "lc_title_" + kind, option_id)
        renpy.save_persistent()
        renpy.restart_interaction()

    def lc_title_reset():
        persistent.lc_title_bg = "pool_evening"
        persistent.lc_title_outfit = "purple_dress"
        persistent.lc_title_expression = "smile"
        renpy.save_persistent()
        renpy.restart_interaction()
