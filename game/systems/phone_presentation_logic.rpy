# Phone messages and notifications - the story-facing phone API
#
# Purpose: phone_add_message is how scenes deliver texts: it stores through phone_store_message
#   (systems/phone_state.rpy), flushes pending reply steps first, marks messages read in the chat
#   that is open, and queues the banner. Also: stat-free reply cards, notification queue and deep
#   links, phone unlock/HUD switches, cinematic mode. Screens live in screens/phone_sweetheart.rpy
#   and screens/phone_hud.rpy. Reply options may carry the phone-moment flags (docs/PHONE_MOMENTS.md):
#   leave_on_read=True (sends nothing, records the choice, shows a 'Seen' receipt) and
#   hesitate=True with an optional draft (a typed-draft animation before the send). Optional
#   send="..." (the bubble text when it differs from the card label) and choice_id="..." (the card
#   draws that choice's stat line in Insight/Full mode; the story scores the pick).
#
# Public API (call these from scenes/screens):
#   phone_add_message(thread_id, sender_id, text="", message_id=None, attachment_id=None, attachment_label=None, mark_unread=True, notify=False, notification_app="Messages", notification_title=None, display_time=None, deadline=True)
#       deliver one message (stable message_id; optional photo/notification); deadline=False
#       (a missed-call row) never resolves an open reply card to its default
#   phone_offer_reply(thread_id, prompt_id, options, default_id) -> bool
#       queue a save-safe, stat-free reply card for a thread (option keys: id, text, followups,
#       leave_on_read, hesitate, draft, send, choice_id, message_id). followups are (sender, text)
#       or (sender, text, message_id); message_id keeps Ryan's bubble on an existing save id.
#       To make the story WAIT for the pick and score it: the label in systems/phone_moments.rpy.
#   phone_choose_reply(thread_id, option_id, staged=False, by_default=False) -> bool
#       queue a picked reply (or post it at a story deadline); by_default: the card ran out, so
#       a leave-on-read default with the chat closed and still unread leaves it unread and unseen
#   phone_select_reply(thread_id, option_id) -> None
#       screen action for a reply option (starts the hesitation typing for hesitate=True)
#   phone_default_reply(thread_id)            pick the default reply
#   lc_phone_reply_caption(option)            stat line for an option's choice_id by choice mode
#       ('' in Normal mode or without a choice_id); render with substitute False
#   phone_pending_reply(thread_id)            the open reply prompt of a thread, or None
#   phone_deliver_reply_step(thread_id, force=False) -> None
#       one timed beat of a queued reply sequence (Ryan's beat waits while his reply is still
#       being typed, unless force)
#   phone_flush_reply_delivery(thread_id) -> None
#       post every pending step now (never waits for typing)
#   phone_reply_typing_text(thread_id)        the hesitation draft in the composer now, or None
#   phone_reply_typing_active(thread_id)      True while a typing record exists (also the moment
#       after the frames end, until Ryan's message is posted)
#   phone_reply_typing_clear(thread_id=None) -> None
#       drop the typing record of one thread (or all)
#   lc_phone_motion_instant()                 True under skip mode or reduced motion (screen
#       shake or transitions off): phone moments play instantly
#   LC_PHONE_TYPING                           transient typing records (never saved)
#   phone_queue_notification(app, title, body, kind="message", thread_id=None, sender=None) -> None
#       queue a banner
#   phone_show_next_notification() -> None    show the next queued banner
#   phone_finish_notification() -> None       banner finished
#   lc_phone_open_from_notification(item) -> None
#       open the phone on the banner's app/thread
#   lc_phone_link_app()                       deep-link app for the handset (default 'home')
#   lc_phone_link_thread()                    deep-link thread or None
#   lc_phone_thread_open(thread_id)           True while the phone shows this chat
#   lc_phone_leave_thread(app, thread_id) -> None
#       leaving a chat marks it read
#   lc_phone_message_pop(thread_id)           UI pop for a message landing in the open chat
#   set_phone_unlocked(value=True) -> None    phone available or not
#   set_phone_hud_enabled(value=True) -> None
#       show/hide the HUD icon
#   phone_unlock_with_tutorial() -> None      unlock the phone and show the first-use tutorial
#   enter_cinematic_mode() -> None            full-screen CG: hide the phone, CG dialogue box
#   exit_cinematic_mode() -> None             back to normal
#   phone_notification_preview(text, max_chars=PHONE_NOTIFICATION_BODY_MAX)
#       one-line banner preview
#   phone_app_icon_path(app)                  icon for an app
#   phone_unread_badge_label(count=None)      badge text ('99+' cap)
#   debug_reset_phone_tutorial() -> None      dev: show the tutorial again
#
# Internal (helpers for this file and its screens; do not call from scenes): _lc_phone_plain,
#   _lc_phone_typing_record
#
# Example:
#   $ phone_add_message(
#       "group", "julian", text="I'm downstairs.", message_id="prologue_julian_downstairs_01",
#       mark_unread=True, notify=True, notification_title="Trip Group",
#   )
#
# Depends on: systems/phone_state.rpy, systems/story_state.rpy, systems/lc_fx.rpy,
#   systems/choice_engine.rpy, systems/stat_delta_colours.rpy,
#   systems/lc_hooks.rpy, python-packages/lc_phone_moments.py,
#   screens/gameplay_toasts.rpy, screens/phone_hud.rpy (defaults), screens/scrapbook_ui.rpy (banner
#   screen)
# Hooks: emits phone_reply_chosen (thread_id, prompt_id, option, unopened=bool) from
#   phone_choose_reply (systems/phone_moments.rpy listens)
# Load order: default (init 0); it calls systems/phone_state.rpy only at run time
# Docs: docs/ARCHITECTURE.md, docs/PHONE_MOMENTS.md   Tests: tests/test_phone_replies.py,
#   tests/test_phone_read_state.py, tests/test_behaviour_freeze.py, tests/test_phone_moments.py

