# Feed - the parody social-feed phone app (placeholder name LC_FEED_APP_NAME)
#
# Purpose: Story code registers feed posts at init and releases them where they should appear;
#   the app joins the phone home grid once the story installs it (Maya's intro on the Day Two
#   photo walk) or any post is out. New posts badge the app icon and the phone HUD; each release
#   call (one post or a batch) shows one phone banner that opens the feed. Opening the feed counts
#   as seeing every released post in it (the list shows the captions); tapping a card also records
#   it as opened. A post may carry a one-time reaction (a label or a callable) that runs after the
#   phone closes, the first time Ryan sees it. Reading the feed never changes stats.
#   Rules live in python-packages/lc_feed.py; this file binds them to the store.
#
# Public API (call these from scenes/screens):
#   lc_feed_register(post_id, day, author, handle, caption, image=None, comments=(), likes=0, when=None, unlock=None, mature=False, reaction=None) -> None
#       register one post at init 1+ (comments: up to 3 (handle, text) pairs; when: None = the
#       story clock at release, a fixed "14:10" or a callable run at release; unlock: None, a
#       zero-argument callable or a dict of story values / "leia_did" / "leia_did_not", checked
#       once at release; mature=True shows an 18+ card instead of the photo outside the viewer,
#       as the Gallery does; reaction: a label name or zero-argument callable run once after the
#       phone closes when Ryan first sees the post); a duplicate id raises
#   lc_feed_install() -> None                 put the app on Ryan's home grid (no post needed)
#   lc_feed_release(*post_ids, notify=True) -> None
#       release posts (each only if its gate holds now and it is not out yet); one banner for the
#       whole call when anything came out and notify; stamps each post's time
#   lc_feed_visible()                         released posts, newest first (entries)
#   lc_feed_entry(post_id)                    the registered entry, or None
#   lc_feed_text(text)                        a post string with typed names filled in
#   lc_feed_avatar(entry)                     a known author's phone avatar path, or None
#   lc_feed_when(entry)                       the post's frozen time text, or "" (no device clock)
#   lc_feed_seen(post_id)                     True once Ryan saw the post (feed opened while it
#       was out, or the post opened); read this in scenes
#   lc_feed_any_seen(*post_ids)               True when any of them was seen
#   lc_feed_opened(post_id)                   True once the post itself was tapped open
#   lc_feed_open_post(post_id) -> None        screen action: mark opened + seen, show lc_feed_post
#   lc_feed_catch_up() -> None                screen timer: marks every listed post seen
#   lc_feed_visit_start() -> None             screen action: a new visit to the feed (blue dots)
#   lc_feed_is_fresh(post_id)                 True while the post's blue "new" dot shows
#   lc_feed_reveal_focus(adj) -> None         card hovered action: scroll a keyboard/gamepad-
#       focused card fully into the feed viewport
#   lc_feed_app_visible()                     True when the app is on the home grid
#   lc_feed_unseen_count()                    released posts not seen yet (icon + HUD badges)
#   lc_feed_badge()                           icon badge text, or None
#   lc_feed_likes(entry)                      "1 like" / "23 likes"
#   lc_feed_photo(entry, width, height, context="list")
#       the post photo fitted to a box; mature photos are a gallery-style 18+ card (no image)
#       except in the "viewer" context, while GALLERY_MASK_MATURE_COVERS is on
#   label lc_feed_reaction_runner             runs pending reactions (called automatically after
#       the phone closes; a scene may also call it)
#   define LC_FEED_APP_NAME                   the app's display name (one-line rename)
#   LC_FEED_POSTS                             the registry {post_id: entry} (init-time data)
#   default lc_feed_installed                 save state: the app is on the phone
#   default lc_feed_released                  save state: post ids in release order
#   default lc_feed_seen_posts                save state: seen post ids
#   default lc_feed_opened_posts              save state: tapped-open post ids
#   default lc_feed_stamps                    save state: {post_id: time text} frozen at release
#   default lc_feed_reacted                   save state: posts whose reaction was queued
#   default lc_feed_reaction_queue            save state: post ids whose reaction has not run yet
#
# Internal (helpers for this file and its screens; do not call from scenes): _lc_feed_warn,
#   _lc_feed_unlocked, _lc_feed_mark, _lc_feed_ui, _lc_feed_view_box, lc_feed_reaction_next,
#   _lc_feed_on_phone_closed
#
# Example:
#   init 1 python:
#       lc_feed_register("d2_maya_group_photo", "ch01_d2", "Maya", "maya.in.frame",
#       "Three attempts. Worth it.", likes=38)
#       lc_feed_register("d2_feed_love_shop", "ch01_d2", "Margaret", "islandmart_marg",
#       "Last chocolate muffins, gone.", unlock={"ch01_d2_errand_lane": "love"},
#       reaction="ch01_d2_feed_react_shop")
#   $ lc_phone_set_story_time("14:10")
#   $ lc_feed_install()
#   $ lc_feed_release("d2_maya_group_photo")
#   $ lc_feed_release("d2_feed_love_shop", "d2_feed_exhib_pool")    (one banner for the batch)
#   if lc_feed_seen("d2_maya_group_photo"):        (a later echo or choice option)
#
# Depends on: python-packages/lc_feed.py, systems/phone_presentation_logic.rpy
#   (phone_queue_notification; a banner with kind "feed" deep-links into the app),
#   systems/story_state.rpy (get_story_value for unlock dicts), systems/gallery.rpy
#   (GALLERY_MASK_MATURE_COVERS), screens/phone_feed.rpy (lc_feed_post screen),
#   screens/phone_sweetheart.rpy (home grid, lc_phone_rounded_photo)
# Hooks: listens to phone_closed (lc_phone_close, screens/phone_sweetheart.rpy) to run reactions
# Load order: init 0, so day registrations at init 1 find the registry
# Docs: docs/FEED.md   Tests: tests/test_feed.py

