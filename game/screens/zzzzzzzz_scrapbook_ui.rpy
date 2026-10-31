# Scrapbook / summer-journal UI.
# Loaded last so these screens and styles replace the stock ones.
# Day-review screens are intentionally not touched.

default lc_cinematic_mode = False
default lc_ui_shooting = False
default lc_dialogue_theme_manual = None
default lc_dialogue_theme_scene = ()

init python:
    import lc_ui_logic

    def lc_ui_play(cue):
        """Style-guide sound hook. No-op until game/audio/ui_<cue>.ogg exists.

        Timings (seconds): polaroid 0.35, rustle 0.40, tape 0.08, bar 0.60,
        tick (hover), thud 0.12.
        """
        if cue not in lc_ui_logic.UI_CUES:
            return
        path = "audio/ui_%s.ogg" % cue
        if renpy.loadable(path):
            renpy.play(path, channel="sound")


    def lc_shown_scene_names():
        names = []
        try:
            tags = renpy.get_showing_tags()
        except Exception:
            return names
        for tag in tags:
            if tag not in ("bg", "cg"):
                continue
            attrs = renpy.get_attributes(tag) or ()
            names.append((tag + " " + " ".join(attrs)).strip())
        return names


    def set_dialogue_theme(theme):
        """Pin the dialogue paper until the shown scene image changes."""
        if theme not in ("day", "night"):
            raise Exception("LC dialogue theme must be 'day' or 'night'.")
        store.lc_dialogue_theme = theme
        store.lc_dialogue_theme_manual = theme
        store.lc_dialogue_theme_scene = tuple(lc_shown_scene_names())


    def lc_refresh_dialogue_theme():
        names = tuple(lc_shown_scene_names())
        manual = store.lc_dialogue_theme_manual
        if manual in ("day", "night") and names != tuple(store.lc_dialogue_theme_scene or ()):
            store.lc_dialogue_theme_manual = None
            manual = None
        store.lc_dialogue_theme = lc_ui_logic.infer_dialogue_theme(
            names,
            manual=manual,
            fallback=store.lc_dialogue_theme or "day",
        )
        if manual not in ("day", "night"):
            store.lc_dialogue_theme_scene = names


    if lc_refresh_dialogue_theme not in config.start_interact_callbacks:
        config.start_interact_callbacks.append(lc_refresh_dialogue_theme)

    # Keep the quick menu up even when an interaction suppresses ordinary overlays.
    if "quick_menu" not in config.always_shown_screens:
        config.always_shown_screens.append("quick_menu")


    def lc_name_kind(who):
        if not who:
            return "neutral"
        key = who.strip().lower()
        aliases = {
            "leia": (getattr(store, "girlfriend_name", "Leia"), "leia"),
            "ryan": (getattr(store, "player_name", "Ryan"), "ryan"),
            "julian": (getattr(store, "friend_name", "Julian"), "julian"),
            "maya": ("maya",),
        }
        for kind, names in aliases.items():
            if key in [n.strip().lower() for n in names if n]:
                return kind
        return "neutral"


    def lc_name_color(kind):
        return {
            "leia": "#6a2338",
            "ryan": "#2f4a52",
            "maya": "#6a4a14",
            "julian": "#3e5a2a",
        }.get(kind, "#3b2a30")


    def lc_speaker_color(who):
        return lc_ui_logic.speaker_color(who, {
            "leia": [getattr(store, "girlfriend_name", "Leia"), "Leia"],
            "ryan": [getattr(store, "player_name", "Ryan"), "Ryan"],
            "julian": [getattr(store, "friend_name", "Julian"), "Julian"],
            "maya": ["Maya"],
        })


    def lc_day_caption():
        flags = getattr(store, "story_flags", {}) or {}
        return lc_ui_logic.day_period_label(flags, store.lc_dialogue_theme or "day")


    def lc_choice_actions(item):
        return [Function(lc_history_record_choice, item.caption), item.action]


    def lc_history_record_choice(caption):
        head, _chips = lc_ui_logic.parse_choice_caption(caption or "")
        if not head:
            return
        entry = renpy.character.HistoryEntry()
        entry.kind = "adv"
        entry.who = "I SAID"
        entry.what = renpy.filter_text_tags(head)
        entry.who_args = {}
        entry.what_args = {}
        entry.window_args = {}
        entry.show_args = {}
        entry.image_tag = None
        entry.multiple = None
        entry.rollback_identifier = None
        store._history_list.append(entry)


    def lc_effect_chips(body):
        chips = []
        for part in (body or "").split("•"):
            piece = " ".join(part.split())
            if not piece or "\n" in piece:
                continue
            bits = piece.split()
            if len(bits) < 2:
                continue
            mark = bits[-1]
            name = " ".join(bits[:-1])
            if mark == "↑":
                chips.append((name, 1, False))
            elif mark == "↓":
                chips.append((name, -1, False))
            else:
                try:
                    chips.append((name, int(mark), True))
                except ValueError:
                    continue
        return chips


    def lc_journal_tab_rows():
        rows = []
        if store.main_menu:
            rows.append(("START", Start(), True))
            if chapter_select_unlocked():
                rows.append(("CHAPTERS", ShowMenu("chapter_select"), False))
            rows.append(("LOAD", ShowMenu("load"), False))
            rows.append(("PREFS", ShowMenu("preferences"), False))
            rows.append(("GALLERY", ShowMenu("gallery_screen"), False))
            rows.append(("ABOUT", ShowMenu("about"), False))
            rows.append(("HELP", ShowMenu("help"), False))
            rows.append(("QUIT", Quit(confirm=False), False))
        else:
            rows.append(("HISTORY", ShowMenu("history"), False))
            rows.append(("SAVE", ShowMenu("save"), False))
            rows.append(("LOAD", ShowMenu("load"), False))
            rows.append(("PREFS", ShowMenu("preferences"), False))
            rows.append(("GALLERY", ShowMenu("gallery_screen"), False))
            rows.append(("STATUS", Show("status_screen"), False))
            if store._in_replay:
                rows.append(("END REPLAY", EndReplay(confirm=True), False))
            else:
                rows.append(("MAIN MENU", MainMenu(), False))
            rows.append(("QUIT", Quit(confirm=True), False))
        return rows


init 999 python:
    _lc_ctc = "gui/scrapbook/ctc.png"
    for _lc_name in ("narrator", "mc", "gf", "friend", "maya", "stranger", "passerby", "stranger_d3"):
        _lc_ch = getattr(store, _lc_name, None)
        if _lc_ch is not None:
            _lc_ch.ctc = _lc_ctc
            _lc_ch.ctc_position = "nestled"


transform lc_lift:
    on idle:
        yoffset 0
    on hover:
        yoffset -3
    on selected_idle:
        yoffset 0
    on selected_hover:
        yoffset -3