init python:
    import time as _lc_phone_clock
    import lc_phone_moments

    PHONE_NOTIFICATION_BODY_MAX = 72
    PHONE_NOTIFICATION_TITLE_MAX = 32

    PHONE_APP_ICON_PATHS = {
        "Phone": "gui/phone/sprite_match/messages.png",
        "Messages": "gui/phone/sprite_match/messages.png",
        "Photos": "gui/phone/sprite_match/photos.png",
        "Shop": "gui/phone/sprite_match/shop.png",
        "Online Shop": "gui/phone/sprite_match/shop.png",
        "Delivery": "gui/phone/sprite_match/delivery.png",
        "Orders": "gui/phone/sprite_match/delivery.png",
        "Wallet": "gui/phone/sprite_match/wallet.png",
        "Status": "gui/phone/sprite_match/status.png",
        "Settings": "gui/phone/sprite_match/settings.png",
    }

    def phone_notification_preview(text, max_chars=PHONE_NOTIFICATION_BODY_MAX):
        """Return a compact single-line notification preview with a clean ellipsis."""
        clean = " ".join((text or "").split())
        if len(clean) <= max_chars:
            return clean

        cutoff = max(4, max_chars - 3)
        shortened = clean[:cutoff].rstrip()

        # Prefer ending at a word boundary when that does not throw away too much text.
        if " " in shortened:
            word_boundary = shortened.rsplit(" ", 1)[0].rstrip()
            if len(word_boundary) >= int(cutoff * 0.72):
                shortened = word_boundary

        return shortened.rstrip(" ,.;:-") + "..."

    def phone_app_icon_path(app):
        """Return the custom UI icon for a phone app, with Phone as fallback."""
        clean = (app or "Phone").strip()
        return PHONE_APP_ICON_PATHS.get(clean, PHONE_APP_ICON_PATHS["Phone"])

    def phone_unread_badge_label(count=None):
        """Return a compact unread badge value suitable for the Phone HUD."""
        value = phone_total_unread() if count is None else int(count)
        if value > 99:
            return "99+"
        return str(max(0, value))

    def set_phone_unlocked(value=True):
        renpy.store.phone_unlocked = bool(value)
        renpy.restart_interaction()
        return None

    def set_phone_hud_enabled(value=True):
        renpy.store.phone_hud_enabled = bool(value)
        renpy.restart_interaction()
        return None

    def enter_cinematic_mode():
        """Full-screen CG. Hides the phone and switches the say box to CG mode."""
        renpy.store.phone_hud_enabled = False
        renpy.store.lc_cinematic_mode = True
        renpy.restart_interaction()
        return None

    def exit_cinematic_mode():
        renpy.store.phone_hud_enabled = True
        renpy.store.lc_cinematic_mode = False
        renpy.restart_interaction()
        return None

    def phone_queue_notification(app, title, body, kind="message", thread_id=None, sender=None):
        item = {
            "app": app,
            "title": phone_notification_preview(title, PHONE_NOTIFICATION_TITLE_MAX),
            "body": phone_notification_preview(body, PHONE_NOTIFICATION_BODY_MAX),
            "kind": kind,
            "thread_id": thread_id,
            "sender": sender or "",
        }
        renpy.store.phone_notification_queue.append(item)
        if renpy.store.phone_notification_current is None:
            phone_show_next_notification()
        return None

    # Notification deep link: (phone_app, phone_thread) read once by the
    # phone_screen defaults the next time the phone opens.
    PHONE_NOTIFICATION_APP_SCREENS = {
        "Messages": "messages",
        "Photos": "photos",
        "Shop": "shop",
        "Online Shop": "shop",
        "Delivery": "delivery",
        "Orders": "delivery",
        "Wallet": "wallet",
    }

    def lc_phone_open_from_notification(item):
        """Open the phone straight on the notification's app or chat thread."""
        item = item or {}
        if not getattr(renpy.store, "phone_unlocked", False):
            phone_finish_notification()
            return None
        thread_id = item.get("thread_id")
        if thread_id:
            phone_mark_thread_read(thread_id)
            target = ("thread", thread_id)
        elif item.get("kind") == "feed":
            # A feed banner (systems/feed.rpy) opens the feed app (a new visit: fresh blue dots).
            lc_feed_visit_start()
            target = ("feed", None)
        else:
            target = (PHONE_NOTIFICATION_APP_SCREENS.get((item.get("app") or "").strip(), "home"), None)
        renpy.store.lc_phone_deep_link = target
        # Drop the rest of the banner queue's current card; the next one still shows.
        phone_finish_notification()
        renpy.show_screen("phone_screen")
        renpy.restart_interaction()
        return None

    def lc_phone_link_app():
        link = getattr(renpy.store, "lc_phone_deep_link", None)
        return link[0] if link else "home"

    def lc_phone_link_thread():
        link = getattr(renpy.store, "lc_phone_deep_link", None)
        return link[1] if link else None

    def phone_show_next_notification():
        if renpy.store.phone_notification_current is not None:
            return None
        if not renpy.store.phone_notification_queue:
            return None
        renpy.store.phone_notification_current = renpy.store.phone_notification_queue.pop(0)
        renpy.show_screen("phone_notification_banner")
        renpy.restart_interaction()
        return None

    def phone_finish_notification():
        renpy.store.phone_notification_current = None
        renpy.hide_screen("phone_notification_banner")
        renpy.restart_interaction()
        if renpy.store.phone_notification_queue:
            phone_show_next_notification()
        return None

    def phone_pending_reply(thread_id):
        return getattr(renpy.store, "phone_reply_prompts", {}).get(thread_id)

    def phone_offer_reply(thread_id, prompt_id, options, default_id):
        """Queue a save-safe reply card for one thread (stat-free: the story scores a pick).

        Options are dicts with id, text and optional followups: (sender, text)
        pairs. Optional "send": the text the bubble posts when it differs from the card label
        ("Show [girlfriend_name]"). Optional "choice_id": the stat line the card shows in
        Insight/Full mode (lc_phone_reply_caption) for a pick the story scores.
        Stable prompt IDs become story-value keys and message-ID prefixes.
        """
        if thread_id not in PHONE_THREAD_ORDER or not prompt_id:
            raise ValueError("Unknown thread or missing reply prompt ID")
        ids = [option["id"] for option in options]
        if not 2 <= len(ids) <= 4 or len(set(ids)) != len(ids) or default_id not in ids:
            raise ValueError("Reply prompts need 2-4 unique choices and a valid default")
        lc_phone_moments.validate_options(options)
        if has_story_value(prompt_id) or phone_pending_reply(thread_id):
            return False
        renpy.store.phone_reply_prompts[thread_id] = {
            "id": prompt_id, "options": options, "default": default_id,
        }
        return True

    def phone_choose_reply(thread_id, option_id, staged=False, by_default=False):
        """Queue a picked reply, or post it in order at a story deadline."""
        prompt = phone_pending_reply(thread_id)
        if not prompt:
            return False
        option = next((item for item in prompt["options"] if item["id"] == option_id), None)
        if option is None:
            return False
        # Remove first so the writer's deadline hook cannot resolve twice.
        del renpy.store.phone_reply_prompts[thread_id]
        set_story_value(prompt["id"], option_id)
        # A default taken at a deadline while the chat is closed: Ryan never opened it.
        unopened = (bool(by_default) and not lc_phone_thread_open(thread_id)
                    and phone_thread_unread_count(thread_id) > 0)
        if lc_phone_moments.is_leave_on_read(option):
            # Ryan reads it and writes nothing; only the other side's follow-ups may come.
            # Unopened, it stays unread (no 'Seen' either).
            if not unopened:
                phone_mark_thread_read(thread_id)
            steps = []
        else:
            steps = [("player", option.get("send", option["text"]), option.get("message_id") or prompt["id"] + "_ryan")]
        # A follow-up is (sender, text) or (sender, text, message_id): the third item keeps an
        # existing save id when a story text moves onto a reply card.
        steps.extend((step[0], step[1], step[2] if len(step) > 2 and step[2] else
                      "{}_followup_{:02d}".format(prompt["id"], index + 1))
                     for index, step in enumerate(option.get("followups", ())))
        lc_hook_run("phone_reply_chosen", thread_id, prompt["id"], option, unopened=unopened)
        if staged and steps:
            # Save state contains plain strings, not callables or displayables.
            if not hasattr(renpy.store, "phone_reply_delivery"):
                renpy.store.phone_reply_delivery = {}
            renpy.store.phone_reply_delivery[thread_id] = steps
        else:
            for sender, text, message_id in steps:
                phone_add_message(thread_id, sender, text=text, message_id=message_id,
                                  mark_unread=False, notify=False)
        return True

    def phone_deliver_reply_step(thread_id, force=False):
        """One timed beat in the existing open-thread sequence overlay. Ryan's own beat waits
        while his hesitating reply is still being typed (force: a story deadline never waits)."""
        pending = getattr(renpy.store, "phone_reply_delivery", {}).get(thread_id)
        if not pending:
            return None
        if pending[0][0] == "player":
            if not force and phone_reply_typing_text(thread_id) is not None:
                return None
            phone_reply_typing_clear(thread_id)
        sender, text, message_id = pending.pop(0)
        if not pending:
            del renpy.store.phone_reply_delivery[thread_id]
        added = phone_store_message(thread_id, sender, text=text, message_id=message_id,
                                    mark_unread=False, notify=False)
        if added and sender != "player":
            lc_phone_message_pop(thread_id)
        renpy.restart_interaction()
        return None

    def phone_flush_reply_delivery(thread_id):
        """A subsequent story message catches up the pending reply in order."""
        while getattr(renpy.store, "phone_reply_delivery", {}).get(thread_id):
            phone_deliver_reply_step(thread_id, force=True)
        phone_reply_typing_clear(thread_id)
        return None

    def phone_default_reply(thread_id):
        prompt = phone_pending_reply(thread_id)
        return phone_choose_reply(thread_id, prompt["default"], by_default=True) if prompt else False

    def phone_select_reply(thread_id, option_id):
        # Ren'Py Function actions must return None or the Phone closes.
        prompt = phone_pending_reply(thread_id)
        option = next((item for item in (prompt or {}).get("options", ()) if item["id"] == option_id), None)
        if phone_choose_reply(thread_id, option_id, staged=True) and option and option.get("hesitate"):
            frames = lc_phone_moments.hesitation_frames(_lc_phone_plain(option.get("draft")),
                                                        _lc_phone_plain(option.get("send", option["text"])),
                                                        skip=lc_phone_motion_instant())
            if frames:
                LC_PHONE_TYPING[thread_id] = {"frames": frames, "start": _lc_phone_clock.time(),
                                              "step": lc_phone_moments.frame_step(frames),
                                              "message_id": option.get("message_id") or prompt["id"] + "_ryan"}
        return None

    def lc_phone_reply_caption(option):
        """Stat line for a scored reply option (its "choice_id"), in the same format and colours
        as a story choice card: Insight arrows, Full numbers. '' in Normal (Immersive) mode, for
        options without a choice_id and for no-stat picks (Developer shows ID / "no stats").
        Computed at render time, so a mode change updates it. Render with substitute False."""
        choice_id = (option or {}).get("choice_id")
        mode = current_choice_mode()
        if not choice_id or mode == "normal":
            return ""
        import lc_ui_logic
        _line, chips = lc_ui_logic.parse_choice_caption(format_choice(choice_id, "-"))
        if chips:
            return lc_choice_effect_markup(chips)
        if mode == "developer":
            return "[{}]  [ID: {}]".format(_choice_effect_text(choice_id, exact=True) or "no stats",
                                           choice_id)
        return ""

    # Hesitation typing (phone moments). Transient: an init-time python_dict is never saved or
    # rolled back. A record only counts while Ryan's queued message (saved state) is still next
    # in phone_reply_delivery, so a rollback or load that undid the pick drops it. The save-safe
    # part (the chosen reply and its queued steps) is stored by phone_choose_reply before the
    # typing starts.
    LC_PHONE_TYPING = python_dict()

    def _lc_phone_typing_record(thread_id):
        record = LC_PHONE_TYPING.get(thread_id)
        if not record:
            return None
        pending = (getattr(renpy.store, "phone_reply_delivery", None) or {}).get(thread_id) or ()
        if not pending or pending[0][2] != record.get("message_id"):
            LC_PHONE_TYPING.pop(thread_id, None)
            return None
        return record

    def _lc_phone_plain(text):
        """Names filled in ('[girlfriend_name]' -> the player's name) before the text is typed
        out a letter at a time, so no frame holds half a substitution."""
        if not text:
            return text
        try:
            return renpy.substitute(text)
        except Exception:
            return text

    def lc_phone_motion_instant():
        """Skip mode or reduced motion (screen shake or transitions off): no typing or ring
        animation, and nothing waits on one."""
        try:
            if renpy.is_skipping():
                return True
        except Exception:
            pass
        return (not getattr(persistent, "lc_screen_shake", True)
                or not _preferences.transitions)

    def phone_reply_typing_active(thread_id):
        return _lc_phone_typing_record(thread_id) is not None

    def phone_reply_typing_text(thread_id):
        record = _lc_phone_typing_record(thread_id)
        if not record:
            return None
        return lc_phone_moments.frame_at(record["frames"], _lc_phone_clock.time() - record["start"],
                                         record["step"])

    def phone_reply_typing_clear(thread_id=None):
        if thread_id is None:
            LC_PHONE_TYPING.clear()
        else:
            LC_PHONE_TYPING.pop(thread_id, None)
        return None

    # The one writer story code calls: phone_store_message plus presentation.
    def phone_add_message(
        thread_id,
        sender_id,
        text="",
        message_id=None,
        attachment_id=None,
        attachment_label=None,
        mark_unread=True,
        notify=False,
        notification_app="Messages",
        notification_title=None,
        display_time=None,
        deadline=True,
    ):
        # Landing in the chat the player is reading right now = already read
        # (darryn 2026-11-08: no badge after reading a thread from a notification).
        if mark_unread and lc_phone_thread_open(thread_id):
            mark_unread = False
        # A new incoming message is the deadline; stable-ID replays are not. deadline=False (a
        # missed-call row) still posts what the player already picked, but leaves an open card open.
        if sender_id != "player" and not (message_id and phone_has_message(message_id)):
            if deadline:
                phone_default_reply(thread_id)
            phone_flush_reply_delivery(thread_id)
        added = phone_store_message(
            thread_id,
            sender_id,
            text=text,
            message_id=message_id,
            attachment_id=attachment_id,
            attachment_label=attachment_label,
            mark_unread=mark_unread,
            display_time=display_time,
        )

        if added and sender_id != "player":
            lc_phone_message_pop(thread_id)

        if added and notify and sender_id != "player":
            title = notification_title or phone_thread_label(thread_id)
            if attachment_id:
                preview = text.strip() if text.strip() else "Sent a photo"
                kind = "photo"
            else:
                preview = text.strip() if text.strip() else "New message"
                kind = "message"
            sender_name = ""
            if sender_id not in (None, "player", "system"):
                sender_name = phone_sender_label(sender_id)
            phone_queue_notification(
                notification_app,
                title,
                preview,
                kind=kind,
                thread_id=thread_id,
                sender=sender_name,
            )

        return added

    def lc_phone_thread_open(thread_id):
        """True while the Phone shows this chat thread."""
        try:
            if not renpy.get_screen("phone_screen"):
                return False
            if renpy.get_screen_variable("phone_app", screen="phone_screen") != "thread":
                return False
            return renpy.get_screen_variable("phone_thread", screen="phone_screen") == thread_id
        except Exception:
            return False

    def lc_phone_leave_thread(app, thread_id):
        """Leaving a chat (back button or closing the Phone) marks it read."""
        if app == "thread" and thread_id:
            phone_mark_thread_read(thread_id)
        return None

    def lc_phone_message_pop(thread_id):
        """UI pop when a message lands in the chat thread that is open right now."""
        if not lc_phone_thread_open(thread_id):
            return None
        return lc_ui_sound("message_pop")

    def debug_reset_phone_tutorial():
        persistent.phone_tutorial_seen = False
        renpy.notify("Phone tutorial reset. It will appear at the next Phone unlock.")
        return None

    def phone_unlock_with_tutorial():
        set_phone_unlocked(True)

        # Release behaviour: tutorial is shown once globally.
        # Developer behaviour: always show it so repeated New Game tests can verify the flow.
        if (not persistent.phone_tutorial_seen) or bool(config.developer):
            renpy.show_screen("phone_first_use_tutorial")
        else:
            renpy.notify("Phone unlocked.")
        return None
