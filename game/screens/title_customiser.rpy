# Title-screen customiser panel (PR 2). Opened from the "Customise" menu item;
# every pick applies live to the title screen behind it.
# Data + unlock rules: systems/title_customiser.rpy.

style lc_tc_tab_text is default:
    font "fonts/Nunito-ExtraBold.ttf"
    size 20
    kerning 2
    color "#ffffffb0"
    hover_color "#ffffff"
    selected_color "#ffffff"

style lc_tc_label_text is default:
    font "fonts/Nunito-Bold.ttf"
    size 16
    color "#fde7f1"
    xalign 0.5
    textalign 0.5

transform lc_tc_panel_in:
    subpixel True
    alpha 0.0
    xoffset -30
    easein 0.3 alpha 1.0 xoffset 0

transform lc_tc_tile:
    subpixel True
    on idle:
        easein 0.2 yoffset 0
    on hover, selected_hover:
        easein 0.18 yoffset -4


screen lc_tc_tab(label, value, tab):
    button:
        padding (18, 8)
        background (Frame("gui/title/chip_hover.png", 20, 20) if tab == value else Frame("gui/title/chip.png", 20, 20))
        hover_background Frame("gui/title/chip_hover.png", 20, 20)
        action [Function(lc_ui_play, "pick"), SetDict(lc_title_ui, "tab", value)]
        hovered Function(lc_ui_play, "tick")
        text label.upper() style "lc_tc_tab_text"


screen lc_tc_tile(thumb, label, selected, locked, action, w, h):
    button:
        at lc_tc_tile
        padding (6, 6)
        xsize (w + 12)
        background Frame("gui/title/card_hover.png" if selected else "gui/title/card.png", 24, 24)
        hover_background Frame("gui/title/card_hover.png", 24, 24)
        action ([Function(lc_ui_play, "thud"), Function(renpy.notify, "Locked: reach this in the story to unlock it.")] if locked else [Function(lc_ui_play, "pick"), action])
        hovered Function(lc_ui_play, "tick")
        vbox:
            spacing 6
            fixed:
                xysize (w, h)
                add thumb
                if locked:
                    add Solid("#1e0c1e99") xysize (w, h)
                    text "LOCKED" font "fonts/Nunito-ExtraBold.ttf" size 18 kerning 3 color "#ffffffc0" xalign 0.5 yalign 0.5
                if selected:
                    text "\u2665" font "fonts/Nunito-ExtraBold.ttf" size 22 color "#ff9fc8" xalign 0.97 yalign 0.03
            text ("???" if locked else label) style "lc_tc_label_text" xsize w


screen lc_title_customiser(tab):
    $ cur_bg = lc_title_current_background()
    $ cur_outfit = lc_title_current_outfit()
    $ cur_expr = lc_title_current_expression()

    frame at lc_tc_panel_in:
        xpos 70
        ypos 46
        xysize (720, 650)
        padding (28, 22)
        background Frame("gui/title/panel.png", 30, 30)

        vbox:
            spacing 14
            hbox:
                xfill True
                text "Customise title screen" font "fonts/Fredoka-SemiBold.ttf" size 34 color "#ffffff"
            hbox:
                spacing 10
                use lc_tc_tab("Background", "background", tab)
                use lc_tc_tab("Outfit", "outfit", tab)
                use lc_tc_tab("Expression", "expression", tab)

            if tab == "background":
                vpgrid:
                    cols 3
                    spacing 12
                    xsize 664
                    ysize 430
                    mousewheel True
                    draggable True
                    scrollbars "vertical"
                    allow_underfull True
                    for b in lc_title_background_options():
                        $ locked = not lc_title_background_unlocked(b)
                        use lc_tc_tile(lc_title_bg_thumb(b), b["label"], b["id"] == cur_bg["id"], locked, Function(lc_title_pick, "bg", b["id"]), 196, 110)
            elif tab == "outfit":
                vpgrid:
                    cols 4
                    spacing 12
                    xsize 664
                    ysize 430
                    mousewheel True
                    draggable True
                    scrollbars "vertical"
                    allow_underfull True
                    for o in lc_title_outfit_options():
                        $ locked = not lc_title_outfit_unlocked(o)
                        use lc_tc_tile(lc_title_outfit_thumb(o, locked), o["label"], o["id"] == cur_outfit["id"], locked, Function(lc_title_pick, "outfit", o["id"]), 140, 170)
            else:
                vpgrid:
                    cols 4
                    spacing 12
                    xsize 664
                    ysize 430
                    mousewheel True
                    draggable True
                    scrollbars "vertical"
                    allow_underfull True
                    for e in lc_title_expression_options():
                        use lc_tc_tile(lc_title_face_thumb(cur_outfit, e), e[1], e[0] == cur_expr[0], False, Function(lc_title_pick, "expression", e[0]), 140, 123)

            hbox:
                xfill True
                spacing 12
                button:
                    padding (16, 8)
                    background Frame("gui/title/chip.png", 20, 20)
                    hover_background Frame("gui/title/chip_hover.png", 20, 20)
                    action [Function(lc_ui_play, "tap"), ToggleField(persistent, "lc_title_all_memories")]
                    hovered Function(lc_ui_play, "tick")
                    text ("18+ options: shown" if persistent.lc_title_all_memories else "18+ options: hidden") style "lc_title_small_text" color "#ffffffd0"
                null width 120
                button:
                    padding (16, 8)
                    background Frame("gui/title/chip.png", 20, 20)
                    hover_background Frame("gui/title/chip_hover.png", 20, 20)
                    action [Function(lc_ui_play, "tap"), Function(lc_title_reset)]
                    hovered Function(lc_ui_play, "tick")
                    text "Reset" style "lc_title_small_text" color "#ffffffd0"
                button:
                    padding (22, 8)
                    background Frame("gui/title/chip_hover.png", 20, 20)
                    hover_background Frame("gui/title/chip_hover.png", 20, 20)
                    action [Function(lc_ui_play, "back"), SetDict(lc_title_ui, "editing", False)]
                    hovered Function(lc_ui_play, "tick")
                    text "Done" style "lc_title_small_text" color "#ffffff"

    key "K_ESCAPE" action SetDict(lc_title_ui, "editing", False)
    key "mouseup_3" action SetDict(lc_title_ui, "editing", False)
