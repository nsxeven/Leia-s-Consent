# Player-facing outfit shop.
# Purchasing adds ownership only; wear acceptance remains a separate Wardrobe decision.

screen shop_screen():

    modal True
    zorder 205

    default shop_selected_outfit = shop_outfit_ids()[0] if shop_outfit_ids() else None

    key "K_ESCAPE" action Return()

    add Solid("#141117")

    if shop_selected_outfit is None:
        frame:
            xalign 0.5
            yalign 0.5
            xsize 1200
            padding (40, 35)
            background Solid("#19151d")

            vbox:
                spacing 20
                text "OUTFIT SHOP" size 42 color "#ffffff"
                text "There are no outfits available in the shop right now." size 22 color "#c8b8c5"
                textbutton "Close":
                    action Return()

    else:
        $ selected_outfit = get_outfit(shop_selected_outfit)
        $ selected_name = selected_outfit["name"]
        $ selected_description = selected_outfit["description"]
        $ selected_cost = selected_outfit["cost"]
        $ selected_category = outfit_category_label(shop_selected_outfit)
        $ selected_contexts = outfit_context_text(shop_selected_outfit)
        $ selected_styles = outfit_style_rows(shop_selected_outfit)
        $ selected_state = shop_item_state(shop_selected_outfit)
        $ selected_state_label = shop_item_status_label(shop_selected_outfit)
        $ selected_state_color = shop_item_status_color(shop_selected_outfit)

        frame:
            xalign 0.5
            yalign 0.5
            xsize 1740
            ysize 980
            background Solid("#19151d")
            padding (42, 34)

            vbox:
                spacing 18
                xfill True
                yfill True

                hbox:
                    xfill True

                    vbox:
                        spacing 3
                        text "OUTFIT SHOP" size 46 color "#ffffff"
                        text "Choose something for [girlfriend_name]. Buying an outfit never guarantees she will wear it." size 19 color "#aa9dab"

                    vbox:
                        xalign 1.0
                        spacing 7
                        text "Money: $[money]" size 22 color "#ffffff" xalign 1.0
                        textbutton "Close":
                            xalign 1.0
                            action Return()

                if last_shop_message:
                    frame:
                        xfill True
                        background Solid("#30242e")
                        padding (20, 13)
                        text "[last_shop_message]" size 17 color "#e6d9e3"

                hbox:
                    spacing 20
                    xfill True
                    yfill True

                    frame:
                        xsize 505
                        yfill True
                        background Solid("#1d1920")
                        padding (18, 18)

                        vbox:
                            spacing 14
                            xfill True
                            yfill True

                            hbox:
                                xfill True
                                text "AVAILABLE OUTFITS" size 23 color "#ffffff"
                                text "[len(shop_outfit_ids())]" size 17 color "#a99ba8" xalign 1.0

                            use lc_scroll_body:
                                vbox:
                                    spacing 12
                                    xfill True

                                    for outfit_id in shop_outfit_ids():
                                        $ card_outfit = get_outfit(outfit_id)
                                        $ card_name = card_outfit["name"]
                                        $ card_cost = card_outfit["cost"]
                                        $ card_category = outfit_category_label(outfit_id)
                                        $ card_state_label = shop_item_status_label(outfit_id)
                                        $ card_state_color = shop_item_status_color(outfit_id)
                                        $ card_selected = shop_selected_outfit == outfit_id

                                        button:
                                            xfill True
                                            padding (20, 18)
                                            background (Solid("#3b2a38") if card_selected else Solid("#211c25"))
                                            hover_background Solid("#30242f")
                                            action SetScreenVariable("shop_selected_outfit", outfit_id)

                                            vbox:
                                                spacing 7
                                                xfill True

                                                hbox:
                                                    xfill True
                                                    text "[card_name]" size 23 color "#ffffff"
                                                    text "$[card_cost]" size 20 color "#eee7ed" xalign 1.0

                                                hbox:
                                                    xfill True
                                                    text "[card_category]" size 15 color "#a99ba8"
                                                    text "[card_state_label]" size 14 color card_state_color xalign 1.0

                    frame:
                        xfill True
                        yfill True
                        background Solid("#211c25")
                        padding (28, 24)

                        use lc_scroll_body:
                            vbox:
                                spacing 18
                                xfill True

                                hbox:
                                    xfill True

                                    vbox:
                                        spacing 5
                                        text "[selected_name]" size 34 color "#ffffff"
                                        text "[selected_category]" size 17 color "#f1a8c8"

                                    vbox:
                                        xalign 1.0
                                        spacing 5
                                        text "$[selected_cost]" size 29 color "#ffffff" xalign 1.0
                                        text "[selected_state_label]" size 15 color selected_state_color xalign 1.0

                                text "[selected_description]" size 20 color "#ddd2db" line_spacing 4

                                frame:
                                    xfill True
                                    background Solid("#2a242d")
                                    padding (20, 17)

                                    vbox:
                                        spacing 7
                                        text "PURCHASE VS. COMFORT" size 17 color "#f1a8c8"
                                        text "Buying this only adds it to [girlfriend_name]'s wardrobe. Whether she is willing to wear it is decided separately by her current comfort and progression." size 17 color "#eee7ed" line_spacing 3

                                vbox:
                                    spacing 8
                                    text "SUITED FOR" size 18 color "#ffffff"
                                    text "[selected_contexts]" size 17 color "#b9aabb"

                                text "STYLE PROFILE" size 22 color "#ffffff"

                                grid 2 2:
                                    spacing 18
                                    xfill True

                                    for style_label, style_value in selected_styles:
                                        frame:
                                            xfill True
                                            background Solid("#272129")
                                            padding (16, 13)
                                            use outfit_style_meter(style_label, style_value)

                                null height 6

                                if selected_state == "owned":
                                    frame:
                                        xfill True
                                        background Solid("#293329")
                                        padding (20, 15)
                                        text "ALREADY OWNED" size 18 color "#b9d7bd" xalign 0.5

                                elif selected_state == "locked":
                                    frame:
                                        xfill True
                                        background Solid("#2c272d")
                                        padding (20, 15)
                                        text "This outfit is not available to purchase yet." size 17 color "#b8a8b5" xalign 0.5

                                elif selected_state == "insufficient":
                                    textbutton "Need $[selected_cost] — You have $[money]":
                                        xfill True
                                        sensitive False

                                else:
                                    textbutton "Buy for $[selected_cost]":
                                        xfill True
                                        action Function(purchase_outfit, shop_selected_outfit)