transform lc_tab_slide:
    on idle:
        xoffset 0
    on hover:
        xoffset 18
    on selected_idle:
        xoffset 18
    on selected_hover:
        xoffset 18
    on insensitive:
        xoffset 0

transform lc_tab_out:
    xoffset 18
    on hover:
        yoffset -3
    on idle:
        yoffset 0

transform lc_choice_slide:
    on idle:
        xoffset 0
        yoffset 0
    on hover:
        xoffset 24
        yoffset -3
    on insensitive:
        xoffset 0
        yoffset 0

transform lc_only_hover:
    alpha 0.0
    on hover:
        alpha 1.0
    on idle:
        alpha 0.0

transform lc_page_in:
    alpha 0.0
    xoffset 16
    easeout 0.28 alpha 1.0 xoffset 0

transform lc_cg_key:
    alpha 0.5
    on idle:
        alpha 0.5
        yoffset 0
    on hover:
        alpha 1.0
        yoffset -3
    on selected_idle:
        alpha 1.0
        yoffset 0
    on selected_hover:
        alpha 1.0
        yoffset -3


screen lc_side_tab(label, action, index, y, accent=False, xpos=1686):
    $ col = index % 8
    button:
        xpos xpos
        ypos y
        xsize (240 if accent else 210)
        ysize 63
        background Frame(("gui/scrapbook/tab_pink.png" if accent else "gui/scrapbook/tab_%d.png" % col), 9, 9)
        hover_background Frame("gui/scrapbook/tab_pink.png", 9, 9)
        selected_idle_background Frame("gui/scrapbook/tab_pink.png", 9, 9)
        selected_hover_background Frame("gui/scrapbook/tab_pink.png", 9, 9)
        padding (21, 0, 12, 0)
        action action
        selected (True if accent else action.get_selected())
        hovered Function(lc_ui_play, "tick")
        at (lc_tab_out if accent else lc_tab_slide)

        hbox:
            yalign 0.5
            spacing 8
            text label style ("lc_tab_text_on" if accent else "lc_tab_text") yalign 0.5
            if accent:
                add "gui/scrapbook/icon_play.png" yalign 0.5


screen lc_journal_tabs(xpos=1686):
    $ tabs = lc_journal_tab_rows()
    for i, row in enumerate(tabs):
        use lc_side_tab(row[0], row[1], i, 72 + i * 72, row[2], xpos)


screen lc_menu_footer(hints=None):
    hbox:
        xpos 36
        ypos 1012
        spacing 12
        button:
            background Frame("gui/scrapbook/frame_keycap.png", 9, 9)
            hover_background Frame("gui/scrapbook/frame_keycap_on.png", 9, 9)
            padding (12, 6)
            ysize 42
            action Return()
            hovered Function(lc_ui_play, "tick")
            at lc_lift
            text "ESC" style "lc_key_text" yalign 0.5
        text "RETURN" yalign 0.5 size 24 color "#cdb9a8" font "fonts/Silkscreen-Regular.ttf"

    if hints:
        hbox:
            xpos 1180
            ypos 1012
            spacing 18
            for key_label, caption in hints:
                hbox:
                    spacing 8
                    button:
                        background Frame("gui/scrapbook/frame_keycap.png", 9, 9)
                        padding (10, 6)
                        ysize 42
                        action NullAction()
                        text key_label style "lc_key_text"
                    text caption yalign 0.5 size 24 color "#cdb9a8" font "fonts/Silkscreen-Regular.ttf"


screen lc_chip(name, amount, exact=False):
    $ up = amount > 0
    $ col = "#5f8a32" if amount > 0 else ("#7a6266" if amount == 0 else "#a8453f")
    frame:
        background Frame(("gui/scrapbook/chip_up.png" if up else "gui/scrapbook/chip_down.png"), 9, 9)
        padding (8, 1, 8, 1)
        ysize 33
        hbox:
            spacing 4
            yalign 0.5
            add ("gui/scrapbook/icon_up.png" if up else "gui/scrapbook/icon_down.png") yalign 0.5
            text lc_ui_logic.chip_label(name, amount, exact):
                font "fonts/Silkscreen-Regular.ttf"
                size 21
                color col
                yalign 0.5


screen lc_keycap_button(label, action, icon=None, selected_on=False, width=None, ghost=False):
    button:
        if width:
            xsize width
        ysize 42
        padding (12, 4)
        background Frame(("gui/scrapbook/frame_keycap_on.png" if selected_on else "gui/scrapbook/frame_keycap.png"), 9, 9)
        hover_background Frame("gui/scrapbook/frame_keycap_on.png", 9, 9)
        selected_idle_background Frame("gui/scrapbook/frame_keycap_on.png", 9, 9)
        selected_hover_background Frame("gui/scrapbook/frame_keycap_on.png", 9, 9)
        action action
        hovered Function(lc_ui_play, "tick")
        at (lc_cg_key if ghost else lc_lift)
        hbox:
            spacing 6
            yalign 0.5
            if icon:
                add icon yalign 0.5
            text label style "lc_key_text" yalign 0.5


## Say ########################################################################

screen say(who, what):
    $ theme = store.lc_dialogue_theme if store.lc_dialogue_theme in ("day", "night") else "day"
    $ cg = store.lc_cinematic_mode
    $ kind = lc_name_kind(who)
    $ box = "gui/scrapbook/say_cg_%s.png" % theme if cg else "gui/scrapbook/say_%s.png" % theme
    $ ink = "#ece2f2" if theme == "night" else "#34242c"
    $ halo = "#1e1628c0" if theme == "night" else "#efe4cdc0"

    window:
        id "window"
        xpos (120 if cg else 132)
        ypos (942 if cg else 792)
        xsize (1680 if cg else 1656)
        ysize (108 if cg else 222)
        background box
        padding (0, 0)

        if who is not None:
            window:
                id "namebox"
                style "namebox"
                xpos (60 if cg else 54)
                ypos (-30 if cg else -42)
                ysize (42 if cg else 54)
                background Frame("gui/scrapbook/name_%s.png" % kind, 9, 9)
                padding (18, 4, 16, 4)

                hbox:
                    yalign 0.5
                    spacing 8
                    if kind == "leia":
                        add "gui/scrapbook/icon_heart.png" yalign 0.5
                    text who id "who":
                        font "fonts/Silkscreen-Bold.ttf"
                        size (21 if cg else 24)
                        color lc_name_color(kind)
                        yalign 0.5

        text what id "what" at lc_dialogue_text_fade:
            xanchor 0.0
            xpos (72 if cg else 84)
            ypos (16 if cg else 28)
            xsize (1480 if cg else 1500)
            ysize (78 if cg else 176)
            font "fonts/PatrickHand-Regular.ttf"
            size (34 if cg else 42)
            color ink
            line_spacing (2 if cg else 8)
            outlines ([(2, halo, 0, 0)] if cg else [])

        if cg:
            add "gui/scrapbook/tape_h.png" xpos -8 ypos -16
            add "gui/scrapbook/tape_h.png" xpos 1600 ypos -16
        else:
            add "gui/scrapbook/tape_corner.png" xpos -18 ypos -18
            add "gui/scrapbook/tape_corner_flip.png" xpos 1600 ypos -18

    if not renpy.variant("small") and not cg:
        add SideImage() xalign 0.0 yalign 1.0


