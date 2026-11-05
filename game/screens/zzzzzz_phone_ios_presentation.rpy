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
        who = sender if sender in ("leia", "julian", "maya", "ryan") else "system"
        if sender == "player":
            who = "ryan"
        return "gui/phone/sweetheart/avatar_%s.png" % who

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


style lc_sw_pixel is default:
    font "fonts/Silkscreen-Regular.ttf"
    size 24
    antialias False
    hinting "none"
    adjust_spacing False
    color "#4a2633"

style lc_sw_pixel_bold is lc_sw_pixel:
    font "fonts/Silkscreen-Bold.ttf"

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
    # Wins over the older Status/Settings docks. Both apps live on the home grid.
    pass


screen lc_sw_px(name, xpos=0, ypos=0):
    add Transform(lc_phone_art(name), nearest=True):
        xpos xpos
        ypos ypos


screen lc_sw_status_bar(ink=None):
    $ c = lc_phone_palette()
    $ theme = lc_phone_theme()
    $ color = ink or c["txt"]
    $ glyphs = "glyphs_wallpaper" if ink else ("glyphs_night" if theme == "night" else "glyphs_day")
    fixed:
        xysize (642, 48)
        text "[lc_phone_clock_text()]":
            style "lc_sw_pixel_bold"
            color color
            xpos 42
            ypos 6
        add Transform(lc_phone_art("island"), nearest=True):
            xalign 0.5
            ypos 9
        add Transform(lc_phone_art(glyphs), nearest=True):
            xpos 498
            ypos 6


screen lc_sw_home_bar(color):
    fixed:
        xysize (642, 1020)
        add Solid(color):
            xalign 0.5
            ypos 996
            xsize 204
            ysize 9


screen lc_sw_back(action, label="HOME", xpos=18, ypos=54):
    $ c = lc_phone_palette()
    $ theme = lc_phone_theme()
    button:
        style "lc_sw_hit"
        xpos xpos
        ypos ypos
        ysize 36
        xminimum 96
        action [Function(lc_ui_play, "back"), action]
        hbox:
            spacing 9
            yalign 0.5
            add Transform(lc_phone_art("chevron_" + theme), nearest=True) yalign 0.5
            text label:
                style "lc_sw_pixel_bold"
                color c["acc"]
                yalign 0.5


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
        background Frame(lc_phone_art("key_berry"), 18, 15)
        hover_background Frame(lc_phone_art("key_berry"), 18, 15)
        action Hide("lc_phone_photo_viewer")
        text "DONE":
            style "lc_sw_pixel_bold"
            color "#faf4e8"
            xalign 0.5
            yalign 0.5


# Click outside the handset to close it, like tapping away from a real phone.
# The backdrop is a full-screen invisible button behind the handset; the
# handset itself sits on a click-catcher so taps on empty parts of the screen
# or bezel never fall through to the backdrop.
screen lc_phone_backdrop(close_action):
    button:
        style "lc_sw_hit"
        xfill True
        yfill True
        keyboard_focus False
        background Solid("#120810c4")
        hover_background Solid("#120810c4")
        action close_action


screen lc_phone_body_blocker():
    button:
        style "lc_sw_hit"
        xysize (702, 1068)
        keyboard_focus False
        action NullAction()


# Message rows are inlined in phone_screen. A used screen is given the full
# area offered by its parent, which would swallow the thread viewport.

