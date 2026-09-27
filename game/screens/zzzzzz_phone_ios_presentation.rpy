# ACTIVE PHONE PRESENTATION.
# This late-loading screen intentionally overrides the legacy phone_screen.rpy
# handset layout. Make Phone Messages/Photos/Home presentation changes here.
# zzzzzzz_phone_hardware_polish.rpy owns only the external handset hardware overlay.

# Cohesive mobile-style Phone presentation.
# Presentation only: story/Phone state and app logic remain in the existing systems.
# Final Status / Settings icon art can later replace the placeholder icon tiles.

init 95 python:
    import datetime

    def lc_phone_clock_text():
        return datetime.datetime.now().strftime("%H:%M")


screen lc_phone_extra_apps():
    # Supersedes the temporary bottom Status/Settings dock. Both are now native
    # app tiles inside the main Phone home grid below.
    pass


screen lc_ios_app_tile(app_id, label, subtitle, action, icon_path=None, placeholder_text=None, badge_text=None):
    fixed:
        xsize 172
        ysize 166

        button:
            xfill True
            yfill True
            padding (6, 6)
            background None
            hover_background Frame("gui/phone/rounded_white.png", 24, 24)
            action action

            vbox:
                xalign 0.5
                spacing 5

                fixed:
                    xsize 96
                    ysize 96
                    xalign 0.5

                    if icon_path:
                        add icon_path xysize (92, 92) xalign 0.5 yalign 0.5
                    else:
                        frame:
                            xysize (92, 92)
                            xalign 0.5
                            yalign 0.5
                            background (Frame("gui/phone/rounded_pink.png", 28, 28) if app_id == "status" else Frame("gui/phone/rounded_blue.png", 28, 28))
                            text placeholder_text size (34 if app_id == "status" else 27) color ("#ffffff" if app_id == "status" else "#007aff") bold True xalign 0.5 yalign 0.5

                    if badge_text:
                        frame:
                            xpos 69
                            ypos -4
                            xminimum 27
                            ysize 27
                            padding (7, 2)
                            background Frame("gui/phone/unread_badge.svg", 12, 12)
                            text badge_text size 11 color "#ffffff" bold True xalign 0.5 yalign 0.5

                text label size 16 color "#1c1c1e" bold True xalign 0.5
                text subtitle size 11 color "#6d6d72" xalign 0.5 text_align 0.5 xmaximum 155


screen lc_ios_status_bar():
    fixed:
        xfill True
        ysize 48

        text "[lc_phone_clock_text()]" size 14 color "#1c1c1e" bold True xpos 16 yalign 0.5

        frame:
            xalign 0.5
            yalign 0.5
            xsize 138
            ysize 31
            background Frame("gui/phone/rounded_shell.png", 18, 18)

        hbox:
            xalign 0.965
            yalign 0.5
            spacing 7
            text "•••" size 15 color "#1c1c1e" bold True
            text "Wi-Fi" size 12 color "#1c1c1e"
            frame:
                xsize 30
                ysize 15
                yalign 0.5
                padding (2, 2)
                background Frame("gui/phone/rounded_light.png", 8, 8)
                frame:
                    xfill True
                    yfill True
                    background Solid("#1c1c1e")


screen lc_ios_back_button(label, action, xpos_value=0, ypos_value=0):
    textbutton label:
        xpos xpos_value
        ypos ypos_value
        xminimum 112
        ysize 43
        padding (14, 6)
        background Frame("gui/phone/rounded_white.png", 22, 22)
        hover_background Frame("gui/phone/rounded_blue.png", 22, 22)
        text_idle_color "#007aff"
        text_hover_color "#007aff"
        text_size 15
        text_bold True
        text_xalign 0.5
        text_yalign 0.5
        action action


screen lc_ios_done_button(action, xalign_value=1.0, ypos_value=0):
    textbutton "Done":
        xalign xalign_value
        ypos ypos_value
        xminimum 84
        ysize 43
        padding (14, 6)
        background Frame("gui/phone/rounded_button_blue.png", 22, 22)
        hover_background Frame("gui/phone/rounded_button_blue_hover.png", 22, 22)
        text_idle_color "#ffffff"
        text_hover_color "#ffffff"
        text_size 15
        text_bold True
        text_xalign 0.5
        text_yalign 0.5
        action action


