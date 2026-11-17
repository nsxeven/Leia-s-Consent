# Leia's map - the place cards of her errand, in the scrapbook look
#
# Purpose: Draws the map of Leia's errand (systems/leia_side.rpy, lc_leia_map): one fixed row of up
#   to four place cards, each with a polaroid of the place's background, its name and a one-line
#   hint. Open cards return their place id. Visited cards carry a BEEN THERE stamp; locked cards are
#   greyed, show Leia's in-character reason in every mode and "Opens on a later day." in
#   Insight/Full. Locked and visited cards still take keyboard/gamepad focus (so their text can be
#   read) but do nothing when activated. No dismiss button: she visits every open place.
#
# Public API (call these from scenes/screens):
#   screen lc_leia_map_screen(day, cards)     the map (called by lc_leia_map; cards from
#       lc_leia_cards / lc_leia_side.cards); returns the picked open place id
#   screen lc_leia_map_card(card, i, still, first)
#       one place card (i: 0-based slot, still: reduced motion, first: default keyboard focus);
#       the "Opens on a later day." line follows the live display mode (lc_leia_side.lock_hint)
#   transform lc_leia_card_in(i)              staggered fade/rise of card i as the map opens
#   transform lc_leia_card_hover              small lift while a card has focus
#   transform lc_leia_card_still              no motion (reduced motion)
#
# Example:
#   $ d2_errand_place = lc_leia_map("ch01_d2")   (systems/leia_side.rpy calls this screen)
#
# Depends on: systems/leia_side.rpy (card dicts), systems/hidden_pov.rpy (lc_pov_reduce_motion),
#   systems/choice_path_tags.rpy (lc_path_stamp_tilt, LC_PATH_STAMP_PAPER), screens/scrapbook_ui.rpy
#   (lc_ui_play, scrapbook frames), systems/lc_hover_fade.rpy (LC_HOVER_IN / LC_HOVER_OUT)
# Hooks: none
# Load order: default (screens at init -500, transforms at init 0)
# Docs: docs/LEIA_SIDE.md   Tests: tests/test_leia_side.py

transform lc_leia_card_in(i):
    subpixel True
    alpha 0.0
    yoffset 28
    pause 0.07 * i
    easein 0.34 alpha 1.0 yoffset 0

transform lc_leia_card_hover:
    subpixel True
    on idle:
        easein LC_HOVER_OUT yoffset 0
    on hover:
        easein LC_HOVER_IN yoffset -10
    on insensitive:
        easein LC_HOVER_OUT yoffset 0

transform lc_leia_card_still:
    alpha 1.0

screen lc_leia_map_screen(day, cards):
    modal True
    zorder 120
    $ still = lc_pov_reduce_motion()
    $ first_open = next((c["id"] for c in cards if c["activatable"]), None)
    $ any_visited = any(c["state"] == "visited" for c in cards)

    # Dims the scene behind the map; a plain image, never a button, so it cannot take focus.
    add Solid("#1e1628a8")

    frame:
        xalign 0.5
        ypos 104
        background Frame("gui/scrapbook/frame_kraft.png", 9, 9)
        padding (30, 6, 30, 6)
        ysize 54
        text ("WHERE TO NEXT?" if any_visited else "WHERE TO FIRST?"):
            size 28
            color "#5a4030"
            font "fonts/Handjet-ExtraBold.ttf"
            yalign 0.5

    hbox:
        xalign 0.5
        ypos 214
        spacing 30
        for i, card in enumerate(cards):
            use lc_leia_map_card(card, i, still, card["id"] == first_open)

    for i, card in enumerate(cards):
        if card["activatable"]:
            key "K_%d" % (i + 1) action Return(card["id"])

