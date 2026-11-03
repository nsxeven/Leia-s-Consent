# Julian — Chapter One Day One sprites + the speaker-swap rule.
#
# Staging rule (darryn, 2026-11-04): Ryan holds the left slot and Leia the right.
# Julian has no slot of his own; while he is the one speaking he swaps into
# Ryan's left slot, and Ryan comes back on the next line anyone else says
# (narration included). This is game-wide and needs no per-scene code:
#   - Ryan's sprites (ryan_casual, ryan_pool) are switches that show Julian's
#     current outfit while `lc_julian_speaking` is true.
#   - `lc_say_swap` (config.say_arguments_callback) flips that flag per line;
#     the slot crossfades itself (0.2s), so the text box and Leia are untouched.
#   - Julian only appears where Ryan's sprite is already on screen, so scenes
#     that keep Ryan off (CGs, the post-towel lounge, bed scenes) stay empty.
#   - `lc_julian_outfit` says what he is wearing; None means no swap
#     (Prologue party: no art yet; while he carries Leia; Day 2 onwards).
#
# Outfit art (941x1672 canvas, same envelope as Ryan and Leia):
#   travel  -> cream shirt + olive shorts
#   pool    -> swim shorts
#   evening -> black button-up + khaki shorts
#   lounge  -> black tee + grey shorts

default lc_julian_outfit = None
default lc_julian_speaking = False

init -1 python:

    import time as _lc_time

    LC_JULIAN_OUTFITS = ("travel", "pool", "evening", "lounge")
    LC_SWAP_SECONDS = 0.2

    # Last swap, kept outside the store (not saved, not rolled back):
    # who was in the slot before, and when the change started.
    _lc_swap = {"from": None, "at": 0.0}

    def _lc_slot_key():
        if store.lc_julian_speaking and store.lc_julian_outfit in LC_JULIAN_OUTFITS:
            return store.lc_julian_outfit
        return "ryan"

    def _lc_slot_image(key, ryan_image):
        return ryan_image if key == "ryan" else "julian_" + key

    def _lc_slot_render(st, at, ryan_image):
        # Crossfade inside the slot itself. A layer dissolve can't be used: a
        # switch like this updates the "before" frame too, so the swap snapped.
        key = _lc_slot_key()
        new = _lc_slot_image(key, ryan_image)
        done = (_lc_time.time() - _lc_swap["at"]) / LC_SWAP_SECONDS
        old_key = _lc_swap["from"]
        if old_key is None or old_key == key or done >= 1.0:
            return new, None
        done = max(0.0, done)
        old = _lc_slot_image(old_key, ryan_image)
        return Fixed(Transform(old, alpha=1.0 - done), Transform(new, alpha=done), fit_first=True), 1.0 / 60

    def lc_left_slot(ryan_image):
        """Ryan's left-slot image, replaced by Julian's outfit while he speaks."""
        return DynamicDisplayable(_lc_slot_render, ryan_image)

init python:

    _lc_prev_say_arguments_callback = config.say_arguments_callback

    def lc_say_swap(who, *args, **kwargs):
        speaking = (who is store.friend) and (store.lc_julian_outfit in LC_JULIAN_OUTFITS)
        if speaking != store.lc_julian_speaking:
            _lc_swap["from"] = _lc_slot_key()
            _lc_swap["at"] = _lc_time.time()
            store.lc_julian_speaking = speaking
        if _lc_prev_say_arguments_callback is not None:
            return _lc_prev_say_arguments_callback(who, *args, **kwargs)
        return args, kwargs

    config.say_arguments_callback = lc_say_swap


init 1:
    # init 1: lc_sprite_silhouette is defined at init 0 in leia_prologue_party.rpy,
    # which loads after this file.
    layeredimage julian_travel_layers:
        always "images/sprites/julian/BASE_CreamShirt.png"

    layeredimage julian_pool_layers:
        always "images/sprites/julian/BASE_SwimShorts.png"

    layeredimage julian_evening_layers:
        always "images/sprites/julian/BASE_BlackShirt.png"

    layeredimage julian_lounge_layers:
        always "images/sprites/julian/BASE_BlackTeeGreyShorts.png"

    image julian_travel = Fixed(lc_sprite_silhouette("julian_travel_layers"), xysize=(941, 1672))
    image julian_pool = Fixed(lc_sprite_silhouette("julian_pool_layers"), xysize=(941, 1672))
    image julian_evening = Fixed(lc_sprite_silhouette("julian_evening_layers"), xysize=(941, 1672))
    image julian_lounge = Fixed(lc_sprite_silhouette("julian_lounge_layers"), xysize=(941, 1672))
