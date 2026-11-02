# Headless Sweetheart phone screenshots. Runs only when LC_PHONE_SHOTS=1.
# Not part of the story. splashscreen jumps here before the main menu.

init -999 python:
    import os as _lc_phone_os
    if _lc_phone_os.environ.get("LC_PHONE_SHOTS") == "1":
        config.gl_vsync = False

label lc_phone_shot_tour:
    $ import os
    $ _shot_dir = os.environ.get("LC_PHONE_SHOT_DIR", "/tmp/lc_phone_shots")
    $ os.makedirs(_shot_dir, exist_ok=True)
    $ lc_ui_shooting = True
    $ preferences.fullscreen = True
    $ preferences.physical_size = (1920, 1080)
    $ persistent.phone_tutorial_seen = True
    $ phone_unlocked = True
    $ phone_hud_enabled = True
    $ quick_menu = True
    # splashscreen dynamically suppresses overlays. This tour is jumped to
    # from splashscreen, so turn them back on or the phone button never draws.
    $ suppress_overlay = False
    $ lc_dialogue_theme = "day"
    $ lc_phone_hearts = True
    $ story_flags["ch01_started"] = True
    pause 0.4

    python:
        def _lc_phone_snap(name):
            try:
                renpy.game.interface.set_mouse_pos(4, 4, 0)
            except Exception:
                pass
            path = os.path.join(store._shot_dir, name + ".png")
            renpy.screenshot(path)
            store.lc_phone_shots.append(path)
            renpy.hide_screen("lc_shot_helper")

        def _lc_phone_shot(name):
            with open("/tmp/shot_trace.txt", "a") as handle:
                handle.write("shot " + name + "\n")
            renpy.hide_screen("lc_shot_helper")
            renpy.show_screen("lc_shot_helper", name)
            # modal=False so the pause ends while the phone screen is up.
            renpy.pause(0.75, hard=True, modal=False)

        def _lc_open_phone(app, thread=None):
            renpy.hide_screen("phone_screen")
            renpy.hide_screen("lc_phone_status")
            renpy.hide_screen("lc_phone_settings")
            renpy.hide_screen("lc_phone_photo_viewer")
            store.lc_phone_deep_link = (app, thread)
            renpy.show_screen("phone_screen")
            renpy.restart_interaction()

        store.lc_phone_shots = []
        # The helper screen lives in the scrapbook UI file and just takes the shot.
        store._lc_snap = _lc_phone_snap

    # Reuse the scrapbook helper, which calls _lc_snap. Point it at our saver.
    python:
        def _lc_snap(name):
            _lc_phone_snap(name)
        store._lc_snap = _lc_snap

    scene bg ch01_pool_day
    $ set_dialogue_theme("day")
    if os.environ.get("LC_PHONE_ONLY") == "home":
        $ _lc_open_phone("home")
        $ _lc_phone_shot("01_home")
        $ renpy.quit()
    if os.environ.get("LC_PHONE_ONLY") == "button":
        show screen say(who="Leia", what="Wait... is that my phone or yours?")
        show screen lc_shot_helper("13_button_idle")
        pause 0.8
        $ renpy.quit()
    show screen say(who="Leia", what="Wait... is that my phone or yours?")
    $ _lc_phone_shot("13_button_idle")

    python:
        with open("/tmp/shot_trace.txt", "a") as handle:
            handle.write("seeding messages\n")
        phone_messages["leia"] = []
        phone_messages["julian"] = []
        phone_messages["maya"] = []
        phone_messages["group"] = []
        phone_photos[:] = []
        phone_add_message("group", "julian", "I'm downstairs.", message_id="shot_j1", mark_unread=True, notify=False)
        phone_add_message("group", "julian", "If either of you makes us miss this flight I am leaving without you.", message_id="shot_j2", mark_unread=True, notify=False)
        phone_add_message("group", "leia", "Two minutes! I can't find my sunglasses.", message_id="shot_l1", mark_unread=True, notify=False)
        phone_add_message("group", "player", text="They're on your head.", message_id="shot_p1", attachment_id="bg ch01_pool_day", attachment_label="Pool", mark_unread=False, notify=False)
        phone_add_message("group", "leia", "...I knew that.", message_id="shot_l2", mark_unread=True, notify=False)
        phone_add_message("group", "maya", "Taxi's here. Julian is timing us.", message_id="shot_m1", mark_unread=True, notify=False)
        phone_add_message("leia", "leia", "...I knew that.", message_id="shot_leia_dm", mark_unread=True, notify=False)
        phone_add_message("julian", "julian", "Advice is billable. I charge by the hour.", message_id="shot_julian_dm", mark_unread=True, notify=False)
        phone_add_photo("shot_pool", "bg ch01_pool_day", "Pool, this morning")
        store.phone_notification_current = {
            "app": "Messages",
            "title": "Trip Group",
            "body": "If either of you makes us miss this flight I am leaving without you.",
            "kind": "message",
            "thread_id": "group",
            "sender": "Julian",
        }
        renpy.show_screen("phone_notification_banner")
    $ _lc_phone_shot("12_notification")
    $ phone_notification_current = None
    hide screen phone_notification_banner

    $ _lc_phone_shot("14_button_badge")
    hide screen say

    $ _lc_open_phone("home")
    $ _lc_phone_shot("01_home")

    $ _lc_open_phone("messages")
    $ _lc_phone_shot("02_messages")

    python:
        phone_mark_thread_read("group")
        _lc_open_phone("thread", "group")
    $ _lc_phone_shot("03_thread_day")

    $ _lc_open_phone("photos")
    $ _lc_phone_shot("05_photos")

    show screen lc_phone_photo_viewer(photo_asset="bg ch01_pool_day")
    $ _lc_phone_shot("06_photo_viewer")
    hide screen lc_phone_photo_viewer

    python:
        store.money = 9000
        for _oid in shop_outfit_ids():
            OUTFIT_DEFINITIONS[_oid]["cost"] = 1250
            break
    $ _lc_open_phone("shop")
    $ _lc_phone_shot("09_shop")

    $ _lc_open_phone("wallet")
    $ _lc_phone_shot("10_wallet")

    $ _lc_open_phone("delivery")
    $ _lc_phone_shot("11_delivery")

    hide screen phone_screen
    show screen lc_phone_status
    $ _lc_phone_shot("07_status")
    hide screen lc_phone_status

    show screen lc_phone_settings
    $ _lc_phone_shot("08_settings")
    hide screen lc_phone_settings

    $ lc_dialogue_theme = "night"
    scene bg ch01_villa_living_night
    $ _lc_open_phone("thread", "group")
    $ _lc_phone_shot("04_thread_night")
    hide screen phone_screen

    show screen say(who="Leia", what="Okay this one's actually good.")
    $ _lc_phone_shot("15_button_night")
    hide screen say

    python:
        with open(os.path.join(store._shot_dir, "manifest.txt"), "w") as handle:
            handle.write("\n".join(store.lc_phone_shots))
    $ renpy.quit()
    return