screen input(prompt):
    modal True
    zorder 150

    add "gui/scrapbook/bg_table.png"

    frame:
        xalign 0.5
        yalign 0.45
        xsize 780
        yminimum 240
        background Frame("gui/scrapbook/frame_kraft.png", 9, 9)
        padding (36, 28)

        vbox:
            spacing 12
            if prompt and "your name" in prompt.lower():
                text "PROPERTY OF" size 24 color "#5a4030" font "fonts/Silkscreen-Bold.ttf"
            elif prompt and "girlfriend" in prompt.lower():
                text "HER NAME" size 24 color "#5a4030" font "fonts/Silkscreen-Bold.ttf"
            elif prompt and "friend" in prompt.lower():
                text "HIS NAME" size 24 color "#5a4030" font "fonts/Silkscreen-Bold.ttf"
            text prompt size 36 color "#3b2a30" font "fonts/PatrickHand-Regular.ttf"
            frame:
                background Frame("gui/scrapbook/frame_paper.png", 9, 9)
                padding (16, 8)
                xfill True
                input id "input" color "#3b2a30" font "fonts/Caveat[wght].ttf" size 48


## Choice #####################################################################

screen choice(items):
    $ dev = current_choice_mode() == "developer"
    zorder 120

    if not dev:
        frame:
            xpos 120
            ypos 78
            background Frame("gui/scrapbook/frame_kraft.png", 9, 9)
            padding (28, 6, 16, 6)
            ysize 48
            text "WHAT DO I SAY?" size 24 color "#5a4030" font "fonts/Silkscreen-Bold.ttf" yalign 0.5

    viewport:
        xpos (80 if dev else 100)
        ypos (70 if dev else 150)
        xsize (1500 if dev else 980)
        ysize (700 if dev else 620)
        scrollbars ("vertical" if dev else None)
        mousewheel True
        draggable dev

        vbox:
            spacing (10 if dev else 16)
            for i, item in enumerate(items):
                if i < 9:
                    key "K_%d" % (i + 1) action lc_choice_actions(item)
                button:
                    action lc_choice_actions(item)
                    sensitive item.action.get_sensitive()
                    xsize (1460 if dev else 820)
                    ysize (90 if dev else 132)
                    yfill False
                    background Frame(("gui/scrapbook/frame_paper.png" if dev else "gui/scrapbook/frame_choice.png"), (9 if dev else 18), 12, 12, 12)
                    hover_background Frame(("gui/scrapbook/frame_paper_hi.png" if dev else "gui/scrapbook/frame_choice_hi.png"), (9 if dev else 18), 12, 12, 12)
                    padding (18, 12, 18, 12)
                    at lc_choice_slide
                    hovered Function(lc_ui_play, "tick")

                    hbox:
                        spacing 14
                        frame:
                            xysize (42, 42)
                            background Frame("gui/scrapbook/frame_paper.png", 9, 9)
                            text str(i + 1) xalign 0.5 yalign 0.5 size 24 color "#7a6266" font "fonts/Silkscreen-Bold.ttf"
                        vbox:
                            spacing 6
                            xsize (1360 if dev else 700)
                            if dev:
                                text item.caption:
                                    size 28
                                    color "#34242c"
                                    font "fonts/PatrickHand-Regular.ttf"
                                    xalign 0.0
                            else:
                                $ line, chips = lc_ui_logic.parse_choice_caption(item.caption)
                                text line:
                                    size 40
                                    color "#34242c"
                                    font "fonts/PatrickHand-Regular.ttf"
                                    xalign 0.0
                                if chips:
                                    hbox:
                                        spacing 8
                                        for chip_name, chip_amount, chip_exact in chips:
                                            use lc_chip(chip_name, chip_amount, chip_exact)

                    if not dev:
                        add "gui/scrapbook/tape_corner_pink_flip.png" xpos 760 ypos -20 at lc_only_hover


## Quick menu #################################################################

screen quick_menu():
    zorder 100

    if quick_menu and not main_menu:
        if store.lc_cinematic_mode:
            hbox:
                xpos 1776
                xanchor 1.0
                ypos 888
                spacing 9
                use lc_keycap_button("", Rollback(), "gui/scrapbook/icon_back.png", width=42, ghost=True)
                use lc_keycap_button("", ShowMenu("history"), "gui/scrapbook/icon_log.png", width=42, ghost=True)
                use lc_keycap_button("", Skip(), "gui/scrapbook/icon_skip.png", width=42, ghost=True)
                use lc_keycap_button("", Preference("auto-forward", "toggle"), "gui/scrapbook/icon_auto.png", width=42, selected_on=preferences.afm_enable, ghost=True)
                use lc_keycap_button("", ShowMenu("save"), "gui/scrapbook/icon_save.png", width=42, ghost=True)
                use lc_keycap_button("", QuickSave(), "gui/scrapbook/icon_qsave.png", width=42, ghost=True)
                use lc_keycap_button("", QuickLoad(), "gui/scrapbook/icon_qload.png", width=42, ghost=True)
                use lc_keycap_button("", ShowMenu("preferences"), "gui/scrapbook/icon_prefs.png", width=42, ghost=True)
                use lc_keycap_button("", HideInterface(), "gui/scrapbook/icon_hide.png", width=42, ghost=True)
        else:
            hbox:
                xpos 132
                ypos 1026
                spacing 0
                use lc_keycap_button(lc_day_caption(), NullAction())

            hbox:
                xpos 1788
                xanchor 1.0
                ypos 1026
                spacing 8
                use lc_keycap_button("BACK", Rollback(), "gui/scrapbook/icon_back.png")
                use lc_keycap_button("LOG", ShowMenu("history"), "gui/scrapbook/icon_log.png")
                use lc_keycap_button("SKIP", Skip(), "gui/scrapbook/icon_skip.png")
                use lc_keycap_button("AUTO", Preference("auto-forward", "toggle"), "gui/scrapbook/icon_auto.png", selected_on=preferences.afm_enable)
                use lc_keycap_button("SAVE", ShowMenu("save"), "gui/scrapbook/icon_save.png")
                use lc_keycap_button("Q.SAVE", QuickSave(), "gui/scrapbook/icon_qsave.png")
                use lc_keycap_button("Q.LOAD", QuickLoad(), "gui/scrapbook/icon_qload.png")
                use lc_keycap_button("PREFS", ShowMenu("preferences"), "gui/scrapbook/icon_prefs.png")


