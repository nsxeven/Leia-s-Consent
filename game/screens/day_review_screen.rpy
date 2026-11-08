# End-of-day scrapbook. Pixel chrome is pre-scaled 3x (nearest) in
# game/images/ui/scrapbook. Handwriting stays smooth Caveat on top.
# Clicks never skip. Holding SPACE (LC_REVIEW_HOLD_SKIP s) sets `skipped` and
# every drop, flash and tick snaps to the end.

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

define lc_font_pixel = "fonts/PixelifySans-Regular.ttf"
define lc_font_pixel_bold = "fonts/PixelifySans-Bold.ttf"
define lc_font_hand = "fonts/Caveat-Medium.ttf"
define lc_font_hand_bold = "fonts/Caveat-SemiBold.ttf"

style lc_pixel is default:
    font lc_font_pixel
    size 24
    color "#3b2a30"
    hinting "bytecode"
    antialias True
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

style lc_review_viewport is viewport
style lc_review_side is side
style lc_review_vscrollbar is vscrollbar:
    xsize 10
    base_bar Solid("#e3d5b8")
    thumb Solid("#8a6a50")
    unscrollable "hide"

init python:
    class LcReviewDelta(renpy.Displayable):
        """The green gain or red loss on a stat bar.

        Owns the whole moving part of the bar on ONE clock: the static fill
        underneath stops at min(old, new), and this draws the stat's own fill,
        the change segment and a dark divider at the boundary, so colours never
        drift apart. Ends with one soft glow instead of a strobe.
        delay <= 0 draws the settled state.
        """

        GLOW = 0.45

        def __init__(self, old, new, delay, width=600, fill=None, key=None, **kwargs):
            super(LcReviewDelta, self).__init__(**kwargs)
            self.key = key
            self.old = float(old)
            self.new = float(new)
            self.delay = float(delay)
            self.t0 = None
            self.inner = int(width)
            self.height = 14
            self.fill = Frame(fill, 0, 6, 0, 0) if fill else None
            self.gain = Frame("images/ui/scrapbook/bar_gain.png", 0, 6, 0, 0)
            # Losses read clearly red: bar_loss_red.png is the gain art's pixel
            # shading on a red ramp (the old pale-pink bar_loss.png read as faded).
            self.loss = Frame("images/ui/scrapbook/bar_loss_red.png", 0, 6, 0, 0)
            self.divider = Solid("#3b2a30")
            self.flash = Frame("images/ui/scrapbook/bar_flash.png", 0, 6, 0, 0)

        def _px(self, value):
            return int(round(value * self.inner / 100.0))

        def _blit(self, rv, d, x0, x1, st, at, alpha=1.0):
            if x1 - x0 <= 0:
                return
            piece = renpy.render(Transform(d, alpha=alpha) if alpha < 1.0 else d, x1 - x0, self.height, st, at)
            rv.blit(piece, (x0, 0))

        def render(self, width, height, st, at):
            if self.t0 is None:
                self.t0 = st
            if self.key is not None and self.delay > 0:
                import time
                elapsed = time.time() - lc_review_anim_start(self.key)
            else:
                elapsed = st - self.t0
            if self.delay <= 0:
                frac = 1.0
            else:
                frac = min(1.0, max(0.0, elapsed / self.delay))
                # Ease out so the bar settles instead of stopping dead.
                frac = 1.0 - (1.0 - frac) ** 2
            current = self.old + (self.new - self.old) * frac
            rv = renpy.Render(self.inner, self.height)
            gain = self.new >= self.old
            if gain:
                seg0, seg1 = self._px(self.old), self._px(current)
                self._blit(rv, self.gain, seg0, seg1, st, at)
                divider = seg0
            else:
                # Not-yet-lost part keeps the stat's own colour.
                if self.fill is not None:
                    self._blit(rv, self.fill, self._px(self.new), self._px(current), st, at)
                seg0, seg1 = self._px(current), self._px(self.old)
                self._blit(rv, self.loss, seg0, seg1, st, at)
                divider = self._px(self.new)
            # One soft glow over the change once it lands (no flicker).
            after = elapsed - self.delay
            if self.delay > 0 and 0 <= after < self.GLOW:
                import math
                glow = 0.22 * math.sin(math.pi * after / self.GLOW)
                lo, hi = min(seg0, seg1), max(seg0, seg1)
                self._blit(rv, self.flash, lo, hi, st, at, alpha=glow)
            # Dark divider where today's change begins, so the change never
            # merges with a similar native colour (e.g. green Momentum).
            if abs(self.new - self.old) > 0 and 0 < divider < self.inner:
                self._blit(rv, self.divider, max(0, divider - 2), divider + 1, st, at)
            if self.delay > 0 and elapsed < self.delay + self.GLOW:
                renpy.redraw(self, 0)
            return rv

    class LcReviewTick(renpy.Displayable):
        """Today's number, counting from yesterday in step with the bar."""

        def __init__(self, old, new, delay, key=None, **kwargs):
            super(LcReviewTick, self).__init__(**kwargs)
            self.key = key
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
                if self.key is not None:
                    import time
                    elapsed = time.time() - lc_review_anim_start(self.key)
                else:
                    elapsed = st - self.t0
                frac = min(1.0, max(0.0, elapsed / self.delay))
                frac = 1.0 - (1.0 - frac) ** 2
            value = int(round(self.old + (self.new - self.old) * frac))
            color = "#5f8a32" if self.new > self.old else "#a8453f"
            text = Text(
                str(value),
                font=lc_font_pixel,
                size=24,
                color=color,
                antialias=True,
                hinting="bytecode",
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
    key "K_SPACE" action Return("next")
    key "K_RETURN" action Return("next")
    key "K_ESCAPE" action Return("next")
    key "K_KP_ENTER" action Return("next")

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
        action Return("next")


screen lc_review_tag(who, title):
    fixed:
        xsize 356
        ysize 92
        add Transform("images/ui/scrapbook/tag.png", xysize=(356, 92))
        text who style "lc_pixel_bold" size 18 color "#5a4030" xpos 44 ypos 10 xmaximum 290 substitute False
        text title style "lc_hand_tag" size 26 xpos 42 ypos 38 xmaximum 296 substitute False


screen lc_review_bar_column(rows, offset, skipped, exact, pitch, col_w, seq_i, seq_phase):
    vbox:
        spacing 0
        xsize col_w
        for index, row in enumerate(rows):
            use lc_review_bar_row(row, index + offset, skipped, exact, pitch, col_w, seq_i, seq_phase) id row["stat"]


screen lc_review_bar_row(row, index, skipped, exact, pitch=56, col_w=730, seq_i=0, seq_phase="done_all"):
    $ duration = LC_REVIEW_BAR_RUN
    $ look = LC_REVIEW_BAR_STYLE[row["stat"]]
    $ fill = "images/ui/scrapbook/bar_fill_{}.png".format(row["stat"])
    $ arrow = "images/ui/scrapbook/arrow_up.png" if row["delta"] > 0 else "images/ui/scrapbook/arrow_down.png"
    # Phase comes from the parent screen's single sequencer. Rows must not own
    # timers: a SetDict/SetScreenVariable rebuild used to restart every other
    # row's wait/run timer and made bars overlap or stall.
    $ phase = lc_review_row_phase(index, seq_i, seq_phase, skipped)
    $ show_wait = (not skipped) and phase == "wait"
    $ show_run = (not skipped) and phase == "run"
    $ show_flash = (not skipped) and phase == "flash"
    $ show_final = skipped or phase == "done"

    $ narrow = col_w < 500
    $ label_size = 16 if narrow else 18
    $ icon_size = 30 if narrow else 39
    $ label_x = icon_size + 6
    $ number_reserve = (100 if narrow else 124) if exact else 4
    $ bar_x = label_x
    $ bar_w = max(80, col_w - bar_x - 36)
    fixed:
        xsize col_w
        ysize pitch
        add Transform("images/ui/scrapbook/icon_{}.png".format(look["icon"]), xysize=(icon_size, icon_size)) xpos 0 yalign 0.5
        text row["label"] style "lc_pixel" size label_size color "#3b2a30" xpos label_x ypos 0 xmaximum (col_w - label_x - number_reserve)
        if exact:
            hbox:
                xanchor 1.0
                xpos (col_w - 2)
                ypos 0
                spacing 4
                text str(row["yesterday"]) style "lc_pixel_dim" size label_size
                add "images/ui/scrapbook/arrow_mid.png" yalign 0.55
                if show_run or show_flash:
                    add LcReviewTick(row["yesterday"], row["today"], duration, key=row["stat"]) yalign 0.45
                elif show_final:
                    text str(row["today"]) style "lc_pixel" size label_size color ("#5f8a32" if row["delta"] > 0 else "#a8453f")
                else:
                    text str(row["yesterday"]) style "lc_pixel_dim" size label_size
        hbox:
            xpos bar_x
            ypos (pitch - 20)
            spacing 6
            fixed:
                xsize (bar_w + 6)
                ysize 20
                add Solid("#3b2a30") xysize (bar_w + 6, 20)
                bar:
                    style "lc_stat_bar"
                    xpos 3
                    ypos 3
                    xsize bar_w
                    ysize 14
                    left_bar Frame(fill, 0, 6, 0, 0)
                    right_bar Frame("images/ui/scrapbook/bar_track.png", 0, 3, 0, 0)
                    # The stat's own fill stays still at the lower value; the
                    # moving part is drawn by LcReviewDelta on a single clock.
                    if show_run or show_flash or show_final:
                        value StaticValue(min(row["yesterday"], row["today"]), 100.0)
                    else:
                        value StaticValue(row["yesterday"], 100.0)
                if show_run or show_flash:
                    add LcReviewDelta(row["yesterday"], row["today"], duration, bar_w, fill, key=row["stat"]) xpos 3 ypos 3
                elif show_final:
                    add LcReviewDelta(row["yesterday"], row["today"], 0, bar_w, fill) xpos 3 ypos 3
                else:
                    add Solid("#7a6266") xpos (3 + int(round(row["yesterday"] * bar_w / 100.0))) ypos 2 xsize 3 ysize 16
            if show_flash:
                add arrow yalign 0.5 at lc_arrow_pop
            elif show_final:
                add arrow yalign 0.5
        # Invisible focus target on top of the row: hover / keyboard focus
        # shows the stat explanation (lc_stat_tip in lc_day_review_screen).
        # Only once this bar has settled: a tooltip change restarts the
        # interaction, which must not happen mid-animation.
        button:
            xpos 0
            ypos 0
            xsize col_w
            ysize pitch
            background None
            hover_background Solid("#cc006614")
            padding (0, 0)
            tooltip (lc_stat_tooltip(row["stat"]) if show_final else None)
            action NullAction()


screen lc_day_review_screen(day_id, replay=False, skipped=False):
    modal True
    zorder 220
    if replay or not persistent.lc_recap_animation:
        $ skipped = True
    default show_choices = True
    # One sequencer for every changed bar. lead → run → flash → next/done_all.
    # Never give each row its own absolute-delay timer (those restart on rebuild).
    default seq_i = 0
    default seq_phase = "lead"
    $ mode = current_choice_mode()
    $ exact = mode in ("full", "developer")
    $ night = lc_review_night_copy(day_id)
    $ cards = lc_review_cards(day_id)
    $ slots = lc_review_polaroid_slots(len(cards))
    $ bars = lc_review_bar_rows(day_id, mode)
    $ choices = lc_review_choice_details(day_id) if mode != "normal" else []
    $ diary = lc_review_diary(day_id)
    $ titles = lc_review_titles(day_id)
    $ stickers = lc_review_stickers(day_id) if titles[0] else []
    $ ticket = lc_review_ticket(day_id)
    $ record = lc_review_days[day_id]
    $ show_stats = lc_review_show_stats(day_id, mode)
    $ unchanged = lc_review_unchanged_count(day_id, mode)
    $ route_label = LC_REVIEW_ROUTES.get(record.get("route"), LC_REVIEW_ROUTES["mixed"])[0]
    $ leave = Hide("lc_review_history_screen") if replay else Return()

    default holding = False
    on "show" action Function(lc_review_hold_reset)
    # A completed SPACE hold finishes everything (same path as replay/animation-off).
    if lc_review_hold_skipped():
        $ skipped = True
    $ animating = (not skipped) and seq_phase != "done_all"

    if animating:
        key "keydown_K_SPACE" action [SetScreenVariable("holding", True), Function(lc_review_hold_down)]
        key "keyup_K_SPACE" action [SetScreenVariable("holding", False), Function(lc_review_hold_up)]
        if holding:
            timer 0.05 repeat True action Function(lc_review_hold_tick)
    else:
        key "keydown_K_SPACE" action Function(lc_review_hold_arm)
        key "keyup_K_SPACE" action If(lc_review_hold_armed(), leave, Function(lc_review_hold_up))
        key "K_ESCAPE" action leave
        key "K_RETURN" action leave

    # Clicks never skip (darryn): this catcher just swallows stray clicks.
    button:
        xpos 0
        ypos 0
        xsize 1920
        ysize 1080
        background None
        hover_background None
        padding (0, 0)
        action NullAction()

    add "images/ui/scrapbook/spread.png" at (lc_spread_still if skipped else lc_spread_in)

    # Once the bar sequencer leaves "lead", freeze polaroids on their landed
    # pose. Otherwise every seq_phase rebuild restarts lc_polaroid_drop ATL.
    $ photos_settled = skipped or seq_phase != "lead"

    if not cards:
        text "No photographs\nfrom today." style "lc_hand" textalign 0.5 xpos lc_px(38) ypos lc_px(88) xsize lc_px(280) color "#7a5648"
    else:
        for index, card in enumerate(cards):
            $ slot = slots[index]
            $ px = lc_px(slot["x"] + 54)
            $ py = lc_px(slot["y"] + 43)
            $ land = lc_review_photo_land(index)
            fixed at (lc_polaroid_still(slot["tilt"], px, py) if photos_settled else lc_polaroid_drop(lc_review_photo_delay(index), slot["tilt"], px, py)):
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
                # No tape on the polaroids (darryn, 2026-11-04).
            if (not skipped) and seq_phase == "lead":
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

    # Right page sits on the paper (x 966–1806, y 42–960). Choices scroll
    # in the space above a reserved block, so every moved stat, both tags,
    # and the handwriting stay on the page. Eight or more bars wrap to two columns.
    $ page_w = 730
    $ text_w = 710
    $ bar_n = len(bars)
    $ two_col = bar_n >= 8
    $ bar_pitch = (48 if two_col else (44 if bar_n >= 7 else (50 if bar_n >= 5 else 56)))
    $ bar_rows = (((bar_n + 1) // 2) if two_col else bar_n)
    $ col_w = (((page_w - 14) // 2) if two_col else page_w)
    $ page_h = 890
    $ footer_h = 0
    $ footer_n = 0
    if show_stats:
        $ footer_h += 24
        $ footer_n += 1
    if show_stats and bars:
        $ footer_h += bar_rows * bar_pitch
        $ footer_n += 1
    if show_stats and (unchanged or not bars):
        $ footer_h += 22
        $ footer_n += 1
    if exact and record.get("modified"):
        $ footer_h += 32
        $ footer_n += 1
    if titles[0]:
        $ footer_h += 92
        $ footer_n += 1
    if stickers:
        $ footer_h += 34
        $ footer_n += 1
    if footer_n > 1:
        $ footer_h += 4 * (footer_n - 1)
    $ split_at = ((bar_n + 1) // 2) if two_col else bar_n

    # Single bar sequencer. Only one timer exists at a time, so a phase change
    # rebuild cannot restart a sibling bar's clock.
    if (not skipped) and show_stats and bars:
        if seq_phase == "lead":
            timer lc_review_bars_lead(len(cards)) action [SetScreenVariable("seq_i", 0), SetScreenVariable("seq_phase", "run"), Function(lc_review_anim_begin, bars[0]["stat"])]
        elif seq_phase == "run":
            timer LC_REVIEW_BAR_RUN action [SetScreenVariable("seq_phase", "flash"), Function(lc_review_sfx, "tick")]
        elif seq_phase == "flash":
            if seq_i + 1 < bar_n:
                timer LC_REVIEW_BAR_GLOW action [SetScreenVariable("seq_i", seq_i + 1), SetScreenVariable("seq_phase", "run"), Function(lc_review_anim_begin, bars[seq_i + 1]["stat"])]
            else:
                timer LC_REVIEW_BAR_GLOW action SetScreenVariable("seq_phase", "done_all")
    elif (not skipped) and seq_phase == "lead":
        timer lc_review_bars_lead(len(cards)) action SetScreenVariable("seq_phase", "done_all")

    fixed:
        xpos lc_px(336)
        ypos 50
        xsize page_w
        ysize page_h
        clipping True
        vbox:
            spacing 4
            xsize page_w
            ysize (page_h - footer_h)
            hbox:
                spacing 10
                xsize text_w
                text night["kicker"] style "lc_pixel_bold" size 28 color "#3b2a30"
                if night["title"]:
                    add "images/ui/scrapbook/diamond.png" yalign 0.55
                    text night["title"] style "lc_pixel_bold" size 28 color "#3b2a30" xmaximum 360
            fixed:
                xsize page_w
                ysize 36
                if night["chapter"]:
                    text night["chapter"] style "lc_pixel" size 18 color "#7a6266" yalign 0.5 xmaximum 360
                if mode != "normal":
                    frame:
                        xalign 1.0
                        yalign 0.5
                        background Frame("images/ui/scrapbook/stamp.png", 9, 9, 9, 9)
                        padding (12, 4)
                        text route_label.upper() style "lc_pixel_bold" size 18 color "#a83a5a"
            add "images/ui/scrapbook/rule_dots.png" xsize text_w ysize 3
            text diary[0] style "lc_hand" size 32 xsize text_w
            add "images/ui/scrapbook/rule.png" xsize text_w ysize 3
            text diary[1] style "lc_hand" size 32 xsize text_w
            add "images/ui/scrapbook/rule.png" xsize text_w ysize 3
            if record.get("partial"):
                text "This page was started mid-day. Earlier changes were not kept." style "lc_hand_quote" size 26 color "#8a5a40" xsize text_w
            if any(card.get("dream") for card in cards):
                text "A dream is not what happened." style "lc_hand_quote" size 26 color "#8a5a40" xsize text_w
            viewport id "lc_review_choices":
                style_prefix "lc_review"
                xfill True
                yfill True
                mousewheel True
                draggable True
                arrowkeys True
                scrollbars "vertical"
                vbox:
                    xsize text_w
                    spacing 4
                    if choices:
                        hbox:
                            spacing 8
                            add "images/ui/scrapbook/bubble.png" yalign 0.5
                            text "WHAT I SAID" style "lc_pixel" size 18 color "#7a6266" yalign 0.5
                        for row in choices:
                            text lc_review_quote(row["text"]) style "lc_hand_quote" size 28 xsize text_w substitute False
                            if exact and show_choices:
                                for line in row["lines"]:
                                    hbox:
                                        spacing 4
                                        box_wrap True
                                        xsize text_w
                                        for chip in line:
                                            frame:
                                                background Frame("images/ui/scrapbook/chip_up.png" if chip["value"] > 0 else "images/ui/scrapbook/chip_down.png", 6, 6, 6, 6)
                                                padding (6, 0)
                                                hbox:
                                                    spacing 3
                                                    add ("images/ui/scrapbook/tick_up.png" if chip["value"] > 0 else "images/ui/scrapbook/tick_down.png") yalign 0.5
                                                    text chip["text"] style "lc_pixel" size 16 color ("#5f8a32" if chip["value"] > 0 else "#a8453f") yalign 0.5
                        if exact:
                            textbutton ("HIDE CHOICE DETAILS" if show_choices else "SHOW CHOICE DETAILS"):
                                action ToggleScreenVariable("show_choices")
                                text_style "lc_pixel"
                                text_size 16
                                text_color "#7a6266"
                                text_hover_color "#3b2a30"
                                background None
                                hover_background None
                                padding (0, 2)
        if footer_h:
            vbox:
                yalign 1.0
                xsize page_w
                ysize footer_h
                spacing 4
                if show_stats:
                    fixed:
                        xsize page_w
                        ysize 24
                        hbox:
                            spacing 8
                            yalign 0.5
                            add "images/ui/scrapbook/mark.png" yalign 0.5
                            text "SINCE YESTERDAY" style "lc_pixel" size 18 color "#7a6266" yalign 0.5
                if show_stats and bars:
                    fixed:
                        xsize page_w
                        ysize (bar_rows * bar_pitch)
                        if two_col:
                            hbox:
                                spacing 14
                                use lc_review_bar_column(bars[:split_at], 0, skipped, exact, bar_pitch, col_w, seq_i, seq_phase) id "bars_left"
                                use lc_review_bar_column(bars[split_at:], split_at, skipped, exact, bar_pitch, col_w, seq_i, seq_phase) id "bars_right"
                        else:
                            use lc_review_bar_column(bars, 0, skipped, exact, bar_pitch, col_w, seq_i, seq_phase) id "bars"
                if show_stats and unchanged:
                    text "{} UNCHANGED".format(unchanged) style "lc_pixel" size 16 color "#7a6266" ysize 22
                elif show_stats and not bars:
                    text "Nothing moved today." style "lc_pixel" size 16 color "#7a6266" ysize 22
                if exact and record.get("modified"):
                    text "Developer or Route Explorer adjustments are included." style "lc_hand_quote" size 22 color "#8a5a40" xsize text_w ysize 32
                if titles[0]:
                    hbox:
                        spacing 8
                        ysize 92
                        use lc_review_tag(player_name, titles[0])
                        use lc_review_tag(girlfriend_name, titles[1])
                if stickers:
                    # Moment stickers (darryn): up to two standout choices of the day.
                    hbox:
                        spacing 10
                        ysize 34
                        for sticker in stickers:
                            frame:
                                background Solid("#f4dde3")
                                padding (10, 4)
                                yalign 0.5
                                hbox:
                                    spacing 6
                                    add "images/ui/scrapbook/mark.png" yalign 0.5
                                    text sticker.upper() style "lc_pixel" size 16 color "#8a3058" yalign 0.5 substitute False

    fixed:
        xpos 1310
        ypos 996
        xsize 144
        ysize 48
        add Frame("images/ui/scrapbook/keycap.png", 9, 9, 9, 9) xysize (144, 48)
        text "SPACE" style "lc_pixel" size 24 color "#cdb9a8" align (0.5, 0.5)
        if animating and holding:
            add Solid("#e8a0b4") xpos 8 ypos 40 ysize 4 xsize max(1, int(128 * lc_review_hold_progress()))

    if animating:
        text "HOLD TO SKIP" style "lc_pixel" size 18 color "#cdb9a8" xanchor 1.0 xpos 1296 ypos 1010

    $ continue_alpha = 0.45 if animating else 1.0
    add "images/ui/scrapbook/continue.png" xpos 1472 ypos 988 alpha continue_alpha
    text ("CLOSE" if replay else "CONTINUE") xpos 1536 ypos 1006 style "lc_pixel_bold" size 24 color "#fff3f7" at Transform(alpha=continue_alpha)
    add "images/ui/scrapbook/continue_arrow.png" xpos 1720 ypos 1010 alpha continue_alpha
    button:
        xpos 1472
        ypos 988
        xysize (312, 66)
        background None
        hover_background None
        padding (0, 0)
        action If(animating, NullAction(), leave)

    # Stat explanation card for the focused bar row. The history replay
    # embeds this screen with `use`, so focus belongs to that screen there.
    use lc_stat_tip(GetTooltip("lc_review_history_screen" if replay else "lc_day_review_screen"))


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
