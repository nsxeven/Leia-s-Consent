# Ryan's thoughts - keep one thought at the end of a day review; it evolves with stats and lane
#
# Purpose: When a day's review closes, offer up to three of Ryan's thoughts drawn from beats this
#   save actually saw that day, plus "keep nothing" (screens/thoughts_screen.rpy). The kept thought
#   is a save-local value; a later day reads it to tint a few `think` lines or add one reply
#   option. Keeping a thought never changes stats. Hidden in the Day One demo build. Rules and the
#   thought pool live in python-packages/lc_thoughts.py; this file binds them to the store.
#
# Public API (call these from scenes/screens):
#   lc_thought_kept(day_id)                   id of the thought kept at the end of day_id, or None
#       (nothing kept, never offered, old save)
#   lc_thought_line(day_id)                   the kept thought's text, resolved now (current stats
#       and lane) with the player's names filled in; None when nothing was kept
#   lc_thought_text(thought_id)               a thought's text for the current stats/lane, names
#       filled in
#   lc_thought_tint(thought_id)               tint stamp label for Insight/Full ('' = base text)
#   lc_thought_lane()                         lane key for variants (lc_thoughts.lane_from_lean of
#       lc_current_lean), or None
#   lc_thought_offer_ids(day_id)              ids the end of day_id's review would offer ([] in the
#       demo build, once the day was decided, or when no beat was seen)
#   lc_thought_offer(day_id) -> None          show the offer and store the answer (keep nothing =
#       None); does nothing when there is nothing to offer
#   lc_thought_keep(day_id, thought_id) -> None
#       store the answer for day_id (None = keep nothing)
#   lc_thought_on_review_closed(day_id) -> None
#       review_closed hook: runs the offer; a failure never stops the review in release
#   default lc_thoughts_kept                  save state: {day_id: thought id or None}
#
# Internal (helpers for this file and its screens; do not call from scenes): _lc_thought_names,
#   _lc_thought_stats
#
# Example:
#   if lc_thought_kept("ch01_d1") == "d1_dream":              (a Day Two echo)
#       think "[lc_d2_dream_echo]"
#   $ lc_d2_thought = lc_thought_line("ch01_d1")              (None when nothing was kept)
#
# Depends on: python-packages/lc_thoughts.py, systems/lc_hooks.rpy, systems/stats.rpy
#   (lc_stats_flat, lc_current_lean), systems/story_state.rpy (has_story_flag, get_story_value),
#   chapters/ch01/ch01_release_demo.rpy (LC_DAY1_DEMO_BUILD), screens/thoughts_screen.rpy
# Hooks: listens to review_closed (systems/day_review.rpy, label lc_day_review)
# Load order: default (init 0); everything it reads is looked up at call time
# Docs: docs/THOUGHTS.md, docs/ARCHITECTURE.md   Tests: tests/test_thoughts.py

default lc_thoughts_kept = {}

init python:
    import lc_thoughts

    def _lc_thought_names():
        return {key: getattr(store, key, None) for key in ("player_name", "girlfriend_name", "friend_name")}

    def _lc_thought_stats():
        try:
            return lc_stats_flat()
        except Exception:
            return {}

    def lc_thought_lane():
        try:
            return lc_thoughts.lane_from_lean(lc_current_lean())
        except Exception:
            return None

    def lc_thought_text(thought_id):
        """Text for the current stats and lane, with the player's names filled in."""
        text = lc_thoughts.thought_text(thought_id, _lc_thought_stats(), lc_thought_lane())
        return lc_thoughts.fill_names(text, _lc_thought_names())

    def lc_thought_tint(thought_id):
        """Which lane/stat tints the thought right now ('' for the base text). Insight/Full only."""
        return lc_thoughts.tint_label(
            lc_thoughts.variant_key(thought_id, _lc_thought_stats(), lc_thought_lane()))

    def lc_thought_kept(day_id):
        return lc_thoughts.kept_id(getattr(store, "lc_thoughts_kept", None), day_id)

    def lc_thought_line(day_id):
        thought_id = lc_thought_kept(day_id)
        if thought_id is None:
            return None
        return lc_thought_text(thought_id)

    def lc_thought_offer_ids(day_id):
        """What the end of day_id's review would offer. Nothing in the Day One demo build, and
        nothing once this save already answered for that day (rollback restores the answer)."""
        if LC_DAY1_DEMO_BUILD:
            return []
        if day_id in (getattr(store, "lc_thoughts_kept", None) or {}):
            return []
        seen = lc_thoughts.seen_beats(day_id, has_story_flag,
                                      lambda key: get_story_value(key, None))
        return lc_thoughts.offer(day_id, _lc_thought_stats(), lc_thought_lane(), seen)

    def lc_thought_keep(day_id, thought_id):
        """Store the answer. Reassigns the dict, so rollback and saves see the change."""
        store.lc_thoughts_kept = lc_thoughts.keep(getattr(store, "lc_thoughts_kept", None),
                                                  day_id, thought_id)
        return None

    def lc_thought_offer(day_id):
        """Show the offer card and store the answer. A reply that was not offered keeps nothing."""
        ids = lc_thought_offer_ids(day_id)
        if not ids:
            return None
        picked = renpy.call_screen("lc_thought_offer_screen", day_id, ids)
        lc_thought_keep(day_id, picked if picked in ids else None)
        return None

    def lc_thought_on_review_closed(day_id):
        """review_closed hook. Release builds never let a broken offer stop the review; Ren'Py's
        own control flow (rollback, load, quit: renpy.game.CONTROL_EXCEPTIONS) always passes."""
        control = getattr(getattr(renpy, "game", None), "CONTROL_EXCEPTIONS", ())
        try:
            lc_thought_offer(day_id)
        except control:
            raise
        except Exception as e:
            if config.developer:
                raise
            try:
                renpy.log("[thoughts] offer failed for %s: %r" % (day_id, e))
            except Exception:
                pass
        return None

    lc_hook_add("review_closed", lc_thought_on_review_closed)
