# Demo end card - the thank-you card after the Day One review in demo builds
#
# Purpose: The card a demo build shows after the Day One review (LC_DAY1_DEMO_BUILD): living title
#   backdrop, logo, thank-you, upcoming releases and the Patreon / Discord / X / F95 links.
#
# Public API (call these from scenes/screens):
#   screen lc_demo_end_screen()               demo end card with links
#   define LC_PATREON_URL                     Patreon link (also LC_DISCORD_URL, LC_X_URL, LC_F95_URL)
#
# Example:
#   call screen lc_demo_end_screen      (chapters/ch01/ch01_release_demo.rpy)
#
# Depends on: systems/title_screen.rpy + systems/title_customiser.rpy (backdrop, logo),
#   screens/scrapbook_ui.rpy (styles), game/00_release_build.rpy (LC_DAY1_DEMO_BUILD)
# Hooks: none
# Load order: default (screens at init -500, transforms and defines at init 0)
# Docs: docs/ARCHITECTURE.md   Tests: tests/test_release_from_main.py

## Demo end card (darryn): shown after the Day 1 review in demo builds
## (LC_DAY1_DEMO_BUILD). Same living backdrop as the title screen, the one-line
## logo with its sheen, a thank-you, upcoming releases, Patreon and Discord.
define LC_PATREON_URL = "https://www.patreon.com/c/LeiasConsent"
define LC_DISCORD_URL = "https://discord.gg/HYmrB8Gjwj"
define LC_X_URL = "https://x.com/LeiasConsent"
# Thread id link: survives F95 renaming the thread for each version.
define LC_F95_URL = "https://f95zone.to/threads/321815/"

transform lc_demo_in(delay=0.0, dy=22):
    subpixel True
    alpha 0.0
    yoffset dy
    pause delay
    easein 0.75 alpha 1.0 yoffset 0

transform lc_demo_slide(delay=0.0):
    subpixel True
    alpha 0.0
    xoffset -40
    pause delay
    easein 0.6 alpha 1.0 xoffset 0

define LC_DEMO_CTA_W = 330
define LC_DEMO_CTA_H = 66
define LC_DEMO_CTA_GAP = 18

transform lc_demo_cta_pulse(phase=0.0):
    # Breathes about its own centre; `phase` offsets each button's beat.
    subpixel True
    zoom 1.0
    pause phase
    block:
        ease 0.9 zoom 1.05
        ease 0.9 zoom 1.0
        pause 0.9
        repeat

screen lc_demo_cta_button(col, row, label, idle_col, hover_col, url, delay, phase):
    fixed at lc_demo_in(delay):
        xpos col * (LC_DEMO_CTA_W + LC_DEMO_CTA_GAP)
        ypos row * (LC_DEMO_CTA_H + LC_DEMO_CTA_GAP)
        xysize (LC_DEMO_CTA_W, LC_DEMO_CTA_H)
        button at lc_demo_cta_pulse(phase):
            align (0.5, 0.5)
            xysize (LC_DEMO_CTA_W, LC_DEMO_CTA_H)
            background Solid(idle_col)
            hover_background Solid(hover_col)
            action [Function(lc_ui_play, "tap"), OpenURL(url)]
            hovered Function(lc_ui_play, "tick")
            text label font "fonts/Fredoka-SemiBold.ttf" size 24 color "#ffffff" xalign 0.5 yalign 0.5

transform lc_demo_pulse:
    subpixel True
    zoom 1.0
    block:
        ease 0.9 zoom 1.06
        ease 0.9 zoom 1.0
        repeat

transform lc_demo_glow:
    alpha 0.35
    block:
        ease 1.4 alpha 0.85
        ease 1.4 alpha 0.35
        repeat

