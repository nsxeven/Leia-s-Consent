# ACTIVE PHONE PRESENTATION — Sweetheart.
# Late-loading phone_screen. Story still reads phone_app and phone_thread.
# Pixel art is pre-scaled 3x (nearest). Patrick Hand stays smooth at 1080p.
# The scrapbook case overlay must not draw on top of this (see the hardware file).

default lc_phone_hearts = True


init 95 python:
    import datetime

    def lc_phone_clock_text():
        return datetime.datetime.now().strftime("%H:%M")

    def lc_phone_theme():
        theme = getattr(store, "lc_dialogue_theme", "day")
        return theme if theme in ("day", "night") else "day"

    def lc_phone_palette(theme=None):
        theme = theme or lc_phone_theme()
        if theme == "night":
            return {
                "bg": "#251722",
                "nav": "#301e2c",
                "line": "#4a2c40",
                "inc": "#40293a",
                "out": "#a8305e",
                "out_t": "#faf4e8",
                "acc": "#f08ab0",
                "mut": "#b58a9e",
                "txt": "#f3e2ea",
                "stamp": "#93708a",
                "track": "#4a2c40",
                "bar": "#a8305e",
            }
        return {
            "bg": "#f8e7e5",
            "nav": "#fdf3ef",
            "line": "#e9c6c8",
            "inc": "#fffbf5",
            "out": "#a8305e",
            "out_t": "#faf4e8",
            "acc": "#a8305e",
            "mut": "#8a5f69",
            "txt": "#4a2633",
            "stamp": "#9a7078",
            "track": "#e9c6c8",
            "bar": "#a8305e",
        }

    def lc_phone_name_color(sender, theme=None):
        theme = theme or lc_phone_theme()
        day = {
            "leia": "#b8325e",
            "julian": "#4f7a2a",
            "maya": "#94680e",
            "player": "#a8305e",
            "ryan": "#a8305e",
        }
        night = {
            "leia": "#f39ab8",
            "julian": "#a9cf7a",
            "maya": "#e9c46a",
            "player": "#f08ab0",
            "ryan": "#f08ab0",
        }
        table = night if theme == "night" else day
        return table.get(sender, lc_phone_palette(theme)["txt"])

    def lc_phone_avatar_ink(sender):
        return {
            "leia": "#6a2338",
            "julian": "#3e5a2a",
            "maya": "#6a4a14",
            "player": "#2f4a52",
            "ryan": "#2f4a52",
        }.get(sender, "#4a2633")

    def lc_phone_avatar(sender):
        who = sender if sender in ("leia", "julian", "maya", "ryan", "group") else "system"
        if sender == "player":
            who = "ryan"
        return "gui/phone/sprite_match/avatar_%s.png" % who

    def lc_phone_initial(sender):
        label = phone_sender_label(sender) or "?"
        return label[:1].upper()

    def lc_phone_art(name):
        return "gui/phone/sweetheart/%s.png" % name

    def lc_phone_one_line(text, limit=36):
        clean = " ".join((text or "").split())
        if len(clean) <= limit:
            return clean
        return clean[: max(1, limit - 3)].rstrip() + "..."

    def lc_phone_price(amount):
        """Dollar label with a thousands separator, so $1250 reads as $1,250."""
        try:
            value = int(amount)
        except Exception:
            return "${}".format(amount)
        return "${:,}".format(value)

    def lc_phone_home_caption():
        raw = lc_day_caption()
        parts = [part for part in raw.split("  ") if part]
        if len(parts) == 2 and parts[1] == "DAY":
            return parts[0]
        if len(parts) == 2:
            return parts[0] + "  -  " + parts[1]
        return raw

    def lc_phone_list_preview(thread_id):
        thread = phone_messages_for_thread(thread_id)
        preview = phone_thread_preview(thread_id)
        if not thread:
            return preview
        sender = thread[-1].get("sender")
        if thread_id == "group" and sender:
            who = "You" if sender == "player" else phone_sender_label(sender)
            return who + ": " + preview
        return preview

    def lc_phone_thread_rows(thread_id):
        if not thread_id:
            return []
        messages = phone_messages_for_thread(thread_id)
        rows = []
        for index, message in enumerate(messages):
            sender = message.get("sender") or "system"
            prev_sender = messages[index - 1].get("sender") if index else None
            next_sender = messages[index + 1].get("sender") if index + 1 < len(messages) else None
            outgoing = sender == "player"
            rows.append({
                "message": message,
                "sender": sender,
                "outgoing": outgoing,
                "show_name": (not outgoing) and sender != prev_sender,
                "tail": sender != next_sender,
            })
        return rows

    # Chat threads stick to the newest message (darryn, 2026-11-04): a thread
    # opens at the bottom, and when a staged reply lands while it is open the
    # view slides down to it, like a real messaging app. Used by every thread.
    # Handset art has a 540px canvas; the flat inner screen is x=17..523.
    # Keep every list, avatar, attachment and card inside this centered lane.
    LC_PHONE_SCREEN_LEFT = 17
    LC_PHONE_SCREEN_RIGHT = 523
    LC_PHONE_CONTENT_LEFT = 42
    LC_PHONE_CONTENT_WIDTH = 456
    LC_PHONE_VIEWPORT_WIDTH = 456
    LC_PHONE_SCROLL_SECONDS = 0.35

    def lc_phone_thread_ranged(adj):
        # Called by Ren'Py whenever the thread's scrollable height changes.
        target = adj.range
        if not getattr(adj, "_lc_opened", False):
            adj._lc_opened = True
            adj.change(target)
            return
        amount = target - adj.value
        if amount > 0:
            adj.animate(amount, LC_PHONE_SCROLL_SECONDS, renpy.atl.warpers["easeout"])
        else:
            adj.change(target)

    def lc_phone_thread_adjustment():
        return ui.adjustment(ranged=lc_phone_thread_ranged)

    def lc_phone_rounded_photo(asset_id, width, height):
        photo = Transform(asset_id, xysize=(width, height), fit="cover")
        mask = Transform("gui/phone/sweetheart/photo_mask.png", xysize=(width, height))
        return AlphaMask(photo, mask)


    # Real apps only. Camera, notes, maps, music, browser, calendar and a calls
    # handset have no screen, so they are not drawn. Handjet is only the status
    # time (size 22) and the home clock (size 70); LC_HANDJET_SCALE is 1.3.
    # Every other phone string uses Patrick Hand.
    LC_SM_HOME = (
        ("messages", "Messages", "app"),
        ("photos", "Photos", "app"),
        ("settings", "Settings", "settings"),
        ("status", "Status", "status"),
        ("delivery", "Delivery", "app"),
        ("shop", "Shop", "app"),
        ("wallet", "Wallet", "app"),
    )
    LC_SM_DOCK = ("messages", "photos", "shop", "wallet")


    def lc_sm_app_badge(app_id):
        if app_id == "messages":
            count = phone_total_unread()
            if count:
                return phone_unread_badge_label(count)
            return None
        if app_id == "status" and not getattr(renpy.store.persistent, "status_page_intro_seen", False):
            return "!"
        return None


