# Discovery registry - optional moments a player can find, and the Moments strip data
#
# Purpose: Each optional moment (Hidden POV opened, detail noticed, door taken, phone moment)
#   registers once at init under its review day. Finding one writes a save-local record, so
#   echoes can read it and the end-of-day review can draw a strip of found moments. Unfound
#   moments show (as grey silhouettes with label and mood only) once the Day has been finished
#   before on this profile. Immersive mode shows no counts and no route words. Rules live in
#   python-packages/lc_discovery.py; this file only binds them to the store.
#
# Public API (call these from scenes/screens):
#   lc_discovery_register(day_id, moment_id, kind, label, mood, image=None) -> None
#       register one moment at init 1+ (kind: pov|notice|door|phone); duplicate id raises
#   lc_discovery_mark(moment_id) -> None      record the moment as found in this save (idempotent);
#       an id that is neither a registered discovery nor a Hidden POV raises in developer builds
#       and is ignored in release
#   lc_discovery_found(moment_id)             True once this save found the moment
#   lc_pov_seen_in_save(moment_id)            True once this save opened that Hidden POV
#   lc_discovery_day_cleared(day_id)          True when the profile had finished the day before
#       this playthrough's review of it (lc_discovery.cleared_before)
#   lc_discovery_strip(day_id, mode=None)     strip items for the review (lc_discovery.strip)
#   lc_discovery_count_line(day_id, mode=None, items=None)
#       'n of m' for Insight/Full once the day is cleared, else None (items: the strip, if built)
#   lc_discovery_thumb(item, width, height)   thumbnail (found) or grey silhouette (unfound);
#       a found moment with no image gets a FOUND stamp on its paper card
#   lc_discovery_on_review_finished(day_id) -> None
#       review_finished hook: remember whether the day was cleared, then clear it
#   lc_discovery_migrate_legacy() -> None     once per profile at init: days finished before this
#       system existed (LC_DISCOVERY_LEGACY_EVIDENCE) count as cleared
#   LC_DISCOVERIES                            the registry {day_id: [entry, ...]} (init-time)
#   LC_DISCOVERY_LEGACY_EVIDENCE              {day_id: persistent field set when it was finished}
#   default lc_discoveries_found              save state: set of found moment ids
#   default lc_discovery_review_cleared       save state: {day_id: cleared before this review}
#   default lc_discovery_run_id               save state: id of this playthrough (set at start)
#   default persistent.lc_days_cleared        profile: review day ids finished at least once
#   default persistent.lc_days_first_run      profile: {day_id: run id that first finished it}
#   default persistent.lc_days_cleared_legacy_checked   profile: migration ran
#
# Internal (helpers for this file and its screens; do not call from scenes): _lc_discovery_mature,
#   _lc_discovery_warn, _lc_discovery_cleared_before, _lc_discovery_found_stamp,
#   lc_discovery_new_run_id
#
# Example:
#   init 1 python:
#       lc_discovery_register("ch01_d2", "d2_knot_door", "door", "Pool, the knot", "you saw it first")
#   $ lc_discovery_mark("d2_knot_door")                       (when the player takes the door)
#   if lc_pov_seen_in_save("d2_breakfast_julian"):            (echo authoring)
#
# Depends on: python-packages/lc_discovery.py, systems/lc_hooks.rpy, systems/hidden_pov.rpy
#   (LC_POV_OPPORTUNITIES, read at call time), systems/choice_engine.rpy (current_choice_mode)
# Hooks: listens to review_finished (systems/day_review.rpy)
# Load order: init 0, so registrations at init 1 (lc_pov_register with day_id) find the registry;
#   the legacy migration runs in the same block (persistent is loaded before init)
# Docs: docs/HIDDEN_POV.md, docs/ARCHITECTURE.md   Tests: tests/test_discovery.py

default lc_discoveries_found = set()
default lc_discovery_review_cleared = {}
default lc_discovery_run_id = lc_discovery_new_run_id()
default persistent.lc_days_cleared = set()
default persistent.lc_days_first_run = {}
default persistent.lc_days_cleared_legacy_checked = False

