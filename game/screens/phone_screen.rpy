# Diegetic in-game phone hub.
# Bright, playful phone presentation with familiar modern mobile UI patterns.

init python:
    if "phone_quick_access" not in config.overlay_screens:
        config.overlay_screens.append("phone_quick_access")


screen phone_screen():

    modal True
    zorder 310

    default phone_app = "home"
    default phone_thread = None
    default hovered_app = None

    key "K_ESCAPE" action Hide("phone_screen")

    # Keep the world visible behind the handset while making the phone easy to read.
    add Solid("#00000066")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 660
        ysize 1010
        background Solid("#e9e9ee")
        padding (14, 14)

        vbox:
            spacing 8
            xfill True
            yfill True

            # Fictional handset speaker / camera area.
            fixed:
                xfill True
                ysize 28

                frame:
                    xalign 0.5
                    yalign 0.5
                    xsize 126
                    ysize 9
                    background Solid("#b9bac2")

                frame:
                    xpos 518
                    yalign 0.5
                    xsize 12
                    ysize 12
                    background Solid("#c4c5cc")

            frame:
                xfill True
                yfill True
                background Solid("#f7f7fa")
                padding (22, 18)

                vbox:
                    spacing 14
                    xfill True
                    yfill True

                    # App header.
                    fixed:
                        xfill True
                        ysize 74

                        vbox:
                            xpos 0
                            ypos 2
                            spacing 1

                            text "LEIA'S CONSENT" size 13 color "#8e8e93"

                            if phone_app == "home":
                                text "Phone" size 30 color "#1c1c1e" bold True
                            elif phone_app == "messages":
                                text "Messages" size 30 color "#1c1c1e" bold True
                            elif phone_app == "thread":
                                text "[phone_thread_label(phone_thread)]" size 27 color "#1c1c1e" bold True
                            elif phone_app == "shop":
                                text "Shop" size 30 color "#1c1c1e" bold True
                            elif phone_app == "photos":
                                text "Photos" size 30 color "#1c1c1e" bold True
                            elif phone_app == "wallet":
                                text "Wallet" size 30 color "#1c1c1e" bold True
                            elif phone_app == "delivery":
                                text "Delivery" size 30 color "#1c1c1e" bold True

                        vbox:
                            xalign 1.0
                            ypos 1
                            spacing 5

                            text "$[money]" size 16 color "#3a3a3c" xalign 1.0
                            textbutton "Close":
                                xalign 1.0
                                background None
                                hover_background None
                                text_idle_color "#007aff"
                                text_hover_color "#5ac8fa"
                                action Hide("phone_screen")

                    if phone_app != "home":
                        textbutton ("‹ Messages" if phone_app == "thread" else "‹ Phone"):
                            background None
                            hover_background None
                            text_idle_color "#007aff"
                            text_hover_color "#5ac8fa"
                            text_size 17
                            action [
                                SetScreenVariable("phone_app", "messages") if phone_app == "thread" else SetScreenVariable("phone_app", "home"),
                                SetScreenVariable("phone_thread", None) if phone_app != "thread" else NullAction(),
                            ]

                    if phone_app == "home":

                        text "Ryan's apps" size 14 color "#8e8e93" xalign 0.5

                        grid 3 2:
                            spacing 12
                            xalign 0.5

                            fixed:
                                xsize 180
                                ysize 205

                                if hovered_app == "messages":
                                    add "gui/phone/icon_glow.svg" xysize (132, 132) xalign 0.5 ypos -1
                                    add "gui/phone/icons/messages.png" xysize (118, 118) xalign 0.5 ypos 6
                                else:
                                    add "gui/phone/icons/messages.png" xysize (108, 108) xalign 0.5 ypos 11

                                text "Messages" size 18 color "#1c1c1e" xalign 0.5 ypos 132
                                if phone_total_unread() > 0:
                                    text "● [phone_unread_badge_label()] unread" size 13 color "#ff3b30" xalign 0.5 ypos 160
                                else:
                                    text "No unread" size 12 color "#8e8e93" xalign 0.5 ypos 160

                                button:
                                    xfill True
                                    yfill True
                                    background None
                                    hover_background None
                                    action SetScreenVariable("phone_app", "messages")
                                    hovered SetScreenVariable("hovered_app", "messages")
                                    unhovered SetScreenVariable("hovered_app", None)

                            fixed:
                                xsize 180
                                ysize 205

                                if hovered_app == "photos":
                                    add "gui/phone/icon_glow.svg" xysize (132, 132) xalign 0.5 ypos -1
                                    add "gui/phone/icons/photos.png" xysize (118, 118) xalign 0.5 ypos 6
                                else:
                                    add "gui/phone/icons/photos.png" xysize (108, 108) xalign 0.5 ypos 11

                                text "Photos" size 18 color "#1c1c1e" xalign 0.5 ypos 132
                                text "Camera roll" size 12 color "#8e8e93" xalign 0.5 ypos 160

                                button:
                                    xfill True
                                    yfill True
                                    background None
                                    hover_background None
                                    action SetScreenVariable("phone_app", "photos")
                                    hovered SetScreenVariable("hovered_app", "photos")
                                    unhovered SetScreenVariable("hovered_app", None)

                            fixed:
                                xsize 180
                                ysize 205

                                if hovered_app == "shop":
                                    add "gui/phone/icon_glow.svg" xysize (132, 132) xalign 0.5 ypos -1
                                    add "gui/phone/icons/shop.png" xysize (118, 118) xalign 0.5 ypos 6
                                else:
                                    add "gui/phone/icons/shop.png" xysize (108, 108) xalign 0.5 ypos 11

                                text "Shop" size 18 color "#1c1c1e" xalign 0.5 ypos 132
                                text "[len(shop_outfit_ids())] items" size 12 color "#8e8e93" xalign 0.5 ypos 160

                                button:
                                    xfill True
                                    yfill True
                                    background None
                                    hover_background None
                                    action SetScreenVariable("phone_app", "shop")
                                    hovered SetScreenVariable("hovered_app", "shop")
                                    unhovered SetScreenVariable("hovered_app", None)

                            fixed:
                                xsize 180
                                ysize 205

                                if hovered_app == "wallet":
                                    add "gui/phone/icon_glow.svg" xysize (132, 132) xalign 0.5 ypos -1
                                    add "gui/phone/icons/wallet.png" xysize (118, 118) xalign 0.5 ypos 6
                                else:
                                    add "gui/phone/icons/wallet.png" xysize (108, 108) xalign 0.5 ypos 11

                                text "Wallet" size 18 color "#1c1c1e" xalign 0.5 ypos 132
                                text "$[money]" size 12 color "#8e8e93" xalign 0.5 ypos 160

                                button:
                                    xfill True
                                    yfill True
                                    background None
                                    hover_background None
                                    action SetScreenVariable("phone_app", "wallet")
                                    hovered SetScreenVariable("hovered_app", "wallet")
                                    unhovered SetScreenVariable("hovered_app", None)

                            fixed:
                                xsize 180
                                ysize 205

                                if hovered_app == "delivery":
                                    add "gui/phone/icon_glow.svg" xysize (132, 132) xalign 0.5 ypos -1
                                    add "gui/phone/icons/delivery.png" xysize (118, 118) xalign 0.5 ypos 6
                                else:
                                    add "gui/phone/icons/delivery.png" xysize (108, 108) xalign 0.5 ypos 11

                                text "Delivery" size 18 color "#1c1c1e" xalign 0.5 ypos 132
                                text "Orders" size 12 color "#8e8e93" xalign 0.5 ypos 160

                                button:
                                    xfill True
                                    yfill True
                                    background None
                                    hover_background None
                                    action SetScreenVariable("phone_app", "delivery")
                                    hovered SetScreenVariable("hovered_app", "delivery")
                                    unhovered SetScreenVariable("hovered_app", None)

                            null width 180 height 205

                        if current_choice_mode() == "developer":
                            frame:
                                xfill True
                                background Solid("#fff0f5")
                                padding (16, 14)

                                vbox:
                                    spacing 8
                                    text "DEVELOPER PHONE TOOLS" size 14 color "#c53e71" bold True
                                    textbutton "Add placeholder messages + image attachment":
                                        background None
                                        hover_background Solid("#ffe3ee")
                                        text_idle_color "#1c1c1e"
                                        text_hover_color "#007aff"
                                        action Function(phone_debug_seed_messages)
                                    textbutton "Clear all phone messages":
                                        background None
                                        hover_background Solid("#ffe3ee")
                                        text_idle_color "#1c1c1e"
                                        text_hover_color "#007aff"
                                        action Function(phone_debug_clear_messages)

                    elif phone_app == "messages":

                        viewport:
                            xfill True
                            yfill True
                            mousewheel True
                            draggable True
                            scrollbars "vertical"

                            vbox:
                                spacing 1
                                xfill True

                                for thread_id in PHONE_THREAD_ORDER:
                                    $ thread_name = phone_thread_label(thread_id)
                                    $ thread_preview = phone_thread_preview(thread_id)
                                    $ unread_count = phone_thread_unread_count(thread_id)

                                    button:
                                        xfill True
                                        ysize 94
                                        padding (10, 10)
                                        background (Solid("#f0f7ff") if unread_count > 0 else Solid("#ffffff"))
                                        hover_background Solid("#e8f2ff")
                                        action [
                                            Function(phone_mark_thread_read, thread_id),
                                            SetScreenVariable("phone_thread", thread_id),
                                            SetScreenVariable("phone_app", "thread"),
                                        ]

                                        hbox:
                                            spacing 12
                                            xfill True
                                            yalign 0.5

                                            add "gui/phone/icons/messages.png" xysize (54, 54) yalign 0.5

                                            vbox:
                                                spacing 4
                                                xfill True
                                                yalign 0.5

                                                hbox:
                                                    xfill True
                                                    text "[thread_name]" size 19 color "#1c1c1e" bold (unread_count > 0)
                                                    if unread_count > 0:
                                                        frame:
                                                            xalign 1.0
                                                            background Solid("#ff3b30")
                                                            padding (8, 3)
                                                            text "[unread_count]" size 12 color "#ffffff" bold True

                                                text "[thread_preview]" size 14 color "#6d6d72" max_width 430

                    elif phone_app == "thread":

                        $ thread_messages = phone_messages_for_thread(phone_thread)

                        viewport:
                            xfill True
                            yfill True
                            mousewheel True
                            draggable True
                            scrollbars "vertical"
                            yinitial 1.0

                            vbox:
                                spacing 12
                                xfill True

                                if not thread_messages:
                                    frame:
                                        xfill True
                                        background Solid("#ffffff")
                                        padding (18, 18)
                                        text "No messages yet." size 15 color "#8e8e93" xalign 0.5

                                for message in thread_messages:
                                    $ message_sender = phone_sender_label(message.get("sender", "system"))
                                    $ from_player = message.get("sender") == "player"
                                    $ message_text = message.get("text", "")
                                    $ attachment_id = message.get("attachment_id")
                                    $ attachment_label = message.get("attachment_label", "Photo attachment")
                                    $ bubble_bg = Solid("#0a84ff") if from_player else Solid("#e9e9eb")
                                    $ bubble_text = "#ffffff" if from_player else "#1c1c1e"

                                    vbox:
                                        xfill True
                                        spacing 4

                                        if not from_player:
                                            text "[message_sender]" size 12 color "#8e8e93" xalign 0.0

                                        frame:
                                            xmaximum 455
                                            xalign (1.0 if from_player else 0.0)
                                            background bubble_bg
                                            padding (15, 11)

                                            vbox:
                                                spacing 8

                                                if message_text:
                                                    text "[message_text]" size 16 color bubble_text line_spacing 3

                                                if attachment_id:
                                                    frame:
                                                        xfill True
                                                        ysize 176
                                                        background Solid("#ffffff")
                                                        padding (14, 12)

                                                        vbox:
                                                            xalign 0.5
                                                            yalign 0.5
                                                            spacing 7
                                                            add "gui/phone/icons/photos.png" xysize (72, 72) xalign 0.5
                                                            text "[attachment_label]" size 13 color "#3a3a3c" xalign 0.5
                                                            if current_choice_mode() == "developer":
                                                                text "Asset: [attachment_id]" size 10 color "#8e8e93" xalign 0.5

                    elif phone_app == "shop":

                        frame:
                            xfill True
                            background Solid("#eaf4ff")
                            padding (15, 13)
                            text "Buying adds an outfit to [girlfriend_name]'s Wardrobe. Whether she wants to wear it is handled separately." size 14 color "#2c2c2e" line_spacing 3

                        if last_shop_message:
                            frame:
                                xfill True
                                background Solid("#fff5d9")
                                padding (14, 11)
                                text "[last_shop_message]" size 14 color "#4a3a16"

                        viewport:
                            xfill True
                            yfill True
                            mousewheel True
                            draggable True
                            scrollbars "vertical"

                            vbox:
                                spacing 12
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
                                        background Solid("#ffffff")
                                        padding (16, 15)

                                        vbox:
                                            spacing 9
                                            xfill True

                                            frame:
                                                xfill True
                                                ysize 118
                                                background Solid("#f2f2f7")
                                                padding (10, 10)

                                                vbox:
                                                    xalign 0.5
                                                    yalign 0.5
                                                    spacing 4
                                                    add "gui/phone/icons/shop.png" xysize (66, 66) xalign 0.5
                                                    if current_choice_mode() == "developer":
                                                        text "[phone_outfit['asset_id']]" size 9 color "#8e8e93" xalign 0.5

                                            hbox:
                                                xfill True
                                                text "[phone_outfit_name]" size 19 color "#1c1c1e" bold True
                                                text "$[phone_outfit_cost]" size 17 color "#1c1c1e" xalign 1.0

                                            text "[phone_outfit_description]" size 14 color "#6d6d72" line_spacing 2
                                            text "[phone_outfit_status]" size 13 color phone_outfit_status_color

                                            if phone_outfit_state == "available":
                                                textbutton "Buy for $[phone_outfit_cost]":
                                                    xfill True
                                                    ysize 46
                                                    background Solid("#0a84ff")
                                                    hover_background Solid("#409cff")
                                                    text_idle_color "#ffffff"
                                                    text_hover_color "#ffffff"
                                                    text_xalign 0.5
                                                    action Function(purchase_outfit, outfit_id)
                                            elif phone_outfit_state == "insufficient":
                                                textbutton "Need $[phone_outfit_cost] — You have $[money]":
                                                    xfill True
                                                    ysize 46
                                                    background Solid("#d1d1d6")
                                                    text_idle_color "#8e8e93"
                                                    text_xalign 0.5
                                                    sensitive False
                                            elif phone_outfit_state == "owned":
                                                textbutton "Owned":
                                                    xfill True
                                                    ysize 46
                                                    background Solid("#d1f2df")
                                                    text_idle_color "#26734d"
                                                    text_xalign 0.5
                                                    sensitive False
                                            else:
                                                textbutton "Locked":
                                                    xfill True
                                                    ysize 46
                                                    background Solid("#e5e5ea")
                                                    text_idle_color "#8e8e93"
                                                    text_xalign 0.5
                                                    sensitive False

                    elif phone_app == "photos":

                        frame:
                            xfill True
                            background Solid("#ffffff")
                            padding (24, 24)

                            vbox:
                                spacing 14
                                add "gui/phone/icons/photos.png" xysize (118, 118) xalign 0.5
                                text "Your Photos" size 24 color "#1c1c1e" bold True xalign 0.5
                                text "Story photos and received image attachments will collect here as they are unlocked." size 15 color "#6d6d72" text_align 0.5 xalign 0.5 line_spacing 4
                                frame:
                                    xfill True
                                    background Solid("#f2f2f7")
                                    padding (16, 14)
                                    text "No photos yet." size 14 color "#8e8e93" xalign 0.5

                    elif phone_app == "wallet":

                        frame:
                            xfill True
                            background Solid("#ffffff")
                            padding (24, 24)

                            vbox:
                                spacing 14
                                add "gui/phone/icons/wallet.png" xysize (118, 118) xalign 0.5
                                text "AVAILABLE MONEY" size 14 color "#8e8e93" xalign 0.5
                                text "$[money]" size 42 color "#1c1c1e" bold True xalign 0.5

                                if last_money_reason:
                                    frame:
                                        xfill True
                                        background Solid("#f2f2f7")
                                        padding (14, 12)
                                        vbox:
                                            spacing 4
                                            text "Last change: [last_money_change]" size 15 color "#3a3a3c" xalign 0.5
                                            text "[last_money_reason]" size 14 color "#8e8e93" xalign 0.5
                                else:
                                    text "No transactions recorded yet." size 14 color "#8e8e93" xalign 0.5

                    elif phone_app == "delivery":

                        frame:
                            xfill True
                            background Solid("#ffffff")
                            padding (24, 24)

                            vbox:
                                spacing 14
                                add "gui/phone/icons/delivery.png" xysize (128, 128) xalign 0.5
                                text "No Active Deliveries" size 23 color "#1c1c1e" bold True xalign 0.5
                                text "Orders from the Shop will appear here when delivery events are introduced." size 15 color "#6d6d72" text_align 0.5 xalign 0.5 line_spacing 4
                                frame:
                                    xfill True
                                    background Solid("#f2f2f7")
                                    padding (16, 14)
                                    text "Nothing on the way." size 14 color "#8e8e93" xalign 0.5

            # Familiar mobile home indicator instead of developer footer text.
            fixed:
                xfill True
                ysize 18

                frame:
                    xalign 0.5
                    yalign 0.5
                    xsize 118
                    ysize 5
                    background Solid("#b7b7bd")
