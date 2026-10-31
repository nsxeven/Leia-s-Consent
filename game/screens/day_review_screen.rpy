# End-of-day scrapbook. Pixel chrome is pre-scaled 3x (nearest) in
# game/images/ui/scrapbook. Handwriting stays smooth Caveat on top.
# A click sets `skipped` and every drop, flash and tick snaps to the end.

transform lc_night_in:
    alpha 0.0
    linear 1.1 alpha 1.0

transform lc_spread_in:
    alpha 0.0
    linear 0.28 alpha 1.0

transform lc_spread_still:
    alpha 1.0

transform lc_polaroid_drop(delay, tilt, x, y):
    anchor (0.5, 0.5)
    xpos x
    ypos y
    alpha 0.0
    yoffset -46
    rotate (tilt + 8.0)
    pause delay
    parallel:
        linear 0.12 alpha 1.0
    parallel:
        easein 0.16 yoffset 9 rotate (tilt - 1.2)
        easeout 0.10 yoffset -7 rotate tilt
        easeout 0.08 yoffset 0

transform lc_polaroid_still(tilt, x, y):
    anchor (0.5, 0.5)
    xpos x
    ypos y
    alpha 1.0
    yoffset 0
    rotate tilt

transform lc_tape_in(delay):
    alpha 0.0
    pause delay
    linear 0.08 alpha 1.0

transform lc_tape_still:
    alpha 1.0

transform lc_arrow_pop:
    alpha 0.0
    yoffset 12
    easeout 0.10 alpha 1.0 yoffset -8
    easeout 0.08 yoffset 3
    easeout 0.06 yoffset 0

transform lc_title_arrive:
    alpha 0.0
    yoffset -12
    easeout 0.25 alpha 1.0 yoffset 0
    pause 2.1
    linear 0.3 alpha 0.0

define lc_font_pixel = "fonts/Silkscreen-Regular.ttf"
define lc_font_pixel_bold = "fonts/Silkscreen-Bold.ttf"
define lc_font_hand = "fonts/Caveat-Medium.ttf"
define lc_font_hand_bold = "fonts/Caveat-SemiBold.ttf"

style lc_pixel is default:
    font lc_font_pixel
    size 24
    color "#3b2a30"
    hinting "none"
    antialias False
    adjust_spacing False
    kerning 0.0

style lc_pixel_bold is lc_pixel:
    font lc_font_pixel_bold

style lc_pixel_dim is lc_pixel:
    color "#7a6266"

style lc_hand is default:
    font lc_font_hand
    size 38
    color "#34242c"
    hinting "auto"

style lc_hand_quote is lc_hand:
    font lc_font_hand_bold
    size 33
    color "#463460"

style lc_hand_tag is lc_hand:
    font lc_font_hand_bold
    size 30
    color "#463020"

style lc_hand_night is lc_hand:
    size 34
    color "#d6c8e0"

style lc_continue is button:
    background Frame("images/ui/scrapbook/continue.png", 9, 9, 9, 9)
    hover_background Frame("images/ui/scrapbook/continue_hover.png", 9, 9, 9, 9)
    xysize (312, 66)
    padding (0, 0)
    hover_sound None
    activate_sound None

style lc_stat_bar is bar:
    left_gutter 0
    right_gutter 0
    thumb None
    thumb_shadow None
    ysize 21
    xsize 600