screen quick_menu():
    variant "touch"
    zorder 100

    if quick_menu and not main_menu:
        hbox:
            xalign 0.5
            ypos 1020
            spacing 10
            use lc_keycap_button("BACK", Rollback(), "gui/scrapbook/icon_back.png")
            use lc_keycap_button("SKIP", Skip(), "gui/scrapbook/icon_skip.png")
            use lc_keycap_button("AUTO", Preference("auto-forward", "toggle"), "gui/scrapbook/icon_auto.png")
            use lc_keycap_button("MENU", ShowMenu("save"), "gui/scrapbook/icon_save.png")


## Menus ######################################################################

screen main_menu():
    tag menu
    add "gui/scrapbook/bg_main_menu.png"
    use lc_journal_tabs(1314)

    text "[config.version]" xpos 1760 ypos 1044 size 21 color "#8a6e5e" font "fonts/Silkscreen-Regular.ttf"

    hbox:
        xpos 1500
        ypos 1012
        spacing 10
        use lc_keycap_button("ENTER", Start())
        text "OPEN" yalign 0.5 size 24 color "#cdb9a8" font "fonts/Silkscreen-Regular.ttf"

    key "K_RETURN" action Start()
    key "K_KP_ENTER" action Start()


screen game_menu(title, scroll=None, yinitial=0.0, spacing=0, hints=None):
    on "show" action Function(lc_ui_play, "rustle")

    add "gui/scrapbook/bg_game_menu.png"

    frame at lc_page_in:
        background None
        xpos 54
        ypos 42
        xsize 1620
        ysize 930
        padding (28, 16, 28, 24)

        if scroll == "viewport":
            viewport:
                yinitial yinitial
                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True
                yfill True
                xfill True
                vbox:
                    spacing spacing
                    transclude

        elif scroll == "vpgrid":
            vpgrid:
                cols 1
                yinitial yinitial
                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True
                spacing spacing
                transclude

        else:
            fixed:
                xfill True
                yfill True
                transclude

    use lc_journal_tabs(1686)
    use lc_menu_footer(hints)

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


screen save():
    tag menu
    use file_slots(_("Save"))


screen load():
    tag menu
    use file_slots(_("Load"))


screen file_slots(title):
    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))
    $ is_save = title == _("Save")
    $ hints = [("DEL", "DELETE"), ("ENTER", "SAVE HERE" if is_save else "LOAD")]

    use game_menu(title, hints=hints):
        fixed:
            vbox:
                spacing 4
                xpos 8
                ypos 0
                hbox:
                    spacing 16
                    text ("SAVE" if is_save else "LOAD") size 48 color "#3b2a30" font "fonts/Silkscreen-Bold.ttf"
                    text "PAGE" size 48 color "#3b2a30" font "fonts/Silkscreen-Bold.ttf"
                text ("PICK A PAGE TO KEEP" if is_save else "PICK UP WHERE I LEFT OFF") size 21 color "#7a6266" font "fonts/Silkscreen-Regular.ttf"
                button:
                    action page_name_value.Toggle()
                    key_events True
                    background None
                    padding (0, 0)
                    input:
                        value page_name_value
                        size 28
                        color "#5a4030"
                        font "fonts/Caveat[wght].ttf"

            hbox:
                xpos 700
                ypos 8
                spacing 6
                if config.has_autosave:
                    use lc_keycap_button("A", FilePage("auto"))
                if config.has_quicksave:
                    use lc_keycap_button("Q", FilePage("quick"))
                for page in range(1, 10):
                    use lc_keycap_button(str(page), FilePage(page))

            text "A = AUTO    Q = QUICK" xpos 700 ypos 58 size 21 color "#7a6266" font "fonts/Silkscreen-Regular.ttf"

            grid 4 2:
                xpos 0
                ypos 110
                xspacing 28
                yspacing 18

                for i in range(8):
                    $ slot = i + 1
                    $ filled = FileLoadable(slot)
                    button:
                        action FileAction(slot)
                        xysize (360, 300)
                        background None
                        padding (0, 0)
                        key "save_delete" action FileDelete(slot)
                        hovered Function(lc_ui_play, "tick")
                        at lc_lift

                        if filled:
                            frame:
                                background Frame("gui/scrapbook/frame_polaroid.png", 12, 12)
                                padding (12, 12, 12, 8)
                                xfill True
                                yfill True
                                vbox:
                                    spacing 6
                                    add FileScreenshot(slot) xysize (324, 180) xalign 0.5
                                    text FileSaveName(slot):
                                        font "fonts/Caveat[wght].ttf"
                                        size 32
                                        color "#463460"
                                        xalign 0.0
                                    text FileTime(slot, format=_("{#file_time}%b %d  %H:%M"), empty=""):
                                        size 18
                                        color "#9b8a80"
                                        font "fonts/Silkscreen-Regular.ttf"
                        else:
                            frame:
                                background None
                                xfill True
                                yfill True
                                fixed:
                                    add "gui/scrapbook/photo_corner.png" align (0.0, 0.0)
                                    add Transform("gui/scrapbook/photo_corner.png", xzoom=-1) align (1.0, 0.0)
                                    add Transform("gui/scrapbook/photo_corner.png", yzoom=-1) align (0.0, 1.0)
                                    add Transform("gui/scrapbook/photo_corner.png", xzoom=-1, yzoom=-1) align (1.0, 1.0)
                                    vbox:
                                        align (0.5, 0.5)
                                        spacing 4
                                        text "EMPTY" xalign 0.5 size 24 color "#3b2a30" font "fonts/Silkscreen-Bold.ttf"
                                        text "SLOT [slot]" xalign 0.5 size 21 color "#a8988a" font "fonts/Silkscreen-Regular.ttf"

            key "save_page_prev" action FilePagePrevious()
            key "save_page_next" action FilePageNext()


## Preferences ################################################################