init 96 python:
    def lc_phone_rounded_photo(asset_id, width, height):
        photo = Transform(asset_id, xysize=(width, height), fit="cover")
        mask = Transform("gui/phone/photo_round_mask.svg", xysize=(width, height))
        return AlphaMask(photo, mask)


screen lc_phone_photo_viewer(photo_asset):
    modal True
    zorder 380

    key "K_ESCAPE" action Hide("lc_phone_photo_viewer")
    key "mouseup_3" action Hide("lc_phone_photo_viewer")

    add Solid("#000000")

    if photo_asset and renpy.has_image(photo_asset):
        add photo_asset:
            xalign 0.5
            yalign 0.5
            fit "contain"
            xysize (1920, 1080)

    button:
        xfill True
        yfill True
        background None
        action Hide("lc_phone_photo_viewer")

    textbutton "Done":
        xalign 0.965
        yalign 0.035
        xminimum 100
        ysize 48
        background Frame("gui/phone/rounded_button_blue.png", 22, 22)
        hover_background Frame("gui/phone/rounded_button_blue_hover.png", 22, 22)
        text_idle_color "#ffffff"
        text_hover_color "#ffffff"
        text_size 16
        text_bold True
        text_xalign 0.5
        text_yalign 0.5
        action Hide("lc_phone_photo_viewer")