init python:
    class LcReviewDelta(renpy.Displayable):
        """The green gain or red loss on a stat bar.

        Moves linearly over `delay` seconds, the same clock AnimatedValue uses,
        then flashes for a third of a second. delay <= 0 draws the settled segment.
        """

        def __init__(self, old, new, delay, **kwargs):
            super(LcReviewDelta, self).__init__(**kwargs)
            self.old = float(old)
            self.new = float(new)
            self.delay = float(delay)
            self.t0 = None
            self.inner = 600
            self.height = 21
            self.gain = Frame("images/ui/scrapbook/bar_gain.png", 0, 6, 0, 0)
            self.flash = Frame("images/ui/scrapbook/bar_flash.png", 0, 6, 0, 0)
            self.loss = "images/ui/scrapbook/bar_loss.png"

        def _px(self, value):
            return int(round(value * self.inner / 100.0))

        def render(self, width, height, st, at):
            if self.t0 is None:
                self.t0 = st
            if self.delay <= 0:
                frac = 1.0
            else:
                frac = min(1.0, max(0.0, (st - self.t0) / self.delay))
            current = self.old + (self.new - self.old) * frac
            lo = min(self.old, current)
            hi = max(self.old, current)
            x0 = self._px(lo)
            x1 = self._px(hi)
            rv = renpy.Render(self.inner, self.height)
            seg = x1 - x0
            if seg > 0:
                elapsed = 0 if self.t0 is None else (st - self.t0)
                flashing = (
                    self.delay > 0
                    and frac >= 1.0
                    and (elapsed - self.delay) < 0.30
                    and int((elapsed - self.delay) * 20) % 2 == 0
                )
                if flashing:
                    piece = renpy.render(self.flash, seg, self.height, st, at)
                elif self.new >= self.old:
                    piece = renpy.render(self.gain, seg, self.height, st, at)
                else:
                    piece = renpy.render(
                        Transform(self.loss, crop=(0, 0, seg, self.height)),
                        seg, self.height, st, at)
                rv.blit(piece, (x0, 0))
            if self.delay > 0 and (st - self.t0) < self.delay + 0.30:
                renpy.redraw(self, 0)
            return rv

    class LcReviewTick(renpy.Displayable):
        """Today's number, counting from yesterday in step with the bar."""

        def __init__(self, old, new, delay, **kwargs):
            super(LcReviewTick, self).__init__(**kwargs)
            self.old = int(old)
            self.new = int(new)
            self.delay = float(delay)
            self.t0 = None

        def render(self, width, height, st, at):
            if self.t0 is None:
                self.t0 = st
            if self.delay <= 0:
                frac = 1.0
            else:
                frac = min(1.0, max(0.0, (st - self.t0) / self.delay))
            value = int(round(self.old + (self.new - self.old) * frac))
            color = "#5f8a32" if self.new > self.old else "#a8453f"
            text = Text(
                str(value),
                font=lc_font_pixel,
                size=24,
                color=color,
                antialias=False,
                hinting="none",
                adjust_spacing=False,
            )
            rend = renpy.render(text, 120, 48, st, at)
            tw, th = rend.get_size()
            rv = renpy.Render(max(1, tw), max(1, th))
            rv.blit(rend, (0, 0))
            if frac < 1.0:
                renpy.redraw(self, 0)
            return rv


screen lc_review_night_screen(day_id):
    modal True
    zorder 220
    $ night = lc_review_night_copy(day_id)
    $ cx = lc_px(LC_REVIEW_NIGHT_CARD[0])
    $ cy = lc_px(LC_REVIEW_NIGHT_CARD[1])
    $ cw = lc_px(LC_REVIEW_NIGHT_CARD[2])
    $ ch = lc_px(LC_REVIEW_NIGHT_CARD[3])

    timer 3.2 action Return("next")
    key "K_SPACE" action Return("skip")
    key "K_RETURN" action Return("skip")
    key "K_ESCAPE" action Return("skip")
    key "K_KP_ENTER" action Return("skip")

    fixed at lc_night_in:
        add "images/ui/scrapbook/night.png"
        fixed:
            xpos cx
            ypos cy
            xsize cw
            ysize ch
            hbox:
                align (0.5, 0.5)
                spacing 16
                text night["kicker"] style "lc_pixel_bold" size 48 color "#a83a5a"
                if night["title"]:
                    add "images/ui/scrapbook/diamond.png" yalign 0.55
                    text night["title"] style "lc_pixel_bold" size 48 color "#a83a5a"
        if night["chapter"]:
            text night["chapter"] style "lc_pixel" size 24 color "#9b8aa6" xalign 0.5 ypos (cy + ch + 16)
        text night["line"] style "lc_hand_night" xalign 0.5 ypos (cy + ch + 52)

    button:
        xfill True
        yfill True
        background None
        hover_background None
        padding (0, 0)
        action Return("skip")


