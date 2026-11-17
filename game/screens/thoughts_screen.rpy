# Ryan's thoughts offer - the "keep one thought" page after a day review
#
# Purpose: A fresh scrapbook spread shown right after the day review closes (systems/thoughts.rpy
#   calls it through the review_closed hook). The left page says what this is; the right page
#   holds up to three handwritten thought cards. Clicking a card keeps it; KEEP NOTHING (where
#   CONTINUE always sits) or Esc keeps nothing. Insight/Full stamp each card with the lane or
#   stat tinting it; Immersive shows only the words.
#
# Public API (call these from scenes/screens):
#   screen lc_thought_offer_screen(day_id, ids)
#       the offer page; returns the kept thought id, or None for keep nothing
#
# Example:
#   $ picked = renpy.call_screen("lc_thought_offer_screen", "ch01_d1", ids)   (lc_thought_offer)
#
# Depends on: systems/thoughts.rpy (lc_thought_text, lc_thought_tint), systems/day_review.rpy
#   (lc_review_night_copy), screens/day_review_screen.rpy (lc_pixel / lc_hand styles),
#   systems/choice_engine.rpy (current_choice_mode)
# Hooks: none
# Load order: default (screens at init -500)
# Docs: docs/THOUGHTS.md   Tests: tests/test_thoughts.py

transform lc_thought_card_in(delay):
    alpha 0.0
    yoffset -18
    pause delay
    easeout 0.24 alpha 1.0 yoffset 0

transform lc_thought_card_still:
    alpha 1.0
    yoffset 0

screen lc_thought_offer_screen(day_id, ids):
    modal True
    zorder 220
    $ mode = current_choice_mode()
    $ night = lc_review_night_copy(day_id)
    $ animate = persistent.lc_recap_animation
    $ card_w = 744
    $ card_h = 246
    $ card_gap = 26

    # Esc keeps nothing. Enter is left to the focused card (keyboard players pick with it).
    key "K_ESCAPE" action Return(None)

    # Stray clicks on the paper do nothing; only a card or KEEP NOTHING answers.
    button:
        xpos 0
        ypos 0
        xsize 1920
        ysize 1080
        background None
        hover_background None
        padding (0, 0)
        action NullAction()

    add "images/ui/scrapbook/spread.png" at (lc_spread_in if animate else lc_spread_still)

    # Left page: what this is, in the review's handwriting.
    fixed:
        xpos 150
        ypos 92
        xsize 700
        ysize 860
        hbox:
            spacing 8
            text night["kicker"] style "lc_pixel_bold" size 28 color "#3b2a30" yalign 0.5
            add "images/ui/scrapbook/diamond.png" yalign 0.5
            text "BEFORE I SLEEP" style "lc_pixel_bold" size 28 color "#3b2a30" yalign 0.5
        add "images/ui/scrapbook/rule_dots.png" xpos 0 ypos 52 xsize 700 ysize 3
        text "Something from today keeps coming back." style "lc_hand" size 34 xpos 0 ypos 66 xsize 700
        add "images/ui/scrapbook/rule.png" xpos 0 ypos 114 xsize 700 ysize 3
        text "If I hang on to one of these, it'll still be on my mind tomorrow." style "lc_hand" size 30 xpos 0 ypos 124 xsize 700
        add "images/ui/scrapbook/rule.png" xpos 0 ypos 168 xsize 700 ysize 3
        text "Or I let all of it go and just sleep." style "lc_hand" size 30 color "#7a5648" xpos 0 ypos 178 xsize 700
        add "images/ui/scrapbook/rule.png" xpos 0 ypos 222 xsize 700 ysize 3
        hbox:
            xpos 0
            ypos 248
            spacing 8
            add "images/ui/scrapbook/mark.png" yalign 0.5
            text "KEEP ONE, OR KEEP NOTHING" style "lc_pixel" size 18 color "#7a6266" yalign 0.5

    # Right page: the thought cards, one per row.
    for index, thought_id in enumerate(ids):
        $ words = lc_thought_text(thought_id)
        $ tint = lc_thought_tint(thought_id) if mode != "normal" else ""
        $ cy = 92 + index * (card_h + card_gap)
        fixed at (lc_thought_card_in(0.15 + index * 0.18) if animate else lc_thought_card_still):
            xpos 1010
            ypos cy
            xsize card_w
            ysize card_h
            button:
                xsize card_w
                ysize card_h
                padding (0, 0)
                background Fixed(Solid("#3b2a30"), Transform(Solid("#fffaf0"), xpos=3, ypos=3, xysize=(card_w - 6, card_h - 6)), xysize=(card_w, card_h))
                hover_background Fixed(Solid("#a83a5a"), Transform(Solid("#f8e3ea"), xpos=3, ypos=3, xysize=(card_w - 6, card_h - 6)), xysize=(card_w, card_h))
                action Return(thought_id)
                fixed:
                    xsize card_w
                    ysize card_h
                    text lc_review_quote(words) style "lc_hand_quote" size 30 xpos 30 ypos 30 xsize (card_w - 60) substitute False
                    hbox:
                        xpos 30
                        ypos (card_h - 48)
                        spacing 8
                        add "images/ui/scrapbook/bubble.png" yalign 0.5
                        text "KEEP THIS ONE" style "lc_pixel" size 16 color "#7a6266" yalign 0.5
                    if tint:
                        frame:
                            xanchor 1.0
                            xpos (card_w - 22)
                            ypos (card_h - 58)
                            background Frame("images/ui/scrapbook/stamp.png", 9, 9, 9, 9)
                            padding (16, 9)
                            text tint.upper() style "lc_pixel_bold" size 16 color "#a83a5a" substitute False
            add "images/ui/scrapbook/tape_top.png" xalign 0.5 ypos -14

    add "images/ui/scrapbook/continue.png" xpos 1472 ypos 988
    text "KEEP NOTHING" xpos 1520 ypos 1006 style "lc_pixel_bold" size 24 color "#fff3f7"
    add "images/ui/scrapbook/continue_arrow.png" xpos 1720 ypos 1010
    button:
        xpos 1472
        ypos 988
        xysize (312, 66)
        background None
        hover_background None
        padding (0, 0)
        action Return(None)
