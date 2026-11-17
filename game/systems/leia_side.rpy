# Leia's side - her errand segment: frame, place map, visit log, outcomes and the +2/day cap
#
# Purpose: Once a day the player can play a short stretch as Leia. This file binds the pure rules in
#   python-packages/lc_leia_side.py to the store: the place registry (each open place is also a
#   Moments strip moment), the save-local visit log and named outcomes, the segment frame (title
#   card, tinted text box via lc_leia_segment_active, the leia_think speaker in game/characters.rpy)
#   and the daily gain cap on her own choices, applied through the choice_effects / choice_applied
#   hooks of systems/choice_engine.rpy so Insight/Full labels show what really lands. No story text.
#
# Public API (call these from scenes/screens):
#   lc_leia_place(day, place_id, label, bg, hint=None, locked_reason=None, mood="", done=None) -> None
#       register a map card at init 1+ (bg: image name such as "bg ch01_d2_cafe", or a file path,
#       checked at init 999; locked_reason = Leia's in-character reason, which locks it; done =
#       optional line shown instead of the hint once visited); open places register an "errand"
#       Moments strip moment (lc_leia_side.moment_id), with bg as its image when bg is an image name
#   lc_leia_register_places(day, places) -> None
#       register a list/tuple of place dicts (keys lc_leia_side.PLACE_KEYS) at init 1+, in order
#   lc_leia_register_choices(day, *choice_ids) -> None
#       mark choice ids as Leia-side at init 1+: their gains share that day's +2 cap
#   lc_leia_is_side_choice(choice_id)         True for a choice registered as Leia-side
#   label lc_leia_segment_begin(day)          a LABEL: `call lc_leia_segment_begin("ch01_d2") from x`
#       (tint on, "Meanwhile - [girlfriend_name]" card); `$ lc_leia_segment_begin(...)` fails
#   label lc_leia_segment_end                 a LABEL: `call lc_leia_segment_end from x` (tint off)
#   lc_leia_segment_active()                  True during her segment (the say screen tints the box)
#   lc_leia_box_matrix(theme)                 matrixcolor for the say box in her segment (day/night)
#   lc_leia_map(day, places=None)             show the map (call screen) and return the picked open
#       place id; None once every open place was visited (no screen). places: None (all
#       registered) or a list/tuple of ids or of the registered place dicts (subset/order)
#   lc_leia_visit(day, place_id) -> None      record a visit (order kept) and mark its moment;
#       a locked/unknown place raises in developer builds and is ignored in release
#   lc_leia_visits(day)                       tuple of places visited that day, in order (never
#       compare it with a list literal; use the three helpers below)
#   lc_leia_first(day)                        the place she went to first that day, or None
#   lc_leia_visited_first(day, place_id)      True when place_id was her first stop that day
#   lc_leia_visited_before(day, place_a, place_b)
#       True when she has been to place_a and not to place_b before it (place_b later or not yet)
#   lc_leia_errand_done(day, places=None)     True once every open place was visited
#   lc_leia_cards(day, places=None, mode=None)
#       the card dicts the map screen draws (state open/visited/locked, reason, lock_hint)
#   lc_leia_mark(outcome_id) -> None          record a named outcome (idempotent)
#   lc_leia_did(outcome_id)                   True once the outcome was marked in this save
#   lc_leia_cap_effects(day, effects)         effects cut to what is left of the day's +2 cap
#   lc_leia_applied_effects(choice_id)        what a Leia-side choice really applied (summed)
#   lc_choice_applied_effects(choice_id)      what ANY picked choice applied: the ledger for
#       Leia-side ids, the registered effects for every other (Ryan's choices are never capped);
#       lane exemptions and lc_exhib_gained subtract/add these
#   LC_LEIA_PLACES                            init-time registry {day: [place entry, ...]}
#   LC_LEIA_SIDE_CHOICES                      init-time {choice_id: day} of Leia-side choices
#   LC_LEIA_BOX_TINT                          {paper: tint colour} for the day-paper text box
#   LC_LEIA_NIGHT_LIFT                        (r, g, b) lift added to the night-paper box
#   default lc_leia_side_state                save state: visits, outcomes, cap ledger (one dict)
#   default lc_leia_segment_day               save state: day id while her segment runs, else None
#
# Internal (helpers for this file and its screens; do not call from scenes): _lc_leia_state,
#   _lc_leia_warn, _lc_leia_places, _lc_leia_check_place, _lc_leia_is_image_name,
#   _lc_leia_choice_effects, _lc_leia_choice_applied, _lc_leia_on_review_finished,
#   _lc_leia_strip_filter, _lc_leia_validate_places
#
# Example:
#   init 1 python:
#       lc_leia_place("ch01_d2", "cafe", "Cafe", "bg ch01_d2_cafe", "Something cold for him.")
#       lc_leia_register_choices("ch01_d2", "ch01_d2_errand_cafe_warm")
#   call lc_leia_segment_begin("ch01_d2") from d2_errand_begin
#   while not lc_leia_errand_done("ch01_d2"):
#       $ d2_errand_place = lc_leia_map("ch01_d2")
#       if d2_errand_place:
#           $ lc_leia_visit("ch01_d2", d2_errand_place)
#           call expression "ch01_d2_errand_" + d2_errand_place
#   if lc_leia_visited_first("ch01_d2", "shop"):
#       leia_think "Muffins first."
#   call lc_leia_segment_end from d2_errand_end
#
# Depends on: python-packages/lc_leia_side.py, systems/lc_hooks.rpy, systems/discovery.rpy
#   (lc_discovery_register / lc_discovery_mark), systems/choice_engine.rpy (current_choice_mode,
#   get_choice_effects and the hook points), screens/leia_map_screen.rpy (lc_leia_map_screen),
#   game/characters.rpy (leia_think)
# Hooks: listens to choice_effects (filter: caps Leia-side gains), choice_applied (records them),
#   review_finished (clears a segment flag a scene forgot to end) and discovery_strip (filter:
#   drops a day's errand moments while she has not gone on that day's errand)
# Load order: init 0, after systems/discovery.rpy (same priority, earlier file) so registrations at
#   init 1 find both registries; init 999 checks every place's bg (images are defined at init 500)
# Docs: docs/LEIA_SIDE.md, docs/ARCHITECTURE.md   Tests: tests/test_leia_side.py