screen preferences():
    tag menu

    use game_menu(_("Preferences"), hints=[("ENTER", "SELECT")]):
        hbox:
            spacing 36
            xfill True

            vbox:
                spacing 10
                xsize 760

                hbox:
                    spacing 14
                    text "PREFS" size 48 color "#3b2a30" font "fonts/Silkscreen-Bold.ttf"
                    text "HOW I PLAY" size 48 color "#3b2a30" font "fonts/Silkscreen-Bold.ttf"
                text "SETTINGS KEEP ACROSS SAVES" size 21 color "#7a6266" font "fonts/Silkscreen-Regular.ttf"

                hbox:
                    spacing 80
                    vbox:
                        spacing 6
                        text "DISPLAY" size 21 color "#7a6266" font "fonts/Silkscreen-Bold.ttf"
                        textbutton _("WINDOW") action Preference("display", "window") style "lc_radio_button" text_style "lc_radio_text"
                        textbutton _("FULLSCREEN") action Preference("display", "fullscreen") style "lc_radio_button" text_style "lc_radio_text"
                    vbox:
                        spacing 6
                        text "SKIP" size 21 color "#7a6266" font "fonts/Silkscreen-Bold.ttf"
                        textbutton _("UNSEEN TEXT") action Preference("skip", "toggle") style "lc_check_button" text_style "lc_check_text"
                        textbutton _("AFTER CHOICES") action Preference("after choices", "toggle") style "lc_check_button" text_style "lc_check_text"
                        textbutton _("TRANSITIONS") action InvertSelected(Preference("transitions", "toggle")) style "lc_check_button" text_style "lc_check_text"

                null height 8
                use lc_pref_slider("TEXT SPEED", Preference("text speed"), "gui/scrapbook/bar_pink.png", ("MAX" if preferences.text_cps == 0 else "%d" % preferences.text_cps))
                use lc_pref_slider("AUTO-FORWARD", Preference("auto-forward time"), "gui/scrapbook/bar_teal.png", "%d" % preferences.afm_time)
                if config.has_music:
                    use lc_pref_slider("MUSIC", Preference("music volume"), "gui/scrapbook/bar_purple.png", "%d%%" % int(preferences.get_volume("music") * 100))
                if config.has_sound:
                    use lc_pref_slider("SOUND", Preference("sound volume"), "gui/scrapbook/bar_gold.png", "%d%%" % int(preferences.get_volume("sound") * 100))
                if config.has_voice:
                    use lc_pref_slider("VOICE", Preference("voice volume"), "gui/scrapbook/bar_grey.png", "%d%%" % int(preferences.get_volume("voice") * 100))
                textbutton _("MUTE ALL") action Preference("all mute", "toggle") style "lc_check_button" text_style "lc_check_text"

            vbox:
                spacing 10
                xsize 740

                text "WHAT I SEE" size 48 color "#3b2a30" font "fonts/Silkscreen-Bold.ttf"
                text "INFORMATION SETTING" size 21 color "#7a6266" font "fonts/Silkscreen-Regular.ttf"

                $ mode_now = current_choice_mode()
                for mode_id in ("normal", "insight", "full"):
                    use lc_info_card(mode_id, mode_now)

                text "changes what I see — never what happens." size 32 color "#463460" font "fonts/Caveat[wght].ttf"

                hbox:
                    spacing 12
                    textbutton "DEVELOPER" action Function(set_choice_display_mode, "developer")
                    textbutton "ROUTE EXPLORER" action Show("lc_route_explorer_screen")

                if mode_now == "developer":
                    text "Developer mode is on. Pick Immersive, Insight, or Full Transparency to leave it." size 28 color "#7a6266" font "fonts/Caveat[wght].ttf"


screen lc_pref_slider(label, value, fill, readout):
    vbox:
        spacing 2
        xfill True
        text label size 21 color "#3b2a30" font "fonts/Silkscreen-Regular.ttf"
        hbox:
            spacing 12
            bar:
                value value
                xsize 560
                ysize 24
                left_bar Frame(fill, 6, 6)
                right_bar Frame("gui/scrapbook/bar_track.png", 6, 6)
                thumb "gui/scrapbook/slider_thumb.png"
                hovered Function(lc_ui_play, "tick")
            text readout yalign 0.5 size 21 color "#7a6266" font "fonts/Silkscreen-Regular.ttf"


screen lc_info_card(mode_id, mode_now):
    $ info = transparency_mode_info(mode_id)
    $ on = mode_now == mode_id
    button:
        action Function(set_player_transparency_mode, mode_id)
        xfill True
        yminimum 132
        background Frame(("gui/scrapbook/frame_card_on.png" if on else "gui/scrapbook/frame_card.png"), 9, 9)
        hover_background Frame("gui/scrapbook/frame_card_on.png", 9, 9)
        padding (16, 10)
        hovered Function(lc_ui_play, "tick")

        vbox:
            spacing 4
            xfill True
            hbox:
                spacing 10
                xfill True
                text info["label"] size 24 color ("#3b2a30" if on else "#7a6266") font "fonts/Silkscreen-Bold.ttf"
                if on:
                    text "SELECTED" size 18 color "#a83a5a" font "fonts/Silkscreen-Regular.ttf" xalign 1.0
            text info["tagline"] size 30 color ("#781446" if on else "#463460") font "fonts/Caveat[wght].ttf"
            if mode_id == "normal":
                text "NO STAT HINTS SHOWN" size 18 color "#a8988a" font "fonts/Silkscreen-Regular.ttf"
            elif mode_id == "insight":
                hbox:
                    spacing 6
                    use lc_chip("LOVE", 1, False)
                    use lc_chip("TRUST", 1, False)
                    use lc_chip("SECRECY", -1, False)
            else:
                hbox:
                    spacing 6
                    use lc_chip("LOVE", 2, True)
                    use lc_chip("TRUST", 2, True)
                    use lc_chip("SECRECY", -1, True)


## History ####################################################################

screen history():
    tag menu
    predict False

    use game_menu(_("History"), hints=[("WHEEL", "SCROLL")]):
        vbox:
            spacing 6
            hbox:
                xfill True
                vbox:
                    spacing 2
                    hbox:
                        spacing 14
                        text "HISTORY" size 48 color "#3b2a30" font "fonts/Silkscreen-Bold.ttf"
                        text ("DAY %d" % lc_ui_logic.story_day_number(story_flags) if lc_ui_logic.story_day_number(story_flags) else "") size 48 color "#3b2a30" font "fonts/Silkscreen-Bold.ttf"
                    text "WHAT WAS SAID" size 21 color "#7a6266" font "fonts/Silkscreen-Regular.ttf"
                vbox:
                    xalign 1.0
                    spacing 2
                    text "NEWEST AT THE BOTTOM" size 21 color "#7a6266" font "fonts/Silkscreen-Regular.ttf" xalign 1.0

        viewport:
            ypos 100
            ysize 780
            xfill True
            mousewheel True
            draggable True
            pagekeys True
            scrollbars "vertical"
            yinitial 1.0

            vbox:
                spacing 6
                if not _history_list:
                    text "The diary is still blank." size 36 color "#7a6266" font "fonts/Caveat[wght].ttf"
                for h in _history_list:
                    $ said = (h.who == "I SAID")
                    $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                    hbox:
                        spacing 12
                        xfill True
                        if said:
                            frame:
                                background Frame("gui/scrapbook/frame_pink.png", 9, 9)
                                padding (8, 2)
                                xsize 108
                                ysize 32
                                text "I SAID" size 18 color "#fff3f7" font "fonts/Silkscreen-Regular.ttf" xalign 0.5 yalign 0.5
                        elif h.who:
                            text h.who:
                                xsize 140
                                font "fonts/Silkscreen-Bold.ttf"
                                size 21
                                color lc_speaker_color(h.who)
                        else:
                            null width 140
                        text what:
                            substitute False
                            xsize 1280
                            font ("fonts/PatrickHand-Regular.ttf" if (h.who and not said) else "fonts/Caveat[wght].ttf")
                            size 34
                            color ("#781446" if said else ("#6e6068" if not h.who else "#34242c"))


