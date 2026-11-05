# Title screen layout. `screen main_menu` (screens/zzzzzzzz_scrapbook_ui.rpy)
# just does `use lc_title_screen`. Logic and the menu-safe list live in
# systems/title_screen.rpy.
#
# Layers, back to front: villa evening (slow push-in) > light leak > left shade >
# bokeh > Leia > vignette > bottom shade > logo, Continue card, menu > memory reel.
#
# Hover rule: hover effects only move things with offsets/zoom inside a
# fixed-size box, so nothing hovering ever changes layout (no menu or reel shift).

define LC_TITLE_BG = "images/backgrounds/villa/villa_pool_evening.webp"
define LC_TITLE_SPRITE = "leia_purple_dress smile"

transform lc_title_bg_drift:
    subpixel True
    xalign 0.5
    yalign 0.5
    zoom 1.16
    block:
        ease 26.0 zoom 1.22
        ease 26.0 zoom 1.16
        repeat

# Leia: placed by her (off-screen) feet so the body breathing envelope
# (same timing as leia_body_idle in game) rises and settles from the bottom.
transform lc_title_leia:
    subpixel True
    zoom 0.74
    xcenter 1470
    yanchor 1.0
    ypos 1277
    alpha 0.0
    parallel:
        pause 0.25
        easein 1.0 alpha 1.0
    parallel:
        block:
            linear 0.65 yzoom 0.985
            pause 0.10
            linear 0.65 yzoom 1.0
            pause 0.10
            repeat

transform lc_title_fade(delay=0.0, dur=0.8):
    alpha 0.0
    pause delay
    easein dur alpha 1.0

transform lc_title_logo_in:
    subpixel True
    alpha 0.0
    yoffset 18
    pause 0.35
    easein 0.9 alpha 1.0 yoffset 0

transform lc_title_reel_scroll(seconds, width):
    subpixel True
    xoffset 0
    linear seconds xoffset -width
    repeat

transform lc_title_card(tilt, lift):
    subpixel True
    rotate tilt
    yoffset lift
    on idle:
        easein 0.30 rotate tilt yoffset lift zoom 1.0
    on hover, selected_hover:
        easein 0.25 rotate 0 yoffset (lift - 18) zoom 1.06

# Menu items: the text slides right, a pink glow fades in and the underline
# grows; all inside a fixed-size button.
transform lc_title_item_slide:
    subpixel True
    xoffset 0
    on idle:
        easein 0.30 xoffset 0
    on hover, selected_hover:
        easein 0.22 xoffset 12

transform lc_title_item_glow:
    alpha 0.0
    on idle:
        easein 0.30 alpha 0.0
    on hover, selected_hover:
        easein 0.22 alpha 1.0

transform lc_title_item_underline:
    subpixel True
    xzoom 0.0
    alpha 0.0
    on idle:
        easein 0.30 xzoom 0.0 alpha 0.0
    on hover, selected_hover:
        easein 0.25 xzoom 1.0 alpha 1.0

style lc_title_item_text is default:
    font "fonts/Nunito-ExtraBold.ttf"
    size 28
    kerning 6
    color "#fff0f6d8"
    # Same outline sizes in every state so the glow copy lines up exactly.
    outlines [(10, "#00000000", 0, 0), (5, "#00000000", 0, 0), (2, "#1e0c1e40", 0, 2)]

style lc_title_item_glow_text is lc_title_item_text:
    color "#ffffff"
    outlines [(10, "#ff7eb614", 0, 0), (5, "#ff7eb630", 0, 0), (2, "#00000000", 0, 2)]

style lc_title_item_button is default:
    padding (0, 0)

style lc_title_small_text is default:
    font "fonts/Nunito-Bold.ttf"
    size 18
    color "#ffffffa0"

style lc_title_caption_text is default:
    font "fonts/Caveat-SemiBold.ttf"
    size 25
    color "#4a3340"
    line_spacing -6
    xalign 0.5
    textalign 0.5


screen lc_title_item(label, action):
    button:
        style "lc_title_item_button"
        xysize (380, 50)
        action action
        hovered Function(lc_ui_play, "tick")
        text label.upper() style "lc_title_item_text" xpos -10 ypos -10 at lc_title_item_slide
        text label.upper() style "lc_title_item_glow_text" xpos -10 ypos -10 at lc_title_item_slide, lc_title_item_glow
        add Solid("#ff8fc0") xysize (130, 3) ypos 44 at lc_title_item_slide, lc_title_item_underline