default lc_leia_side_state = {}
default lc_leia_segment_day = None

init python:
    import lc_leia_side

    # Init-time data (never saved).
    LC_LEIA_PLACES = {}
    LC_LEIA_SIDE_CHOICES = {}

    # Text box while her segment runs: a blush multiplied into the day paper; the night paper is
    # too dark for a multiply to show, so it gets a pink-lilac lift added instead.
    LC_LEIA_BOX_TINT = {"day": "#ffe0ea"}
    LC_LEIA_NIGHT_LIFT = (0.13, 0.04, 0.10)

    def _lc_leia_state():
        return getattr(store, "lc_leia_side_state", None) or {}

    def _lc_leia_warn(message):
        """Developer builds fail loudly; release builds only log."""
        text = "[leia_side] " + message
        if config.developer:
            raise Exception(text)
        try:
            renpy.log(text)
        except Exception:
            pass
        return None

    def _lc_leia_is_image_name(bg):
        """'bg ch01_d2_cafe' is an image name; 'images/.../x.webp' is a file path."""
        return lc_leia_side.is_image_name(bg)

    def lc_leia_place(day, place_id, label, bg, hint=None, locked_reason=None, mood="", done=None):
        """Register one map card at init (see python-packages/lc_leia_side.py)."""
        lc_leia_side.register_place(LC_LEIA_PLACES, day, place_id, label, bg, hint,
                                    locked_reason=locked_reason, mood=mood, done=done)
        if locked_reason is None:
            image = bg if _lc_leia_is_image_name(bg) else None
            lc_discovery_register(day, lc_leia_side.moment_id(day, place_id), lc_leia_side.MOMENT_KIND,
                                  label, mood, image=image)
        return None

    def lc_leia_register_places(day, places):
        """Register a list/tuple of place dicts (lc_leia_side.PLACE_KEYS) at init, in order."""
        if isinstance(places, (str, dict)) or not isinstance(places, (list, tuple)):
            raise ValueError("lc_leia_register_places(%r, ...) takes a list or tuple of place dicts, got %r"
                             % (day, places))
        for place in places:
            lc_leia_place(day, **lc_leia_side.place_kwargs(place))
        return None

    def lc_leia_register_choices(day, *choice_ids):
        """Leia-side choice ids share the day's +2 gain cap. One day per id."""
        for choice_id in choice_ids:
            known = LC_LEIA_SIDE_CHOICES.get(choice_id)
            if known is not None and known != day:
                raise ValueError("Leia side choice %r is already registered for %s" % (choice_id, known))
            LC_LEIA_SIDE_CHOICES[choice_id] = day
        return None

    def lc_leia_is_side_choice(choice_id):
        return choice_id in LC_LEIA_SIDE_CHOICES

    def lc_leia_segment_active():
        return getattr(store, "lc_leia_segment_day", None) is not None

    def lc_leia_box_matrix(theme):
        """The say box's matrixcolor in her segment: day paper multiplied by a blush, night paper
        lifted (premultiplied alpha: the offset column scales with the pixel's alpha)."""
        if theme == "night":
            r, g, b = LC_LEIA_NIGHT_LIFT
            return Matrix([1.0, 0.0, 0.0, r,
                           0.0, 1.0, 0.0, g,
                           0.0, 0.0, 1.0, b,
                           0.0, 0.0, 0.0, 1.0])
        return TintMatrix(LC_LEIA_BOX_TINT.get(theme, LC_LEIA_BOX_TINT["day"]))

    def _lc_leia_places(day, places=None):
        """The day's place entries; a bad places argument raises in developer builds and falls
        back to every registered place in release."""
        try:
            return lc_leia_side.places(LC_LEIA_PLACES, day, places)
        except ValueError as e:
            _lc_leia_warn("%s" % (e,))
            return lc_leia_side.places(LC_LEIA_PLACES, day)

    def _lc_leia_check_place(day, place_id, caller):
        if not any(e["id"] == place_id for e in LC_LEIA_PLACES.get(day, ())):
            _lc_leia_warn("%s: place %r is not registered for %s" % (caller, place_id, day))
        return None

    def lc_leia_visits(day):
        return tuple(lc_leia_side.visits(_lc_leia_state(), day))

    def lc_leia_first(day):
        return lc_leia_side.first_visit(_lc_leia_state(), day)

    def lc_leia_visited_first(day, place_id):
        _lc_leia_check_place(day, place_id, "lc_leia_visited_first")
        return lc_leia_side.visited_first(_lc_leia_state(), day, place_id)

    def lc_leia_visited_before(day, place_a, place_b):
        _lc_leia_check_place(day, place_a, "lc_leia_visited_before")
        _lc_leia_check_place(day, place_b, "lc_leia_visited_before")
        return lc_leia_side.visited_before(_lc_leia_state(), day, place_a, place_b)

    def lc_leia_errand_done(day, places=None):
        return lc_leia_side.errand_done(_lc_leia_places(day, places), lc_leia_visits(day))

    def lc_leia_cards(day, places=None, mode=None):
        mode = mode or current_choice_mode()
        return lc_leia_side.cards(_lc_leia_places(day, places), lc_leia_visits(day), mode)

    def lc_leia_visit(day, place_id):
        """Record a visit in this save (rollback restores it with the store) and mark its moment."""
        try:
            new = lc_leia_side.visit(_lc_leia_state(), _lc_leia_places(day), day, place_id)
        except ValueError as e:
            _lc_leia_warn("lc_leia_visit: %s" % (e,))
            return None
        store.lc_leia_side_state = new
        lc_discovery_mark(lc_leia_side.moment_id(day, place_id))
        return None

    def lc_leia_map(day, places=None):
        """Show the map and return the open place the player picked (None when all are visited)."""
        place_list = _lc_leia_places(day, places)
        done = lc_leia_visits(day)
        remaining = lc_leia_side.open_remaining(place_list, done)
        if not remaining:
            return None
        cards = lc_leia_side.cards(place_list, done, current_choice_mode())
        # Like a `call screen` statement under `window auto`: no empty text box behind the map.
        hide_window = getattr(store, "_window_hide", None)
        if hide_window is not None:
            hide_window(None, auto=True)
        picked = renpy.call_screen("lc_leia_map_screen", day=day, cards=cards)
        if picked not in remaining:
            _lc_leia_warn("lc_leia_map: %r is not an open place on %s" % (picked, day))
            return None
        return picked

    def lc_leia_mark(outcome_id):
        new = lc_leia_side.mark(_lc_leia_state(), outcome_id)
        if new is not _lc_leia_state():
            store.lc_leia_side_state = new
        return None

    def lc_leia_did(outcome_id):
        return lc_leia_side.did(_lc_leia_state(), outcome_id)

    def lc_leia_cap_effects(day, effects):
        return lc_leia_side.cap_effects(_lc_leia_state(), day, effects)

    def lc_leia_applied_effects(choice_id):
        return lc_leia_side.applied_effects(_lc_leia_state(), choice_id)

    def lc_choice_applied_effects(choice_id):
        """What a picked choice really applied: the cap ledger for Leia-side ids (summed over her
        picks), the registered effects for every other id (Ryan's choices are never capped)."""
        if choice_id in LC_LEIA_SIDE_CHOICES:
            return lc_leia_side.applied_effects(_lc_leia_state(), choice_id)
        return get_choice_effects(choice_id)

    def _lc_leia_choice_effects(effects, choice_id):
        """choice_effects filter: Leia-side gains are cut to what is left of the day's cap."""
        day = LC_LEIA_SIDE_CHOICES.get(choice_id)
        if day is None:
            return effects
        return lc_leia_side.cap_effects(_lc_leia_state(), day, effects)

    def _lc_leia_choice_applied(choice_id, effects):
        """choice_applied hook: put what a Leia-side choice really applied in the day's ledger."""
        day = LC_LEIA_SIDE_CHOICES.get(choice_id)
        if day is None:
            return None
        store.lc_leia_side_state = lc_leia_side.record_gain(_lc_leia_state(), day, choice_id, effects)
        return None

    def _lc_leia_on_review_finished(day_id):
        """review_finished hook: a segment still open at the day review means a scene jumped out
        (or forgot `call lc_leia_segment_end`). Clear it so the tint can't leak, then complain."""
        open_day = getattr(store, "lc_leia_segment_day", None)
        if open_day is None:
            return None
        store.lc_leia_segment_day = None
        _lc_leia_warn("segment %r was still open at the %s review: `call lc_leia_segment_end` "
                      "before leaving her segment" % (open_day, day_id))
        return None

    def _lc_leia_strip_filter(items, day_id):
        """discovery_strip filter: no 'Her errand' silhouettes for a day she never went out on
        (an old save already past the errand), so missing it never reads as a failure."""
        if lc_leia_visits(day_id):
            return items
        return [item for item in items if item.get("kind") != lc_leia_side.MOMENT_KIND]

    def _lc_leia_validate_places():
        """Every place's bg must be a defined image or a loadable file (runs at init 999)."""
        problems = lc_leia_side.bad_images(LC_LEIA_PLACES, lambda n: renpy.has_image(n, exact=True),
                                           lambda p: renpy.loadable(p))
        if problems:
            _lc_leia_warn("lc_leia_place backgrounds that don't exist:\n  " + "\n  ".join(problems))
        return None

    lc_hook_add("choice_effects", _lc_leia_choice_effects)
    lc_hook_add("choice_applied", _lc_leia_choice_applied)
    lc_hook_add("review_finished", _lc_leia_on_review_finished)
    lc_hook_add("discovery_strip", _lc_leia_strip_filter)

# Runs after every registration (init 1+) and every image statement (init 500).
init 999 python:
    _lc_leia_validate_places()


# Her segment opens on a title card over black; scenes then `scene` their own background. The
# text box stays tinted (screen say reads lc_leia_segment_active) until lc_leia_segment_end.
label lc_leia_segment_begin(day):
    $ lc_leia_segment_day = day
    scene black
    with fade
    centered "Meanwhile — [girlfriend_name]"
    return

label lc_leia_segment_end:
    $ lc_leia_segment_day = None
    return
