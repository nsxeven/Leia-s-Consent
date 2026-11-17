# Feed screens - the feed list inside the phone and an opened post
#
# Purpose: Draws the social-feed app (systems/feed.rpy) in the sprite-matched phone style: white
#   cards, phone blue, Patrick Hand. lc_feed_list is used inside phone_screen's content viewport
#   when phone_app == "feed" (newest post first, an empty state before any post); the list being
#   on screen marks every post in it seen (phone_screen's catch-up timer), and tapping a card calls
#   lc_feed_open_post, which shows lc_feed_post. Keyboard/gamepad focus scrolls the focused card
#   into view (lc_feed_reveal_focus). A post photo opens the shared full-screen photo viewer.
#   Mature photos show a gallery-style 18+ card (no image) on the list and the opened post.
#
# Public API (call these from scenes/screens):
#   screen lc_feed_list(yadj=None)            feed cards (or the empty state) for phone_screen;
#       yadj = the content viewport's yadjustment
#   screen lc_feed_post(post_id)              one opened post on the handset (zorder 340)
#
# Internal (helpers for this file and its screens; do not call from scenes): lc_feed_author_row
#
# Example:
#   elif phone_app == "feed":
#       use lc_feed_list(feed_yadj)
#
# Depends on: systems/feed.rpy, screens/phone_sweetheart.rpy (lc_phone_backdrop,
#   lc_phone_body_blocker, lc_phone_back, lc_phone_close, lc_phone_photo_viewer, styles)
# Hooks: none
# Load order: init 0 (screens only)
# Docs: docs/FEED.md   Tests: tests/test_feed.py

# Avatar (or an initial tile), author, @handle and time of a post.
screen lc_feed_author_row(entry):
    $ _avatar = lc_feed_avatar(entry)
    $ _author = lc_feed_text(entry["author"])
    hbox:
        spacing 12
        if _avatar:
            add _avatar xysize (52, 52) yalign 0.5
        else:
            frame:
                style "lc_sw_frame"
                xysize (52, 52)
                yalign 0.5
                background Frame("gui/phone/sprite_match/key.png", 18, 18)
                text (_author[:1].upper() or "?"):
                    style "lc_sw_hand"
                    size 28
                    color "#FFFFFF"
                    xalign 0.5
                    yalign 0.5
                    substitute False
        vbox:
            yalign 0.5
            text _author:
                style "lc_sw_hand"
                size 26
                color "#293C53"
                substitute False
            $ _when = lc_feed_when(entry)
            $ _meta = "@" + lc_feed_text(entry["handle"]) + (("  -  " + _when) if _when else "")
            text _meta:
                style "lc_sw_hand"
                size 20
                color "#6E8399"
                substitute False


screen lc_feed_list(yadj=None):
    $ _posts = lc_feed_visible()
    if not _posts:
        frame:
            style "lc_sw_frame"
            xfill True
            background Frame("gui/phone/sprite_match/card.png", 18, 18)
            padding (20, 28)
            vbox:
                spacing 10
                xfill True
                add Transform("gui/phone/sprite_match/feed.png", nearest=True) xalign 0.5 xysize (72, 72)
                text "No posts yet":
                    style "lc_sw_hand"
                    size 28
                    color "#293C53"
                    xalign 0.5
                    text_align 0.5
                text "Posts from people you follow show up here.":
                    style "lc_sw_hand"
                    size 26
                    color "#6E8399"
                    xalign 0.5
                    text_align 0.5
                    xmaximum 420
    for _entry in _posts:
        $ _pid = _entry["id"]
        $ _new = lc_feed_is_fresh(_pid)
        $ _ncom = len(_entry["comments"])
        $ _footer = lc_feed_likes(_entry) + (("  -  %d comment%s" % (_ncom, "" if _ncom == 1 else "s")) if _ncom else "")
        button:
            style "lc_sw_hit"
            xfill True
            padding (14, 12, 14, 14)
            background Frame("gui/phone/sprite_match/card.png", 18, 18)
            hover_background Frame("gui/phone/sprite_match/row_hover.png", 18, 18)
            hovered Function(lc_feed_reveal_focus, yadj)
            action [Function(lc_ui_play, "app_tap"), Function(lc_feed_open_post, _pid)]
            vbox:
                spacing 10
                xsize (LC_PHONE_CONTENT_WIDTH - 28)
                fixed:
                    xfill True
                    ysize 56
                    use lc_feed_author_row(_entry)
                    if _new:
                        add "gui/phone/sprite_match/dot.png" xalign 1.0 yalign 0.5
                if _entry["image"]:
                    add lc_feed_photo(_entry, LC_PHONE_CONTENT_WIDTH - 28, 240, "list")
                text lc_phone_one_line(lc_feed_text(_entry["caption"]), 140):
                    style "lc_sw_hand"
                    size 24
                    color "#293C53"
                    xmaximum (LC_PHONE_CONTENT_WIDTH - 28)
                    substitute False
                text _footer:
                    style "lc_sw_hand"
                    size 20
                    color "#3D8FD4"
                if current_choice_mode() == "developer":
                    text "Post: [_pid]":
                        style "lc_sw_hand"
                        size 18
                        color "#6E8399"


