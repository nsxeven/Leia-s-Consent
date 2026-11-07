# Stat explanation card shown next to whichever stat row has focus.
#
# Rows carry the text in their `tooltip` property (see lc_stat_tooltip() in
# systems/stat_tooltips.rpy), so mouse hover, keyboard and controller focus all
# work the same way and nothing depends on hovered/unhovered screen variables.
# Each screen that shows stat rows ends with:
#     use lc_stat_tip(GetTooltip("<that screen's name>"))
# Use it at the screen's top level: nearrect needs the full screen area to
# line the card up with the focused row. On touch screens the card shows while
# a finger rests on a row.

style lc_stat_tip_row is default:
    xfill True
    padding (8, 4)
    background None
    hover_background Solid("#cc006614")

style lc_stat_tip_text is default:
    font "fonts/PatrickHand-Regular.ttf"
    size 24
    color "#3b2a30"
    line_spacing 2
    adjust_spacing False


screen lc_stat_tip(tip, look="scrapbook"):
    if tip and look == "phone":
        # Berry key art (the phone's button colour) so the card stands out
        # from the cream stat cards underneath.
        $ _tip_card = Frame(lc_phone_art("key_berry"), 16, 16)
        nearrect:
            focus "tooltip"
            prefer_top True
            frame:
                xalign 0.5
                xmaximum 580
                background _tip_card
                padding (22, 14)
                text tip:
                    style "lc_sw_hand"
                    size 28
                    color "#faf4e8"
                    substitute False
    elif tip:
        nearrect:
            focus "tooltip"
            prefer_top True
            frame:
                xalign 0.5
                xmaximum 540
                background Frame("gui/scrapbook/frame_paper.png", 9, 9)
                padding (20, 14)
                text tip style "lc_stat_tip_text" substitute False
