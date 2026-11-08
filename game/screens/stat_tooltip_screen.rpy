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


# The card sits next to the focused stat row. darryn 2026-11-08: one compact size
# per look, fades in AND out. The tooltip focus rect disappears the moment focus
# leaves, so the card keeps the last rect + text and is placed with
# `nearrect rect`, letting the hide fade play where the card was.
transform lc_stat_tip_fade:
    on show:
        alpha 0.0 yoffset 6
        ease 0.18 alpha 1.0 yoffset 0
    on hide:
        ease 0.18 alpha 0.0 yoffset 6

define LC_STAT_TIP_SIZE = {"phone": (None, 176), "scrapbook": (540, 196)}

screen lc_stat_tip(tip, look="scrapbook"):
    default _last_tip = None
    default _last_rect = None
    $ _rect = GetFocusRect("tooltip") if tip else None
    $ _last_tip = tip or _last_tip
    $ _last_rect = _rect or _last_rect
    if _last_rect:
        nearrect:
            rect _last_rect
            prefer_top True
            showif tip:
                if look == "phone":
                    # Same white card + blue outline as the phone's own cards.
                    frame at lc_stat_tip_fade:
                        xalign 0.5
                        xsize LC_PHONE_CONTENT_WIDTH
                        ysize LC_STAT_TIP_SIZE["phone"][1]
                        background Frame("gui/phone/sprite_match/tip_card.png", 18, 18)
                        padding (20, 12)
                        text (_last_tip or ""):
                            style "lc_sw_hand"
                            size 24
                            color "#293C53"
                            yalign 0.5
                            substitute False
                else:
                    frame at lc_stat_tip_fade:
                        xalign 0.5
                        xsize LC_STAT_TIP_SIZE["scrapbook"][0]
                        ysize LC_STAT_TIP_SIZE["scrapbook"][1]
                        background Frame("gui/scrapbook/frame_paper.png", 9, 9)
                        padding (20, 12)
                        text (_last_tip or "") style "lc_stat_tip_text" yalign 0.5 substitute False