style lc_sw_pixel is default:
    font "fonts/Handjet-SemiBold.ttf"
    size 24
    antialias True
    hinting "bytecode"
    adjust_spacing False
    color "#4a2633"

style lc_sw_pixel_bold is lc_sw_pixel:
    font "fonts/Handjet-ExtraBold.ttf"

style lc_sw_hand is default:
    font "fonts/PatrickHand-Regular.ttf"
    size 33
    color "#4a2633"
    adjust_spacing False

style lc_sw_hit is button:
    background None
    hover_background None
    padding (0, 0)
    xpadding 0
    ypadding 0
    xminimum 0
    yminimum 0

style lc_sw_frame is frame:
    background None
    padding (0, 0)
    xpadding 0
    ypadding 0
    yminimum 0


screen lc_phone_extra_apps():
    # Older builds drew a second Status/Settings row on top of the phone.
    # Those apps are on the home grid now, so this overlay stays empty.
    pass


screen lc_phone_photo_viewer(photo_asset):
    modal True
    zorder 380

    key "K_ESCAPE" action Hide("lc_phone_photo_viewer")
    key "mouseup_3" action Hide("lc_phone_photo_viewer")

    add Solid("#12080e")

    if photo_asset and renpy.has_image(photo_asset):
        add photo_asset:
            xalign 0.5
            yalign 0.5
            fit "contain"
            xysize (1760, 960)

    button:
        style "lc_sw_hit"
        xfill True
        yfill True
        action Hide("lc_phone_photo_viewer")

    button:
        style "lc_sw_hit"
        xpos 1680
        ypos 36
        xminimum 150
        ysize 54
        background Frame("gui/phone/sprite_match/key.png", 18, 18)
        hover_background Frame("gui/phone/sprite_match/key.png", 18, 18)
        action Hide("lc_phone_photo_viewer")
        text "Done":
            style "lc_sw_hand"
            size 28
            color "#FFFFFF"
            xalign 0.5
            yalign 0.5


screen lc_phone_backdrop(close_action):
    button:
        style "lc_sw_hit"
        xfill True
        yfill True
        keyboard_focus False
        background Solid("#071225c4")
        hover_background Solid("#071225c4")
        action close_action


screen lc_phone_body_blocker():
    button:
        style "lc_sw_hit"
        xysize (540, 1040)
        keyboard_focus False
        action NullAction()