screen lc_review_tag(who, title):
    fixed:
        xsize 372
        ysize 120
        add "images/ui/scrapbook/tag.png"
        text who style "lc_pixel_bold" size 24 color "#5a4030" xpos 48 ypos 16 xmaximum 300 substitute False
        text title style "lc_hand_tag" xpos 46 ypos 50 xmaximum 310 substitute False


screen lc_review_bar_row(row, index, photo_count, bar_count, skipped, exact):
    $ timing = lc_review_bar_timing(index, photo_count, bar_count)
    $ start = timing[0]
    $ duration = timing[1]
    $ look = LC_REVIEW_BAR_STYLE[row["stat"]]
    $ fill = "images/ui/scrapbook/bar_fill_{}.png".format(row["stat"])
    $ arrow = "images/ui/scrapbook/arrow_up.png" if row["delta"] > 0 else "images/ui/scrapbook/arrow_down.png"
    default phase = "done" if skipped else "wait"
    $ show_wait = (not skipped) and phase == "wait"
    $ show_run = (not skipped) and phase == "run"
    $ show_flash = (not skipped) and phase == "flash"
    $ show_final = skipped or phase == "done"

    if show_wait:
        timer start action SetScreenVariable("phase", "run")
    elif show_run:
        timer duration action [SetScreenVariable("phase", "flash"), Function(lc_review_sfx, "tick")]
    elif show_flash:
        timer 0.30 action SetScreenVariable("phase", "done")

    fixed:
        xsize 762
        ysize 72
        add "images/ui/scrapbook/icon_{}.png".format(look["icon"]) xpos 0 ypos 26
        text row["label"] style "lc_pixel" size 24 color "#3b2a30" xpos 48 ypos 0
        if exact:
            hbox:
                xanchor 1.0
                xpos 654
                ypos 0
                spacing 6
                text str(row["yesterday"]) style "lc_pixel_dim" size 24
                add "images/ui/scrapbook/arrow_mid.png" yalign 0.55
                if show_run or show_flash:
                    add LcReviewTick(row["yesterday"], row["today"], duration) yalign 0.45
                elif show_final:
                    text str(row["today"]) style "lc_pixel" size 24 color ("#5f8a32" if row["delta"] > 0 else "#a8453f")
                else:
                    text str(row["yesterday"]) style "lc_pixel_dim" size 24
        hbox:
            xpos 48
            ypos 34
            spacing 10
            fixed:
                xsize 606
                ysize 27
                add Solid("#3b2a30")
                bar:
                    style "lc_stat_bar"
                    xpos 3
                    ypos 3
                    left_bar Frame(fill, 0, 6, 0, 0)
                    right_bar Frame("images/ui/scrapbook/bar_track.png", 0, 3, 0, 0)
                    if show_run or show_flash:
                        value AnimatedValue(value=row["today"], range=100.0, delay=duration, old_value=row["yesterday"])
                    elif show_final:
                        value StaticValue(row["today"], 100.0)
                    else:
                        value StaticValue(row["yesterday"], 100.0)
                if show_run or show_flash:
                    add LcReviewDelta(row["yesterday"], row["today"], duration) xpos 3 ypos 3
                elif show_final:
                    add LcReviewDelta(row["yesterday"], row["today"], 0) xpos 3 ypos 3
                else:
                    add Solid("#7a6266") xpos (3 + int(round(row["yesterday"] * 6))) ypos 2 xsize 3 ysize 23
            if show_flash:
                add arrow yalign 0.45 at lc_arrow_pop
            elif show_final:
                add arrow yalign 0.45


