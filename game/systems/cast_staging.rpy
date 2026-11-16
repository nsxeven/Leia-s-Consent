# Cast staging - who is on stage, in which outfit and with which face
#
# Purpose: Owns the sprite staging model: writers declare the scene's cast and expressions; the say
#   callback puts each speaker in the LEFT/RIGHT slot on their line (Leia always RIGHT, Ryan or the
#   speaking guest LEFT; no sprites over a CG). It does not define sprite images (game/sprites/,
#   *_visuals.rpy) or transforms (systems/dialogue_staging.rpy).
#
# Public API (call these from scenes/screens):
#   cast(**members) -> None                   declare the scene's cast (who=outfit) after `scene
#       bg`; replaces the old cast
#   cast_add(**members) -> None               add people or change an outfit mid-scene (None
#       removes; a rustle plays)
#   cast_remove(*people) -> None              take people out; anyone on stage fades out
#   face(who, expression) -> None             set an expression now or for their next entrance
#   cast_hold() -> None                       freeze automatic staging for hand-placed show/hide
#       lines
#   cast_resume(**adopt) -> None              hand staging back; who="<tag>" adopts a hand-placed
#       sprite
#   lc_cast_who(character)                    cast id ('leia', 'ryan', ...) for a Character, or None
#   lc_stage_speaker(who) -> None             put `who` on stage for their line (called by the say
#       callback)
#   lc_cast_say_callback(who, *args, **kwargs)
#       config.say_arguments_callback installed by this file
#   default lc_cast                           save state: {who: outfit} for the current scene
#   default lc_faces                          save state: {who: expression}
#   default lc_stage                          save state: {'left': who, 'right': who}
#   default lc_cast_held                      save state: True between cast_hold() and cast_resume()
#
# Internal (helpers for this file and its screens; do not call from scenes): _lc_sprite_name,
#   _lc_slot_for, _lc_occupant, _lc_put, _lc_staging_blocked, _lc_refresh, _lc_clear_slots
#
# Example:
#   $ cast(ryan="prologue_party", leia="prologue_party", julian="party")
#   $ face("leia", "shy")
#   $ cast_add(leia="towel")        $ cast_remove("leia")
#   $ cast_hold()  ...  $ cast_resume(leia="leia_purple_dress_wet")
#
# Notes: Adding a sprite later = define `image <who>_<outfit>` (expressions: `image <who>_<outfit> smile`)
#   and name the outfit in cast(). Speakers are matched by Character object in LC_CAST_SPEAKERS.
#   `$ cast()` empties the stage. A sprite appears on that character's first line, then stays.
#
# Depends on: systems/dialogue_staging.rpy (transforms), Character objects in game/characters.rpy,
#   lc_sfx (systems/lc_fx.rpy), lc_title_note_sprite (systems/title_customiser.rpy)
# Hooks: none (chains any earlier config.say_arguments_callback)
# Load order: default (init 0)
# Docs: docs/SPRITE_STAGING.md   Tests: tests/test_cast_staging.py, tests/test_outfit_change_sfx.py

default lc_cast = {}
default lc_faces = {}
default lc_stage = {"left": None, "right": None}
default lc_cast_held = False

