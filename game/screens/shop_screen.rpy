# Prototype outfit shop. Final visual design comes later.

screen shop_screen():

    modal True
    zorder 205

    key "K_ESCAPE" action Return()

    add Solid("#000000bb")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1180
        ysize 900
        padding (38, 32)

        vbox:
            spacing 18
            xfill True

            hbox:
                xfill True
                text "OUTFIT SHOP" size 40
                textbutton "Close":
                    xalign 1.0
                    action Return()

            text "Money: $[money]" size 28
            text "Purchasing only adds an outfit to the wardrobe. It does not guarantee that [girlfriend_name] will agree to wear it." size 20

            if last_shop_message:
                text "[last_shop_message]" size 21

            viewport:
                xfill True
                yfill True
                mousewheel True
                draggable True
                scrollbars "vertical"

                vbox:
                    spacing 18
                    xfill True

                    for outfit_id in shop_outfit_ids():
                        $ outfit = get_outfit(outfit_id)
                        $ outfit_name_value = outfit["name"]
                        $ outfit_description = outfit["description"]
                        $ outfit_cost = outfit["cost"]
                        $ already_owned = owns_outfit(outfit_id)
                        $ unlocked = is_shop_unlocked(outfit_id)

                        frame:
                            xfill True
                            padding (24, 20)

                            vbox:
                                spacing 10
                                xfill True

                                hbox:
                                    xfill True
                                    text "[outfit_name_value]" size 28
                                    text "$[outfit_cost]" size 25 xalign 1.0

                                text "[outfit_description]" size 20

                                if already_owned:
                                    text "OWNED" size 21
                                elif not unlocked:
                                    text "LOCKED" size 21
                                elif can_afford(outfit_cost):
                                    textbutton "Buy — $[outfit_cost]":
                                        action Function(purchase_outfit, outfit_id)
                                else:
                                    textbutton "Need $[outfit_cost]":
                                        sensitive False