screen phone_screen():
    modal True
    zorder 310

    default phone_app = lc_phone_link_app()
    default phone_thread = lc_phone_link_thread()
    default hovered_app = None
    # One scroll position per open thread; a fresh phone session starts each at the bottom.
    default thread_adjs = {}

    on "show" action [SetVariable("lc_phone_deep_link", None), Function(lc_ui_play, "phone_open")]
    on "hide" action Function(lc_ui_play, "phone_close")
    on "replace" action SetVariable("lc_phone_deep_link", None)

    key "K_ESCAPE" action Hide("phone_screen")

    $ c = lc_phone_palette()
    $ theme = lc_phone_theme()

    use lc_phone_backdrop(Hide("phone_screen"))

    fixed:
        xalign 0.5
        yalign 0.5
        xysize (702, 1068)
        use lc_phone_body_blocker

        fixed:
            xpos 30
            ypos 24
            xysize (642, 1020)
            clipping True

            if phone_app == "home":
                add Transform(lc_phone_art("wallpaper"), nearest=True)
                use lc_sw_status_bar("#5a2533")
                text "[lc_phone_clock_text()]":
                    style "lc_sw_pixel_bold"
                    size 96
                    color "#5a2533"
                    xalign 0.5
                    ypos 48
                text "[lc_phone_home_caption()]":
                    style "lc_sw_pixel_bold"
                    color "#5a2533"
                    xalign 0.5
                    ypos 168
                    outlines [(3, "#fbe7d8", 1, 1), (0, "#fbe7d8", 0, 0)]
                $ unread_total = phone_total_unread()
                $ unread_badge = phone_unread_badge_label() if unread_total else None
                $ status_badge = "!" if not getattr(persistent, "status_page_intro_seen", False) else None

                ## Home grid: Delivery, Status, Settings. Dock holds the other four.
                for slot, app_id, label, badge, action in (
                    (0, "delivery", "DELIVERY", None, SetScreenVariable("phone_app", "delivery")),
                    (1, "status", "STATUS", status_badge, Show("lc_phone_status")),
                    (2, "settings", "SETTINGS", None, Show("lc_phone_settings")),
                ):
                    $ ix = 57 + slot * 147
                    button:
                        style "lc_sw_hit"
                        xpos ix
                        ypos (204 if hovered_app == app_id else 210)
                        xysize (78, 120)
                        action [Function(lc_ui_play, "app_tap"), action]
                        hovered SetScreenVariable("hovered_app", app_id)
                        unhovered SetScreenVariable("hovered_app", None)
                        add Transform(lc_phone_art("icon_" + app_id), nearest=True)
                        if badge:
                            fixed:
                                xpos 48
                                ypos -12
                                xysize (33, 33)
                                add Transform(lc_phone_art("badge_small"), nearest=True)
                                text badge:
                                    style "lc_sw_pixel_bold"
                                    size 18
                                    color "#faf4e8"
                                    xalign 0.5
                                    yalign 0.45
                    text label:
                        style "lc_sw_pixel"
                        color "#3b2a30"
                        xpos (ix + 36)
                        xanchor 0.5
                        ypos 292
                        outlines [(3, "#fbe7d8", 1, 1)]

                add Solid("#faf4e8"):
                    xpos 306
                    ypos 852
                    xysize (9, 9)
                add Solid("#b5a5ab"):
                    xpos 324
                    ypos 852
                    xysize (9, 9)

                add Transform(lc_phone_art("dock"), nearest=True):
                    xpos 21
                    ypos 882
                for slot, app_id, action in (
                    (0, "messages", SetScreenVariable("phone_app", "messages")),
                    (1, "photos", SetScreenVariable("phone_app", "photos")),
                    (2, "shop", SetScreenVariable("phone_app", "shop")),
                    (3, "wallet", SetScreenVariable("phone_app", "wallet")),
                ):
                    $ ix = 57 + slot * 147
                    button:
                        style "lc_sw_hit"
                        xpos ix
                        ypos (888 if hovered_app == app_id else 894)
                        xysize (78, 78)
                        action [Function(lc_ui_play, "app_tap"), action]
                        hovered SetScreenVariable("hovered_app", app_id)
                        unhovered SetScreenVariable("hovered_app", None)
                        add Transform(lc_phone_art("icon_" + app_id), nearest=True)
                        if app_id == "messages" and unread_badge:
                            fixed:
                                xpos 48
                                ypos -12
                                xysize (33, 33)
                                add Transform(lc_phone_art("badge_small"), nearest=True)
                                text unread_badge:
                                    style "lc_sw_pixel_bold"
                                    size 18
                                    color "#faf4e8"
                                    xalign 0.5
                                    yalign 0.45
                use lc_sw_home_bar("#faf4e8")

                if current_choice_mode() == "developer":
                    hbox:
                        xpos 36
                        ypos 800
                        spacing 12
                        textbutton "SEED":
                            style "lc_sw_hit"
                            background Frame(lc_phone_art("card_" + theme), 18, 18)
                            text_font "fonts/Silkscreen-Regular.ttf"
                            text_antialias False
                            text_hinting "none"
                            text_color c["txt"]
                            text_size 18
                            xminimum 140
                            ysize 42
                            action Function(phone_debug_seed_messages)
                        textbutton "CLEAR":
                            style "lc_sw_hit"
                            background Frame(lc_phone_art("card_" + theme), 18, 18)
                            text_font "fonts/Silkscreen-Regular.ttf"
                            text_antialias False
                            text_hinting "none"
                            text_color c["txt"]
                            text_size 18
                            xminimum 140
                            ysize 42
                            action Function(phone_debug_clear_messages)

            else:
                add Solid(c["bg"])
                if lc_phone_hearts and phone_app in ("messages", "thread"):
                    add Transform(lc_phone_art("hearts_" + theme), nearest=True)

                if phone_app == "thread":
                    add Solid(c["nav"]):
                        xysize (642, 156)
                    add Solid(c["line"]):
                        ypos 156
                        xysize (642, 3)
                    use lc_sw_status_bar()
                    $ back_count = phone_total_unread()
                    use lc_sw_back(SetScreenVariable("phone_app", "messages"), "", xpos=12, ypos=66)
                    if back_count > 0:
                        fixed:
                            xpos 48
                            ypos 66
                            xysize (36, 30)
                            add Transform(lc_phone_art("badge_" + theme), nearest=True, xysize=(36, 30))
                            text "[back_count]":
                                style "lc_sw_pixel_bold"
                                size 18
                                color "#faf4e8"
                                xalign 0.5
                                yalign 0.4
                    if phone_thread == "group":
                        add Transform(lc_phone_art("avatar_group"), nearest=True):
                            xalign 0.5
                            ypos 48
                    else:
                        fixed:
                            xalign 0.5
                            ypos 48
                            xysize (54, 54)
                            add Transform(lc_phone_avatar(phone_thread or "system"), nearest=True, xysize=(54, 54))
                            text lc_phone_initial(phone_thread or "system"):
                                style "lc_sw_pixel_bold"
                                size 28
                                color lc_phone_avatar_ink(phone_thread or "system")
                                xalign 0.5
                                yalign 0.45
                    text phone_thread_label(phone_thread).upper():
                        style "lc_sw_pixel_bold"
                        color c["txt"]
                        xalign 0.5
                        ypos 108
                    $ thread_yadj = thread_adjs.setdefault(phone_thread, lc_phone_thread_adjustment())
                    viewport:
                        ypos 168
                        xysize (642, 726)
                        mousewheel True
                        draggable True
                        scrollbars None
                        yadjustment thread_yadj
                        vbox:
                            xfill True
                            spacing 4
                            first_spacing 4
                            if phone_thread:
                                text "TODAY  [lc_phone_clock_text()]":
                                    style "lc_sw_pixel"
                                    color c["stamp"]
                                    xalign 0.5
                            $ thread_rows = lc_phone_thread_rows(phone_thread)
                            if not thread_rows:
                                text "No messages yet.":
                                    style "lc_sw_hand"
                                    color c["mut"]
                                    xalign 0.5
                                    text_align 0.5
                            for row in thread_rows:
                                $ _sender = row["sender"]
                                $ _out = row["outgoing"]
                                $ _message = row["message"]
                                $ _body = (_message.get("text") or "").strip()
                                $ _attachment = _message.get("attachment_id")
                                $ _kind = ("out_" if _out else "in_") + theme
                                # 75% of the 642 screen. Bubbles hug the text up to this, then wrap.
                                $ _bubble_max = 480
                                hbox:
                                    xfill True
                                    spacing 0
                                    # box_align keeps spare width on one side, so bubbles
                                    # stay flush instead of being spread toward the centre.
                                    box_align (1.0 if _out else 0.0)
                                    if not _out:
                                        null width 8
                                        fixed:
                                            xysize (36, 36)
                                            yalign 1.0
                                            if row["tail"]:
                                                add Transform(lc_phone_avatar(_sender), nearest=True, xysize=(36, 36))
                                                text lc_phone_initial(_sender):
                                                    style "lc_sw_pixel_bold"
                                                    color lc_phone_avatar_ink(_sender)
                                                    xalign 0.5
                                                    yalign 0.45
                                        null width 8
                                    vbox:
                                        spacing 2
                                        xmaximum _bubble_max
                                        xalign (1.0 if _out else 0.0)
                                        if row["show_name"]:
                                            text phone_sender_label(_sender):
                                                style "lc_sw_pixel"
                                                color lc_phone_name_color(_sender)
                                                xalign 0.0
                                        if _body:
                                            # fit_first keeps the tail on the bubble corner
                                            # without stretching the row to the viewport.
                                            fixed:
                                                fit_first True
                                                xalign (1.0 if _out else 0.0)
                                                frame:
                                                    style "lc_sw_frame"
                                                    background Frame(lc_phone_art("bubble_" + _kind), 12, 12)
                                                    padding (14, 6, 14, 8)
                                                    xmaximum _bubble_max
                                                    xfill False
                                                    text _body:
                                                        style "lc_sw_hand"
                                                        size 30
                                                        line_spacing 0
                                                        xalign 0.0
                                                        text_align 0.0
                                                        color (c["out_t"] if _out else c["txt"])
                                                        xmaximum (_bubble_max - 28)
                                                if row["tail"]:
                                                    add Transform(lc_phone_art("tail_" + _kind), nearest=True):
                                                        xalign (1.0 if _out else 0.0)
                                                        yalign 1.0
                                                        xoffset (4 if _out else -4)
                                                        yoffset 2
                                        if _attachment and renpy.has_image(_attachment):
                                            button:
                                                style "lc_sw_hit"
                                                xysize (min(420, _bubble_max), 220)
                                                xalign (1.0 if _out else 0.0)
                                                xfill False
                                                action Show("lc_phone_photo_viewer", photo_asset=_attachment)
                                                add lc_phone_rounded_photo(_attachment, min(420, _bubble_max), 220)
                                    null width 16
                            null height 12
                    fixed:
                        ypos 894
                        xysize (642, 126)
                        add Solid(c["line"]) xysize (642, 3)
                        add Solid(c["nav"]):
                            ypos 3
                            xysize (642, 123)
                        add Transform(lc_phone_art("plus_" + theme), nearest=True):
                            xpos 21
                            ypos 24
                        add Frame(lc_phone_art("field_" + theme), 24, 24):
                            xpos 78
                            ypos 21
                            xysize (468, 51)
                        text "Message":
                            style "lc_sw_hand"
                            size 30
                            color c["mut"]
                            xpos 102
                            ypos 28
                        add Transform(lc_phone_art("send_" + theme), nearest=True):
                            xpos 564
                            ypos 24
                    use lc_sw_home_bar(c["txt"])

                elif phone_app == "messages":
                    use lc_sw_status_bar()
                    use lc_sw_back(SetScreenVariable("phone_app", "home"))
                    text "MESSAGES":
                        style "lc_sw_pixel_bold"
                        size 48
                        color c["txt"]
                        xpos 30
                        ypos 96
                    add Transform(lc_phone_art("compose_" + theme), nearest=True):
                        xpos 582
                        ypos 60
                    add Transform(lc_phone_art("search_" + theme), nearest=True):
                        xpos 27
                        ypos 162
                    text "Search":
                        style "lc_sw_hand"
                        size 28
                        color c["mut"]
                        xpos 84
                        ypos 168
                    viewport:
                        ypos 222
                        xysize (642, 740)
                        mousewheel True
                        draggable True
                        scrollbars None
                        vbox:
                            xfill True
                            for thread_id in PHONE_THREAD_ORDER:
                                $ thread_name = phone_thread_label(thread_id)
                                $ thread_preview = lc_phone_one_line(lc_phone_list_preview(thread_id), 34)
                                $ unread_count = phone_thread_unread_count(thread_id)
                                button:
                                    style "lc_sw_hit"
                                    xfill True
                                    ysize 96
                                    hover_background Solid(c["nav"])
                                    action [Function(phone_mark_thread_read, thread_id), SetScreenVariable("phone_thread", thread_id), SetScreenVariable("phone_app", "thread")]
                                    if unread_count > 0:
                                        add Transform(lc_phone_art("dot"), nearest=True):
                                            xpos 12
                                            ypos 30
                                    if thread_id == "group":
                                        add Transform(lc_phone_art("avatar_group"), nearest=True):
                                            xpos 36
                                            ypos 18
                                    else:
                                        fixed:
                                            xpos 36
                                            ypos 18
                                            xysize (54, 54)
                                            add Transform(lc_phone_avatar(thread_id), nearest=True, xysize=(54, 54))
                                            text lc_phone_initial(thread_id):
                                                style "lc_sw_pixel_bold"
                                                color lc_phone_avatar_ink(thread_id)
                                                xalign 0.5
                                                yalign 0.45
                                    text thread_name.upper():
                                        style ("lc_sw_pixel_bold" if unread_count else "lc_sw_pixel")
                                        color c["txt"]
                                        xpos 108
                                        ypos 16
                                    text ("NOW" if unread_count else ""):
                                        style "lc_sw_pixel"
                                        color (c["acc"] if unread_count else c["mut"])
                                        xpos 520
                                        ypos 16
                                        xanchor 1.0
                                    add Transform(lc_phone_art("chevron_" + theme), nearest=True):
                                        xpos 588
                                        ypos 22
                                    text thread_preview:
                                        style "lc_sw_hand"
                                        size 30
                                        color (c["txt"] if unread_count else c["mut"])
                                        xpos 108
                                        ypos 48
                                        xmaximum 480
                                    add Solid(c["line"]):
                                        xpos 108
                                        ypos 93
                                        xysize (534, 3)
                    use lc_sw_home_bar(c["txt"])

                else:
                    use lc_sw_status_bar()
                    use lc_sw_back([SetScreenVariable("phone_app", "home"), SetScreenVariable("phone_thread", None)])
                    if phone_app == "shop":
                        text "SHOP":
                            style "lc_sw_pixel_bold"
                            size 48
                            color c["txt"]
                            xpos 36
                            ypos 96
                    elif phone_app == "photos":
                        text "PHOTOS":
                            style "lc_sw_pixel_bold"
                            size 48
                            color c["txt"]
                            xpos 36
                            ypos 96
                    elif phone_app == "wallet":
                        text "WALLET":
                            style "lc_sw_pixel_bold"
                            size 48
                            color c["txt"]
                            xpos 36
                            ypos 96
                    elif phone_app == "delivery":
                        text "DELIVERY":
                            style "lc_sw_pixel_bold"
                            size 48
                            color c["txt"]
                            xpos 36
                            ypos 96

                    viewport:
                        ypos 168
                        xysize (642, 800)
                        mousewheel True
                        draggable True
                        scrollbars None
                        frame:
                            style "lc_sw_frame"
                            background None
                            xsize 642
                            padding (36, 0, 36, 18)
                            vbox:
                                spacing 18
                                xfill True

                                if phone_app == "shop" and not LC_SHOP_ENABLED:
                                    # Shop under development (LC_SHOP_ENABLED in shop_screen.rpy).
                                    text "COMING SOON":
                                        style "lc_sw_pixel_bold"
                                        size 30
                                        color c["acc"]
                                    text "The Shop is still under development. New outfits for [girlfriend_name] will arrive here in a future update.":
                                        style "lc_sw_hand"
                                        size 30
                                        color c["mut"]
                                        xmaximum 570
                                elif phone_app == "shop":
                                    text "Purchases add outfits to [girlfriend_name]'s wardrobe. Whether she wears them is tracked separately.":
                                        style "lc_sw_hand"
                                        size 30
                                        color c["mut"]
                                        xmaximum 570
                                    if last_shop_message:
                                        text "[last_shop_message]":
                                            style "lc_sw_hand"
                                            size 30
                                            color c["txt"]
                                            xmaximum 570
                                    for outfit_id in shop_outfit_ids():
                                        $ phone_outfit = get_outfit(outfit_id)
                                        $ phone_outfit_name = phone_outfit["name"]
                                        $ phone_outfit_description = phone_outfit["description"]
                                        $ phone_outfit_cost = phone_outfit["cost"]
                                        $ phone_outfit_state = shop_item_state(outfit_id)
                                        $ phone_outfit_status = shop_item_status_label(outfit_id)
                                        frame:
                                            style "lc_sw_frame"
                                            xfill True
                                            background Frame(lc_phone_art("card_" + theme), 18, 18)
                                            padding (18, 16)
                                            vbox:
                                                spacing 8
                                                xfill True
                                                hbox:
                                                    spacing 12
                                                    add Transform(lc_phone_art("icon_shop"), nearest=True)
                                                    vbox:
                                                        spacing 4
                                                        xfill True
                                                        text phone_outfit_name:
                                                            style "lc_sw_pixel_bold"
                                                            color c["txt"]
                                                        text phone_outfit_description:
                                                            style "lc_sw_hand"
                                                            size 28
                                                            color c["mut"]
                                                            xmaximum 430
                                                text phone_outfit_status:
                                                    style "lc_sw_pixel"
                                                    size 18
                                                    color c["acc"]
                                                if phone_outfit_state == "available":
                                                    textbutton "BUY FOR [lc_phone_price(phone_outfit_cost)]":
                                                        style "lc_sw_hit"
                                                        xfill True
                                                        yminimum 68
                                                        padding (36, 18)
                                                        background Frame(lc_phone_art("key_berry"), 16, 16)
                                                        hover_background Frame(lc_phone_art("key_berry"), 16, 16)
                                                        text_font "fonts/Silkscreen-Bold.ttf"
                                                        text_size 21
                                                        text_antialias False
                                                        text_hinting "none"
                                                        text_xalign 0.5
                                                        text_yalign 0.5
                                                        text_color "#faf4e8"
                                                        action Function(purchase_outfit, outfit_id)
                                                elif phone_outfit_state == "owned":
                                                    text "OWNED":
                                                        style "lc_sw_pixel_bold"
                                                        color "#4f7a2a"
                                                        xalign 0.5
                                                else:
                                                    text ("NEED $[phone_outfit_cost]" if phone_outfit_state == "insufficient" else "LOCKED"):
                                                        style "lc_sw_pixel"
                                                        color c["mut"]
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
                                                        ysize 320
                                                        action Show("lc_phone_photo_viewer", photo_asset=photo_asset)
                                                        add lc_phone_rounded_photo(photo_asset, 570, 320)
                                                else:
                                                    frame:
                                                        style "lc_sw_frame"
                                                        xfill True
                                                        ysize 180
                                                        background Frame(lc_phone_art("card_" + theme), 18, 18)
                                                        add Transform(lc_phone_art("icon_photos"), nearest=True) xalign 0.5 yalign 0.5
                                                text photo_label:
                                                    style "lc_sw_pixel"
                                                    color c["mut"]
                                                    xalign 0.5
                                                if current_choice_mode() == "developer":
                                                    text "Asset: [photo_asset]":
                                                        style "lc_sw_pixel"
                                                        size 18
                                                        color c["mut"]
                                                        xalign 0.5
                                    else:
                                        vbox:
                                            spacing 16
                                            xfill True
                                            add Transform(lc_phone_art("icon_photos"), nearest=True) xalign 0.5
                                            text "YOUR PHOTOS":
                                                style "lc_sw_pixel_bold"
                                                color c["txt"]
                                                xalign 0.5
                                            text "Story photos and pictures people send you collect here.":
                                                style "lc_sw_hand"
                                                size 30
                                                color c["mut"]
                                                text_align 0.5
                                                xalign 0.5
                                                xmaximum 540

                                elif phone_app == "wallet":
                                    frame:
                                        style "lc_sw_frame"
                                        xfill True
                                        background Frame(lc_phone_art("card_" + theme), 18, 18)
                                        padding (24, 28)
                                        vbox:
                                            spacing 12
                                            xfill True
                                            add Transform(lc_phone_art("icon_wallet"), nearest=True) xalign 0.5
                                            text "AVAILABLE":
                                                style "lc_sw_pixel"
                                                color c["mut"]
                                                xalign 0.5
                                            text "$[money]":
                                                style "lc_sw_pixel_bold"
                                                size 64
                                                color c["txt"]
                                                xalign 0.5
                                            if last_money_reason:
                                                text "Last change: [last_money_change]":
                                                    style "lc_sw_hand"
                                                    size 30
                                                    color c["txt"]
                                                    xalign 0.5
                                                text "[last_money_reason]":
                                                    style "lc_sw_hand"
                                                    size 28
                                                    color c["mut"]
                                                    xalign 0.5
                                                    text_align 0.5
                                                    xmaximum 520

                                elif phone_app == "delivery":
                                    frame:
                                        style "lc_sw_frame"
                                        xfill True
                                        background Frame(lc_phone_art("card_" + theme), 18, 18)
                                        padding (24, 36)
                                        vbox:
                                            spacing 16
                                            xfill True
                                            add Transform(lc_phone_art("icon_delivery"), nearest=True) xalign 0.5
                                            text "NO ACTIVE DELIVERIES":
                                                style "lc_sw_pixel_bold"
                                                color c["txt"]
                                                text_align 0.5
                                                xalign 0.5
                                            text "Orders show up here when a delivery actually happens.":
                                                style "lc_sw_hand"
                                                size 30
                                                color c["mut"]
                                                text_align 0.5
                                                xalign 0.5
                                                xmaximum 520

                                null height 36
                    use lc_sw_home_bar(c["txt"])

        add Transform(lc_phone_art("bezel_" + theme), nearest=True)


