# Diegetic in-game phone hub.
# Core app logic remains lightweight; presentation uses the custom icon set.

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

    add Solid("#000000aa")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 660
        ysize 1010
        background Solid("#0d0b0f")
        padding (16, 16)

        vbox:
            spacing 10
            xfill True
            yfill True

            # Simple fictional handset speaker / camera area.
            hbox:
                xfill True
                ysize 26

                null width 240

                frame:
                    xsize 130
                    ysize 10
                    yalign 0.5
                    background Solid("#29232b")

                frame:
                    xsize 12
                    ysize 12
                    yalign 0.5
                    xoffset 12
                    background Solid("#3b323d")

            frame:
                xfill True
                yfill True
                background Solid("#19151d")
                padding (24, 20)

                vbox:
                    spacing 16
                    xfill True
                    yfill True

                    hbox:
                        xfill True

                        vbox:
                            spacing 2
                            text "LEIA'S CONSENT" size 16 color "#a99ba8"
                            if phone_app == "home":
                                text "PHONE" size 30 color "#ffffff"
                            elif phone_app == "messages":
                                text "MESSAGES" size 30 color "#ffffff"
                            elif phone_app == "thread":
                                text "[phone_thread_label(phone_thread)]" size 30 color "#ffffff"
                            elif phone_app == "shop":
                                text "ONLINE SHOP" size 30 color "#ffffff"
                            elif phone_app == "photos":
                                text "PHOTOS" size 30 color "#ffffff"
                            elif phone_app == "wallet":
                                text "WALLET" size 30 color "#ffffff"
                            elif phone_app == "delivery":
                                text "DELIVERIES" size 30 color "#ffffff"

                        vbox:
                            xalign 1.0
                            spacing 4

                            text "$[money]" size 18 color "#ffffff" xalign 1.0
                            textbutton "Close":
                                xalign 1.0
                                action Hide("phone_screen")

                    if phone_app != "home":
                        textbutton "← Back":
                            action [
                                SetScreenVariable("phone_app", "messages") if phone_app == "thread" else SetScreenVariable("phone_app", "home"),
                                SetScreenVariable("phone_thread", None) if phone_app != "thread" else NullAction(),
                            ]

                    if phone_app == "home":

                        text "Ryan's apps" size 15 color "#a99ba8" xalign 0.5

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

                                text "Messages" size 18 color "#ffffff" xalign 0.5 ypos 132
                                if phone_total_unread() > 0:
                                    text "● [phone_unread_badge_label()] unread" size 13 color "#f06b70" xalign 0.5 ypos 160
                                else:
                                    text "No unread" size 12 color "#857987" xalign 0.5 ypos 160

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

                                text "Photos" size 18 color "#ffffff" xalign 0.5 ypos 132
                                text "Camera roll" size 12 color "#857987" xalign 0.5 ypos 160

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

                                text "Shop" size 18 color "#ffffff" xalign 0.5 ypos 132
                                text "[len(shop_outfit_ids())] items" size 12 color "#857987" xalign 0.5 ypos 160

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

                                text "Wallet" size 18 color "#ffffff" xalign 0.5 ypos 132
                                text "$[money]" size 12 color "#857987" xalign 0.5 ypos 160

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

                                text "Delivery" size 18 color "#ffffff" xalign 0.5 ypos 132
                                text "Orders" size 12 color "#857987" xalign 0.5 ypos 160

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
                                background Solid("#2a2027")
                                padding (16, 14)

                                vbox:
                                    spacing 8
                                    text "DEVELOPER PHONE TOOLS" size 15 color "#f1a8c8"
                                    textbutton "Add placeholder messages + image attachment":
                                        action Function(phone_debug_seed_messages)
                                    textbutton "Clear all phone messages":
                                        action Function(phone_debug_clear_messages)

                    elif phone_app == "messages":

                        text "Threads use stable internal IDs, so renamed characters still display correctly." size 14 color "#a99ba8"

                        viewport:
                            xfill True
                            yfill True
                            mousewheel True
                            draggable True
                            scrollbars "vertical"

                            vbox:
                                spacing 12
                                xfill True

                                for thread_id in PHONE_THREAD_ORDER:
                                    $ thread_name = phone_thread_label(thread_id)
                                    $ thread_preview = phone_thread_preview(thread_id)
                                    $ unread_count = phone_thread_unread_count(thread_id)

                                    button:
                                        xfill True
                                        padding (18, 16)
                                        background (Solid("#352735") if unread_count > 0 else Solid("#242027"))
                                        hover_background Solid("#3a303b")
                                        action [
                                            Function(phone_mark_thread_read, thread_id),
                                            SetScreenVariable("phone_thread", thread_id),
                                            SetScreenVariable("phone_app", "thread"),
                                        ]

                                        vbox:
                                            spacing 6
                                            xfill True

                                            hbox:
                                                xfill True
                                                text "[thread_name]" size 21 color "#ffffff"
                                                if unread_count > 0:
                                                    text "[unread_count] NEW" size 13 color "#f1a8c8" xalign 1.0

                                            text "[thread_preview]" size 14 color "#b8a8b5"

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
                                        background Solid("#242027")
                                        padding (18, 18)
                                        text "No messages yet. Story messages will appear here as the relationship develops." size 15 color "#b8a8b5"

                                for message in thread_messages:
                                    $ message_sender = phone_sender_label(message.get("sender", "system"))
                                    $ from_player = message.get("sender") == "player"
                                    $ message_text = message.get("text", "")
                                    $ attachment_id = message.get("attachment_id")
                                    $ attachment_label = message.get("attachment_label", "Photo attachment")

                                    frame:
                                        xmaximum 470
                                        xalign (1.0 if from_player else 0.0)
                                        background (Solid("#3a2a38") if from_player else Solid("#272229"))
                                        padding (16, 13)

                                        vbox:
                                            spacing 7
                                            xfill True

                                            text "[message_sender]" size 13 color "#f1a8c8"

                                            if message_text:
                                                text "[message_text]" size 16 color "#ffffff" line_spacing 3

                                            if attachment_id:
                                                frame:
                                                    xfill True
                                                    ysize 210
                                                    background Solid("#18151b")
                                                    padding (14, 14)

                                                    vbox:
                                                        xalign 0.5
                                                        yalign 0.5
                                                        spacing 8
                                                        add "gui/phone/icons/photos.png" xysize (70, 70) xalign 0.5
                                                        text "[attachment_label]" size 13 color "#a99ba8" xalign 0.5
                                                        text "Asset: [attachment_id]" size 11 color "#776d77" xalign 0.5

                    elif phone_app == "shop":

                        frame:
                            xfill True
                            background Solid("#2a242d")
                            padding (15, 13)
                            text "Buying an outfit only adds it to [girlfriend_name]'s Wardrobe. Her willingness to wear it remains a separate mechanic." size 14 color "#e1d6df" line_spacing 3

                        if last_shop_message:
                            frame:
                                xfill True
                                background Solid("#30242e")
                                padding (14, 11)
                                text "[last_shop_message]" size 14 color "#eadde7"

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
                                        background Solid("#242027")
                                        padding (16, 15)

                                        vbox:
                                            spacing 9
                                            xfill True

                                            frame:
                                                xfill True
                                                ysize 125
                                                background Solid("#1b171e")
                                                padding (10, 10)

                                                vbox:
                                                    xalign 0.5
                                                    yalign 0.5
                                                    spacing 5
                                                    add "gui/phone/icons/shop.png" xysize (68, 68) xalign 0.5
                                                    text "[phone_outfit['asset_id']]" size 10 color "#817681" xalign 0.5

                                            hbox:
                                                xfill True
                                                text "[phone_outfit_name]" size 20 color "#ffffff"
                                                text "$[phone_outfit_cost]" size 18 color "#ffffff" xalign 1.0

                                            text "[phone_outfit_description]" size 14 color "#b8a8b5" line_spacing 2
                                            text "[phone_outfit_status]" size 13 color phone_outfit_status_color

                                            if phone_outfit_state == "available":
                                                textbutton "Buy for $[phone_outfit_cost]":
                                                    xfill True
                                                    action Function(purchase_outfit, outfit_id)
                                            elif phone_outfit_state == "insufficient":
                                                textbutton "Need $[phone_outfit_cost] — You have $[money]":
                                                    xfill True
                                                    sensitive False
                                            elif phone_outfit_state == "owned":
                                                textbutton "Owned — open Wardrobe from the regular UI to equip":
                                                    xfill True
                                                    sensitive False
                                            else:
                                                textbutton "Locked":
                                                    xfill True
                                                    sensitive False

                    elif phone_app == "photos":

                        frame:
                            xfill True
                            background Solid("#242027")
                            padding (20, 20)

                            vbox:
                                spacing 12
                                add "gui/phone/icons/photos.png" xysize (105, 105) xalign 0.5
                                text "PHOTO APP" size 22 color "#ffffff" xalign 0.5
                                text "The camera roll is scaffolded for story photos and received image attachments. Stable asset IDs are already supported by the message system." size 15 color "#cbbdca" text_align 0.5 xalign 0.5 line_spacing 4
                                text "Photo thumbnails and full previews will be added as story CG assets come online." size 14 color "#9e919c" text_align 0.5 xalign 0.5 line_spacing 3

                    elif phone_app == "wallet":

                        frame:
                            xfill True
                            background Solid("#242027")
                            padding (22, 22)

                            vbox:
                                spacing 14
                                add "gui/phone/icons/wallet.png" xysize (105, 105) xalign 0.5
                                text "AVAILABLE MONEY" size 15 color "#a99ba8" xalign 0.5
                                text "$[money]" size 42 color "#ffffff" xalign 0.5

                                if last_money_reason:
                                    text "Last change: [last_money_change]" size 15 color "#cbbdca" xalign 0.5
                                    text "[last_money_reason]" size 14 color "#9e919c" xalign 0.5
                                else:
                                    text "No transactions recorded yet." size 14 color "#9e919c" xalign 0.5

                    elif phone_app == "delivery":

                        frame:
                            xfill True
                            background Solid("#242027")
                            padding (22, 22)

                            vbox:
                                spacing 14
                                add "gui/phone/icons/delivery.png" xysize (120, 120) xalign 0.5
                                text "NO ACTIVE DELIVERIES" size 21 color "#ffffff" xalign 0.5
                                text "Future shop purchases can create story-aware orders here: processing, out for delivery, delivered, or collected." size 15 color "#cbbdca" text_align 0.5 xalign 0.5 line_spacing 4
                                text "The app is intentionally scaffolded now so later delivery events can plug in without changing the Phone layout." size 14 color "#9e919c" text_align 0.5 xalign 0.5 line_spacing 3

            hbox:
                xfill True
                ysize 22

                text "PHONE V1 — CUSTOM UI ICON PASS" size 10 color "#5f5661" xalign 0.5
