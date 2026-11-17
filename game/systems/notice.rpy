# Things Ryan noticed - optional push-in notices on a CG, a save-local record and Status pins
#
# Purpose: A registered notice shows a small eye cue while its source CG is on screen between
#   lc_notice_begin/lc_notice_end. Clicking it pushes the camera in on a detail already in the art
#   (zoom <= 1.4) over the same line and shows Ryan's one or two thought captions (lane-specific
#   when given; Love captions are about Leia), then eases back on click. Opening records the
#   notice in this save (read with lc_noticed) and marks its `notice` discovery; the phone Status
#   app pins it under "Things I noticed". Noticing never changes stats. A sibling of Hidden POV:
#   same scope, availability and reserved-rect rules, its own eye art. Rules live in
#   python-packages/lc_notice.py; registrations are validated at init 999.
#
# Public API (call these from scenes/screens):
#   lc_notice_register(notice_id, source, center, focus_rect, zoom=1.35, lines=None, lane_lines=None, closeup=None, day_id=None, label=None, mood=None, caption_box=None) -> None
#       register one notice at init 1+; lane_lines = {"love"|"exhib"|"ntr": [1-2 lines]};
#       closeup = an existing close-up render to cut to instead of zooming; day_id also
#       registers a `notice` discovery on that day's Moments strip; caption_box = (x, y, width)
#       of the caption paper when the default spot would cover something the captions name
#   lc_notice_begin(notice_id) -> None        open the notice's scope (its eye cue may show)
#   lc_notice_end() -> None                   close the current scope
#   lc_notice_in_scope(notice_id)             True while the notice's source CG is showing
#   lc_notice_available()                     True when the cue may show now
#   lc_notice_open(notice_id) -> None         the cue's action: push-in viewer + save-local record
#   lc_notice_close() -> None                 close the viewer (after its ease back)
#   lc_noticed(notice_id)                     True once this save noticed it
#   lc_noticed_any(*notice_ids)               True once this save noticed any of them
#   lc_notice_lane()                          caption lane now ("love"/"exhib"/"ntr") or None: the
#       lean, with the Love lean taking the exhib captions when Leia's tint is Exhibitionism
#   lc_notice_captions(notice_id, lane="current")
#       the captions for a lane (default: the lane now), player names filled in
#   lc_notice_focus(notice_id)                (xalign, yalign, zoom) of the push-in
#   lc_notice_caption_box(notice_id)          caption paper (x, y, w, h): its caption_box, else the
#       bottom spot, or the top spot when the detail sits under the dialogue box
#   lc_notice_instant()                       True when the push-in must be instant (reduced motion;
#       opening stops Skip, so the push-in then plays normally)
#   lc_notice_pins()                          Status pins, registration order, with the captions
#       seen when each was noticed
#   lc_notice_validate(notice_id)             problems with one registration
#   lc_notice_validate_all()                  {notice_id: problems} for every registration
#   LC_NOTICES                                the registry {notice_id: entry} (init-time)
#   LC_NOTICE_HITBOX, LC_NOTICE_HITBOX_TOUCH  cue hit squares (px; same as Hidden POV)
#   LC_NOTICE_IN, LC_NOTICE_OUT               push-in / ease-back seconds
#   default lc_noticed_record                 save state: {notice_id: caption lane seen}
#
# Internal (helpers for this file and its screens; do not call from scenes): _lc_notice_warn,
#   _lc_notice_names, lc_notice_hitbox_size, lc_notice_hover_sound, lc_notice_afm_callback,
#   lc_notice_scope_cleanup
#
# Example:
#   init 1 python:
#       lc_notice_register("d2_notice_bed_hand", source="cg ch01_d2_leia_sleeping",
#                          center=(600, 640), focus_rect=(300, 380, 600, 640),
#                          lines=["..."], lane_lines={"love": ["..."]}, day_id="ch01_d2")
#   $ lc_notice_begin("d2_notice_bed_hand")   ...   $ lc_notice_end()
#   if lc_noticed_any("d2_notice_bed_hand", "d2_notice_breakfast_smile"):   (a later talk)
#
# Depends on: python-packages/lc_notice.py, systems/hidden_pov.rpy (LC_POV_RESERVED_RECTS,
#   LC_POV_OPPORTUNITIES, lc_pov_reduce_motion), systems/discovery.rpy (lc_discovery_register,
#   lc_discovery_mark), systems/stats.rpy (lc_current_lean, lc_leia_tint), screens/scrapbook_ui.rpy
#   (lc_phone_covers_scene, lc_journal_menu_open), screens/notice_screen.rpy
# Hooks: none (chains config.afm_callback after Hidden POV, adds a start_interact callback and the
#   lc_notice_hotspot overlay)
# Load order: init 0 registry and API (notices register at init 1); init 999 validation, after
#   every registration file and the Hidden POV registry
# Docs: docs/NOTICES.md, docs/ARCHITECTURE.md   Tests: tests/test_notice.py