## Confirm, skip, notify ######################################################

screen confirm(message, yes_action, no_action):
    modal (not lc_ui_shooting)
    zorder 500

    add Solid("#0e0912aa")

    $ yes_label = "YES, LEAVE" if message and "main menu" in message.lower() else "YES"
    $ no_label = "STAY" if message and "main menu" in message.lower() else "NO"

    frame:
        xalign 0.5
        yalign 0.42
        xsize 760
        yminimum 280
        background Frame("gui/scrapbook/frame_sticky.png", 9, 9)
        padding (28, 22)

        vbox:
            spacing 12
            text "ARE YOU SURE?" size 24 color "#6a5a1a" font "fonts/Silkscreen-Bold.ttf"
            text message size 40 color "#34242c" font "fonts/PatrickHand-Regular.ttf" xalign 0.0
            hbox:
                spacing 24
                xalign 0.0
                textbutton yes_label:
                    action yes_action
                    background Frame("gui/scrapbook/frame_pink.png", 9, 9)
                    hover_background Frame("gui/scrapbook/frame_pink_hover.png", 9, 9)
                    text_idle_color "#fff3f7"
                    text_hover_color "#fff3f7"
                    text_font "fonts/Silkscreen-Bold.ttf"
                    text_size 24
                    padding (18, 8)
                    at lc_lift
                textbutton no_label:
                    action no_action
                    background Frame("gui/scrapbook/frame_paper.png", 9, 9)
                    hover_background Frame("gui/scrapbook/ink_loop.png", 54, 12, 54, 12)
                    text_idle_color "#3b2a30"
                    text_hover_color "#3b2a30"
                    text_selected_color "#3b2a30"
                    text_font "fonts/Silkscreen-Bold.ttf"
                    text_size 24
                    padding (28, 8)
                    at lc_lift

    add "gui/scrapbook/tape_pink_h.png" xalign 0.5 ypos 300

    key "game_menu" action no_action


screen skip_indicator():
    zorder 200
    fixed:
        xpos 30
        ypos 48
        xsize 294
        ysize 45
        add "gui/scrapbook/skip_tape.png"
        text "SKIPPING" align (0.32, 0.5) size 24 color "#5a0030" font "fonts/Silkscreen-Bold.ttf"


screen notify(message):
    zorder 200
    frame at notify_appear:
        xpos 1880
        xanchor 1.0
        ypos 36
        background Frame("gui/scrapbook/frame_paper.png", 9, 9)
        padding (18, 10)
        hbox:
            spacing 10
            add "gui/scrapbook/icon_qsave.png" yalign 0.5
            text "[message!tq]" yalign 0.5 size 24 color "#3b2a30" font "fonts/Silkscreen-Bold.ttf"
    add "gui/scrapbook/tape_h.png" xpos 1680 ypos 24
    timer 3.25 action Hide("notify")


## Overlays that should share the kit #########################################

screen choice_feedback_overlay():
    zorder 295
    $ _runtime = _lc_choice_toast_runtime
    if _runtime.payload:
        $ _choice_toast = _runtime.payload
        $ _choice_toast_serial = _choice_toast.get("serial", 0)
        $ _choice_toast_title = _choice_toast.get("title", "CHOICE")
        $ _choice_toast_body = _choice_toast.get("body", "")
        $ _noted = _choice_toast_title == "CHOICE IMPACT"
        $ _chips = lc_effect_chips(_choice_toast_body)

        frame at gameplay_toast_appear:
            xpos 1880
            xanchor 1.0
            ypos 36
            xmaximum 520
            background Frame("gui/scrapbook/frame_paper.png", 9, 9)
            padding (16, 10)

            vbox:
                spacing 6
                text ("NOTED" if _noted else _choice_toast_title) size 21 color "#7a6266" font "fonts/Silkscreen-Bold.ttf"
                if _chips and _choice_toast_title != "DEBUG CHOICE":
                    hbox:
                        spacing 6
                        box_wrap True
                        for chip_name, chip_amount, chip_exact in _chips:
                            use lc_chip(chip_name, chip_amount, chip_exact)
                else:
                    text _choice_toast_body size 30 color "#34242c" font "fonts/Caveat[wght].ttf"

        timer 3.20 action Function(clear_choice_feedback, _choice_toast_serial)


screen phone_notification_overlay():
    zorder 294
    if phone_notification_payload:
        $ _phone_toast = phone_notification_payload
        $ _phone_toast_serial = _phone_toast.get("serial", 0)
        frame at gameplay_toast_appear:
            xpos 36
            ypos 36
            xmaximum 520
            background Frame("gui/scrapbook/frame_paper.png", 9, 9)
            padding (16, 12)
            hbox:
                spacing 12
                add "gui/phone/icons/messages.png" xysize (42, 42) yalign 0.5
                vbox:
                    spacing 2
                    text _phone_toast.get("title", "Phone") size 24 color "#3b2a30" font "fonts/Silkscreen-Bold.ttf"
                    text _phone_toast.get("body", "") size 28 color "#7a6266" font "fonts/Caveat[wght].ttf"
        timer 3.60 action Function(clear_phone_notification, _phone_toast_serial)


screen phone_notification_banner():
    zorder 620
    if phone_notification_current:
        fixed:
            at phone_notification_slide
            xalign 0.5
            yalign 0.0
            xsize 700
            ysize 116
            frame:
                background Frame("gui/scrapbook/frame_paper.png", 9, 9)
                padding (18, 12)
                xfill True
                yfill True
                vbox:
                    spacing 2
                    text phone_notification_current["app"] size 18 color "#cc0066" font "fonts/Silkscreen-Bold.ttf"
                    text phone_notification_current["title"] size 28 color "#3b2a30" font "fonts/PatrickHand-Regular.ttf"
                    text phone_notification_current["body"] size 24 color "#7a6266" font "fonts/Caveat[wght].ttf"
        timer 3.75 action Function(phone_finish_notification)