screen lc_demo_release_row(title, note, badge, delay):
    hbox at lc_demo_slide(delay):
        spacing 18
        fixed:
            xysize (170, 40)
            yalign 0.5
            add Solid("#ff8fc0" if badge == "NEXT UP" else "#ffffff40") xysize (170, 40)
            text badge font "fonts/Handjet-ExtraBold.ttf" size 18 color ("#3b1028" if badge == "NEXT UP" else "#ffffff") xalign 0.5 yalign 0.5
            if badge == "NEXT UP":
                add Solid("#ffffff40") xysize (170, 40) at lc_demo_glow
        vbox:
            spacing 2
            yalign 0.5
            text title font "fonts/Fredoka-SemiBold.ttf" size 34 color "#ffffff"
            text note style "lc_title_small_text" size 22 color "#ffffffc0"

screen lc_demo_end_screen():
    modal True
    zorder 190
    on "show" action Function(lc_bgm, "polaroid_summer", 3.0)

    # Living backdrop, same layers as the title screen.
    add lc_title_bg_now() at lc_title_bg_drift
    add "gui/title/light_leak.png"
    add "gui/title/shade_left.png"
    add SnowBlossom(Transform("gui/title/bokeh.png", alpha=0.6), count=18, border=60, xspeed=(-18, 18), yspeed=(-40, -12), start=4, horizontal=False)
    add lc_title_leia_now() at lc_title_leia
    add "gui/title/vignette.png"
    add "gui/title/shade_bottom.png" yalign 1.0

    # One-line logo with its sheen, floating.
    fixed at lc_title_logo_in:
        xpos 96
        ypos 58
        xysize (860, 140)
        add lc_title_logo() at lc_title_logo_float

    vbox:
        xpos 136
        ypos 236
        xsize 900
        spacing 14

        text "Thank you for playing the demo!" font "fonts/Fredoka-SemiBold.ttf" size 54 color "#ffffff" at lc_demo_in(0.9)
        text "You've finished the Prologue and Chapter One (Day One). Your tags, stickers and gallery unlocks are saved for the full game." style "lc_title_small_text" size 25 color "#ffffffd0" xmaximum 860 at lc_demo_in(1.2)

        null height 18
        text "UPCOMING RELEASES" font "fonts/Handjet-ExtraBold.ttf" size 26 color "#ff9fc8" at lc_demo_in(1.6)
        use lc_demo_release_row("Day 2", "The next update", "NEXT UP", 1.9)
        use lc_demo_release_row("Days 3–5", "In development", "SOON", 2.2)

        null height 22
        text "Follow along, get early builds and vote on what comes next:" style "lc_title_small_text" size 22 color "#ffffffb0" at lc_demo_in(2.6)
        # Four calls to action in fixed slots (darryn 2026-11-09): each button
        # enters and pulses on its own, centred in its slot, so the scaling never
        # moves its neighbours or the text below.
        fixed:
            xysize (LC_DEMO_CTA_W * 2 + LC_DEMO_CTA_GAP, LC_DEMO_CTA_H * 2 + LC_DEMO_CTA_GAP)
            use lc_demo_cta_button(0, 0, "SUPPORT ON PATREON", "#ff6fae", "#ff8fc0", LC_PATREON_URL, 2.8, 0.0)
            use lc_demo_cta_button(1, 0, "JOIN THE DISCORD", "#5865f2", "#7983f5", LC_DISCORD_URL, 2.95, 0.45)
            use lc_demo_cta_button(0, 1, "FOLLOW ON X", "#14171c", "#2b313b", LC_X_URL, 3.1, 0.9)
            use lc_demo_cta_button(1, 1, "FEEDBACK ON F95", "#b8343f", "#d24a55", LC_F95_URL, 3.25, 1.35)
        text "Enjoyed it? A like and a comment on the F95 thread really helps, and every bit of feedback gets read." style "lc_title_small_text" size 20 color "#ffffffa0" xmaximum 860 at lc_demo_in(3.45)

        null height 4
        fixed at lc_demo_in(3.6):
            xysize (380, 50)
            use lc_title_item("Main Menu", Return(), "back")

    hbox:
        xalign 1.0
        xoffset -40
        ypos 34
        spacing 14
        text "DEMO" style "lc_title_small_text" yalign 0.5
        add "gui/title/badge18.png" yalign 0.5

    key "game_menu" action Return()
