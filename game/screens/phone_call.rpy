# Phone call screen - the incoming-call moment, and reply delivery in one-to-one chats
#
# Purpose: screen phone_call is the incoming call: the handset (home art or the player's
#   wallpaper) dimmed, the caller's avatar with a soft ripple, their name, and two phone
#   buttons, Let it ring / Answer. It returns 'ignored' or 'answered' to phone_call_offer
#   (systems/phone_moments.rpy), which stores it. Reduced motion or skip mode draws the ripple
#   still. The lc_phone_moments_overlay posts staged reply steps while a one-to-one chat is open
#   (the Trip Group keeps its Chapter 1 cadence in chapters/ch01/day1/ch01_phone_moments.rpy) and
#   posts Ryan's hesitating reply in any chat once its typing ends.
#
# Public API (call these from scenes/screens):
#   screen phone_call(caller_id)              the incoming call; returns 'answered' / 'ignored'
#       (shown by phone_call_offer; never call it directly from a scene)
#   screen lc_phone_moments_overlay()         overlay: open-chat reply delivery (registered here)
#   lc_phone_open_thread()                    the chat thread the phone shows now, or None
#   transform lc_phone_call_ripple(delay=0.0)
#       the expanding ring behind the caller's avatar
#   LC_PHONE_CALL_CADENCE                     (Ryan's beat, a reply beat) seconds in 1:1 chats
#
# Example:
#   $ outcome = phone_call_offer("maya", "ch01_d2_call_maya")    (systems/phone_moments.rpy)
#
# Depends on: systems/phone_moments.rpy, systems/phone_presentation_logic.rpy,
#   screens/phone_sweetheart.rpy (styles, lc_phone_avatar, lc_phone_backdrop, clock),
#   screens/phone_wallpaper.rpy (wallpaper layers, LC_WP_MASK), systems/phone_group_avatar.rpy
# Hooks: none (registers the lc_phone_moments_overlay overlay)
# Load order: default (init 0); the overlay registers after the Chapter 1 phone overlay's
#   init 998, so it is drawn above it (it draws nothing; it only runs timers)
# Docs: docs/PHONE_MOMENTS.md   Tests: tests/test_phone_moments.py

init 999 python:
    # load order: init 999, after ch01_phone_sequence_overlay (init 998), so the existing
    # overlay order stays as it was and this one is appended last.
    if "lc_phone_moments_overlay" not in config.overlay_screens:
        config.overlay_screens.append("lc_phone_moments_overlay")

init python:
    LC_PHONE_CALL_CADENCE = (0.45, 0.9)

    def lc_phone_open_thread():
        screen = renpy.get_screen("phone_screen")
        if screen is None:
            return None
        scope = getattr(screen, "scope", None) or {}
        if scope.get("phone_app") != "thread":
            return None
        return scope.get("phone_thread")


transform lc_phone_call_ripple(delay=0.0):
    alpha 0.0
    zoom 1.0
    pause delay
    block:
        alpha 0.42
        zoom 1.0
        easeout 1.7 alpha 0.0 zoom 1.55
        pause 0.1
        repeat


screen phone_call(caller_id):
    modal True
    zorder 330

    on "show" action Function(lc_phone_call_ring)

    $ _still = lc_phone_motion_instant()
    $ _caller_art = phone_group_avatar() if caller_id == "group" else lc_phone_avatar(caller_id)

    use lc_phone_backdrop(NullAction())
    fixed:
        xalign 0.5
        yalign 0.5
        xysize (540, 1040)
        use lc_phone_body_blocker
        $ _wallpaper = lc_phone_wallpaper()
        if _wallpaper:
            use lc_phone_wallpaper_layers(_wallpaper)
        else:
            add "gui/phone/sprite_match/phone_home.png"
        add AlphaMask(Solid("#0b1626e8", xysize=(LC_WP_W, LC_WP_H)), LC_WP_MASK):
            xpos LC_WP_X
            ypos LC_WP_Y
        text "[lc_phone_clock_text()]":
            style "lc_sw_pixel_bold"
            size 22
            color "#FFFFFF"
            xpos 40
            ypos 16
        text "Incoming call":
            style "lc_sw_hand"
            size 30
            color "#BFD3EA"
            xalign 0.5
            ypos 176
        fixed:
            xysize (320, 320)
            xalign 0.5
            ypos 236
            if _still:
                add Transform("gui/phone/sprite_match/avatar_system.png", xysize=(236, 236), matrixcolor=ColorizeMatrix("#7FB4E6", "#7FB4E6")):
                    align (0.5, 0.5)
                    alpha 0.28
            else:
                for _ring in range(2):
                    add Transform("gui/phone/sprite_match/avatar_system.png", xysize=(200, 200), matrixcolor=ColorizeMatrix("#7FB4E6", "#7FB4E6")):
                        align (0.5, 0.5)
                        at lc_phone_call_ripple(_ring * 0.9)
            add _caller_art:
                xysize (200, 200)
                align (0.5, 0.5)
        text phone_thread_label(caller_id):
            style "lc_sw_hand"
            size 54
            color "#FFFFFF"
            xalign 0.5
            ypos 580
            xmaximum 460
            text_align 0.5
        text "mobile":
            style "lc_sw_hand"
            size 26
            color "#8FA6C0"
            xalign 0.5
            ypos 650
        # The two buttons sit in the handset's dock tray.
        hbox:
            xalign 0.5
            ypos 920
            spacing 28
            textbutton "Let it ring":
                style "lc_phone_btn"
                xfill False
                xsize 196
                action Return("ignored")
            textbutton "Answer":
                style "lc_phone_btn_primary"
                xfill False
                xsize 196
                action Return("answered")


# Posts staged reply steps while a one-to-one chat is open (the Trip Group keeps its own
# cadence in ch01_phone_sequence_overlay), and Ryan's hesitating reply in any chat once its
# typing has played. Draws nothing.
screen lc_phone_moments_overlay():
    zorder 321
    $ _lc_pm_thread = lc_phone_open_thread()
    if _lc_pm_thread:
        $ _lc_pm_steps = (phone_reply_delivery or {}).get(_lc_pm_thread) or ()
        $ _lc_pm_typing = phone_reply_typing_active(_lc_pm_thread)
        if _lc_pm_steps and phone_reply_typing_text(_lc_pm_thread) is None:
            $ _lc_pm_player = _lc_pm_steps[0][0] == "player"
            if _lc_pm_thread != "group" or (_lc_pm_typing and _lc_pm_player):
                timer (LC_PHONE_CALL_CADENCE[0] if _lc_pm_player else LC_PHONE_CALL_CADENCE[1]) repeat True action Function(phone_deliver_reply_step, _lc_pm_thread)
