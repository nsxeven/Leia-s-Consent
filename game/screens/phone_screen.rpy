# Diegetic in-game phone hub.
# Placeholder geometry is used until final phone art/icons are generated.

init python:
    if "phone_quick_access" not in config.overlay_screens:
        config.overlay_screens.append("phone_quick_access")


screen phone_quick_access():

    zorder 110

    if quick_menu and not renpy.get_screen("main_menu") and not renpy.get_screen("phone_screen"):
        button:
            xalign 0.985
            yalign 0.91
            xsize 86
            ysize 116
            padding (8, 8)
            background Solid("#171319")
            hover_background Solid("#3a2a37")
            action Show("phone_screen")

            vbox:
                xalign 0.5
                yalign 0.5
                spacing 4

                frame:
                    xalign 0.5
                    xsize 38
                    ysize 58
                    background Solid("#29222c")
                    padding (4, 4)

                    text "P" size 24 color "#f1a8c8" xalign 0.5 yalign 0.5

                text "PHONE" size 11 color "#ffffff" xalign 0.5

                if phone_total_unread() > 0:
                    text "[phone_total_unread()] NEW" size 10 color "#f1a8c8" xalign 0.5


screen phone_screen():

    modal True
    zorder 310

    default phone_app = "home"
    default phone_thread = None

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

            # Placeholder speaker / camera area. Replace with generated phone art later.
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

                        text "A diegetic hub for messages, shopping, photos, and future apps." size 16 color "#b8a8b5"

                        grid 2 2:
                            spacing 14
                            xfill True

                            button:
                                xfill True
                                ysize 185
                                padding (18, 18)
                                background Solid("#2b202a")
                                hover_background Solid("#3a2a37")
                                action SetScreenVariable("phone_app", "messages")

                                vbox:
                                    spacing 10
                                    text "MESSAGES" size 24 color "#ffffff"
                                    text "Texts, group chats, and future photo attachments." size 14 color "#cbbdca"
                                    if phone_total_unread() > 0:
                                        text "[phone_total_unread()] unread" size 15 color "#f1a8c8"
                                    else:
                                        text "No unread messages" size 15 color "#9e919c"

                            button:
                                xfill True
                                ysize 185
                                padding (18, 18)
                                background Solid("#20282a")
                                hover_background Solid("#2d383b")
                                action SetScreenVariable("phone_app", "shop")

                                vbox:
                                    spacing 10
                                    text "SHOP" size 24 color "#ffffff"
                                    text "Buy outfits online using the real economy system." size 14 color "#cbbdca"
                                    text "[len(shop_outfit_ids())] items" size 15 color "#b9d7bd"

                            button:
                                xfill True
                                ysize 185
                                padding (18, 18)
                                background Solid("#29242d")
                                hover_background Solid("#39313e")
                                action SetScreenVariable("phone_app", "photos")

                                vbox:
                                    spacing 10
                                    text "PHOTOS" size 24 color "#ffffff"
                                    text "Camera roll / received images scaffolded for later." size 14 color "#cbbdca"
                                    text "COMING LATER" size 14 color "#a99ba8"

                            button:
                                xfill True
                                ysize 185
                                padding (18, 18)
                                background Solid("#27232b")
                                hover_background Solid("#38313c")
                                action SetScreenVariable("phone_app", "wallet")

                                vbox:
                                    spacing 10
                                    text "WALLET" size 24 color "#ffffff"
                                    text "Quick view of current spending money." size 14 color "#cbbdca"
                                    text "$[money]" size 22 color "#ffffff"

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
                                                        text "PHOTO PLACEHOLDER" size 17 color "#ffffff" xalign 0.5
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
                                                    text "OUTFIT PREVIEW" size 15 color "#ffffff" xalign 0.5
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
                                text "PHOTO APP SCAFFOLD" size 22 color "#ffffff"
                                text "The first version does not maintain a separate camera roll yet. Message attachments already carry stable asset IDs and labels, so future Leia selfies or received photos can plug into this phone without rewriting the message system." size 15 color "#cbbdca" line_spacing 4
                                text "Final phone body, icons, thumbnails, and image previews will replace these placeholders after the ComfyUI art pass." size 14 color "#9e919c" line_spacing 3

                    elif phone_app == "wallet":

                        frame:
                            xfill True
                            background Solid("#242027")
                            padding (22, 22)

                            vbox:
                                spacing 14
                                text "AVAILABLE MONEY" size 15 color "#a99ba8"
                                text "$[money]" size 42 color "#ffffff"

                                if last_money_reason:
                                    text "Last change: [last_money_change]" size 15 color "#cbbdca"
                                    text "[last_money_reason]" size 14 color "#9e919c"
                                else:
                                    text "No transactions recorded yet." size 14 color "#9e919c"

                                text "Future versions can add deliveries, order history, or other phone-based economy features here without changing the core money system." size 14 color "#b8a8b5" line_spacing 3

            hbox:
                xfill True
                ysize 22

                text "PLACEHOLDER PHONE — FINAL COMFYUI DEVICE ART LATER" size 10 color "#5f5661" xalign 0.5
