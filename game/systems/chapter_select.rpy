# Chapter Select - start a new game at a later Day with a consistent preset
#
# Purpose: Seeds the story values, flags, stats and outfits a day reads, then jumps to that day's
#   normal entry label; it never edits story scenes. Each Day pack registers its own preset in
#   CHAPTER_SELECT_PRESETS (its *_chapter.rpy, init 1): button label and note, the route list and
#   heading the screen shows, and the seed function that fills the store. This file keeps the
#   generic part: the registry, the reset every preset starts from, apply, and the unlock rule.
#   CHAPTER_SELECT_RULE decides when the main-menu entry shows. The screen is
#   screens/chapter_select_screen.rpy. Each Day pack's "finished" seed also fills the phone with
#   what that Day delivered in play (its messages, Photos attachments, answered reply cards, the
#   Trip Group picture) through the chapter_select_phone* helpers below: read, no banners.
#
# Public API (call these from scenes/screens):
#   define CHAPTER_SELECT_RULE                'always' | 'developer' | 'unlocked' |
#       'developer_or_unlocked' | 'never'
#   define CHAPTER_SELECT_PRESETS             {day: dict(label, note, heading, routes, seed[, default,
#       unlock_flag])}, filled by the Day packs in play order
#   chapter_select_days()                     [(day, button label, note)] in play order
#   chapter_select_default_day()              the Day the page opens on (registered default=True)
#   chapter_select_unlocked()                 True when the main-menu Chapter Select entry should
#       show
#   chapter_select_apply(day, route)          seed a new game for (day, route preset); returns the
#       entry label
#   chapter_select_unlock_after_day_two(flag_id, value=True) -> None
#       story_flag_set hook: the preset's unlock_flag (first finished Day Two) unlocks it
#   chapter_select_phone(thread_id, sender_id, message_id, text="", attachment_id=None, attachment_label=None, display_time=None) -> None
#       an earlier Day's message as play left it: read, no banner, sound or reply deadline;
#       an attachment also lands in Photos
#   chapter_select_phone_reply(prompt_id, option_id, left_on_read=None, time=None) -> None
#       an earlier Day's reply card, already answered (the story value a pick records);
#       left_on_read=thread_id also leaves the 'Seen' receipt stamped `time`
#   chapter_select_phone_group(stage, maya_member=False) -> None
#       the Trip Group picture stage ('trio' / 'four') and Maya's membership
#   label ch01_chapter_select_entry           label the screen starts the new game through
#
# Internal (helpers for this file and the Day packs' seed functions; do not call from scenes):
#   _chapter_select_reset
#
# Example (a Day pack's *_chapter.rpy):
#   init 1 python:
#       def ch01_d6_select_seed(route):
#           ch01_d5_select_finished(route)          # earlier Days' "finished" seeds, in order
#           return "ch01_day6_start"
#       CHAPTER_SELECT_PRESETS["day6"] = dict(label=lc_chapters.select_label("day6"), note="...",
#           heading=_("Stored Day Five ending"), routes=CH01_SELECT_DAY6_ROUTES, seed=ch01_d6_select_seed)
#
# Depends on: systems/lc_hooks.rpy, systems/story_state.rpy, systems/stats.rpy,
#   systems/wardrobe_logic.rpy, systems/day_review.rpy (lc_review_reset), systems/phone_state.rpy
#   (phone_store_message), systems/phone_group_avatar.rpy, python-packages/lc_phone_moments.py
#   (read receipts), the Day packs' *_chapter.rpy (presets), game/00_release_build.rpy
# Hooks: listens to story_flag_set (unlock after the registered unlock_flag)
# Load order: define (init 0) for the registry, which the Day packs fill at init 1; the functions at
#   init 10, after the story-state, stats and hook helpers (init <= 0) they call while seeding
# Docs: docs/ARCHITECTURE.md, docs/DAY_PACK.md   Tests: tests/test_lc_chapters.py,
#   tests/test_release_from_main.py, tests/test_behaviour_freeze.py,
#   tests/test_chapter_select_phone.py

define CHAPTER_SELECT_RULE = "developer_or_unlocked" if LC_IS_RELEASE else "always"  # game/00_release_build.rpy
define CHAPTER_SELECT_PRESETS = {}  # filled by the Day packs (*_chapter.rpy, init 1), in play order