screen lc_phone_status_row(row):
    $ c = lc_phone_palette()
    vbox:
        spacing 6
        xfill True
        hbox:
            xfill True
            text row["label"]:
                style "lc_sw_pixel_bold"
                color c["txt"]
            if row["detail"]:
                text row["detail"]:
                    style "lc_sw_pixel"
                    size 18
                    color c["mut"]
                    xalign 1.0
        bar:
            value StaticValue(row["value"], 100)
            xfill True
            ysize 12
            left_bar Solid(c["bar"])
            right_bar Solid(c["track"])
        if row["internal_key"]:
            text row["internal_key"]:
                style "lc_sw_pixel"
                size 18
                color c["mut"]


screen lc_phone_status_section(title, rows):
    $ c = lc_phone_palette()
    $ theme = lc_phone_theme()
    frame:
        style "lc_sw_frame"
        xfill True
        background Frame(lc_phone_art("card_" + theme), 18, 18)
        padding (18, 16)
        vbox:
            spacing 14
            xfill True
            text title:
                style "lc_sw_pixel"
                color c["mut"]
            for row in rows:
                use lc_phone_status_row(row)


screen lc_phone_status():
    modal True
    zorder 340
    key "K_ESCAPE" action Hide("lc_phone_status")

    $ c = lc_phone_palette()
    $ theme = lc_phone_theme()
    $ _mode = current_choice_mode()
    $ _relationship_rows = status_relationship_rows(_mode)
    $ _leia_rows = status_leia_rows(_mode)
    $ _ryan_rows = status_ryan_rows(_mode)
    $ _route_rows = status_route_rows(_mode)

    use lc_phone_backdrop([Hide("lc_phone_status"), Hide("phone_screen")])
    fixed:
        xalign 0.5
        yalign 0.5
        xysize (702, 1068)
        use lc_phone_body_blocker
        fixed:
            xpos 30
            ypos 24
            xysize (642, 1020)
            clipping True
            add Solid(c["bg"])
            use lc_sw_status_bar()
            use lc_sw_back(Hide("lc_phone_status"))
            text "STATUS":
                style "lc_sw_pixel_bold"
                size 48
                color c["txt"]
                xpos 30
                ypos 96
            text transparency_mode_label().upper():
                style "lc_sw_pixel"
                color c["mut"]
                xpos 420
                ypos 114
            viewport:
                ypos 168
                xysize (642, 800)
                mousewheel True
                draggable True
                scrollbars None
                vbox:
                    spacing 16
                    xpos 24
                    xsize 594
                    if not getattr(persistent, "status_page_intro_seen", False):
                        frame:
                            style "lc_sw_frame"
                            xfill True
                            background Frame(lc_phone_art("card_" + theme), 18, 18)
                            padding (18, 16)
                            vbox:
                                spacing 8
                                text "YOUR LIVE DASHBOARD":
                                    style "lc_sw_pixel_bold"
                                    color c["acc"]
                                text "Status tracks the relationship, [girlfriend_name], and [player_name]. Settings chooses how much of it you can see.":
                                    style "lc_sw_hand"
                                    size 30
                                    color c["txt"]
                                    xmaximum 540
                                textbutton "GOT IT":
                                    style "lc_sw_hit"
                                    xalign 0.0
                                    xfill False
                                    xminimum 200
                                    yminimum 64
                                    padding (32, 16)
                                    background Frame(lc_phone_art("key_berry"), 16, 16)
                                    hover_background Frame(lc_phone_art("key_berry"), 16, 16)
                                    text_font "fonts/Silkscreen-Bold.ttf"
                                    text_size 24
                                    text_antialias False
                                    text_hinting "none"
                                    text_xalign 0.5
                                    text_yalign 0.5
                                    text_color "#faf4e8"
                                    action Function(lc_mark_status_intro_seen)
                    frame:
                        style "lc_sw_frame"
                        xfill True
                        background Frame(lc_phone_art("card_" + theme), 18, 18)
                        padding (18, 16)
                        vbox:
                            spacing 8
                            text "[girlfriend_name] right now":
                                style "lc_sw_pixel_bold"
                                color c["txt"]
                            text "[leia_overview_text()]":
                                style "lc_sw_hand"
                                size 28
                                color c["mut"]
                                xmaximum 540
                    use lc_phone_status_section("RELATIONSHIP", _relationship_rows)
                    use lc_phone_status_section(girlfriend_name.upper(), _leia_rows)
                    use lc_phone_status_section(player_name.upper(), _ryan_rows)
                    if _route_rows:
                        use lc_phone_status_section("ROUTE TENDENCIES", _route_rows)
                    textbutton "OPEN SETTINGS":
                        style "lc_sw_hit"
                        xfill True
                        ysize 54
                        background Frame(lc_phone_art("card_" + theme), 18, 18)
                        hover_background Frame(lc_phone_art("key_berry"), 18, 15)
                        text_font "fonts/Silkscreen-Bold.ttf"
                        text_antialias False
                        text_hinting "none"
                        text_idle_color c["acc"]
                        text_hover_color "#faf4e8"
                        action [Hide("lc_phone_status"), Show("lc_phone_settings")]
                    text "[status_mode_note()]":
                        style "lc_sw_hand"
                        size 28
                        color c["mut"]
                        text_align 0.5
                        xalign 0.5
                        xmaximum 540
                    null height 18
            use lc_sw_home_bar(c["txt"])
        add Transform(lc_phone_art("bezel_" + theme), nearest=True)