screen phone_screen():
    modal True
    zorder 310

    default phone_app = "home"
    default phone_thread = None
    default hovered_app = None

    key "K_ESCAPE" action Hide("phone_screen")

    add Solid("#00000066")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1070
        background None
        padding (15, 15)

        fixed:
            xfill True
            yfill True

            frame:
                xfill True
                yfill True
                background Frame("gui/phone/rounded_screen.png", 30, 30)
                padding (18, 12)

                fixed:
                    xfill True
                    yfill True

                    if phone_app == "home":
                        add Solid("#f0eaf2")
                    else:
                        add Solid("#f2f2f7")

                    vbox:
                        spacing 8
                        xfill True
                        yfill True

                        use lc_ios_status_bar

                        fixed:
                            xfill True
                            ysize 98

                            if phone_app != "home":
                                use lc_ios_back_button(("‹ Messages" if phone_app == "thread" else "‹ Back"), [SetScreenVariable("phone_app", "messages") if phone_app == "thread" else SetScreenVariable("phone_app", "home"), SetScreenVariable("phone_thread", None) if phone_app != "thread" else NullAction()], xpos_value=0, ypos_value=2)

                            vbox:
                                xpos 0
                                ypos 50
                                spacing 0

                                if phone_app == "home":
                                    text "Phone" size 34 color "#1c1c1e" bold True
                                    text "Ryan's apps" size 13 color "#6d6d72"
                                elif phone_app == "messages":
                                    text "Messages" size 31 color "#1c1c1e" bold True
                                elif phone_app == "thread":
                                    text "[phone_thread_label(phone_thread)]" size 28 color "#1c1c1e" bold True
                                elif phone_app == "shop":
                                    text "Shop" size 31 color "#1c1c1e" bold True
                                elif phone_app == "photos":
                                    text "Photos" size 31 color "#1c1c1e" bold True
                                elif phone_app == "wallet":
                                    text "Wallet" size 31 color "#1c1c1e" bold True
                                elif phone_app == "delivery":
                                    text "Delivery" size 31 color "#1c1c1e" bold True

                            use lc_ios_done_button(Hide("phone_screen"), xalign_value=1.0, ypos_value=2)

                        if phone_app == "home":
                            $ phone_photo_count = len(phone_photo_items())
                            $ unread_total = phone_total_unread()
                            $ unread_badge = str(unread_total) if unread_total > 0 else None
                            $ status_badge = "!" if not getattr(persistent, "status_page_intro_seen", False) else None

                            frame:
                                xfill True
                                yfill True
                                background Solid("#ffffff00")
                                padding (8, 8)

                                vbox:
                                    spacing 8
                                    xfill True

                                    grid 3 3:
                                        spacing 7
                                        xalign 0.5

                                        use lc_ios_app_tile("messages", "Messages", ("{} unread".format(unread_total) if unread_total else "Conversations"), SetScreenVariable("phone_app", "messages"), icon_path="gui/phone/icons/messages.png", badge_text=unread_badge)
                                        use lc_ios_app_tile("photos", "Photos", ("{} saved".format(phone_photo_count) if phone_photo_count else "Camera roll"), SetScreenVariable("phone_app", "photos"), icon_path="gui/phone/icons/photos.png")
                                        use lc_ios_app_tile("shop", "Shop", "{} items".format(len(shop_outfit_ids())), SetScreenVariable("phone_app", "shop"), icon_path="gui/phone/icons/shop.png")
                                        use lc_ios_app_tile("wallet", "Wallet", "${}".format(money), SetScreenVariable("phone_app", "wallet"), icon_path="gui/phone/icons/wallet.png")
                                        use lc_ios_app_tile("delivery", "Delivery", "Orders", SetScreenVariable("phone_app", "delivery"), icon_path="gui/phone/icons/delivery.png")
                                        use lc_ios_app_tile("status", "Status", "Relationship", Show("lc_phone_status"), placeholder_text="ST", badge_text=status_badge)
                                        use lc_ios_app_tile("settings", "Settings", transparency_mode_label(), Show("lc_phone_settings"), placeholder_text="SET")
                                        null width 172 height 166
                                        null width 172 height 166

                                    if current_choice_mode() == "developer":
                                        frame:
                                            xfill True
                                            background Frame("gui/phone/rounded_white.png", 24, 24)
                                            padding (14, 12)
                                            vbox:
                                                spacing 7
                                                text "DEVELOPER TOOLS" size 12 color "#c53e71" bold True
                                                hbox:
                                                    spacing 8
                                                    textbutton "Seed messages":
                                                        xsize 240
                                                        ysize 40
                                                        background Frame("gui/phone/rounded_light.png", 20, 20)
                                                        hover_background Frame("gui/phone/rounded_blue.png", 20, 20)
                                                        text_idle_color "#1c1c1e"
                                                        text_hover_color "#007aff"
                                                        text_xalign 0.5
                                                        text_yalign 0.5
                                                        action Function(phone_debug_seed_messages)
                                                    textbutton "Clear messages":
                                                        xsize 240
                                                        ysize 40
                                                        background Frame("gui/phone/rounded_light.png", 20, 20)
                                                        hover_background Frame("gui/phone/rounded_blue.png", 20, 20)
                                                        text_idle_color "#1c1c1e"
                                                        text_hover_color "#007aff"
                                                        text_xalign 0.5
                                                        text_yalign 0.5
                                                        action Function(phone_debug_clear_messages)

                        elif phone_app == "messages":
                            viewport:
                                xfill True
                                yfill True
                                mousewheel True
                                draggable True
                                vbox:
                                    spacing 9
                                    xfill True
                                    for thread_id in PHONE_THREAD_ORDER:
                                        $ thread_name = phone_thread_label(thread_id)
                                        $ thread_preview = phone_thread_preview(thread_id)
                                        $ unread_count = phone_thread_unread_count(thread_id)
                                        button:
                                            xfill True
                                            ysize 94
                                            padding (14, 11)
                                            background Frame("gui/phone/rounded_white.png", 25, 25)
                                            hover_background Frame("gui/phone/rounded_blue.png", 25, 25)
                                            action [Function(phone_mark_thread_read, thread_id), SetScreenVariable("phone_thread", thread_id), SetScreenVariable("phone_app", "thread")]
                                            hbox:
                                                spacing 13
                                                xfill True
                                                yalign 0.5
                                                add "gui/phone/icons/messages.png" xysize (54, 54) yalign 0.5
                                                vbox:
                                                    spacing 4
                                                    xfill True
                                                    yalign 0.5
                                                    hbox:
                                                        xfill True
                                                        text "[thread_name]" size 18 color "#1c1c1e" bold (unread_count > 0)
                                                        if unread_count > 0:
                                                            frame:
                                                                xalign 1.0
                                                                xminimum 31
                                                                ysize 26
                                                                padding (7, 2)
                                                                background Frame("gui/phone/unread_badge.svg", 12, 12)
                                                                text "[unread_count]" size 11 color "#ffffff" bold True xalign 0.5 yalign 0.5
                                                    text "[thread_preview]" size 13 color "#6d6d72" xmaximum 435

                        elif phone_app == "thread":
                            $ thread_messages = phone_messages_for_thread(phone_thread)
                            viewport:
                                xfill True
                                yfill True
                                mousewheel True
                                draggable True
                                yinitial 1.0
                                vbox:
                                    spacing 10
                                    xfill True
                                    if not thread_messages:
                                        frame:
                                            xfill True
                                            background Frame("gui/phone/rounded_white.png", 24, 24)
                                            padding (18, 18)
                                            text "No messages yet." size 15 color "#8e8e93" xalign 0.5
                                    for message in thread_messages:
                                        $ message_sender = phone_sender_label(message.get("sender", "system"))
                                        $ from_player = message.get("sender") == "player"
                                        $ message_text = message.get("text", "")
                                        $ attachment_id = message.get("attachment_id")
                                        $ attachment_label = message.get("attachment_label", "Photo attachment")
                                        $ bubble_text = "#ffffff" if from_player else "#1c1c1e"
                                        vbox:
                                            xfill True
                                            spacing 3
                                            if not from_player:
                                                text "[message_sender]" size 11 color "#8e8e93" xalign 0.02
                                            if message_text:
                                                frame:
                                                    xmaximum 460
                                                    xalign (1.0 if from_player else 0.0)
                                                    background (Frame("gui/phone/bubble_outgoing.png", 30, 30) if from_player else Frame("gui/phone/bubble_incoming.png", 30, 30))
                                                    padding ((17, 12, 20, 15) if from_player else (20, 12, 17, 15))
                                                    text "[message_text]" size 16 color bubble_text line_spacing 3
                                            if attachment_id:
                                                vbox:
                                                    xmaximum 460
                                                    xalign (1.0 if from_player else 0.0)
                                                    spacing 4
                                                    if renpy.has_image(attachment_id):
                                                        button:
                                                            xalign (1.0 if from_player else 0.0)
                                                            xysize (430, 242)
                                                            padding (0, 0)
                                                            background None
                                                            hover_background None
                                                            action Show("lc_phone_photo_viewer", photo_asset=attachment_id)
                                                            add lc_phone_rounded_photo(attachment_id, 430, 242)
                                                    else:
                                                        add "gui/phone/icons/photos.png" xysize (72, 72) xalign 0.5
                                                    if current_choice_mode() == "developer":
                                                        text "Asset: [attachment_id]" size 9 color "#8e8e93" xalign 0.5

                        elif phone_app == "shop":
                            frame:
                                xfill True
                                background Frame("gui/phone/rounded_blue.png", 24, 24)
                                padding (14, 12)
                                text "Purchases add outfits to [girlfriend_name]'s Wardrobe. Her willingness to wear them is tracked separately." size 13 color "#2c2c2e" line_spacing 3
                            if last_shop_message:
                                frame:
                                    xfill True
                                    background Frame("gui/phone/rounded_yellow.png", 24, 24)
                                    padding (14, 11)
                                    text "[last_shop_message]" size 13 color "#4a3a16"
                            viewport:
                                xfill True
                                yfill True
                                mousewheel True
                                draggable True
                                vbox:
                                    spacing 11
                                    xfill True
                                    for outfit_id in shop_outfit_ids():
                                        $ phone_outfit = get_outfit(outfit_id)
                                        $ phone_outfit_name = phone_outfit["name"]
                                        $ phone_outfit_description = phone_outfit["description"]
                                        $ phone_outfit_cost = phone_outfit["cost"]
                                        $ phone_outfit_state = shop_item_state(outfit_id)
                                        $ phone_outfit_status = shop_item_status_label(outfit_id)
                                        $ phone_outfit_status_color = shop_item_status_color(outfit_id)
                                        frame:
                                            xfill True
                                            background Frame("gui/phone/rounded_white.png", 24, 24)
                                            padding (15, 14)
                                            vbox:
                                                spacing 8
                                                xfill True
                                                hbox:
                                                    spacing 12
                                                    add "gui/phone/icons/shop.png" xysize (64, 64)
                                                    vbox:
                                                        spacing 3
                                                        xfill True
                                                        text "[phone_outfit_name]" size 18 color "#1c1c1e" bold True
                                                        text "[phone_outfit_description]" size 13 color "#6d6d72" xmaximum 410
                                                    text "$[phone_outfit_cost]" size 16 color "#1c1c1e" bold True xalign 1.0
                                                text "[phone_outfit_status]" size 12 color phone_outfit_status_color
                                                if phone_outfit_state == "available":
                                                    textbutton "Buy for $[phone_outfit_cost]":
                                                        xfill True
                                                        ysize 44
                                                        background Frame("gui/phone/rounded_button_blue.png", 22, 22)
                                                        hover_background Frame("gui/phone/rounded_button_blue_hover.png", 22, 22)
                                                        text_idle_color "#ffffff"
                                                        text_hover_color "#ffffff"
                                                        text_xalign 0.5
                                                        text_yalign 0.5
                                                        action Function(purchase_outfit, outfit_id)
                                                elif phone_outfit_state == "owned":
                                                    textbutton "Owned":
                                                        xfill True
                                                        ysize 42
                                                        background Frame("gui/phone/rounded_green.png", 22, 22)
                                                        text_idle_color "#26734d"
                                                        text_xalign 0.5
                                                        text_yalign 0.5
                                                        sensitive False
                                                else:
                                                    textbutton ("Need $[phone_outfit_cost]" if phone_outfit_state == "insufficient" else "Locked"):
                                                        xfill True
                                                        ysize 42
                                                        background Frame("gui/phone/rounded_light.png", 22, 22)
                                                        text_idle_color "#8e8e93"
                                                        text_xalign 0.5
                                                        text_yalign 0.5
                                                        sensitive False

                        elif phone_app == "photos":
                            $ photo_items = phone_photo_items()
                            if photo_items:
                                viewport:
                                    xfill True
                                    yfill True
                                    mousewheel True
                                    draggable True
                                    vbox:
                                        spacing 10
                                        xfill True
                                        for photo in photo_items:
                                            $ photo_asset = photo.get("asset_id")
                                            $ photo_label = photo.get("label", "Photo")
                                            vbox:
                                                spacing 4
                                                xfill True
                                                if photo_asset and renpy.has_image(photo_asset):
                                                    button:
                                                        xalign 0.5
                                                        xysize (540, 304)
                                                        padding (0, 0)
                                                        background None
                                                        hover_background None
                                                        action Show("lc_phone_photo_viewer", photo_asset=photo_asset)
                                                        fixed:
                                                            xfill True
                                                            yfill True
                                                            clipping True
                                                            add lc_phone_rounded_photo(photo_asset, 540, 304)
                                                else:
                                                    frame:
                                                        xfill True
                                                        ysize 190
                                                        background Frame("gui/phone/rounded_light.png", 22, 22)
                                                        add "gui/phone/icons/photos.png" xysize (96, 96) xalign 0.5 yalign 0.5
                                                if current_choice_mode() == "developer":
                                                    text "Asset: [photo_asset]" size 9 color "#8e8e93" xalign 0.5
                            else:
                                frame:
                                    xfill True
                                    background Frame("gui/phone/rounded_white.png", 26, 26)
                                    padding (25, 25)
                                    vbox:
                                        spacing 14
                                        add "gui/phone/icons/photos.png" xysize (110, 110) xalign 0.5
                                        text "Your Photos" size 23 color "#1c1c1e" bold True xalign 0.5
                                        text "Story photos and received image attachments collect here automatically." size 14 color "#6d6d72" text_align 0.5 xalign 0.5 line_spacing 4

                        elif phone_app == "wallet":
                            frame:
                                xfill True
                                background Frame("gui/phone/rounded_white.png", 26, 26)
                                padding (26, 26)
                                vbox:
                                    spacing 13
                                    add "gui/phone/icons/wallet.png" xysize (104, 104) xalign 0.5
                                    text "AVAILABLE MONEY" size 12 color "#8e8e93" xalign 0.5
                                    text "$[money]" size 42 color "#1c1c1e" bold True xalign 0.5
                                    if last_money_reason:
                                        frame:
                                            xfill True
                                            background Frame("gui/phone/rounded_light.png", 22, 22)
                                            padding (14, 12)
                                            vbox:
                                                spacing 4
                                                text "Last change: [last_money_change]" size 14 color "#3a3a3c" xalign 0.5
                                                text "[last_money_reason]" size 13 color "#8e8e93" xalign 0.5

                        elif phone_app == "delivery":
                            frame:
                                xfill True
                                background Frame("gui/phone/rounded_white.png", 26, 26)
                                padding (26, 26)
                                vbox:
                                    spacing 14
                                    add "gui/phone/icons/delivery.png" xysize (112, 112) xalign 0.5
                                    text "No Active Deliveries" size 22 color "#1c1c1e" bold True xalign 0.5
                                    text "Orders will appear here when story delivery events are introduced." size 14 color "#6d6d72" text_align 0.5 xalign 0.5 line_spacing 4

                    frame:
                        xalign 0.5
                        yalign 0.995
                        xsize 126
                        ysize 5
                        background Frame("gui/phone/rounded_shell.png", 10, 10)


