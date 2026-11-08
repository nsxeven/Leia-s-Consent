## TAGS page: equip Ryan's and Leia's tags separately, browse moment stickers.
## Opened from the in-game menu next to STATUS. Locked entries show as ???.

screen lc_tag_button(who, tag, earned, equipped):
    button:
        xsize 470
        ysize 54
        padding (16, 8)
        background Frame("gui/scrapbook/frame_keycap_on.png" if equipped else "gui/scrapbook/frame_keycap.png", 9, 9)
        hover_background Frame("gui/scrapbook/frame_keycap_on.png", 9, 9)
        insensitive_background Frame("gui/scrapbook/frame_keycap.png", 9, 9)
        sensitive earned
        action Function(lc_tag_equip, who, tag)
        hovered Function(lc_ui_play, "tick")
        hbox:
            yalign 0.5
            spacing 10
            if earned:
                text tag size 24 color ("#cc0066" if equipped else "#3b2a30") yalign 0.5 substitute False
                if equipped:
                    text "EQUIPPED" size 16 color "#cc0066" font "fonts/Handjet-SemiBold.ttf" yalign 0.5
            else:
                text "???" size 24 color "#a8979b" yalign 0.5


screen lc_tag_column(who, name):
    $ current = lc_tag_equipped(who)
    vbox:
        spacing 8
        xsize 500
        text name.upper() size 30 color "#3b2a30" substitute False
        button:
            xsize 470
            ysize 54
            padding (16, 8)
            background Frame("gui/scrapbook/frame_keycap_on.png" if current is None else "gui/scrapbook/frame_keycap.png", 9, 9)
            hover_background Frame("gui/scrapbook/frame_keycap_on.png", 9, 9)
            action Function(lc_tag_equip, who, None)
            hovered Function(lc_ui_play, "tick")
            hbox:
                yalign 0.5
                spacing 10
                text "Automatic (from your choices)" size 22 color ("#cc0066" if current is None else "#3b2a30") yalign 0.5
                if current is None:
                    text "EQUIPPED" size 16 color "#cc0066" font "fonts/Handjet-SemiBold.ttf" yalign 0.5
        for tag, earned in lc_tag_list(who):
            use lc_tag_button(who, tag, earned, earned and current == tag)


screen lc_tags_screen():

    modal True
    zorder 180

    key "K_ESCAPE" action Return()

    $ stickers = lc_sticker_list()
    $ earned_n = sum(1 for _t, e in lc_tag_list("ryan") + lc_tag_list("leia") if e)
    $ total_n = len(lc_tag_list("ryan")) + len(lc_tag_list("leia"))

    add "gui/scrapbook/bg_game_menu.png"
    use lc_journal_tabs(1686)

    frame:
        xpos 70
        ypos 48
        xsize 1580
        ysize 900
        background None
        padding (28, 18)

        vbox:
            spacing 22
            xfill True
            yfill True

            hbox:
                xfill True
                vbox:
                    spacing 3
                    text "TAGS" size 46 color "#3b2a30"
                    text "Tags you have earned on any playthrough. Equip one for each of you; it shows on Status, the day review and title badges." size 19 color "#7a6266"
                vbox:
                    xalign 1.0
                    spacing 8
                    text ("Collected: {} / {}".format(earned_n, total_n)) size 20 color "#7a6266" xalign 1.0
                    textbutton "Close":
                        xalign 1.0
                        action Return()

            use lc_scroll_body:
                vbox:
                    spacing 26
                    xfill True
                    hbox:
                        spacing 60
                        use lc_tag_column("ryan", player_name)
                        use lc_tag_column("leia", girlfriend_name)

                    vbox:
                        spacing 10
                        text "MOMENT STICKERS" size 30 color "#3b2a30"
                        text "Small moments from your days. Collect them; they can't be equipped." size 18 color "#7a6266"
                        hbox:
                            box_wrap True
                            spacing 12
                            box_wrap_spacing 12
                            xsize 1460
                            for sticker, earned in stickers:
                                frame:
                                    background Solid("#f4dde3" if earned else "#e7dde0")
                                    padding (14, 8)
                                    hbox:
                                        spacing 8
                                        if earned:
                                            add "images/ui/scrapbook/mark.png" yalign 0.5
                                            text sticker.upper() size 18 color "#8a3058" font "fonts/Handjet-SemiBold.ttf" yalign 0.5 substitute False
                                        else:
                                            text "???" size 18 color "#a8979b" font "fonts/Handjet-SemiBold.ttf" yalign 0.5
                    null height 20