screen lc_feed_post(post_id):
    modal True
    zorder 340
    key "K_ESCAPE" action Function(lc_phone_back)
    key "game_menu" action Function(lc_phone_back)

    $ _entry = lc_feed_entry(post_id)

    use lc_phone_backdrop(Function(lc_phone_close))
    fixed:
        xalign 0.5
        yalign 0.5
        xysize (540, 1040)
        use lc_phone_body_blocker
        add "gui/phone/sprite_match/phone_app.png"
        text "[lc_phone_clock_text()]":
            style "lc_sw_pixel_bold"
            size 22
            color "#303B51"
            xpos 40
            ypos 16
        button:
            style "lc_sw_hit"
            xpos 28
            ypos 92
            xysize (56, 56)
            action Function(lc_phone_back)
            add "gui/phone/sprite_match/chevron.png" xalign 0.5 yalign 0.5
        text LC_FEED_APP_NAME:
            style "lc_sw_hand"
            size 36
            color "#293C53"
            xpos 76
            ypos 98
        if _entry:
            # No focusable cards here: the arrow and page keys scroll a long post (and move
            # focus once it reaches either end).
            viewport:
                ypos 164
                xpos LC_PHONE_CONTENT_LEFT
                xsize LC_PHONE_VIEWPORT_WIDTH
                ysize 820
                mousewheel True
                draggable True
                arrowkeys True
                pagekeys True
                scrollbars None
                vbox:
                    xsize LC_PHONE_CONTENT_WIDTH
                    spacing 14
                    use lc_feed_author_row(_entry)
                    if _entry["image"]:
                        if renpy.has_image(_entry["image"], exact=True):
                            button:
                                style "lc_sw_hit"
                                xfill True
                                ysize LC_PHONE_CONTENT_WIDTH
                                action [Function(lc_ui_play, "app_tap"), Show("lc_phone_photo_viewer", photo_asset=_entry["image"])]
                                add lc_feed_photo(_entry, LC_PHONE_CONTENT_WIDTH, LC_PHONE_CONTENT_WIDTH, "post")
                            if _entry["mature"] and not GALLERY_MASK_MATURE_COVERS:
                                text "18+  -  tap the photo to view it full screen.":
                                    style "lc_sw_hand"
                                    size 20
                                    color "#6E8399"
                        else:
                            add lc_feed_photo(_entry, LC_PHONE_CONTENT_WIDTH, LC_PHONE_CONTENT_WIDTH, "post")
                    frame:
                        style "lc_sw_frame"
                        xfill True
                        background Frame("gui/phone/sprite_match/card.png", 18, 18)
                        padding (16, 14)
                        vbox:
                            spacing 10
                            text lc_feed_text(_entry["caption"]):
                                style "lc_sw_hand"
                                size 26
                                color "#293C53"
                                xmaximum (LC_PHONE_CONTENT_WIDTH - 32)
                                substitute False
                            text lc_feed_likes(_entry):
                                style "lc_sw_hand"
                                size 22
                                color "#3D8FD4"
                    if _entry["comments"]:
                        frame:
                            style "lc_sw_frame"
                            xfill True
                            background Frame("gui/phone/sprite_match/card.png", 18, 18)
                            padding (16, 14)
                            vbox:
                                spacing 10
                                for _handle, _comment in _entry["comments"]:
                                    vbox:
                                        spacing 0
                                        text lc_feed_text(_handle):
                                            style "lc_sw_hand"
                                            size 22
                                            color "#3D8FD4"
                                            substitute False
                                        text lc_feed_text(_comment):
                                            style "lc_sw_hand"
                                            size 24
                                            color "#293C53"
                                            xmaximum (LC_PHONE_CONTENT_WIDTH - 32)
                                            substitute False
                    null height 28