screen status_choice_tutorial():
    modal True
    zorder 410
    add Solid("#0e0912aa")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 820
        background Frame("gui/scrapbook/frame_paper.png", 9, 9)
        padding (32, 26)
        vbox:
            spacing 12
            text "YOUR CHOICES CHANGE THE RELATIONSHIP" size 21 color "#cc0066" font "fonts/Silkscreen-Bold.ttf" xalign 0.5 text_align 0.5
            text "That choice changed one or more underlying stats." size 36 color "#3b2a30" font "fonts/PatrickHand-Regular.ttf" xalign 0.5 text_align 0.5
            text "Open your Phone and tap STATUS to see how [player_name], [girlfriend_name], and the relationship are developing. SETTINGS lets you choose how much of the hidden system the game reveals." size 28 color "#7a6266" font "fonts/Caveat[wght].ttf" xalign 0.5 text_align 0.5
            hbox:
                xalign 0.5
                spacing 16
                textbutton "OPEN PHONE":
                    action [Hide("status_choice_tutorial"), Show("phone_screen")]
                    background Frame("gui/scrapbook/frame_pink.png", 9, 9)
                    hover_background Frame("gui/scrapbook/frame_pink_hover.png", 9, 9)
                    text_idle_color "#fff3f7"
                    text_hover_color "#fff3f7"
                    padding (16, 8)
                textbutton "LATER":
                    action Hide("status_choice_tutorial")
                    background Frame("gui/scrapbook/frame_kraft.png", 9, 9)
                    padding (16, 8)


## Adult notice and demo end ##################################################

screen lc_adult_notice_screen():
    modal (not lc_ui_shooting)
    zorder 400
    add "gui/scrapbook/bg_table.png"

    add "gui/scrapbook/wax_seal.png" xalign 0.5 ypos 150

    frame:
        xalign 0.5
        yalign 0.52
        xsize 980
        ysize 520
        background Frame("gui/scrapbook/frame_paper.png", 9, 9)
        padding (48, 56)

        vbox:
            spacing 16
            xfill True
            text "MATURE CONTENT" xalign 0.5 size 48 color "#a83a5a" font "fonts/Silkscreen-Bold.ttf"
            text "ADULTS ONLY  -  18+" xalign 0.5 size 24 color "#8a4a5c" font "fonts/Silkscreen-Regular.ttf"
            text "This fictional visual novel is intended only for adults." xalign 0.5 text_align 0.5 size 36 color "#34242c" font "fonts/Caveat[wght].ttf"
            null height 12
            hbox:
                xalign 0.5
                spacing 24
                textbutton "I'M 18+  CONTINUE":
                    action [SetField(persistent, "lc_adult_notice_accepted", True), Function(renpy.save_persistent), Return(True)]
                    background Frame("gui/scrapbook/frame_pink.png", 9, 9)
                    hover_background Frame("gui/scrapbook/frame_pink_hover.png", 9, 9)
                    text_idle_color "#fff3f7"
                    text_hover_color "#fff3f7"
                    text_font "fonts/Silkscreen-Bold.ttf"
                    text_size 24
                    padding (20, 10)
                    at lc_lift
                textbutton "EXIT TO MENU":
                    action Return(False)
                    background Frame("gui/scrapbook/frame_kraft.png", 9, 9)
                    hover_background Frame("gui/scrapbook/frame_paper_hi.png", 9, 9)
                    text_idle_color "#7a6266"
                    text_hover_color "#3b2a30"
                    text_font "fonts/Silkscreen-Regular.ttf"
                    text_size 24
                    padding (20, 10)

    text "SHOWN ONCE  -  REMEMBERED ON THIS DEVICE" xalign 0.5 ypos 900 size 21 color "#9b8a80" font "fonts/Silkscreen-Regular.ttf"
    key "game_menu" action Return(False)


screen lc_demo_end_screen():
    modal True
    add "gui/scrapbook/bg_table.png"
    add Solid("#120c18cc")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 980
        yminimum 360
        background Frame("gui/scrapbook/frame_night.png", 9, 9)
        padding (40, 36)
        vbox:
            spacing 16
            text "THANK YOU FOR PLAYING" xalign 0.5 size 42 color "#d6c8e0" font "fonts/Silkscreen-Bold.ttf"
            text "This demo includes the Prologue and Chapter One, Day One." xalign 0.5 text_align 0.5 size 36 color "#efe4cd" font "fonts/PatrickHand-Regular.ttf"
            text "More of the story is in development." xalign 0.5 size 32 color "#cbb8d4" font "fonts/Caveat[wght].ttf"
            textbutton "RETURN" action Return() xalign 0.5


screen lc_shot_helper(name):
    zorder 2000
    timer 0.12 action Function(_lc_snap, name)


## Shot tour (LC_UI_SHOTS=1) ##################################################

label splashscreen:
    python:
        import os
        if os.environ.get("LC_UI_SHOTS") == "1":
            renpy.jump("lc_ui_shot_tour")
    return