init 10 python:
    import lc_phone_moments

    def chapter_select_days():
        """[(day, button label, note)] for every registered preset, in play order."""
        return [(day, p["label"], p["note"]) for day, p in CHAPTER_SELECT_PRESETS.items()]

    def chapter_select_default_day():
        """The Day the Chapter Select page opens on: the preset registered with default=True."""
        for day, p in CHAPTER_SELECT_PRESETS.items():
            if p.get("default"):
                return day
        return next(iter(CHAPTER_SELECT_PRESETS), None)

    def chapter_select_unlocked():
        """True when the main-menu Chapter Select entry should be offered."""
        if LC_DAY1_DEMO_BUILD:
            return False
        rule = store.CHAPTER_SELECT_RULE
        dev = bool(config.developer)
        unlocked = bool(getattr(persistent, "ch01_chapter_select_unlocked", False))
        if rule == "always":
            return True
        if rule == "developer":
            return dev
        if rule == "unlocked":
            return unlocked
        if rule == "developer_or_unlocked":
            return dev or unlocked
        return False

    def _chapter_select_reset(stats, hist):
        lc_review_reset()
        store.story_flags = {}
        store.story_values = {}
        # Stat model v2: Love, Trust, Exhibitionism (exh), Temptation (tem), Sharing (sha, default 0).
        # Preset numbers are the old presets converted with lc_stat_model.migrate_stats, with the
        # Exhibitionism routes raised to typical v2 values so the Day 2 lane and the Day 4/5
        # "her own call" steps resolve the same way they did before.
        store.relationship_stats = {"love": stats["love"], "trust": stats["trust"],
                                    "sharing": stats.get("sha", 0), "temptation": stats["tem"]}
        store.partner_stats = {"exhibitionism": stats["exh"]}
        store.player_stats = {}
        store.choice_history = list(hist)
        store.last_choice_id = None
        store.owned_outfits = ["casual_default"]
        store.equipped_outfit = "casual_default"
        store.money = 500
        set_phone_unlocked(True)
        set_phone_hud_enabled(True)

    def chapter_select_apply(day, route):
        """Seed a new game for the chosen day and route preset. Returns the entry label."""
        entry = CHAPTER_SELECT_PRESETS[day]["seed"](route)
        set_story_flag("chapter_select_used")
        set_story_value("chapter_select_preset", "{}:{}".format(day, route))
        return entry

    # Phone history. A Day pack's "finished" seed replays what that Day put on the phone, in play
    # order, as a player who read every chat would have it at the next Day's start.
    def chapter_select_phone(thread_id, sender_id, message_id, text="", attachment_id=None,
                             attachment_label=None, display_time=None):
        """Chapter Select: one earlier-Day message, stored read (no banner, sound or reply deadline).
        Stable message ids keep it idempotent; an attachment is indexed in Photos as in play."""
        phone_store_message(thread_id, sender_id, text=text, message_id=message_id,
                            attachment_id=attachment_id, attachment_label=attachment_label,
                            mark_unread=False, notify=False, display_time=display_time)
        return None

    def chapter_select_phone_reply(prompt_id, option_id, left_on_read=None, time=None):
        """Chapter Select: an earlier Day's reply card, answered with option_id (the story value
        phone_choose_reply records, so the card is never offered again). The posted messages come
        from chapter_select_phone. left_on_read=thread_id: the pick left the chat on read, so the
        'Seen' receipt sits under its last incoming message, stamped `time`."""
        set_story_value(prompt_id, option_id)
        if left_on_read:
            store.lc_phone_read_receipts = lc_phone_moments.record_left_on_read(
                getattr(store, "lc_phone_read_receipts", None), left_on_read, prompt_id,
                lc_phone_moments.last_incoming_id(phone_messages_for_thread(left_on_read)), time)
        return None

    def chapter_select_phone_group(stage, maya_member=False):
        """Chapter Select: the Trip Group picture stage and whether Maya is in the group."""
        store.phone_group_avatar_stage = stage
        store.phone_group_maya_member = bool(maya_member)
        return None

    # Unlock after the first completed Day Two, without editing any story scene.
    def chapter_select_unlock_after_day_two(flag_id, value=True):
        """story_flag_set hook: the first finished Day Two (a preset's unlock_flag) unlocks Chapter Select."""
        if value and any(p.get("unlock_flag") == flag_id for p in CHAPTER_SELECT_PRESETS.values()):
            if not getattr(persistent, "ch01_chapter_select_unlocked", False):
                persistent.ch01_chapter_select_unlocked = True

    lc_hook_add("story_flag_set", chapter_select_unlock_after_day_two)


label ch01_chapter_select_entry:
    # Entered from the Chapter Select screen (Start) with the choice stored in
    # persistent.ch01_chapter_select_pending = (day, route).
    $ _cs_pending = persistent.ch01_chapter_select_pending or (chapter_select_default_day(), "love")
    $ _cs_entry = chapter_select_apply(_cs_pending[0], _cs_pending[1])
    $ persistent.ch01_chapter_select_pending = None
    jump expression _cs_entry
