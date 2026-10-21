# Full Transparency route selector (player-facing; no developer unlock needed).
screen lc_route_explorer_screen():
    modal True
    zorder 380

    key "K_ESCAPE" action Hide("lc_route_explorer_screen")
    add Solid("#000000dd")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1030
        ysize 840
        background Solid("#211c25")
        padding (40, 34)

        vbox:
            spacing 18
            xfill True

            hbox:
                xfill True
                text "ROUTE EXPLORER" size 40 color "#ffffff"
                textbutton "Close":
                    xalign 1.0
                    action Hide("lc_route_explorer_screen")

            text "Available in Full Transparency. Choose which relationship direction upcoming route checks should favor." size 21 color "#d6c7d2"
            text "Already viewed scenes and choices are not undone. Switching changes current stats and future branch selection. Save before experimenting." size 18 color "#b6a6b4" line_spacing 3
            text "Current: [lc_route_explorer_current_label()]" size 24 color "#f1a8c8"

            if not lc_route_explorer_allowed():
                text "Switch to Full Transparency in Gameplay Settings to use this tool." size 19 color "#eeafaf"
            elif not has_story_flag("ch01_started"):
                text "Route switching becomes available after Chapter One begins." size 19 color "#eeafaf"
            elif has_story_flag("ch01_day_02_complete"):
                text "A later-day route is already committed in this save. Start from a chapter checkpoint to explore a different path." size 19 color "#eeafaf"
            else:
                for route_id, route_label, route_description in LC_ROUTE_EXPLORER_OPTIONS:
                    frame:
                        xfill True
                        background Solid("#302631")
                        padding (18, 13)
                        vbox:
                            spacing 6
                            textbutton "[route_label]":
                                text_size 25
                                selected (lc_route_explorer_current() == route_id)
                                action Function(lc_route_explorer_set_focus, route_id)
                            text "[route_description]" size 18 color "#c7b8c4"

            text "Love, Exhibitionism, and NTR risk are the early chapter's available directions. Later specialized routes such as NTS Discovery still require their actual story decisions." size 16 color "#9d8e9b" line_spacing 3