screen lc_title_polaroid(card):
    # The fixed box keeps the reel's layout constant while the card tilts and zooms.
    fixed:
        xysize (378, 378)
        button:
            xalign 0.5
            yalign 0.5
            background None
            padding (0, 0)
            xysize (248, 286)
            at lc_title_card(card["tilt"], card["lift"])
            if card["locked"]:
                action NullAction()
            else:
                action ShowMenu("gallery_screen")
                hovered Function(lc_ui_play, "tick")
                hover_foreground "gui/title/polaroid_hover.png"
            add "gui/title/polaroid.png"
            fixed:
                xpos 30
                ypos 30
                xysize (188, 150)
                clipping True
                if card["locked"]:
                    add "gui/title/locked.png"
                    text "?" font "fonts/Fredoka-SemiBold.ttf" size 56 color "#c9bcae" xalign 0.5 yalign 0.5
                else:
                    add lc_title_photo(card["image"])
            text card["title"] style "lc_title_caption_text" xpos 124 xanchor 0.5 ypos 188 xmaximum 190


screen lc_title_reel():
    $ cards = lc_title_reel_cards(persistent.lc_title_all_memories)
    $ width = len(cards) * LC_TITLE_REEL_STEP
    fixed:
        xpos 0
        ypos 742
        xysize (1920, 338)
        hbox at lc_title_reel_scroll(lc_title_reel_seconds(len(cards)), width):
            xpos -40
            ypos 0
            spacing -130
            for copy in (0, 1):
                for card in cards:
                    use lc_title_polaroid(card)

    button:
        xalign 1.0
        xoffset -44
        ypos 700
        padding (18, 7)
        background Frame("gui/title/chip.png", 20, 20)
        hover_background Frame("gui/title/chip_hover.png", 20, 20)
        action ToggleField(persistent, "lc_title_all_memories")
        hovered Function(lc_ui_play, "tick")
        text ("Memories: all unlocked" if persistent.lc_title_all_memories else "Memories: safe for work") style "lc_title_small_text" color "#ffffffd0"


screen lc_title_continue(slot):
    button:
        xpos 130
        ypos 236
        xysize (540, 104)
        padding (12, 12)
        background Frame("gui/title/card.png", 24, 24)
        hover_background Frame("gui/title/card_hover.png", 24, 24)
        action FileLoad(slot, confirm=False, slot=True)
        hovered Function(lc_ui_play, "tick")
        at lc_title_fade(0.5, 0.7)
        hbox:
            spacing 18
            yalign 0.5
            fixed:
                xysize (142, 80)
                add Transform(FileScreenshot(slot, slot=True), fit="cover", xysize=(142, 80))
            vbox:
                yalign 0.5
                spacing 2
                text "Continue" font "fonts/Fredoka-SemiBold.ttf" size 32 color "#ffffff"
                text lc_title_continue_label(slot) style "lc_title_small_text" color "#f7d3e3" xmaximum 340


screen lc_title_screen():
    default extras = False
    $ slot = lc_title_continue_slot()
    $ version = lc_title_version()

    # Background, light and Leia.
    add LC_TITLE_BG at lc_title_bg_drift
    add "gui/title/light_leak.png"
    add "gui/title/shade_left.png"
    add SnowBlossom(Transform("gui/title/bokeh.png", alpha=0.55), count=14, border=60, xspeed=(-18, 18), yspeed=(-34, -10), start=6, horizontal=False)
    add LC_TITLE_SPRITE at lc_title_leia
    add "gui/title/vignette.png"
    add "gui/title/shade_bottom.png" yalign 1.0

    # One-line logo across the top left, then Continue and the menu.
    add "gui/title/logo_line.png" zoom 0.78 xpos 96 ypos 58 at lc_title_logo_in

    if slot:
        use lc_title_continue(slot)

    vbox:
        xpos 136
        ypos (372 if slot else 262)
        spacing 0
        at lc_title_fade(0.6, 0.7)
        use lc_title_item("New Game", Start())
        use lc_title_item("Load", ShowMenu("load"))
        use lc_title_item("Gallery", ShowMenu("gallery_screen"))
        use lc_title_item("Settings", ShowMenu("preferences"))
        use lc_title_item("Extras", ToggleScreenVariable("extras"))
        if extras:
            hbox:
                spacing 26
                xoffset 4
                ysize 36
                if chapter_select_unlocked():
                    textbutton "Chapters" action ShowMenu("chapter_select") text_style "lc_title_small_text" text_hover_color "#ff9fc8"
                textbutton "About" action ShowMenu("about") text_style "lc_title_small_text" text_hover_color "#ff9fc8"
                textbutton "Help" action ShowMenu("help") text_style "lc_title_small_text" text_hover_color "#ff9fc8"
        use lc_title_item("Quit", Quit(confirm=False))

    # Corners.
    hbox:
        xalign 1.0
        xoffset -40
        ypos 34
        spacing 14
        if version:
            text version style "lc_title_small_text" yalign 0.5
        add "gui/title/badge18.png" yalign 0.5

    use lc_title_reel()

    key "K_RETURN" action Start()
    key "K_KP_ENTER" action Start()