init python:
    import lc_discovery
    import uuid as _lc_discovery_uuid

    # Init-time data (never saved): one row per registered moment, per review day.
    LC_DISCOVERIES = {}

    # Completion evidence that existed before this system: a profile with the field set had
    # finished that day (persistent.ch01_chapter_select_unlocked is set by the first finished
    # Day Two, systems/chapter_select.rpy).
    LC_DISCOVERY_LEGACY_EVIDENCE = {"ch01_d2": "ch01_chapter_select_unlocked"}

    def lc_discovery_new_run_id():
        """A fresh id for a new playthrough (the lc_discovery_run_id default)."""
        return _lc_discovery_uuid.uuid4().hex

    def _lc_discovery_warn(message):
        """Developer builds fail loudly (like _lc_pov_warn); release builds only log."""
        text = "[discovery] " + message
        if config.developer:
            raise Exception(text)
        try:
            renpy.log(text)
        except Exception:
            pass
        return None

    def lc_discovery_register(day_id, moment_id, kind, label, mood, image=None):
        """Register one optional moment at init (see python-packages/lc_discovery.py)."""
        lc_discovery.register(LC_DISCOVERIES, day_id, moment_id, kind, label, mood, image=image)
        return None

    def lc_discovery_found(moment_id):
        return moment_id in (getattr(store, "lc_discoveries_found", None) or ())

    def lc_discovery_mark(moment_id):
        """Record a found moment in this save. Rollback restores the set with the store;
        a second mark changes nothing (no new rollback entry, no double count). An unknown id
        (a typo) raises in developer builds and records nothing in release."""
        if (lc_discovery.find(LC_DISCOVERIES, moment_id) is None
                and moment_id not in (getattr(store, "LC_POV_OPPORTUNITIES", None) or {})):
            if config.developer:
                _lc_discovery_warn("lc_discovery_mark: unknown moment id %r (register it with "
                                   "lc_discovery_register or lc_pov_register)" % (moment_id,))
            return None
        found = getattr(store, "lc_discoveries_found", None) or set()
        if moment_id in found:
            return None
        store.lc_discoveries_found = set(found) | {moment_id}
        return None

    def lc_pov_seen_in_save(moment_id):
        """True once this save opened the Hidden POV moment (save-local, unlike the Gallery)."""
        if not lc_discovery_found(moment_id):
            return False
        entry = lc_discovery.find(LC_DISCOVERIES, moment_id)
        if entry is not None:
            return entry["kind"] == "pov"
        return moment_id in (getattr(store, "LC_POV_OPPORTUNITIES", None) or {})

    def _lc_discovery_cleared_before(day_id):
        return lc_discovery.cleared_before(day_id, getattr(persistent, "lc_days_cleared", None),
                                           getattr(persistent, "lc_days_first_run", None),
                                           getattr(store, "lc_discovery_run_id", None))

    def lc_discovery_day_cleared(day_id):
        snapshot = getattr(store, "lc_discovery_review_cleared", None) or {}
        if day_id in snapshot:
            return bool(snapshot[day_id])
        return _lc_discovery_cleared_before(day_id)

    def lc_discovery_on_review_finished(day_id):
        """Remember, once per save, whether the profile had finished this day before; then mark
        it finished, with this playthrough as its first run. The first review of a day therefore
        shows found moments only, also after rolling back past the review and replaying it
        (persistent is not rolled back; the run id is). A broken hook never stops the review in
        release; developer builds raise."""
        try:
            cleared = set(getattr(persistent, "lc_days_cleared", None) or ())
            snapshot = dict(getattr(store, "lc_discovery_review_cleared", None) or {})
            if day_id not in snapshot:
                snapshot[day_id] = _lc_discovery_cleared_before(day_id)
                store.lc_discovery_review_cleared = snapshot
            if day_id not in cleared:
                run_id = getattr(store, "lc_discovery_run_id", None)
                if run_id:
                    first = dict(getattr(persistent, "lc_days_first_run", None) or {})
                    first[day_id] = run_id
                    persistent.lc_days_first_run = first
                persistent.lc_days_cleared = cleared | {day_id}
        except Exception as e:
            if config.developer:
                raise
            _lc_discovery_warn("review_finished hook failed for %s: %r" % (day_id, e))
        return None

    lc_hook_add("review_finished", lc_discovery_on_review_finished)

    def lc_discovery_migrate_legacy():
        """Once per profile: days finished before this system existed count as cleared, from the
        completion evidence in LC_DISCOVERY_LEGACY_EVIDENCE. Runs at init, before any play, so the
        unlock a first Day Two sets just before its own review never counts for that review."""
        if getattr(persistent, "lc_days_cleared_legacy_checked", False):
            return None
        cleared = set(getattr(persistent, "lc_days_cleared", None) or ())
        for day_id, field in LC_DISCOVERY_LEGACY_EVIDENCE.items():
            if getattr(persistent, field, False):
                cleared.add(day_id)
        persistent.lc_days_cleared = cleared
        persistent.lc_days_cleared_legacy_checked = True
        return None

    lc_discovery_migrate_legacy()

    def lc_discovery_strip(day_id, mode=None):
        return lc_discovery.strip(LC_DISCOVERIES, day_id,
                                  getattr(store, "lc_discoveries_found", None) or set(),
                                  lc_discovery_day_cleared(day_id), mode or current_choice_mode())

    def lc_discovery_count_line(day_id, mode=None, items=None):
        if not lc_discovery_day_cleared(day_id):
            return None
        mode = mode or current_choice_mode()
        if items is None:
            items = lc_discovery_strip(day_id, mode)
        return lc_discovery.count_line(items, mode)

    def _lc_discovery_mature(item):
        if item.get("kind") == "pov":
            pov = (getattr(store, "LC_POV_OPPORTUNITIES", None) or {}).get(item["id"], {})
            return bool(pov.get("mature"))
        return False

    def _lc_discovery_found_stamp():
        """Berry ink-stamp 'FOUND' (outlined box, slight tilt) for image-less found tiles."""
        ink = "#a83a5a"
        word = Text("FOUND", font="fonts/Handjet-ExtraBold.ttf", size=30, color=ink, xalign=0.5, yalign=0.5)
        w, h = 96, 40
        box = Fixed(Solid(ink, xysize=(w, 3)), Solid(ink, xysize=(w, 3), ypos=h - 3),
                    Solid(ink, xysize=(3, h)), Solid(ink, xysize=(3, h), xpos=w - 3),
                    word, xysize=(w, h))
        return Transform(box, rotate=-8, rotate_pad=False, alpha=0.85, xalign=0.5, yalign=0.5)

    def lc_discovery_thumb(item, width, height):
        """Found: the art, fitted like the review polaroids (mature art blurred with an 18+ mark,
        as the Gallery masks mature covers). Unfound: a greyed, blurred silhouette of the same
        art, or a plain paper card when the moment has no image. A found moment with no image
        gets a tilted FOUND stamp on its card, so it can't pass for an unfound one."""
        image = item.get("image")
        paper = Solid("#e6d9c2" if item.get("found") else "#cfc4b4", xysize=(width, height))
        if not (image and renpy.has_image(image, exact=True)):
            if item.get("found"):
                return Fixed(paper, _lc_discovery_found_stamp(), xysize=(width, height))
            return paper
        art = Transform(image, fit="cover", xysize=(width, height))
        if not item.get("found"):
            grey = Transform(art, blur=14, alpha=0.55,
                             matrixcolor=SaturationMatrix(0.0) * BrightnessMatrix(-0.12))
            return Fixed(paper, grey, xysize=(width, height))
        if _lc_discovery_mature(item):
            mark = Text("18+", font="fonts/Handjet-ExtraBold.ttf", size=20, color="#fff3f7",
                        outlines=[(2, "#3b2a30", 0, 0)], xalign=0.96, yalign=0.06)
            return Fixed(Transform(art, blur=10), mark, xysize=(width, height))
        return art