init python:

    # who-id -> name of the Character in the store
    LC_CAST_SPEAKERS = (
        ("ryan", "mc"),
        ("leia", "gf"),
        ("julian", "friend"),
        ("stranger", "stranger"),
        ("maya", "maya"),
    )
    LC_SLOT_TAG = {"left": "lc_slot_left", "right": "lc_slot_right"}

    def lc_cast_who(character):
        for who, var in LC_CAST_SPEAKERS:
            if character is getattr(store, var, None):
                return who
        return None

    def _lc_sprite_name(who):
        outfit = store.lc_cast.get(who)
        if not outfit:
            return None
        base = "%s_%s" % (who, outfit)
        expr = store.lc_faces.get(who, "neutral")
        if renpy.has_image(base + " " + expr, exact=True):
            return (base, expr)
        if renpy.has_image(base + " neutral", exact=True):
            return (base, "neutral")
        if renpy.has_image(base, exact=True):
            return (base,)
        return None

    def _lc_slot_for(who):
        if who == "leia":
            return "right"
        if "leia" in store.lc_cast or who == "ryan":
            return "left"
        return "right"

    def _lc_occupant(slot):
        if renpy.showing(LC_SLOT_TAG[slot]):
            return store.lc_stage.get(slot)
        return None

    def _lc_put(slot, who, entering):
        name = _lc_sprite_name(who)
        if name is None:
            return False
        if slot == "right":
            pos = prologue_leia_enter_right if entering else prologue_leia_right
        else:
            pos = prologue_other_enter_left if entering else prologue_other_left
        renpy.show(name, at_list=[pos, leia_body_idle], tag=LC_SLOT_TAG[slot])
        store.lc_stage[slot] = who
        lc_title_note_sprite(name[0])  # unlocks this outfit on the title-screen customiser
        return True

    def _lc_staging_blocked():
        # Sprites follow what is actually on screen: hidden only while a `cg`
        # image is showing. (Not lc_cinematic_mode: a scene that forgets
        # exit_cinematic_mode() after a CG must not lose its sprites.)
        if store.lc_cast_held or not store.lc_cast:
            return True
        try:
            return "cg" in renpy.get_showing_tags("master")
        except Exception:
            return bool(getattr(store, "lc_cinematic_mode", False))

    def lc_stage_speaker(who):
        """Put `who` on stage for the line they are about to say."""
        if who is None or who not in store.lc_cast or _lc_staging_blocked():
            return
        slot = _lc_slot_for(who)
        current = _lc_occupant(slot)
        if current == who:
            return
        if _lc_put(slot, who, entering=current is None):
            renpy.transition(sprite_enter_exit if current is None else Dissolve(0.22), layer="master")

    def _lc_refresh(who):
        """Re-show `who` in place after an outfit or expression change."""
        for slot in ("left", "right"):
            if _lc_occupant(slot) == who:
                if _lc_put(slot, who, entering=False):
                    renpy.with_statement(sprite_change)
                return

    def _lc_clear_slots():
        for slot, tag in LC_SLOT_TAG.items():
            if renpy.showing(tag):
                renpy.hide(tag)
            store.lc_stage[slot] = None

    def cast(**members):
        """Declare who is in the scene (who=outfit). Replaces the previous cast."""
        store.lc_cast = dict((k, v) for k, v in members.items() if v)
        store.lc_faces = {}
        store.lc_cast_held = False
        _lc_clear_slots()

    LC_OUTFIT_CHANGE_SFX = "cloth_change"

    def cast_add(**members):
        """Add people or change outfits mid-scene (who=outfit; None removes)."""
        for who, outfit in members.items():
            if not outfit:
                cast_remove(who)
                continue
            joining = who not in store.lc_cast
            changed = store.lc_cast.get(who) != outfit
            store.lc_cast[who] = outfit
            if joining and who == "leia":
                # A guest who had the right side (Leia absent) steps out; they
                # come back on the left when they next speak. Ryan keeps his place.
                guest = _lc_occupant("right")
                if guest is not None and guest != "leia":
                    renpy.hide(LC_SLOT_TAG["right"])
                    store.lc_stage["right"] = None
                    renpy.with_statement(sprite_enter_exit)
            elif changed:
                # Someone already in the scene changes clothes: soft fabric
                # rustle (darryn 2026-11-09). Joining in a new outfit is silent.
                lc_sfx(LC_OUTFIT_CHANGE_SFX)
                _lc_refresh(who)

    def cast_remove(*people):
        """Take people out of the scene; anyone on stage leaves with a fade."""
        left_stage = False
        for who in people:
            store.lc_cast.pop(who, None)
            for slot, tag in LC_SLOT_TAG.items():
                if _lc_occupant(slot) == who:
                    renpy.hide(tag)
                    store.lc_stage[slot] = None
                    left_stage = True
        if left_stage:
            renpy.with_statement(sprite_enter_exit)

    def face(who, expression):
        """Set an expression; applies now if they are on stage, else on entry."""
        if store.lc_faces.get(who) == expression:
            return
        store.lc_faces[who] = expression
        _lc_refresh(who)

    def cast_hold():
        """Freeze automatic staging for hand-choreographed show/hide lines.
        Whoever is in a slot stays put; nobody new is brought on."""
        store.lc_cast_held = True

    def cast_resume(**adopt):
        """Hand staging back. adopt: who="<manual tag>" turns a hand-placed
        sprite back into that character's slot without a blink."""
        store.lc_cast_held = False
        moved = False
        for who, tag in adopt.items():
            if who not in store.lc_cast:
                continue
            if renpy.showing(tag):
                renpy.hide(tag)
            if _lc_put(_lc_slot_for(who), who, entering=False):
                moved = True
        if moved:
            renpy.with_statement(Dissolve(0.15))

    _lc_prev_say_args_cb = config.say_arguments_callback

    def lc_cast_say_callback(who, *args, **kwargs):
        lc_stage_speaker(lc_cast_who(who))
        if _lc_prev_say_args_cb is not None:
            return _lc_prev_say_args_cb(who, *args, **kwargs)
        return args, kwargs

    config.say_arguments_callback = lc_cast_say_callback