screen lc_leia_map_card(card, i, still, first):
    $ state = card["state"]
    $ locked = state == "locked"
    $ visited = state == "visited"
    $ says = card["label"] + ". " + (card["reason"] if locked else card["hint"])
    $ lock_hint = lc_leia_side.lock_hint(card["state"], current_choice_mode())
    $ says += (" " + lock_hint) if lock_hint else ""
    $ says += {"open": " Open.", "visited": " Already visited.", "locked": " Locked."}[state]
    # 16:9 like the backgrounds, so cover fills it exactly; the crop keeps odd-sized art inside.
    $ thumb = Transform(Transform(card["bg"], fit="cover", xysize=(352, 198)), crop=(0, 0, 352, 198))
    if locked:
        $ thumb = Transform(thumb, matrixcolor=SaturationMatrix(0.0) * BrightnessMatrix(-0.08), alpha=0.6)
    elif visited:
        $ thumb = Transform(thumb, matrixcolor=SaturationMatrix(0.55))

    fixed:
        xysize (404, 664)
        at (lc_leia_card_still if still else lc_leia_card_in(i))

        button:
            ypos 14
            xysize (404, 640)
            if card["activatable"]:
                action Return(card["id"])
            else:
                # Focusable so the reason can be read with keys/gamepad; activating does nothing.
                action NullAction()
            default_focus first
            alt says
            background Frame("gui/scrapbook/frame_choice.png", 18, 12, 12, 12)
            hover_background Frame("gui/scrapbook/frame_choice_hi.png", 18, 12, 12, 12)
            padding (22, 22, 22, 18)
            hovered Function(lc_ui_play, "tick")
            at (lc_leia_card_still if still else lc_leia_card_hover)

            fixed:
                xysize (360, 600)

                # The polaroid: paper border, the place's background, state marks on top.
                frame:
                    xysize (360, 206)
                    background Frame("gui/scrapbook/frame_paper.png", 9, 9)
                    padding (4, 4, 4, 4)
                    add thumb
                if locked:
                    add "images/ui/scrapbook/icon_lock.png" xalign 0.5 ypos 103 yanchor 0.5 zoom 1.6
                if visited:
                    frame at lc_path_stamp_tilt:
                        xalign 0.5
                        ypos 80
                        background Solid("#b04a6e")
                        padding (3, 3, 3, 3)
                        frame:
                            background Solid(LC_PATH_STAMP_PAPER)
                            padding (14, 2, 14, 4)
                            text "BEEN THERE":
                                size 34
                                color "#b04a6e"
                                font "fonts/Handjet-ExtraBold.ttf"

                vbox:
                    ypos 222
                    xsize 360
                    spacing 10
                    text card["label"]:
                        size 38
                        color ("#7a6266" if locked else "#34242c")
                        font "fonts/Handjet-ExtraBold.ttf"

                    if locked:
                        text card["reason"]:
                            size 29
                            color "#6a5258"
                            italic True
                            font "fonts/PatrickHand-Regular.ttf"
                            line_spacing 2
                        if lock_hint:
                            text lock_hint:
                                size 28
                                color "#7a4a3a"
                                font "fonts/PatrickHand-Regular.ttf"
                    else:
                        text card["hint"]:
                            size 31
                            color "#34242c"
                            font "fonts/PatrickHand-Regular.ttf"
                            line_spacing 2

                # Footer: the slot's number key on open cards, the state word on the others.
                hbox:
                    yalign 1.0
                    spacing 12
                    if card["activatable"]:
                        frame:
                            xysize (42, 42)
                            background Frame("gui/scrapbook/frame_paper.png", 9, 9)
                            text str(i + 1) xalign 0.5 yalign 0.5 size 24 color "#7a6266" font "fonts/Handjet-ExtraBold.ttf"
                        text "GO HERE" size 26 color "#b04a6e" font "fonts/Handjet-ExtraBold.ttf" yalign 0.5
                    elif visited:
                        text "DONE" size 26 color "#7a6266" font "fonts/Handjet-ExtraBold.ttf" yalign 0.5
                    else:
                        text "LOCKED" size 26 color "#7a6266" font "fonts/Handjet-ExtraBold.ttf" yalign 0.5