screen lc_phone_settings_mode(mode_id):
    $ c = lc_phone_palette()
    $ theme = lc_phone_theme()
    $ _selected = current_choice_mode() == mode_id
    $ _info = transparency_mode_info(mode_id)
    button:
        style "lc_sw_hit"
        xfill True
        yminimum 96
        padding (28, 16)
        background Frame(lc_phone_art("key_berry" if _selected else "card_" + theme), 18, 15)
        hover_background Frame(lc_phone_art("key_berry"), 18, 15)
        action Function(lc_phone_set_information_mode, mode_id)
        vbox:
            spacing 4
            xfill True
            hbox:
                xfill True
                box_align 0.0
                spacing 16
                text _info["label"].upper():
                    style "lc_sw_pixel_bold"
                    color ("#faf4e8" if _selected else c["txt"])
                    yalign 0.5
                if _selected:
                    text "ON":
                        style "lc_sw_pixel_bold"
                        size 18
                        color "#faf4e8"
                        yalign 0.5
            text _info["tagline"]:
                style "lc_sw_hand"
                size 28
                color ("#fbe7d8" if _selected else c["mut"])
            text _info["description"]:
                style "lc_sw_hand"
                size 26
                color ("#fbe7d8" if _selected else c["mut"])
                xmaximum 420


