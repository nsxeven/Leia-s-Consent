# Title customiser data - title-screen background, Leia outfit and expression
#
# Purpose: Registry and unlock rules for the title-screen picks plus the title-only breathing rig.
#   An option unlocks forever once it was SEEN in any playthrough (Ren'Py's seen record); mature
#   options only show when 18+ title options are on (persistent.lc_title_all_memories). Panel:
#   screens/title_customiser.rpy.
#
# Public API (call these from scenes/screens):
#   lc_title_register_outfit(outfit_id, label, base, chest, seen_tag=None, mature=False, default=False, always_unlocked=False, credit=None, hair=None, seen_cgs=(), order=None) -> None
#       add/replace a title outfit (from an `init 1 python:` block; the Day packs register theirs
#       in their first *_visuals.rpy, numbered with order= so the menu keeps one order)
#   lc_title_register_background(bg_id, label, path, seen_tags=(), mature=False, default=False, order=None) -> None
#       add/replace a title background
#   lc_title_note_sprite(tag) -> None         cast system: note a shown sprite (unlocks outfits)
#   lc_title_pick(kind, option_id) -> None    screen action: choose an option
#   lc_title_reset() -> None                  screen action: back to defaults
#   lc_title_bg_now()                         current background displayable
#   lc_title_leia_now()                       current Leia rig displayable
#   lc_title_logo()                           the logo with its sheen
#   lc_title_leia_rig(o, expression)          animated Leia for an outfit/expression
#   lc_title_show_mature() -> bool            True when 18+ options are shown
#   lc_title_current_outfit()                 current outfit record
#   lc_title_current_expression()             current expression
#   lc_title_current_background()             current background record
#   lc_title_outfit_options()                 outfits the panel lists
#   lc_title_expression_options()             expressions the panel lists
#   lc_title_background_options()             backgrounds the panel lists
#   lc_title_outfit_unlocked(o)               True when an outfit is unlocked
#   lc_title_background_unlocked(b)           True when a background is unlocked
#   lc_title_outfit_thumb(o, locked=False)    outfit thumbnail
#   lc_title_face_thumb(o, expression)        face thumbnail
#   lc_title_bg_thumb(b, w=196, h=110)        background thumbnail
#   lc_title_cached(key, make)                cache a displayable by key
#   default persistent.lc_title_bg            chosen background
#   default persistent.lc_title_outfit        chosen outfit
#   default persistent.lc_title_expression    chosen expression
#
# Internal (helpers for this file and its screens; do not call from scenes): _lc_title_sorted, lc_title_seen_tags,
#   lc_title_outfit, lc_title_background, lc_title_bg_image
#
# Example:
#   init 1 python:
#       lc_title_register_outfit("my_outfit", "My Outfit", "<base.png>", "<chest.png>", seen_tag="leia_my_outfit")
#
# Depends on: systems/lc_title_touch.rpy, systems/title_screen.rpy
#   (persistent.lc_title_all_memories), systems/cast_staging.rpy (calls lc_title_note_sprite)
# Hooks: none
# Load order: init -1 registry (so `init 1` blocks can register); the rest init 0
# Docs: docs/TITLE_SCREEN.md   Tests: tests/test_title_customiser.py

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

    _lc_title_order = python_dict()  # internal: (kind, id) -> menu position (order=)

    def _lc_title_sorted(items, kind):
        """items in menu order: by order= (unset: after every ordered one), then registration."""
        keyed = [(_lc_title_order.get((kind, o["id"]), 10 ** 9), n, o) for n, o in enumerate(items)]
        return [o for _key, _n, o in sorted(keyed, key=lambda t: (t[0], t[1]))]

    def lc_title_register_outfit(outfit_id, label, base, chest, seen_tag=None, mature=False,
                                 default=False, always_unlocked=False, credit=None, hair=None, seen_cgs=(),
                                 order=None):
        """Add (or replace) a title-screen outfit.

        base/chest: image paths on the 941 x 1672 Leia canvas.
        seen_tag:   the in-game sprite tag (e.g. "leia_blue_bikini"); the outfit unlocks
                    once any image with this tag has been shown in any playthrough.
        seen_cgs:   CG names (without "cg ") that show Leia in this outfit; seeing any of
                    them also unlocks it (covers playthroughs from before this feature).
        always_unlocked: for outfits that are owned outright (e.g. a patron's pack).
        credit:     optional line shown under the sprite, e.g. "Outfit made for <name>".
        order:      menu position (lower first); the Day packs number theirs so the menu keeps
                    one order across Days.
        """
        global LC_TITLE_OUTFITS
        LC_TITLE_OUTFITS = [o for o in LC_TITLE_OUTFITS if o["id"] != outfit_id]
        LC_TITLE_OUTFITS.append(dict(
            id=outfit_id, label=label, base=base, chest=chest, hair=hair or (LC_LEIA_SPRITE_DIR + "Hair.png"),
            seen_tag=seen_tag, mature=bool(mature), default=bool(default),
            always_unlocked=bool(always_unlocked), credit=credit, seen_cgs=tuple(seen_cgs),
        ))
        if order is not None:
            _lc_title_order["outfit", outfit_id] = order
        LC_TITLE_OUTFITS = _lc_title_sorted(LC_TITLE_OUTFITS, "outfit")

    def lc_title_register_background(bg_id, label, path, seen_tags=(), mature=False, default=False, order=None):
        """Add (or replace) a title-screen background; unlocks once any `bg <tag>` in seen_tags was shown.
        order: menu position (lower first), as for outfits."""
        global LC_TITLE_BACKGROUNDS
        LC_TITLE_BACKGROUNDS = [b for b in LC_TITLE_BACKGROUNDS if b["id"] != bg_id]
        LC_TITLE_BACKGROUNDS.append(dict(id=bg_id, label=label, path=path, seen_tags=tuple(seen_tags),
                                         mature=bool(mature), default=bool(default)))
        if order is not None:
            _lc_title_order["background", bg_id] = order
        LC_TITLE_BACKGROUNDS = _lc_title_sorted(LC_TITLE_BACKGROUNDS, "background")

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
        # Touch reactions (systems/lc_title_touch.rpy) swap the face, bounce the
        # chest and nudge the body without rebuilding the rig, so breathing never restarts.
        rig = Fixed(
            o["base"],
            lc_title_touch_chest(At(o["chest"], lc_title_chest_breathe)),
            lc_title_face_disp(face),
            At(o["hair"], lc_title_hair_idle),
            xysize=(941, 1672),
        )
        return lc_title_touch_body(Fixed(lc_sprite_silhouette(rig), xysize=(941, 1672)))

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