screen lc_phone_status_row(row):
    vbox:
        spacing 5
        xfill True
        hbox:
            xfill True
            text row["label"] size 14 color "#1c1c1e" bold True
            if row["detail"]:
                text row["detail"] size 12 color "#6d6d72" xalign 1.0
        bar:
            value StaticValue(row["value"], 100)
            xfill True
            ysize 9
            left_bar Solid("#cc5d91")
            right_bar Solid("#dedee3")
        if row["internal_key"]:
            text row["internal_key"] size 9 color "#8e8e93"


screen lc_phone_status_section(title, rows):
    frame:
        xfill True
        background Frame("gui/phone/rounded_white.png", 24, 24)
        padding (16, 14)
        vbox:
            spacing 11
            xfill True
            text title size 13 color "#8e8e93" bold True
            for row in rows:
                use lc_phone_status_row(row)


screen lc_phone_status():
    modal True
    zorder 340
    key "K_ESCAPE" action Hide("lc_phone_status")

    $ _mode = current_choice_mode()
    $ _relationship_rows = status_relationship_rows(_mode)
    $ _leia_rows = status_leia_rows(_mode)
    $ _ryan_rows = status_ryan_rows(_mode)
    $ _route_rows = status_route_rows(_mode)

    add Solid("#00000066")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1070
        background None
        padding (15, 15)

        frame:
            xfill True
            yfill True
            background Frame("gui/phone/rounded_screen.png", 30, 30)
            padding (18, 12)

            vbox:
                spacing 8
                xfill True
                yfill True
                use lc_ios_status_bar

                fixed:
                    xfill True
                    ysize 100
                    use lc_ios_back_button("‹ Phone", Hide("lc_phone_status"), xpos_value=0, ypos_value=2)
                    use lc_ios_done_button(Hide("lc_phone_status"), xalign_value=1.0, ypos_value=2)
                    vbox:
                        ypos 51
                        spacing 0
                        text "Status" size 31 color "#1c1c1e" bold True
                        text "[transparency_mode_label()] visibility" size 12 color "#6d6d72"

                viewport:
                    xfill True
                    yfill True
                    mousewheel True
                    draggable True
                    vbox:
                        spacing 11
                        xfill True

                        if not getattr(persistent, "status_page_intro_seen", False):
                            frame:
                                xfill True
                                background Frame("gui/phone/rounded_blue.png", 24, 24)
                                padding (16, 14)
                                vbox:
                                    spacing 7
                                    text "YOUR LIVE DASHBOARD" size 13 color "#007aff" bold True
                                    text "Status tracks the relationship, Leia's developing traits, and Ryan's mindset. What you can see depends on Settings." size 13 color "#2c2c2e" line_spacing 3
                                    textbutton "Got it":
                                        xfill True
                                        ysize 41
                                        background Frame("gui/phone/rounded_button_blue.png", 22, 22)
                                        hover_background Frame("gui/phone/rounded_button_blue_hover.png", 22, 22)
                                        text_idle_color "#ffffff"
                                        text_hover_color "#ffffff"
                                        text_xalign 0.5
                                        text_yalign 0.5
                                        action Function(lc_mark_status_intro_seen)

                        frame:
                            xfill True
                            background Frame("gui/phone/rounded_white.png", 24, 24)
                            padding (16, 14)
                            vbox:
                                spacing 5
                                text "[girlfriend_name] right now" size 17 color "#1c1c1e" bold True
                                text "[leia_overview_text()]" size 13 color "#5f5f64" line_spacing 3

                        use lc_phone_status_section("RELATIONSHIP", _relationship_rows)
                        use lc_phone_status_section(girlfriend_name.upper(), _leia_rows)
                        use lc_phone_status_section(player_name.upper(), _ryan_rows)
                        if _route_rows:
                            use lc_phone_status_section("ROUTE TENDENCIES", _route_rows)

                        textbutton "Open Settings":
                            xfill True
                            ysize 46
                            background Frame("gui/phone/rounded_white.png", 22, 22)
                            hover_background Frame("gui/phone/rounded_blue.png", 22, 22)
                            text_idle_color "#007aff"
                            text_hover_color "#007aff"
                            text_xalign 0.5
                            text_yalign 0.5
                            action [Hide("lc_phone_status"), Show("lc_phone_settings")]

                        text "[status_mode_note()]" size 11 color "#8e8e93" text_align 0.5 xalign 0.5
                        null height 12

                frame:
                    xalign 0.5
                    xsize 126
                    ysize 5
                    background Frame("gui/phone/rounded_shell.png", 10, 10)


