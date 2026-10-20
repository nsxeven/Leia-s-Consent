# An entirely scripted story prop. No real surveillance or install workflow.
screen ch01_evidence(kind):
    modal True
    zorder 210
    add Solid("#080b12ee")
    frame:
        align (0.5, 0.5)
        xsize 1140
        ysize 920
        padding (44, 32)
        background Solid("#151c29")
        vbox:
            spacing 18
            text ("Maya → Leia" if kind == "hike" else "Leia's messages" if kind == "club" else "Echo · story feed") size 34 color "#ffffff"
            if kind == "meeting":
                text "Fictional interface · scripted story events only" size 20 color "#9db0c9"
            viewport:
                ysize 720
                mousewheel True
                draggable True
                scrollbars "vertical"
                vbox:
                    spacing 20
                    for sender, body in ch01_evidence_rows(kind):
                        vbox:
                            spacing 6
                            text sender size 23 color "#efb5ce"
                            text body size 26 color "#eef0f5" xmaximum 990
            textbutton "Put the phone down" action Return() text_size 25
    key "game_menu" action Return()

screen ch01_club_typing():
    zorder 110
    frame:
        align (0.5, 0.18)
        padding (24, 14)
        background Solid("#151c29e8")
        text "[girlfriend_name] is typing…" size 26 color "#ffffff"