screen lc_phone_settings():
    modal True
    zorder 340
    key "K_ESCAPE" action Hide("lc_phone_settings")

    $ c = lc_phone_palette()
    $ theme = lc_phone_theme()

    use lc_phone_backdrop([Hide("lc_phone_settings"), Hide("phone_screen")])
    fixed:
        xalign 0.5
        yalign 0.5
        xysize (702, 1068)
        use lc_phone_body_blocker
        fixed:
            xpos 30
            ypos 24
            xysize (642, 1020)
            clipping True
            add Solid(c["bg"])
            use lc_sw_status_bar()
            use lc_sw_back(Hide("lc_phone_settings"))
            text "SETTINGS":
                style "lc_sw_pixel_bold"
                size 48
                color c["txt"]
                xpos 36
                ypos 96
            viewport:
                ypos 168
                xysize (642, 800)
                mousewheel True
                draggable True
                scrollbars None
                frame:
                    style "lc_sw_frame"
                    background None
                    xsize 642
                    padding (36, 0, 36, 18)
                    vbox:
                        spacing 12
                        xfill True
                        text "These settings only change what the interface reveals. They never alter stats, story outcomes, or difficulty.":
                            style "lc_sw_hand"
                            size 28
                            color c["mut"]
                            text_align 0.5
                            xalign 0.5
                            xmaximum 540
                        use lc_phone_settings_mode("normal")
                        use lc_phone_settings_mode("insight")
                        use lc_phone_settings_mode("full")
                        use lc_phone_settings_mode("developer")
                        textbutton "OPEN STATUS":
                            style "lc_sw_hit"
                            xfill True
                            ysize 54
                            background Frame(lc_phone_art("card_" + theme), 18, 18)
                            hover_background Frame(lc_phone_art("key_berry"), 18, 15)
                            text_font "fonts/Silkscreen-Bold.ttf"
                            text_antialias False
                            text_hinting "none"
                            text_idle_color c["acc"]
                            text_hover_color "#faf4e8"
                            action [Hide("lc_phone_settings"), Show("lc_phone_status")]
                        if current_choice_mode() == "developer":
                            text "Developer exposes internal IDs, stat keys, route tendencies, and debug information.":
                                style "lc_sw_hand"
                                size 26
                                color c["mut"]
                                xmaximum 540
                        null height 18
            use lc_sw_home_bar(c["txt"])
        add Transform(lc_phone_art("bezel_" + theme), nearest=True)