screen lc_day_review_screen(day_id, replay=False, skipped=False):
    modal True
    zorder 220
    if replay or not persistent.lc_recap_animation:
        $ skipped = True
    default show_choices = True
    $ mode = current_choice_mode()
    $ exact = mode in ("full", "developer")
    $ night = lc_review_night_copy(day_id)
    $ cards = lc_review_cards(day_id)
    $ slots = lc_review_polaroid_slots(len(cards))
    $ bars = lc_review_bar_rows(day_id, mode)
    $ choices = lc_review_choice_details(day_id) if mode != "normal" else []
    $ diary = lc_review_diary(day_id)
    $ titles = lc_review_titles(day_id)
    $ ticket = lc_review_ticket(day_id)
    $ record = lc_review_days[day_id]
    $ show_stats = lc_review_show_stats(day_id, mode)
    $ unchanged = lc_review_unchanged_count(day_id, mode)
    $ route_label = LC_REVIEW_ROUTES.get(record.get("route"), LC_REVIEW_ROUTES["mixed"])[0]
    $ leave = Hide("lc_review_history_screen") if replay else Return()

    if not skipped:
        key "K_SPACE" action SetScreenVariable("skipped", True)
    else:
        key "K_SPACE" action leave

    key "K_ESCAPE" action leave
    key "K_RETURN" action leave

    # Clicks that miss a real button skip the drops and the bars.
    button:
        xpos 0
        ypos 0
        xsize 1920
        ysize 1080
        background None
        hover_background None
        padding (0, 0)
        action If(skipped, NullAction(), SetScreenVariable("skipped", True))

    add "images/ui/scrapbook/spread.png" at (lc_spread_still if skipped else lc_spread_in)

    if not cards:
        text "No photographs\nfrom today." style "lc_hand" textalign 0.5 xpos lc_px(38) ypos lc_px(88) xsize lc_px(280) color "#7a5648"
    else:
        for index, card in enumerate(cards):
            $ slot = slots[index]
            $ px = lc_px(slot["x"] + 54)
            $ py = lc_px(slot["y"] + 43)
            $ land = lc_review_photo_land(index)
            fixed at (lc_polaroid_still(slot["tilt"], px, py) if skipped else lc_polaroid_drop(lc_review_photo_delay(index), slot["tilt"], px, py)):
                xsize lc_px(108)
                ysize lc_px(86)
                add Solid("#140a0866") xpos 8 ypos 12 xsize 324 ysize 258
                add "images/ui/scrapbook/polaroid.png"
                fixed:
                    xpos 15
                    ypos 15
                    xsize 294
                    ysize 192
                    clipping True
                    if renpy.has_image("cg " + card["image"]):
                        add Transform(Transform("cg " + card["image"], fit="cover", xysize=(98, 64)), zoom=3, nearest=True)
                if card.get("dream"):
                    text "DREAM" style "lc_pixel_bold" size 18 color "#a83a5a" xpos 24 ypos 214
                for tape_name in slot["tapes"]:
                    if tape_name == "top":
                        add "images/ui/scrapbook/tape_top.png" xpos 117 ypos -10 at (lc_tape_still if skipped else lc_tape_in(land))
                    elif tape_name == "corner":
                        add "images/ui/scrapbook/tape_corner.png" xpos -18 ypos -16 at (lc_tape_still if skipped else lc_tape_in(land))
                    else:
                        add "images/ui/scrapbook/tape_corner_flip.png" xpos 270 ypos -16 at (lc_tape_still if skipped else lc_tape_in(land))
            if not skipped:
                timer land action Function(lc_review_sfx, "paper")

    if len(cards) < 5:
        fixed:
            xpos lc_px(96)
            ypos lc_px(250)
            xsize 372
            ysize 108
            add "images/ui/scrapbook/ticket.png"
            text ticket["title"] style "lc_pixel_bold" size 24 color "#6a2338" xpos 24 ypos 16
            text ticket["detail"] style "lc_pixel" size 24 color "#8a4a5c" xpos 24 ypos 52
            text "Nº" style "lc_pixel" size 18 color "#8a4a5c" xpos 292 ypos 28
            text ticket["number"] style "lc_pixel_bold" size 24 color "#6a2338" xpos 286 ypos 52
        add "images/ui/scrapbook/tape_corner_flip.png" xpos (lc_px(96) + 324) ypos (lc_px(250) - 18)

    fixed:
        xpos lc_px(338)
        ypos lc_px(18)
        xsize lc_px(256)
        ysize lc_px(292)
        vbox:
            spacing 8
            hbox:
                spacing 14
                text night["kicker"] style "lc_pixel_bold" size 32 color "#3b2a30"
                if night["title"]:
                    add "images/ui/scrapbook/diamond.png" yalign 0.55
                    text night["title"] style "lc_pixel_bold" size 32 color "#3b2a30" xmaximum 420
            fixed:
                xsize 740
                ysize 44
                if night["chapter"]:
                    text night["chapter"] style "lc_pixel" size 24 color "#7a6266" yalign 0.5
                if mode != "normal":
                    frame:
                        xalign 1.0
                        yalign 0.5
                        background Frame("images/ui/scrapbook/stamp.png", 9, 9, 9, 9)
                        padding (16, 6)
                        text route_label.upper() style "lc_pixel_bold" size 24 color "#a83a5a"
            add "images/ui/scrapbook/rule_dots.png" xsize 740 ysize 3
            viewport:
                xsize 750
                ysize 560
                mousewheel True
                draggable True
                arrowkeys True
                vbox:
                    xsize 730
                    spacing 6
                    text diary[0] style "lc_hand" xmaximum 730
                    add "images/ui/scrapbook/rule.png" xsize 730 ysize 3
                    text diary[1] style "lc_hand" xmaximum 730
                    add "images/ui/scrapbook/rule.png" xsize 730 ysize 3
                    if record.get("partial"):
                        text "This page was started mid-day. Earlier changes were not kept." style "lc_hand_quote" size 28 color "#8a5a40" xmaximum 730
                    if any(card.get("dream") for card in cards):
                        text "A dream is not what happened." style "lc_hand_quote" size 28 color "#8a5a40" xmaximum 730
                    if choices:
                        null height 8
                        hbox:
                            spacing 8
                            add "images/ui/scrapbook/bubble.png" yalign 0.5
                            text "WHAT I SAID" style "lc_pixel" size 24 color "#7a6266" yalign 0.5
                        for row in choices:
                            text lc_review_quote(row["text"]) style "lc_hand_quote" xsize 680 substitute False
                            if exact and show_choices:
                                for line in row["lines"]:
                                    hbox:
                                        spacing 6
                                        for chip in line:
                                            frame:
                                                background Frame("images/ui/scrapbook/chip_up.png" if chip["value"] > 0 else "images/ui/scrapbook/chip_down.png", 6, 6, 6, 6)
                                                padding (8, 1)
                                                hbox:
                                                    spacing 4
                                                    add ("images/ui/scrapbook/tick_up.png" if chip["value"] > 0 else "images/ui/scrapbook/tick_down.png") yalign 0.5
                                                    text chip["text"] style "lc_pixel" size 24 color ("#5f8a32" if chip["value"] > 0 else "#a8453f") yalign 0.5
                        if exact:
                            textbutton ("HIDE CHOICE DETAILS" if show_choices else "SHOW CHOICE DETAILS"):
                                action ToggleScreenVariable("show_choices")
                                text_style "lc_pixel"
                                text_size 18
                                text_color "#7a6266"
                                text_hover_color "#3b2a30"
                                background None
                                hover_background None
                                padding (0, 6)
                    if show_stats:
                        null height 8
                        hbox:
                            spacing 8
                            add "images/ui/scrapbook/mark.png" yalign 0.5
                            text "SINCE YESTERDAY" style "lc_pixel" size 24 color "#7a6266" yalign 0.5
                        for index, row in enumerate(bars):
                            use lc_review_bar_row(row, index, len(cards), len(bars), skipped, exact)
                        if unchanged:
                            hbox:
                                spacing 10
                                text "{} UNCHANGED".format(unchanged) style "lc_pixel" size 24 color "#7a6266" yalign 0.5
                                add "images/ui/scrapbook/rule.png" yalign 0.5 xsize 280 ysize 3
                        elif not bars:
                            text "Nothing moved today." style "lc_pixel" size 24 color "#7a6266"
                    if exact and record.get("modified"):
                        text "This playthrough includes developer or Route Explorer adjustments." style "lc_hand_quote" size 26 color "#8a5a40" xmaximum 730
        if titles[0]:
            hbox:
                spacing 8
                xpos 0
                ypos 748
                use lc_review_tag(player_name, titles[0])
                use lc_review_tag(girlfriend_name, titles[1])

    fixed:
        xpos 980
        ypos 1005
        xsize 144
        ysize 48
        add Frame("images/ui/scrapbook/keycap.png", 9, 9, 9, 9) xysize (144, 48)
        text "SPACE" style "lc_pixel" size 24 color "#cdb9a8" align (0.5, 0.5)

    # Continue sits on the table beside the book, clear of the page.
    add "images/ui/scrapbook/continue.png" xpos 1160 ypos 1000
    text ("CLOSE" if replay else "CONTINUE") xpos 1220 ypos 1018 style "lc_pixel_bold" size 24 color "#fff3f7"
    add "images/ui/scrapbook/continue_arrow.png" xpos 1408 ypos 1022
    button:
        xpos 1160
        ypos 1000
        xysize (312, 66)
        background None
        hover_background None
        padding (0, 0)
        action leave


