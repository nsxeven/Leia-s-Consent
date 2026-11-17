# Feed - the parody social-feed phone app (placeholder name LC_FEED_APP_NAME)
#
# Purpose: Story code registers feed posts at init and releases each one where it should appear;
#   the app joins the phone home grid once the story installs it (Maya's intro on the Day Two
#   photo walk) or any post is out. New posts badge the app icon; the first post of each day
#   also shows a phone banner that opens the feed. Opening a post writes a save-local seen
#   record that later scenes may read. Reading the feed never changes stats or story state.
#   Rules live in python-packages/lc_feed.py; this file binds them to the store.
#
# Public API (call these from scenes/screens):
#   lc_feed_register(post_id, day, author, handle, caption, image=None, comments=(), likes=0, when=None, unlock=None, mature=False) -> None
#       register one post at init 1+ (comments: up to 3 (handle, text) pairs; unlock: None or a
#       zero-argument callable checked once at release; mature=True blurs the photo outside the
#       full-screen viewer); a duplicate id raises
#   lc_feed_install() -> None                 put the app on Ryan's home grid (no post needed)
#   lc_feed_release(post_id, notify=True) -> None
#       make a post appear (unread badge; a banner for the day's first post when notify); a post
#       whose unlock condition is False now, or that is already out, changes nothing
#   lc_feed_visible()                         released posts, newest first (entries)
#   lc_feed_entry(post_id)                    the registered entry, or None
#   lc_feed_text(text)                        a post string with typed names filled in
#   lc_feed_avatar(entry)                     a known author's phone avatar path, or None
#   lc_feed_seen(post_id)                     True once this save opened the post
#   lc_feed_any_seen(*post_ids)               True when any of them was opened
#   lc_feed_open_post(post_id) -> None        screen action: mark seen, show screen lc_feed_post
#   lc_feed_app_visible()                     True when the app is on the home grid
#   lc_feed_unseen_count()                    released posts not opened yet
#   lc_feed_badge()                           icon badge text, or None
#   lc_feed_photo(entry, width, height, context="list")
#       the post photo fitted to a box; mature photos blurred with an 18+ mark except in the
#       "viewer" context
#   define LC_FEED_APP_NAME                   the app's display name (one-line rename)
#   LC_FEED_POSTS                             the registry {post_id: entry} (init-time data)
#   default lc_feed_installed                 save state: the app is on the phone
#   default lc_feed_released                  save state: post ids in release order
#   default lc_feed_seen_posts                save state: opened post ids
#   default lc_feed_banner_days               save state: days that already showed a banner
#
# Internal (helpers for this file and its screens; do not call from scenes): _lc_feed_warn
#
# Example:
#   init 1 python:
#       lc_feed_register("d2_maya_group_photo", "ch01_d2", "Maya", "maya.in.frame",
#                        "Three attempts. Worth it.", likes=38)
#   $ lc_feed_install()
#   $ lc_feed_release("d2_maya_group_photo")
#   if lc_feed_seen("d2_maya_group_photo"):        (a later echo or choice option)
#
# Depends on: python-packages/lc_feed.py, systems/phone_presentation_logic.rpy
#   (phone_queue_notification; a banner with kind "feed" deep-links into the app),
#   screens/phone_feed.rpy (lc_feed_post screen), screens/phone_sweetheart.rpy (home grid)
# Hooks: none
# Load order: init 0, so day registrations at init 1 find the registry
# Docs: docs/FEED.md   Tests: tests/test_feed.py

define LC_FEED_APP_NAME = "Instababe"

default lc_feed_installed = False
default lc_feed_released = []
default lc_feed_seen_posts = set()
default lc_feed_banner_days = set()

init python:
    import lc_feed

    # Init-time data (never saved): one row per registered post.
    LC_FEED_POSTS = {}

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
                         when=None, unlock=None, mature=False):
        """Register one post at init (see python-packages/lc_feed.py)."""
        lc_feed.register(LC_FEED_POSTS, post_id, day, author, handle, caption, image=image,
                         comments=comments, likes=likes, when=when, unlock=unlock, mature=mature)
        return None

    def lc_feed_install():
        store.lc_feed_installed = True
        return None

    def lc_feed_release(post_id, notify=True):
        """Release a post. Rebinds the store lists (rollback restores them with the story)."""
        if post_id not in LC_FEED_POSTS:
            _lc_feed_warn("lc_feed_release: unknown post id %r" % (post_id,))
            return None
        released, days, banner = lc_feed.release(
            LC_FEED_POSTS, getattr(store, "lc_feed_released", None),
            getattr(store, "lc_feed_banner_days", None), post_id)
        if released is getattr(store, "lc_feed_released", None):
            return None
        store.lc_feed_released = released
        store.lc_feed_banner_days = days
        if banner and notify:
            entry = LC_FEED_POSTS[post_id]
            phone_queue_notification(LC_FEED_APP_NAME, lc_feed_text(entry["author"]),
                                     lc_feed_text(entry["caption"]), kind="feed")
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

    def lc_feed_seen(post_id):
        return post_id in (getattr(store, "lc_feed_seen_posts", None) or ())

    def lc_feed_any_seen(*post_ids):
        return lc_feed.any_seen(getattr(store, "lc_feed_seen_posts", None), post_ids)

    def lc_feed_open_post(post_id):
        """Screen action for a post card. Marks it seen (kept when the player saves on the open
        phone) and shows the post. Never touches stats. Returns None."""
        if post_id not in LC_FEED_POSTS:
            _lc_feed_warn("lc_feed_open_post: unknown post id %r" % (post_id,))
            return None
        seen = getattr(store, "lc_feed_seen_posts", None)
        marked = lc_feed.mark_seen(seen, post_id)
        if marked is not seen:
            store.lc_feed_seen_posts = marked
            renpy.retain_after_load()
        renpy.show_screen("lc_feed_post", post_id=post_id)
        renpy.restart_interaction()
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
        art = lc_phone_rounded_photo(image, width, height)
        if lc_feed.photo_masked(entry, context):
            mark = Text("18+", font="fonts/Handjet-ExtraBold.ttf", size=26, color="#FFFFFF",
                        outlines=[(2, "#14243D", 0, 0)], xalign=0.96, yalign=0.06)
            return Fixed(Transform(art, blur=14), mark, xysize=(width, height))
        return art