label lc_ui_shot_tour:
    $ import os
    $ _shot_dir = os.environ.get("LC_UI_SHOT_DIR", "/tmp/lc_ui_shots")
    $ os.makedirs(_shot_dir, exist_ok=True)
    $ lc_ui_shooting = True
    $ lc_ui_shots = []

    python:
        def _lc_mark(msg):
            with open("/tmp/shot_trace.txt", "a") as handle:
                handle.write(msg + "\n")

        def _lc_snap(name):
            path = os.path.join(store._shot_dir, name + ".png")
            renpy.screenshot(path)
            store.lc_ui_shots.append(path)
            for scr in (
                "lc_shot_helper",
                "lc_adult_notice_screen",
                "confirm",
                "gallery_screen",
                "status_screen",
            ):
                if renpy.get_screen(scr) is not None:
                    renpy.hide_screen(scr)
            _lc_mark("saved " + name + " qm=" + str(renpy.get_screen("quick_menu") is not None))

        def _lc_shot(name):
            _lc_mark("pause " + name)
            renpy.show_screen("lc_shot_helper", name)
            renpy.pause(0.3, hard=True)

    scene bg ch01_pool_day
    $ _lc_mark("qm screen " + str(renpy.get_screen("quick_menu")) + " flag " + str(quick_menu))
    show screen say(who="Leia", what="\"Morning. You're not getting up yet, are you?\"")
    $ _lc_shot("02_dialogue_day")
    hide screen say

    scene bg ch01_restaurant_bar
    show screen say(who="Leia", what="\"Can we just enjoy tonight? No big talks.\"")
    $ _lc_shot("02_dialogue_night")
    hide screen say

    $ enter_cinematic_mode()
    scene cg ch01_drive_to_dinner
    show screen say(who="Leia", what="\"You know the speed limit applies on holiday too, right?\"")
    $ _lc_shot("09_dialogue_cg_day")
    hide screen say
    scene cg ch01_dinner_arrival
    show screen say(who=None, what="Dinner started exactly the way I expected.")
    $ _lc_shot("09_dialogue_cg_night")
    hide screen say
    $ exit_cinematic_mode()

    scene bg ch01_restaurant_bar
    python:
        class _ShotItem(object):
            def __init__(self, caption):
                self.caption = caption
                self.action = Return(True)
        store._shot_items = [
            _ShotItem("You're right. Let's just enjoy tonight.\n[Love ↑ • Boredom ↓]"),
            _ShotItem("Can we talk somewhere quieter?\n[Love ↑ • Trust ↑ • Secrecy ↓]"),
            _ShotItem("You can enjoy yourself. I'll get a drink.\n[Trust ↓ • Acceptance ↑]"),
        ]
    show screen choice(_shot_items)
    show screen say(who="Leia", what="\"Can we just enjoy tonight?\"")
    $ _lc_shot("03_choice")
    hide screen choice
    hide screen say

    $ main_menu = True
    $ renpy.show_screen("main_menu")
    $ _lc_shot("01_main_menu")
    hide screen main_menu
    $ main_menu = False

    $ renpy.show_screen("save")
    $ _lc_shot("04_save")
    hide screen save

    $ renpy.show_screen("preferences")
    $ _lc_shot("05_preferences")
    hide screen preferences

    $ renpy.show_screen("history")
    $ _lc_shot("06_history")
    hide screen history

    $ _lc_mark("before adult")
    $ renpy.show_screen("lc_adult_notice_screen")
    $ _lc_mark("shown adult")
    $ _lc_shot("07_adult_notice")
    hide screen lc_adult_notice_screen

    $ renpy.show_screen("confirm", message="Return to the main menu?\nUnsaved progress will be lost.", yes_action=Hide("confirm"), no_action=Hide("confirm"))
    $ _lc_shot("08_confirm")
    hide screen confirm

    $ renpy.show_screen("gallery_screen")
    $ _lc_shot("10_gallery")
    hide screen gallery_screen

    $ renpy.show_screen("status_screen")
    $ _lc_shot("11_status")
    hide screen status_screen

    $ renpy.show_screen("help")
    $ _lc_shot("12_help")
    hide screen help

    $ renpy.show_screen("chapter_select")
    $ _lc_shot("13_chapters")
    hide screen chapter_select

    "Shots written."
    $ renpy.quit()
    return


## Styles #####################################################################

style button:
    background Frame("gui/scrapbook/frame_keycap.png", 9, 9)
    hover_background Frame("gui/scrapbook/frame_keycap_on.png", 9, 9)
    selected_idle_background Frame("gui/scrapbook/frame_keycap_on.png", 9, 9)
    selected_hover_background Frame("gui/scrapbook/frame_keycap_on.png", 9, 9)
    insensitive_background Frame("gui/scrapbook/frame_pink_off.png", 9, 9)
    padding (16, 8)
    yminimum 42

style button_text:
    font "fonts/Silkscreen-Regular.ttf"
    size 24
    idle_color "#cdb9a8"
    hover_color "#fff3f7"
    selected_color "#fff3f7"
    selected_idle_color "#fff3f7"
    selected_hover_color "#fff3f7"
    insensitive_color "#b5a5ab"
    xalign 0.5
    textalign 0.5

style lc_tab_text is button_text:
    idle_color "#3b2a30"
    hover_color "#fff3f7"
    selected_color "#fff3f7"
    selected_idle_color "#fff3f7"
    selected_hover_color "#fff3f7"
    size 22
    xalign 0.0
    textalign 0.0

style lc_tab_text_on is lc_tab_text:
    idle_color "#fff3f7"
    hover_color "#fff3f7"
    selected_color "#fff3f7"

style lc_key_text is button_text:
    idle_color "#cdb9a8"
    hover_color "#fff3f7"
    selected_color "#fff3f7"
    selected_idle_color "#fff3f7"
    size 21
    xalign 0.5

style lc_radio_button is button:
    background None
    hover_background Frame("gui/scrapbook/ink_loop.png", 54, 12, 54, 12)
    selected_idle_background Frame("gui/scrapbook/ink_loop.png", 54, 12, 54, 12)
    selected_hover_background Frame("gui/scrapbook/ink_loop.png", 54, 12, 54, 12)
    padding (16, 2)
    yminimum 36

style lc_radio_text is button_text:
    idle_color "#7a6266"
    hover_color "#3b2a30"
    selected_color "#3b2a30"
    selected_idle_color "#3b2a30"
    selected_hover_color "#a83a5a"
    xalign 0.5
    size 21

style lc_check_button is button:
    background None
    hover_background None
    selected_idle_background None
    selected_hover_background None
    insensitive_background None
    foreground "gui/scrapbook/check_off.png"
    hover_foreground "gui/scrapbook/check_off.png"
    selected_idle_foreground "gui/scrapbook/check_on.png"
    selected_hover_foreground "gui/scrapbook/check_on.png"
    padding (40, 2, 8, 2)
    yminimum 36

style lc_check_text is button_text:
    idle_color "#7a6266"
    hover_color "#cc0066"
    selected_color "#3b2a30"
    selected_idle_color "#3b2a30"
    selected_hover_color "#cc0066"
    xalign 0.0
    size 21

style label_text:
    color "#3b2a30"
    font "fonts/Silkscreen-Bold.ttf"

style gui_text:
    color "#3b2a30"
    font "fonts/Silkscreen-Regular.ttf"

style window:
    xalign None
    yalign None
    xanchor 0.0
    yanchor 0.0
    background None
    padding (0, 0, 0, 0)

style namebox:
    background None
    padding (12, 4, 12, 4)
    xalign None
    yalign None
    xanchor 0.0
    yanchor 0.0
    xsize None

style say_dialogue:
    color "#34242c"
    font "fonts/PatrickHand-Regular.ttf"
    size 42
    xpos 0
    ypos 0
    xalign None
    yalign None
    xanchor 0.0
    yanchor 0.0
    text_align 0.0
    textalign 0.0
    ymaximum None
    xmaximum 1520
    layout "tex"

style say_label:
    font "fonts/Silkscreen-Bold.ttf"
    size 24
    color "#6a2338"
    xalign 0.0
    yalign 0.5
    textalign 0.0

style vscrollbar:
    base_bar Frame("gui/scrapbook/vscroll_bar.png", 6, 6)
    thumb Frame("gui/scrapbook/vscroll_thumb.png", 6, 6)
    xsize 18
    unscrollable "hide"

style frame:
    background Frame("gui/scrapbook/frame_paper.png", 9, 9)
    padding (18, 14)

style nvl_window:
    background Frame("gui/scrapbook/frame_paper.png", 9, 9)

style nvl_dialogue:
    color "#34242c"
    font "fonts/PatrickHand-Regular.ttf"