define LC_FEED_APP_NAME = "Instababe"

# The feed list viewport inside phone_screen (screens/phone_sweetheart.rpy): its top inside the
# 1040 px handset, its height, and how much of the next card stays in view when the focus scrolls.
define LC_FEED_VIEW_Y = 164
define LC_FEED_VIEW_H = 820
define LC_FEED_REVEAL_MARGIN = 48

default lc_feed_installed = False
default lc_feed_released = []
default lc_feed_seen_posts = set()
default lc_feed_opened_posts = set()
default lc_feed_stamps = {}
default lc_feed_reacted = set()
default lc_feed_reaction_queue = []

init python:
    import lc_feed

    # Init-time data (never saved): one row per registered post.
    LC_FEED_POSTS = {}

    # Display-only state (never saved, outside rollback): posts that were new on this visit.
    _lc_feed_ui = python_dict(fresh=frozenset())

    def _lc_feed_warn(message):
        """Developer builds fail loudly; release builds only log."""
        text = "[feed] " + message
        if config.developer:
            raise Exception(text)
        try:
            renpy.log(text)
        except Exception:
            pass
        return None

    def lc_feed_register(post_id, day, author, handle, caption, image=None, comments=(), likes=0,
                         when=None, unlock=None, mature=False, reaction=None):
        """Register one post at init (see python-packages/lc_feed.py)."""
        lc_feed.register(LC_FEED_POSTS, post_id, day, author, handle, caption, image=image,
                         comments=comments, likes=likes, when=when, unlock=unlock, mature=mature,
                         reaction=reaction)
        return None

    def lc_feed_install():
        store.lc_feed_installed = True
        return None

    def _lc_feed_unlocked(entry):
        """The post's gate, answered from this save (story values, Leia's recorded choices)."""
        did = getattr(store, "lc_leia_did", None)
        return lc_feed.unlock_ok(entry, get_value=get_story_value,
                                 leia_did=did if callable(did) else None)

    def lc_feed_release(*post_ids, notify=True):
        """Release posts (a batch shows ONE banner). Rebinds the store values, so rollback
        restores them with the story. notify=False: no banner."""
        if len(post_ids) == 1 and isinstance(post_ids[0], (list, tuple)):
            post_ids = tuple(post_ids[0])
        unknown = [pid for pid in post_ids if pid not in LC_FEED_POSTS]
        if unknown:
            _lc_feed_warn("lc_feed_release: unknown post id(s) %r" % (unknown,))
            post_ids = [pid for pid in post_ids if pid in LC_FEED_POSTS]
        released, newly = lc_feed.release(LC_FEED_POSTS, getattr(store, "lc_feed_released", None),
                                          post_ids, _lc_feed_unlocked)
        if not newly:
            return None
        story_time = getattr(store, "lc_phone_story_time", None)
        stamps = dict(getattr(store, "lc_feed_stamps", None) or {})
        for pid in newly:
            when = lc_feed.stamp(LC_FEED_POSTS[pid], story_time)
            if when:
                stamps[pid] = when
        store.lc_feed_released = released
        store.lc_feed_stamps = stamps
        if notify:
            title, body = lc_feed.banner_text([LC_FEED_POSTS[pid] for pid in newly])
            phone_queue_notification(LC_FEED_APP_NAME, lc_feed_text(title), lc_feed_text(body),
                                     kind="feed")
        return None

    def lc_feed_visible():
        return lc_feed.visible(LC_FEED_POSTS, getattr(store, "lc_feed_released", None))

    def lc_feed_entry(post_id):
        return LC_FEED_POSTS.get(post_id)

    def lc_feed_text(text):
        """A post string with [player_name]-style names filled in (render with substitute False)."""
        try:
            return renpy.substitute(text or "")
        except Exception:
            return text or ""

    def lc_feed_avatar(entry):
        """The phone avatar for a known author (gui/phone/sprite_match/avatar_<name>.png), else None
        (the screen then draws an initial tile)."""
        path = "gui/phone/sprite_match/avatar_%s.png" % (entry.get("author") or "").strip().lower()
        return path if renpy.loadable(path) else None

    def lc_feed_when(entry):
        """The time frozen at release; older releases fall back to a fixed `when` string."""
        if not entry:
            return ""
        stamp = (getattr(store, "lc_feed_stamps", None) or {}).get(entry["id"])
        if stamp:
            return stamp
        when = entry.get("when")
        return when if isinstance(when, str) else ""

    def lc_feed_likes(entry):
        return lc_feed.likes_label(entry["likes"])

    def lc_feed_seen(post_id):
        return post_id in (getattr(store, "lc_feed_seen_posts", None) or ())

    def lc_feed_any_seen(*post_ids):
        return lc_feed.any_seen(getattr(store, "lc_feed_seen_posts", None), post_ids)

    def lc_feed_opened(post_id):
        return post_id in (getattr(store, "lc_feed_opened_posts", None) or ())

    def _lc_feed_mark(post_ids):
        """Mark posts seen and queue their first-sight reactions. True when anything changed."""
        seen = getattr(store, "lc_feed_seen_posts", None)
        marked = lc_feed.mark_many(seen, post_ids)
        if marked is seen:
            return False
        newly = [pid for pid in post_ids if pid not in (seen or ())]
        store.lc_feed_seen_posts = marked
        due = lc_feed.reactions_due(LC_FEED_POSTS, newly,
                                    getattr(store, "lc_feed_reacted", None))
        if due:
            store.lc_feed_reacted = set(getattr(store, "lc_feed_reacted", None) or ()) | set(due)
            store.lc_feed_reaction_queue = list(getattr(store, "lc_feed_reaction_queue", None) or ()) + due
        # Kept when the player saves with the phone open.
        renpy.retain_after_load()
        return True

    def lc_feed_visit_start():
        """A new visit to the feed: the blue dots show what is new since the last visit."""
        _lc_feed_ui["fresh"] = frozenset(lc_feed.unseen_ids(
            LC_FEED_POSTS, getattr(store, "lc_feed_released", None),
            getattr(store, "lc_feed_seen_posts", None)))
        return None

    def lc_feed_catch_up():
        """Timer action while the feed list is on screen: every listed post counts as seen (the
        list shows its caption). Returns None."""
        new = lc_feed.unseen_ids(LC_FEED_POSTS, getattr(store, "lc_feed_released", None),
                                 getattr(store, "lc_feed_seen_posts", None))
        if new:
            _lc_feed_ui["fresh"] = frozenset(_lc_feed_ui["fresh"]) | frozenset(new)
            _lc_feed_mark(new)
            renpy.restart_interaction()
        return None

    def lc_feed_is_fresh(post_id):
        return post_id in _lc_feed_ui["fresh"] or not lc_feed_seen(post_id)

    def lc_feed_open_post(post_id):
        """Screen action for a post card. Marks it opened and seen (kept when the player saves on
        the open phone) and shows the post. Never touches stats. Returns None."""
        if post_id not in LC_FEED_POSTS:
            _lc_feed_warn("lc_feed_open_post: unknown post id %r" % (post_id,))
            return None
        _lc_feed_mark((post_id,))
        opened = getattr(store, "lc_feed_opened_posts", None)
        marked = lc_feed.mark_seen(opened, post_id)
        if marked is not opened:
            store.lc_feed_opened_posts = marked
            renpy.retain_after_load()
        renpy.show_screen("lc_feed_post", post_id=post_id)
        renpy.restart_interaction()
        return None

    def _lc_feed_view_box():
        """(top, bottom) of the feed viewport in screen pixels (the handset is centred)."""
        top = (config.screen_height - 1040) // 2 + LC_FEED_VIEW_Y
        return top, top + LC_FEED_VIEW_H

    def lc_feed_reveal_focus(adj):
        """Card `hovered` action: when keyboard or gamepad focus lands on a card that is cut off,
        scroll the feed so the whole card shows (with a peek of the next one, so focus can move
        on). Mouse hover never scrolls. Returns None."""
        if adj is None:
            return None
        try:
            if renpy.display.focus.focus_type == "mouse":
                return None
        except Exception:
            pass
        x, y, w, h = renpy.focus_coordinates()
        if y is None:
            return None
        top, bottom = _lc_feed_view_box()
        delta = lc_feed.reveal_delta(y, h, top, bottom, LC_FEED_REVEAL_MARGIN)
        if delta:
            adj.change(adj.value + delta)
        return None

    def lc_feed_app_visible():
        return lc_feed.app_visible(getattr(store, "lc_feed_installed", False),
                                   getattr(store, "lc_feed_released", None))

    def lc_feed_unseen_count():
        return lc_feed.unseen_count(LC_FEED_POSTS, getattr(store, "lc_feed_released", None),
                                    getattr(store, "lc_feed_seen_posts", None))

    def lc_feed_badge():
        return lc_feed.badge_label(lc_feed_unseen_count())

    def lc_feed_photo(entry, width, height, context="list"):
        image = entry.get("image") if entry else None
        if not (image and renpy.has_image(image, exact=True)):
            return Solid("#E1E7EF", xysize=(width, height))
        if lc_feed.photo_masked(entry, context, GALLERY_MASK_MATURE_COVERS):
            # Gallery rule: a mature cover shows no image until the player opens it.
            cover = AlphaMask(Solid("#2B2F45", xysize=(width, height)),
                              Transform("gui/phone/sweetheart/photo_mask.png", xysize=(width, height)))
            hint = "18+  /  tap to view" if context == "post" else "18+  /  open the post to view"
            return Fixed(cover,
                         Text("MATURE", font="fonts/Handjet-ExtraBold.ttf", size=34,
                              color="#F3C9CF", xalign=0.5, yalign=0.42),
                         Text(hint, style="lc_sw_hand", size=22, color="#EADDE7",
                              xalign=0.5, yalign=0.62),
                         xysize=(width, height))
        return lc_phone_rounded_photo(image, width, height)

    def lc_feed_reaction_next():
        """Pop the next pending reaction. A callable reaction runs here and None comes back; a
        label reaction comes back as its name for lc_feed_reaction_runner to call."""
        queue = list(getattr(store, "lc_feed_reaction_queue", None) or ())
        while queue:
            pid = queue.pop(0)
            store.lc_feed_reaction_queue = queue
            entry = LC_FEED_POSTS.get(pid)
            reaction = entry.get("reaction") if entry else None
            if reaction is None:
                continue
            if callable(reaction):
                reaction()
                return None
            if renpy.has_label(reaction):
                return reaction
            _lc_feed_warn("feed post %r: reaction label %r does not exist" % (pid, reaction))
        store.lc_feed_reaction_queue = queue
        return None

    def _lc_feed_on_phone_closed():
        """phone_closed hook: when Ryan closed the phone with reactions pending, play them now
        as story statements, then return to the line under the phone. Only from a player action
        during a dialogue line or menu (never during story Python, a replay or a menu context)."""
        if not getattr(store, "lc_feed_reaction_queue", None):
            return None
        try:
            ctx = renpy.game.context()
            if not ctx.interacting or renpy.context_nesting_level() or store.main_menu:
                return None
            if getattr(store, "_in_replay", None):
                return None
            node = renpy.game.script.lookup(ctx.current)
            if not isinstance(node, (renpy.ast.Say, renpy.ast.Menu)):
                return None
        except Exception:
            return None
        renpy.call("lc_feed_reaction_runner", from_current=True)

    lc_hook_add("phone_closed", _lc_feed_on_phone_closed)


# Plays every pending first-sight reaction in order (labels are called; callables already ran in
# lc_feed_reaction_next). Started automatically when the phone closes; scenes may call it before
# reading lc_feed_seen to flush anything still pending.
label lc_feed_reaction_runner:
    while lc_feed_reaction_queue:
        $ _lc_feed_target = lc_feed_reaction_next()
        if _lc_feed_target:
            call expression _lc_feed_target
    $ _lc_feed_target = None
    return
