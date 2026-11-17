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
#   lc_discovery_mark(moment_id) -> None      record the moment as found in this save (idempotent)
#   lc_discovery_found(moment_id)             True once this save found the moment
#   lc_pov_seen_in_save(moment_id)            True once this save opened that Hidden POV
#   lc_discovery_day_cleared(day_id)          True when the profile had finished the day before
#       this save's review of it
#   lc_discovery_strip(day_id, mode=None)     strip items for the review (lc_discovery.strip)
#   lc_discovery_count_line(day_id, mode=None)
#       'n of m' for Insight/Full once the day is cleared, else None
#   lc_discovery_thumb(item, width, height)   thumbnail (found) or grey silhouette (unfound)
#   lc_discovery_on_review_finished(day_id) -> None
#       review_finished hook: remember whether the day was cleared, then clear it
#   LC_DISCOVERIES                            the registry {day_id: [entry, ...]} (init-time)
#   default lc_discoveries_found              save state: set of found moment ids
#   default lc_discovery_review_cleared       save state: {day_id: cleared before this review}
#   default persistent.lc_days_cleared        profile: review day ids finished at least once
#
# Internal (helpers for this file and its screens; do not call from scenes): _lc_discovery_mature
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
# Load order: init 0, so registrations at init 1 (lc_pov_register with day_id) find the registry
# Docs: docs/HIDDEN_POV.md, docs/ARCHITECTURE.md   Tests: tests/test_discovery.py

default lc_discoveries_found = set()
default lc_discovery_review_cleared = {}
default persistent.lc_days_cleared = set()

init python:
    import lc_discovery

    # Init-time data (never saved): one row per registered moment, per review day.
    LC_DISCOVERIES = {}

    def lc_discovery_register(day_id, moment_id, kind, label, mood, image=None):
        """Register one optional moment at init (see python-packages/lc_discovery.py)."""
        lc_discovery.register(LC_DISCOVERIES, day_id, moment_id, kind, label, mood, image=image)
        return None

    def lc_discovery_found(moment_id):
        return moment_id in (getattr(store, "lc_discoveries_found", None) or ())

    def lc_discovery_mark(moment_id):
        """Record a found moment in this save. Rollback restores the set with the store;
        a second mark changes nothing (no new rollback entry, no double count)."""
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
        return moment_id in globals().get("LC_POV_OPPORTUNITIES", {})

    def lc_discovery_day_cleared(day_id):
        snapshot = getattr(store, "lc_discovery_review_cleared", None) or {}
        if day_id in snapshot:
            return bool(snapshot[day_id])
        return day_id in (getattr(persistent, "lc_days_cleared", None) or ())

    def lc_discovery_on_review_finished(day_id):
        """Remember, once per save, whether the profile had finished this day before; then mark
        it finished. The first review of a day therefore shows found moments only."""
        try:
            cleared = set(getattr(persistent, "lc_days_cleared", None) or ())
            snapshot = dict(getattr(store, "lc_discovery_review_cleared", None) or {})
            if day_id not in snapshot:
                snapshot[day_id] = day_id in cleared
                store.lc_discovery_review_cleared = snapshot
            if day_id not in cleared:
                persistent.lc_days_cleared = cleared | {day_id}
        except Exception:
            pass
        return None

    lc_hook_add("review_finished", lc_discovery_on_review_finished)

    def lc_discovery_strip(day_id, mode=None):
        return lc_discovery.strip(LC_DISCOVERIES, day_id,
                                  getattr(store, "lc_discoveries_found", None) or set(),
                                  lc_discovery_day_cleared(day_id), mode or current_choice_mode())

    def lc_discovery_count_line(day_id, mode=None):
        if not lc_discovery_day_cleared(day_id):
            return None
        mode = mode or current_choice_mode()
        return lc_discovery.count_line(lc_discovery_strip(day_id, mode), mode)

    def _lc_discovery_mature(item):
        if item.get("kind") == "pov":
            return bool(globals().get("LC_POV_OPPORTUNITIES", {}).get(item["id"], {}).get("mature"))
        return False

    def lc_discovery_thumb(item, width, height):
        """Found: the art, fitted like the review polaroids (mature art blurred with an 18+ mark,
        as the Gallery masks mature covers). Unfound: a greyed, blurred silhouette of the same
        art, or a plain paper card when the moment has no image."""
        image = item.get("image")
        paper = Solid("#e6d9c2" if item.get("found") else "#cfc4b4", xysize=(width, height))
        if not (image and renpy.has_image(image, exact=True)):
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