screen lc_phone_settings_mode(mode_id):
    $ _selected = current_choice_mode() == mode_id
    $ _info = transparency_mode_info(mode_id)

    button:
        xfill True
        yminimum 88
        padding (16, 12)
        background Frame("gui/phone/rounded_white.png", 24, 24)
        hover_background Frame("gui/phone/rounded_blue.png", 24, 24)
        action Function(lc_phone_set_information_mode, mode_id)

        hbox:
            spacing 12
            xfill True
            yalign 0.5
            frame:
                xsize 42
                ysize 42
                background (Frame("gui/phone/rounded_pink.png", 18, 18) if _selected else Frame("gui/phone/rounded_light.png", 18, 18))
                text ("✓" if _selected else "") size 21 color "#ffffff" bold True xalign 0.5 yalign 0.5
            vbox:
                spacing 3
                xfill True
                text _info["label"] size 17 color "#1c1c1e" bold True
                text _info["tagline"] size 12 color "#5f5f64"
                text _info["description"] size 11 color "#8e8e93" line_spacing 2 xmaximum 430


screen lc_phone_settings():
    modal True
    zorder 340
    key "K_ESCAPE" action Hide("lc_phone_settings")

    add Solid("#00000066")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1070
        background None
        padding (15, 15)

        frame:
            xfill True
            yfill True
            background Frame("gui/phone/rounded_screen.png", 30, 30)
            padding (18, 12)

            vbox:
                spacing 8
                xfill True
                yfill True
                use lc_ios_status_bar

                fixed:
                    xfill True
                    ysize 100
                    use lc_ios_back_button("‹ Phone", Hide("lc_phone_settings"), xpos_value=0, ypos_value=2)
                    use lc_ios_done_button(Hide("lc_phone_settings"), xalign_value=1.0, ypos_value=2)
                    vbox:
                        ypos 51
                        spacing 0
                        text "Settings" size 31 color "#1c1c1e" bold True
                        text "Information visibility" size 12 color "#6d6d72"

                frame:
                    xfill True
                    background Frame("gui/phone/rounded_blue.png", 24, 24)
                    padding (14, 12)
                    text "These settings only change what the interface reveals. They never alter stats, story outcomes, or difficulty." size 12 color "#5f5f64" text_align 0.5 xalign 0.5 line_spacing 3

                viewport:
                    xfill True
                    yfill True
                    mousewheel True
                    draggable True
                    vbox:
                        spacing 9
                        xfill True
                        use lc_phone_settings_mode("normal")
                        use lc_phone_settings_mode("insight")
                        use lc_phone_settings_mode("full")
                        use lc_phone_settings_mode("developer")

                        textbutton "Open Status":
                            xfill True
                            ysize 46
                            background Frame("gui/phone/rounded_white.png", 22, 22)
                            hover_background Frame("gui/phone/rounded_blue.png", 22, 22)
                            text_idle_color "#007aff"
                            text_hover_color "#007aff"
                            text_xalign 0.5
                            text_yalign 0.5
                            action [Hide("lc_phone_settings"), Show("lc_phone_status")]

                        if current_choice_mode() == "developer":
                            frame:
                                xfill True
                                background Frame("gui/phone/rounded_yellow.png", 22, 22)
                                padding (14, 12)
                                text "Developer exposes internal IDs, stat keys, route tendencies, and debug information. It is intended for testing rather than a first blind playthrough." size 11 color "#4a3a16" line_spacing 3

                        null height 12

                frame:
                    xalign 0.5
                    xsize 126
                    ysize 5
                    background Frame("gui/phone/rounded_shell.png", 10, 10)