default lc_notice_active = None
default lc_notice_viewed = False
default lc_noticed_record = {}

init python:
    import lc_notice
    import time as _lc_notice_time

    LC_NOTICES = {}
    LC_NOTICE_HITBOX = 120
    LC_NOTICE_HITBOX_TOUCH = 160
    LC_NOTICE_IN = 0.9
    LC_NOTICE_OUT = 0.45

    def _lc_notice_warn(message, fatal=False):
        """Developer builds fail loudly; release builds only log."""
        text = "[notice] " + message
        if fatal and config.developer:
            raise Exception(text)
        print(text)
        try:
            renpy.log(text)
        except Exception:
            pass
        return None

    def lc_notice_register(notice_id, source, center, focus_rect, zoom=1.35, lines=None,
                           lane_lines=None, closeup=None, day_id=None, label=None, mood=None,
                           caption_box=None):
        """Register one notice (rules: python-packages/lc_notice.py)."""
        lc_notice.register(LC_NOTICES, notice_id, source, center, focus_rect, zoom=zoom,
                           lines=lines, lane_lines=lane_lines, closeup=closeup, day_id=day_id,
                           label=label, mood=mood, caption_box=caption_box)
        if day_id is not None:
            lc_discovery_register(day_id, notice_id, "notice", label or lc_notice.DEFAULT_LABEL,
                                  mood or "", image=closeup or source)
        return None

    def lc_notice_hitbox_size():
        return LC_NOTICE_HITBOX_TOUCH if renpy.variant("touch") else LC_NOTICE_HITBOX

    def lc_notice_begin(notice_id):
        if notice_id not in LC_NOTICES:
            raise ValueError("Unknown notice: " + notice_id)
        previous = store.lc_notice_active
        if previous is not None:
            _lc_notice_warn("lc_notice_begin(%r) while %r is still active; ending %r first. "
                            "Add $ lc_notice_end() before the next begin." % (notice_id, previous, previous))
            lc_notice_end()
        store.lc_notice_active = notice_id
        store.lc_notice_viewed = False
        return None

    def lc_notice_end():
        store.lc_notice_active = None
        store.lc_notice_viewed = False
        renpy.hide_screen("lc_notice_viewer")
        return None

    def lc_notice_in_scope(notice_id):
        entry = LC_NOTICES.get(notice_id)
        return bool(entry and renpy.showing(entry["source"], layer="master"))

    def lc_notice_available():
        notice_id = store.lc_notice_active
        return bool(
            notice_id and not store.lc_notice_viewed
            and lc_notice_in_scope(notice_id)
            and renpy.get_screen("say")
            and not renpy.get_screen("lc_notice_viewer")
            and not renpy.get_screen("lc_pov_viewer")
            and not renpy.get_screen("main_menu")
            and not renpy.get_screen("game_menu")
            and not lc_phone_covers_scene()
            and store.quick_menu
            and not store._windows_hidden
            and not lc_journal_menu_open()
        )

    def lc_notice_lane():
        """Caption lane from the stats-model lean; on the Love lean Leia's Love-lane tint can pick
        the exhib captions (lc_notice.lane_from_lean). Release builds fall back to the base lines."""
        try:
            lean = lc_current_lean()
            tint = lc_leia_tint("love") if lean == "love" else None
            return lc_notice.lane_from_lean(lean, tint)
        except Exception:
            if config.developer:
                raise
            return None

    def _lc_notice_names():
        return {key: getattr(store, key, None) for key in ("player_name", "girlfriend_name", "friend_name")}

    def lc_notice_captions(notice_id, lane="current"):
        if lane == "current":
            lane = lc_notice_lane()
        names = _lc_notice_names()
        return [lc_notice.fill_names(line, names)
                for line in lc_notice.caption_lines(LC_NOTICES[notice_id], lane)]

    def lc_notice_focus(notice_id):
        entry = LC_NOTICES[notice_id]
        return lc_notice.focus_transform(entry["focus_rect"], entry["zoom"],
                                         (config.screen_width, config.screen_height))

    def lc_notice_caption_box(notice_id):
        """Caption paper (x, y, w, h): the registration's caption_box, else the dialogue-box spot,
        or the top spot when the detail sits under it."""
        return lc_notice.caption_box(LC_NOTICES[notice_id], (config.screen_width, config.screen_height))

    def lc_notice_instant():
        """No push-in animation with reduced motion (Hidden POV's rule). lc_notice_open stops Skip
        before the viewer shows, so opening during Skip still animates; the is_skipping check
        only guards a viewer that is somehow up while skipping."""
        return bool(renpy.is_skipping() or lc_pov_reduce_motion())

    def lc_noticed(notice_id):
        return lc_notice.noticed(getattr(store, "lc_noticed_record", None), notice_id)

    def lc_noticed_any(*notice_ids):
        return lc_notice.noticed_any(getattr(store, "lc_noticed_record", None), notice_ids)

    def lc_notice_open(notice_id):
        # Called only by the cue's click action, never by screen evaluation, hover or prediction.
        if store.lc_notice_active != notice_id or not lc_notice_available():
            return None
        renpy.stop_skipping()  # do not resume Skip (same as Hidden POV).
        store.lc_notice_viewed = True
        # Save-local record: a new dict, so rollback restores it with the store; the first lane
        # seen stands. retain_after_load keeps it in a save made on this same line.
        store.lc_noticed_record = lc_notice.record(getattr(store, "lc_noticed_record", None),
                                                   notice_id, lc_notice_lane())
        if LC_NOTICES[notice_id]["day_id"]:
            lc_discovery_mark(notice_id)
        renpy.retain_after_load()
        renpy.show_screen("lc_notice_viewer", notice_id=notice_id)
        return None

    # Auto-forward grace after the viewer closes (plain list, not rollback-tracked).
    _lc_notice_afm_hold = python_list([0.0])

    def lc_notice_close():
        renpy.hide_screen("lc_notice_viewer")
        _lc_notice_afm_hold[0] = _lc_notice_time.time() + 2.0
        return None

    def lc_notice_hover_sound():
        # Must return None: a `hovered` action that returns a value ends the say interaction.
        lc_ui_sound("tick", hover=True)
        return None

    def lc_notice_pins():
        names = _lc_notice_names()
        items = lc_notice.pins(LC_NOTICES, getattr(store, "lc_noticed_record", None))
        for item in items:
            item["lines"] = [lc_notice.fill_names(line, names) for line in item["lines"]]
            item["label"] = lc_notice.fill_names(item["label"], names)
        return items

    # Chain Hidden POV's afm callback (this file loads after systems/hidden_pov.rpy): Auto
    # waits while the viewer is open and restarts its countdown after it closes.
    _lc_notice_prior_afm_callback = config.afm_callback
    def lc_notice_afm_callback():
        if renpy.get_screen("lc_notice_viewer"):
            return False
        if _lc_notice_time.time() < _lc_notice_afm_hold[0]:
            return False
        if _lc_notice_prior_afm_callback is not None:
            return _lc_notice_prior_afm_callback()
        return True
    config.afm_callback = lc_notice_afm_callback

    def lc_notice_scope_cleanup():
        notice_id = store.lc_notice_active
        if notice_id and not lc_notice_in_scope(notice_id):
            lc_notice_end()
        return None

    config.start_interact_callbacks.append(lc_notice_scope_cleanup)
    if "lc_notice_hotspot" not in config.overlay_screens:
        config.overlay_screens.append("lc_notice_hotspot")

    # ------------------------------------------------------- registration checks
    def lc_notice_validate(notice_id):
        entry = LC_NOTICES[notice_id]
        problems = []
        for key in ("source", "closeup"):
            if entry[key] and not renpy.has_image(entry[key], exact=True):
                problems.append("%s=%r is not a defined image" % (key, entry[key]))
        povs = [(mid, pov.get("source"), lc_notice.hit_rect(pov["center"], LC_NOTICE_HITBOX_TOUCH))
                for mid, pov in sorted((getattr(store, "LC_POV_OPPORTUNITIES", None) or {}).items())]
        problems += lc_notice.validate(entry, LC_NOTICE_HITBOX_TOUCH, LC_POV_RESERVED_RECTS, povs,
                                       LC_NOTICES.values(),
                                       (config.screen_width, config.screen_height))
        return problems

    def lc_notice_validate_all():
        report = {}
        for notice_id in sorted(LC_NOTICES):
            problems = lc_notice_validate(notice_id)
            if problems:
                report[notice_id] = problems
        return report

# Runs after every registration file (init 1+) and the Hidden POV registry.
init 999 python:
    _lc_notice_report = lc_notice_validate_all()
    if _lc_notice_report:
        _lc_notice_warn("Notice registration problems:\n" + "\n".join(
            "  %s: %s" % (nid, problem)
            for nid in sorted(_lc_notice_report) for problem in _lc_notice_report[nid]), fatal=True)