screen phone_screen():
    modal True
    zorder 310

    default phone_app = lc_phone_link_app()
    default phone_thread = lc_phone_link_thread()
    default thread_adjs = {}

    on "show" action [SetVariable("lc_phone_deep_link", None), Function(lc_ui_play, "phone_open")]
    on "hide" action Function(lc_ui_play, "phone_close")
    on "replace" action SetVariable("lc_phone_deep_link", None)

    key "K_ESCAPE" action Hide("phone_screen")

    use lc_phone_backdrop(Hide("phone_screen"))

    fixed:
        xalign 0.5
        yalign 0.5
        xysize (540, 1040)
        use lc_phone_body_blocker

        if phone_app == "home":
            add "gui/phone/sprite_match/phone_home.png"
            text "[lc_phone_clock_text()]":
                style "lc_sw_pixel_bold"
                size 22
                color "#FFFFFF"
                xpos 40
                ypos 16
                outlines [(2, "#102033", 0, 1)]
            text "[lc_phone_home_caption()]":
                style "lc_sw_hand"
                size 26
                color "#FFFFFF"
                xalign 0.5
                ypos 96
                xmaximum 440
                outlines [(2, "#102033", 0, 1)]
            text "[lc_phone_clock_text()]":
                style "lc_sw_pixel_bold"
                size 70
                color "#FFFFFF"
                xalign 0.5
                ypos 132
                outlines [(2, "#102033", 0, 1)]

            for i, row in enumerate(LC_SM_HOME):
                $ app_id = row[0]
                $ label = row[1]
                $ kind = row[2]
                $ ix = 56 + (i % 4) * 114
                $ iy = 280 + (i // 4) * 150
                $ badge = lc_sm_app_badge(app_id)
                if kind == "status":
                    $ app_action = Show("lc_phone_status")
                elif kind == "settings":
                    $ app_action = Show("lc_phone_settings")
                else:
                    $ app_action = SetScreenVariable("phone_app", app_id)
                button:
                    style "lc_sw_hit"
                    xpos ix
                    ypos iy
                    at lc_lift
                    xysize (80, 118)
                    action [Function(lc_ui_play, "app_tap"), app_action]
                    add Transform("gui/phone/sprite_match/" + app_id + ".png", nearest=True)
                    if badge:
                        fixed:
                            xpos 50
                            ypos -8
                            xysize (36 if len(badge) <= 1 else 54, 28)
                            add Frame("gui/phone/sprite_match/badge.png", 10, 10)
                            text badge:
                                style "lc_sw_pixel_bold"
                                size 16
                                color "#FFFFFF"
                                xalign 0.5
                                yalign 0.45
                    text label:
                        style "lc_sw_hand"
                        size 22
                        color "#FFFFFF"
                        outlines [(2, "#14243D", 0, 1)]
                        xalign 0.5
                        ypos 84
                        xsize 108
                        text_align 0.5

            for slot, app_id in enumerate(LC_SM_DOCK):
                $ ix = 50 + slot * 120
                $ iy = 902
                $ badge = lc_sm_app_badge(app_id)
                button:
                    style "lc_sw_hit"
                    xpos ix
                    ypos iy
                    at lc_lift
                    xysize (80, 80)
                    action [Function(lc_ui_play, "app_tap"), SetScreenVariable("phone_app", app_id)]
                    add Transform("gui/phone/sprite_match/" + app_id + ".png", nearest=True)
                    if badge:
                        fixed:
                            xpos 50
                            ypos -8
                            xysize (36 if len(badge) <= 1 else 54, 28)
                            add Frame("gui/phone/sprite_match/badge.png", 10, 10)
                            text badge:
                                style "lc_sw_pixel_bold"
                                size 16
                                color "#FFFFFF"
                                xalign 0.5
                                yalign 0.45

            if current_choice_mode() == "developer":
                hbox:
                    xpos 36
                    ypos 800
                    spacing 12
                    textbutton "Seed":
                        style "lc_sw_hit"
                        background Frame("gui/phone/sprite_match/card.png", 16, 16)
                        text_style "lc_sw_hand"
                        text_size 22
                        text_color "#293C53"
                        xminimum 120
                        ysize 42
                        action Function(phone_debug_seed_messages)
                    textbutton "Clear":
                        style "lc_sw_hit"
                        background Frame("gui/phone/sprite_match/card.png", 16, 16)
                        text_style "lc_sw_hand"
                        text_size 22
                        text_color "#293C53"
                        xminimum 120
                        ysize 42
                        action Function(phone_debug_clear_messages)

        elif phone_app == "thread":
            add "gui/phone/sprite_match/phone_thread.png"
            text "[lc_phone_clock_text()]":
                style "lc_sw_pixel_bold"
                size 22
                color "#303B51"
                xpos 40
                ypos 16
            button:
                style "lc_sw_hit"
                xpos 28
                ypos 96
                xysize (52, 56)
                action [Function(lc_ui_play, "back"), SetScreenVariable("phone_app", "messages")]
                add "gui/phone/sprite_match/chevron.png" xalign 0.5 yalign 0.5
            if phone_thread == "group":
                add phone_group_avatar():
                    xpos 78
                    ypos 92
                    xysize (68, 68)
            else:
                add lc_phone_avatar(phone_thread or "system"):
                    xpos 78
                    ypos 92
                    xysize (68, 68)
            $ _thread_title = phone_thread_label(phone_thread) if phone_thread else "Messages"
            text _thread_title:
                style "lc_sw_hand"
                size 36
                color "#293C53"
                xpos 158
                ypos 104
                xmaximum 300
            $ thread_yadj = thread_adjs.setdefault(phone_thread, lc_phone_thread_adjustment())
            $ reply_prompt = phone_pending_reply(phone_thread)
            viewport:
                ypos 198
                xpos LC_PHONE_CONTENT_LEFT
                xsize LC_PHONE_VIEWPORT_WIDTH
                ysize (420 if reply_prompt else 692)
                mousewheel True
                draggable True
                scrollbars None
                yadjustment thread_yadj
                vbox:
                    xsize LC_PHONE_CONTENT_WIDTH
                    spacing 14
                    text "Today · [lc_phone_clock_text()]":
                        style "lc_sw_hand"
                        size 24
                        color "#8692A6"
                        xalign 0.5
                    $ thread_rows = lc_phone_thread_rows(phone_thread)
                    if not thread_rows:
                        text "No messages yet.":
                            style "lc_sw_hand"
                            size 28
                            color "#6E8399"
                            xalign 0.5
                            text_align 0.5
                    for row in thread_rows:
                        $ _sender = row["sender"]
                        $ _out = row["outgoing"]
                        $ _message = row["message"]
                        $ _body = (_message.get("text") or "").strip()
                        $ _attachment = _message.get("attachment_id")
                        $ _group = phone_thread == "group"
                        $ _bubble_max = 360 if _group else 410
                        if _sender == "system":
                            # Group events (picture changed, member added): a centred
                            # blue pill, no avatar or name (darryn 2026-11-08).
                            frame:
                                style "lc_sw_frame"
                                xalign 0.5
                                xmaximum 400
                                background Frame("gui/phone/sprite_match/key.png", 18, 18)
                                padding (18, 8)
                                text _body:
                                    style "lc_sw_hand"
                                    size 22
                                    color "#FFFFFF"
                                    text_align 0.5
                                    xalign 0.5
                        else:
                            hbox:
                                xfill True
                                spacing 8
                                box_align (1.0 if _out else 0.0)
                                if _group and not _out:
                                    fixed:
                                        xysize (40, 40)
                                        yalign 1.0
                                        if row["tail"]:
                                            add lc_phone_avatar(_sender) xysize (40, 40)
                                vbox:
                                    spacing 4
                                    xmaximum _bubble_max
                                    xalign (1.0 if _out else 0.0)
                                    if _group and row["show_name"] and not _out:
                                        text phone_sender_label(_sender):
                                            style "lc_sw_hand"
                                            size 22
                                            color "#6E8399"
                                    if _body:
                                        frame:
                                            style "lc_sw_frame"
                                            background Frame("gui/phone/sprite_match/bubble_out.png" if _out else "gui/phone/sprite_match/bubble_in.png", 18, 18)
                                            padding (16, 12)
                                            xmaximum _bubble_max
                                            text _body:
                                                style "lc_sw_hand"
                                                size 32
                                                color "#293C53"
                                                xmaximum (_bubble_max - 36)
                                                line_spacing 2
                                    if _attachment and renpy.has_image(_attachment):
                                        button:
                                            style "lc_sw_hit"
                                            xysize (min(320, _bubble_max), 180)
                                            xalign (1.0 if _out else 0.0)
                                            action Show("lc_phone_photo_viewer", photo_asset=_attachment)
                                            add lc_phone_rounded_photo(_attachment, min(320, _bubble_max), 180)
                    if thread_rows and thread_rows[-1]["outgoing"]:
                        text "Read [lc_phone_clock_text()]":
                            style "lc_sw_hand"
                            size 22
                            color "#8B99AB"
                            xalign 1.0
                    null height 8
            if reply_prompt:
                frame:
                    style "lc_sw_frame"
                    xpos LC_PHONE_CONTENT_LEFT
                    ypos 625
                    xsize LC_PHONE_CONTENT_WIDTH
                    ysize 266
                    background Frame("gui/phone/sprite_match/card.png", 16, 16)
                    padding (12, 9)
                    vbox:
                        xfill True
                        spacing 5
                        text "Reply as [player_name] · choose one":
                            style "lc_sw_hand"
                            size 25
                            color "#425f80"
                        for reply_option in reply_prompt["options"]:
                            button:
                                style "lc_sw_hit"
                                xfill True
                                ysize 58
                                background Frame("gui/phone/sprite_match/reply_choice.png", 18, 18)
                                hover_background Frame("gui/phone/sprite_match/row_hover.png", 18, 18)
                                action Function(phone_select_reply, phone_thread, reply_option["id"])
                                text "↩":
                                    font "DejaVuSans.ttf"
                                    size 24
                                    color "#557da7"
                                    xpos 14
                                    yalign 0.5
                                text reply_option["text"]:
                                    style "lc_sw_hand"
                                    size 24
                                    color "#293C53"
                                    xpos 49
                                    yalign 0.5
                                    xmaximum 366
            text "+":
                style "lc_sw_hand"
                size 30
                color "#6884A0"
                xpos 42
                ypos 920
            $ _composer = ("Choose a reply…" if reply_prompt else
                           "Message " + (phone_thread_label(phone_thread) if phone_thread else "") + "...")
            text _composer:
                style "lc_sw_hand"
                size 26
                color "#9BA9BA"
                xpos 74
                ypos 926
                xmaximum 370

        else:
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
                action [Function(lc_ui_play, "back"), SetScreenVariable("phone_app", "home"), SetScreenVariable("phone_thread", None)]
                add "gui/phone/sprite_match/chevron.png" xalign 0.5 yalign 0.5
            if phone_app == "messages":
                text "Messages":
                    style "lc_sw_hand"
                    size 36
                    color "#293C53"
                    xpos 76
                    ypos 98
            elif phone_app == "photos":
                text "Photos":
                    style "lc_sw_hand"
                    size 36
                    color "#293C53"
                    xpos 76
                    ypos 98
            elif phone_app == "shop":
                text "Shop":
                    style "lc_sw_hand"
                    size 36
                    color "#293C53"
                    xpos 76
                    ypos 98
            elif phone_app == "wallet":
                text "Wallet":
                    style "lc_sw_hand"
                    size 36
                    color "#293C53"
                    xpos 76
                    ypos 98
            elif phone_app == "delivery":
                text "Delivery":
                    style "lc_sw_hand"
                    size 36
                    color "#293C53"
                    xpos 76
                    ypos 98
            else:
                text "Phone":
                    style "lc_sw_hand"
                    size 36
                    color "#293C53"
                    xpos 76
                    ypos 98

            viewport:
                ypos 164
                xpos LC_PHONE_CONTENT_LEFT
                xsize LC_PHONE_VIEWPORT_WIDTH
                ysize 820
                mousewheel True
                draggable True
                scrollbars None
                vbox:
                    xsize LC_PHONE_CONTENT_WIDTH
                    spacing 14

                    if phone_app == "messages":
                        for thread_id in PHONE_THREAD_ORDER:
                            $ thread_name = phone_thread_label(thread_id)
                            $ thread_preview = lc_phone_one_line(lc_phone_list_preview(thread_id), 34)
                            $ unread_count = phone_thread_unread_count(thread_id)
                            button:
                                style "lc_sw_hit"
                                xfill True
                                ysize 100
                                hover_background Frame("gui/phone/sprite_match/row_hover.png", 18, 18)
                                action [Function(phone_mark_thread_read, thread_id), SetScreenVariable("phone_thread", thread_id), SetScreenVariable("phone_app", "thread")]
                                if unread_count > 0:
                                    add "gui/phone/sprite_match/dot.png":
                                        xpos 4
                                        ypos 38
                                if thread_id == "group":
                                    add phone_group_avatar():
                                        xpos 18
                                        ypos 16
                                        xysize (58, 58)
                                else:
                                    add lc_phone_avatar(thread_id):
                                        xpos 18
                                        ypos 16
                                        xysize (58, 58)
                                text thread_name:
                                    style "lc_sw_hand"
                                    size 28
                                    color ("#293C53" if unread_count else "#5C6E82")
                                    xpos 88
                                    ypos 14
                                    xmaximum 280
                                if unread_count:
                                    text "Now":
                                        style "lc_sw_hand"
                                        size 22
                                        color "#3D8FD4"
                                        xpos 374
                                        ypos 16
                                text thread_preview:
                                    style "lc_sw_hand"
                                    size 22
                                    color ("#293C53" if unread_count else "#6E8399")
                                    xpos 88
                                    ypos 50
                                    xmaximum 320
                                add "gui/phone/sprite_match/chevron.png":
                                    xpos 420
                                    ypos 32
                                    xysize (22, 22)
                                add Solid("#E1E7EF"):
                                    xpos 88
                                    ypos 97
                                    xysize (340, 2)

                    elif phone_app == "shop" and not LC_SHOP_ENABLED:
                        # Shop under development (LC_SHOP_ENABLED in shop_screen.rpy).
                        text "Coming soon":
                            style "lc_sw_hand"
                            size 30
                            color "#3D8FD4"
                        text "The Shop is still under development. New outfits for [girlfriend_name] will arrive here in a future update.":
                            style "lc_sw_hand"
                            size 28
                            color "#6E8399"
                            xmaximum 440

                    elif phone_app == "shop":
                        text "Purchases add outfits to [girlfriend_name]'s wardrobe. Whether she wears them is tracked separately.":
                            style "lc_sw_hand"
                            size 26
                            color "#6E8399"
                            xmaximum 440
                        if last_shop_message:
                            text "[last_shop_message]":
                                style "lc_sw_hand"
                                size 26
                                color "#293C53"
                                xmaximum 440
                        for outfit_id in shop_outfit_ids():
                            $ phone_outfit = get_outfit(outfit_id)
                            $ phone_outfit_name = phone_outfit["name"]
                            $ phone_outfit_description = gallery_customize_names(phone_outfit["description"])
                            $ phone_outfit_cost = phone_outfit["cost"]
                            $ phone_outfit_state = shop_item_state(outfit_id)
                            $ phone_outfit_status = shop_item_status_label(outfit_id)
                            frame:
                                style "lc_sw_frame"
                                xfill True
                                background Frame("gui/phone/sprite_match/card.png", 18, 18)
                                padding (16, 14)
                                vbox:
                                    spacing 8
                                    xfill True
                                    text phone_outfit_name:
                                        style "lc_sw_hand"
                                        size 28
                                        color "#293C53"
                                    text phone_outfit_description:
                                        style "lc_sw_hand"
                                        size 24
                                        color "#6E8399"
                                        xmaximum 410
                                    text phone_outfit_status:
                                        style "lc_sw_hand"
                                        size 22
                                        color "#3D8FD4"
                                    if phone_outfit_state == "available":
                                        textbutton "Buy for [lc_phone_price(phone_outfit_cost)]":
                                            style "lc_sw_hit"
                                            xfill True
                                            yminimum 52
                                            background Frame("gui/phone/sprite_match/key.png", 16, 16)
                                            hover_background Frame("gui/phone/sprite_match/key.png", 16, 16)
                                            text_style "lc_sw_hand"
                                            text_size 24
                                            text_color "#FFFFFF"
                                            action Function(purchase_outfit, outfit_id)
                                    elif phone_outfit_state == "owned":
                                        text "Owned":
                                            style "lc_sw_hand"
                                            size 24
                                            color "#1E8449"
                                            xalign 0.5
                                    else:
                                        $ _shop_state_label = ("Need " + lc_phone_price(phone_outfit_cost)) if phone_outfit_state == "insufficient" else "Locked"
                                        text _shop_state_label:
                                            style "lc_sw_hand"
                                            size 22
                                            color "#6E8399"
                                            xalign 0.5

                    elif phone_app == "photos":
                        $ photo_items = phone_photo_items()
                        if photo_items:
                            for photo in photo_items:
                                $ photo_asset = photo.get("asset_id")
                                $ photo_label = photo.get("label", "Photo")
                                vbox:
                                    spacing 6
                                    xfill True
                                    if photo_asset and renpy.has_image(photo_asset):
                                        button:
                                            style "lc_sw_hit"
                                            xfill True
                                            ysize 240
                                            action Show("lc_phone_photo_viewer", photo_asset=photo_asset)
                                            add lc_phone_rounded_photo(photo_asset, LC_PHONE_CONTENT_WIDTH, 240)
                                    else:
                                        frame:
                                            style "lc_sw_frame"
                                            xfill True
                                            ysize 140
                                            background Frame("gui/phone/sprite_match/card.png", 18, 18)
                                            add Transform("gui/phone/sprite_match/photos.png", nearest=True) xalign 0.5 yalign 0.5 xysize (64, 64)
                                    text photo_label:
                                        style "lc_sw_hand"
                                        size 22
                                        color "#6E8399"
                                        xalign 0.5
                                    if current_choice_mode() == "developer":
                                        text "Asset: [photo_asset]":
                                            style "lc_sw_hand"
                                            size 18
                                            color "#6E8399"
                                            xalign 0.5
                        else:
                            text "Your photos":
                                style "lc_sw_hand"
                                size 30
                                color "#293C53"
                                xalign 0.5
                            text "Story photos and pictures people send you collect here.":
                                style "lc_sw_hand"
                                size 26
                                color "#6E8399"
                                text_align 0.5
                                xalign 0.5
                                xmaximum 440

                    elif phone_app == "wallet":
                        frame:
                            style "lc_sw_frame"
                            xfill True
                            background Frame("gui/phone/sprite_match/card.png", 18, 18)
                            padding (20, 24)
                            vbox:
                                spacing 8
                                xfill True
                                add Transform("gui/phone/sprite_match/wallet.png", nearest=True) xalign 0.5 xysize (72, 72)
                                text "Available":
                                    style "lc_sw_hand"
                                    size 24
                                    color "#6E8399"
                                    xalign 0.5
                                text "$[money]":
                                    style "lc_sw_hand"
                                    size 48
                                    color "#293C53"
                                    xalign 0.5
                                if last_money_reason:
                                    text "Last change: [last_money_change]":
                                        style "lc_sw_hand"
                                        size 24
                                        color "#293C53"
                                        xalign 0.5
                                    text "[last_money_reason]":
                                        style "lc_sw_hand"
                                        size 22
                                        color "#6E8399"
                                        xalign 0.5
                                        text_align 0.5
                                        xmaximum 420

                    elif phone_app == "delivery":
                        frame:
                            style "lc_sw_frame"
                            xfill True
                            background Frame("gui/phone/sprite_match/card.png", 18, 18)
                            padding (20, 28)
                            vbox:
                                spacing 10
                                xfill True
                                add Transform("gui/phone/sprite_match/delivery.png", nearest=True) xalign 0.5 xysize (72, 72)
                                text "No active deliveries":
                                    style "lc_sw_hand"
                                    size 28
                                    color "#293C53"
                                    text_align 0.5
                                    xalign 0.5
                                text "Orders show up here when a delivery actually happens.":
                                    style "lc_sw_hand"
                                    size 26
                                    color "#6E8399"
                                    text_align 0.5
                                    xalign 0.5
                                    xmaximum 420

                    null height 28


screen lc_phone_status_row(row):
    button:
        style "lc_sw_hit"
        xfill True
        # Padding clears the hover art's rounded 18px border so the bar sits
        # fully inside the highlight (darryn 2026-11-08).
        padding (14, 8, 14, 12)
        hover_background Frame("gui/phone/sprite_match/row_hover.png", 18, 18)
        tooltip row.get("tooltip")
        action NullAction()
        vbox:
            spacing 4
            xfill True
            hbox:
                xfill True
                text row["label"]:
                    style "lc_sw_hand"
                    size 24
                    color "#293C53"
                if row["detail"]:
                    text row["detail"]:
                        style "lc_sw_hand"
                        size 20
                        color "#6E8399"
                        xalign 1.0
            bar:
                value StaticValue(row["value"], 100)
                xfill True
                ysize 12
                left_bar Solid("#3D8FD4")
                right_bar Solid("#D3DEEA")
            if row["internal_key"]:
                text row["internal_key"]:
                    style "lc_sw_hand"
                    size 18
                    color "#6E8399"


screen lc_phone_status_section(title, rows):
    frame:
        style "lc_sw_frame"
        xfill True
        background Frame("gui/phone/sprite_match/card.png", 18, 18)
        padding (14, 12)
        vbox:
            spacing 10
            xfill True
            text title:
                style "lc_sw_hand"
                size 20
                color "#6E8399"
            for row in rows:
                use lc_phone_status_row(row)


screen lc_phone_status():
    modal True
    zorder 340
    key "K_ESCAPE" action Hide("lc_phone_status")
    key "game_menu" action Hide("lc_phone_status")

    $ _mode = current_choice_mode()
    $ _relationship_rows = status_relationship_rows(_mode)
    $ _leia_rows = status_leia_rows(_mode)
    $ _ryan_rows = status_ryan_rows(_mode)
    $ _route_rows = status_route_rows(_mode)

    use lc_phone_backdrop([Hide("lc_phone_status"), Hide("phone_screen")])
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
            ypos 88
            xysize (56, 56)
            action [Function(lc_ui_play, "back"), Hide("lc_phone_status")]
            add "gui/phone/sprite_match/chevron.png" xalign 0.5 yalign 0.5
        text "Status":
            style "lc_sw_hand"
            size 36
            color "#293C53"
            xpos 76
            ypos 96
        text transparency_mode_label():
            style "lc_sw_hand"
            size 20
            color "#6E8399"
            xpos 76
            ypos 138
            xmaximum 420
        viewport:
            ypos 176
            xpos LC_PHONE_CONTENT_LEFT
            xsize LC_PHONE_VIEWPORT_WIDTH
            ysize 800
            mousewheel True
            draggable True
            scrollbars None
            vbox:
                spacing 12
                xsize LC_PHONE_CONTENT_WIDTH
                if not getattr(persistent, "status_page_intro_seen", False):
                    frame:
                        style "lc_sw_frame"
                        xfill True
                        background Frame("gui/phone/sprite_match/card.png", 18, 18)
                        padding (14, 12)
                        vbox:
                            spacing 8
                            text "Your live dashboard":
                                style "lc_sw_hand"
                                size 26
                                color "#3D8FD4"
                            text "Status tracks the relationship, [girlfriend_name], and [player_name]. Settings chooses how much of it you can see.":
                                style "lc_sw_hand"
                                size 24
                                color "#293C53"
                                xmaximum 440
                            textbutton "Got it":
                                style "lc_sw_hit"
                                xminimum 160
                                yminimum 48
                                background Frame("gui/phone/sprite_match/key.png", 16, 16)
                                hover_background Frame("gui/phone/sprite_match/key.png", 16, 16)
                                text_style "lc_sw_hand"
                                text_size 24
                                text_color "#FFFFFF"
                                action Function(lc_mark_status_intro_seen)
                frame:
                    style "lc_sw_frame"
                    xfill True
                    background Frame("gui/phone/sprite_match/card.png", 18, 18)
                    padding (14, 12)
                    vbox:
                        spacing 6
                        text "[girlfriend_name] right now":
                            style "lc_sw_hand"
                            size 26
                            color "#293C53"
                        text "[leia_overview_text()]":
                            style "lc_sw_hand"
                            size 24
                            color "#6E8399"
                            xmaximum 440
                use lc_phone_status_section("Relationship", _relationship_rows)
                use lc_phone_status_section(girlfriend_name, _leia_rows)
                use lc_phone_status_section(player_name, _ryan_rows)
                if _route_rows:
                    use lc_phone_status_section("Route tendencies", _route_rows)
                textbutton "Open settings":
                    style "lc_sw_hit"
                    xfill True
                    ysize 52
                    # Label centred inside the card, white on the blue hover key.
                    text_xalign 0.5
                    text_yalign 0.5
                    background Frame("gui/phone/sprite_match/card.png", 18, 18)
                    hover_background Frame("gui/phone/sprite_match/key.png", 18, 18)
                    text_style "lc_sw_hand"
                    text_size 24
                    text_idle_color "#3D8FD4"
                    text_hover_color "#FFFFFF"
                    action [Hide("lc_phone_status"), Show("lc_phone_settings")]
                text "[status_mode_note()]":
                    style "lc_sw_hand"
                    size 22
                    color "#6E8399"
                    text_align 0.5
                    xalign 0.5
                    xmaximum 440
                text "Hover over a stat to see what it means.":
                    style "lc_sw_hand"
                    size 22
                    color "#6E8399"
                    text_align 0.5
                    xalign 0.5
                    xmaximum 440
                null height 16
    use lc_stat_tip(GetTooltip("lc_phone_status"), look="phone")


screen lc_phone_settings_mode(mode_id):
    $ _selected = current_choice_mode() == mode_id
    $ _info = transparency_mode_info(mode_id)
    button:
        style "lc_sw_hit"
        xfill True
        yminimum 96
        padding (16, 12)
        background Frame("gui/phone/sprite_match/key.png" if _selected else "gui/phone/sprite_match/card.png", 18, 18)
        hover_background Frame("gui/phone/sprite_match/key.png" if _selected else "gui/phone/sprite_match/row_hover.png", 18, 18)
        action Function(lc_phone_set_information_mode, mode_id)
        vbox:
            spacing 4
            xfill True
            # Mode name on the left; the selected mode gets a bold "On" in a
            # white pill, flush right (darryn 2026-11-08).
            # Fixed height: yfit with yalign-ed children takes the whole
            # available height, which blew the card up (#160).
            fixed:
                xfill True
                ysize 40
                text _info["label"]:
                    style "lc_sw_hand"
                    size 26
                    color ("#FFFFFF" if _selected else "#293C53")
                    xalign 0.0
                    yalign 0.5
                if _selected:
                    frame:
                        xalign 1.0
                        yalign 0.5
                        background Frame("gui/phone/sprite_match/pill_white.png", 15, 15)
                        padding (14, 1, 14, 3)
                        text "On":
                            style "lc_sw_hand"
                            size 22
                            bold True
                            color "#2E74B0"
                            yalign 0.5
            text _info["tagline"]:
                style "lc_sw_hand"
                size 22
                color ("#EAF4FF" if _selected else "#6E8399")
                xmaximum 420
            text _info["description"]:
                style "lc_sw_hand"
                size 22
                color ("#EAF4FF" if _selected else "#6E8399")
                xmaximum 420


screen lc_phone_settings():
    modal True
    zorder 340
    key "K_ESCAPE" action Hide("lc_phone_settings")

    use lc_phone_backdrop([Hide("lc_phone_settings"), Hide("phone_screen")])
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
            action [Function(lc_ui_play, "back"), Hide("lc_phone_settings")]
            add "gui/phone/sprite_match/chevron.png" xalign 0.5 yalign 0.5
        text "Settings":
            style "lc_sw_hand"
            size 36
            color "#293C53"
            xpos 76
            ypos 98
        viewport:
            ypos 168
            xpos LC_PHONE_CONTENT_LEFT
            xsize LC_PHONE_VIEWPORT_WIDTH
            ysize 810
            mousewheel True
            draggable True
            scrollbars None
            vbox:
                spacing 12
                xsize LC_PHONE_CONTENT_WIDTH
                text "These settings only change what the interface reveals. They never alter stats, story outcomes, or difficulty.":
                    style "lc_sw_hand"
                    size 24
                    color "#6E8399"
                    text_align 0.5
                    xalign 0.5
                    xmaximum 440
                use lc_phone_settings_mode("normal")
                use lc_phone_settings_mode("insight")
                use lc_phone_settings_mode("full")
                if config.developer or not LC_IS_RELEASE:
                    use lc_phone_settings_mode("developer")
                textbutton "Open status":
                    style "lc_sw_hit"
                    xfill True
                    ysize 52
                    background Frame("gui/phone/sprite_match/card.png", 18, 18)
                    hover_background Frame("gui/phone/sprite_match/key.png", 18, 18)
                    text_style "lc_sw_hand"
                    text_size 24
                    text_idle_color "#3D8FD4"
                    text_hover_color "#FFFFFF"
                    action [Hide("lc_phone_settings"), Show("lc_phone_status")]
                if current_choice_mode() == "developer":
                    text "Developer exposes internal IDs, stat keys, route tendencies, and debug information.":
                        style "lc_sw_hand"
                        size 22
                        color "#6E8399"
                        xmaximum 440
                null height 16