screen lc_review_settings():
    frame:
        xfill True
        background Solid("#211c25")
        padding (26, 22)
        vbox:
            spacing 14
            text "DAY REVIEW & CHARACTER TITLES" size 27 color "#ffffff"
            text "Recap detail follows your Information Transparency mode. Photos only use moments shown in this playthrough." size 18 color "#c8b8c5"
            textbutton ("Scrapbook animation: On" if persistent.lc_recap_animation else "Scrapbook animation: Off"):
                action ToggleField(persistent, "lc_recap_animation")
            hbox:
                spacing 25
                text "Titles:" size 21
                textbutton "Off" action SetField(persistent, "lc_title_style", "off")
                textbutton "Story" action SetField(persistent, "lc_title_style", "story")
                textbutton "Genre" action SetField(persistent, "lc_title_style", "genre")
            text ("Selected: " + persistent.lc_title_style.title()) size 17 color "#c8b8c5"
            text "Genre titles can include provocative labels after explicit story milestones. They never change your route." size 17 color "#c8b8c5"
            textbutton ("Brief sprite title badges: On" if persistent.lc_title_badges else "Brief sprite title badges: Off"):
                action ToggleField(persistent, "lc_title_badges")
            text "DAY ONE DREAM" size 23 color "#ffffff"
            hbox:
                spacing 25
                textbutton "Ask each time" action SetField(persistent, "lc_day1_dream", "ask")
                textbutton "Full scene" action SetField(persistent, "lc_day1_dream", "show")
                textbutton "Brief summary" action SetField(persistent, "lc_day1_dream", "summary")
            text ("Selected: " + persistent.lc_day1_dream.title() + ". The waking choice and its consequences remain unchanged. This does not disable NTR elsewhere.") size 17 color "#c8b8c5"

screen lc_title_badge(character_id, title):
    zorder 90
    timer 2.8 action Hide("lc_title_badge")
    if persistent.lc_title_badges and persistent.lc_title_style != "off" and phone_hud_enabled and quick_menu and not renpy.get_screen("lc_day_review_screen") and any(tag.startswith(character_id + "_") for tag in renpy.get_showing_tags()):
        frame:
            xpos (0.78 if character_id == "leia" else 0.22)
            xanchor 0.5
            ypos 0.14
            padding (18, 10)
            background Solid("#211a28df")
            at lc_title_arrive
            text title size 23 color "#f0c4da" substitute False


screen lc_review_history_screen(day_id):
    modal True
    zorder 230
    use lc_day_review_screen(day_id, replay=True)
    key "K_ESCAPE" action Hide("lc_review_history_screen")
