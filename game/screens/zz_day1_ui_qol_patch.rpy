# Day One UI/QOL patch.
# - Choice feedback is transient and does not resurrect after rollback.
# - Long/multiline menu choices are visually centered.
# - Status + Settings are accessible as Phone-native surfaces.
# - The first real stat-changing story choice teaches the player where Status lives.

style choice_button_text:
    text_align 0.5
    xalign 0.5
    line_spacing 4


init 90 python:

    class LCChoiceToastRuntime(renpy.python.NoRollback):
        def __init__(self):
            self.payload = None
            self.serial = 0


    # Underscore-prefixed runtime object is deliberately transient UI state.
    # Its contents should not be restored by rollback or treated as story state.
    if not hasattr(renpy.store, "_lc_choice_toast_runtime"):
        renpy.store._lc_choice_toast_runtime = LCChoiceToastRuntime()


    def clear_choice_feedback(serial):
        runtime = renpy.store._lc_choice_toast_runtime
        payload = runtime.payload
        if payload and payload.get("serial") == serial:
            runtime.payload = None
        return None


    def show_choice_feedback(choice_id):
        """Show mode-safe post-choice feedback as transient, non-rollback UI."""
        effects = get_choice_effects(choice_id)
        if not effects:
            return None

        mode = current_choice_mode()

        if mode == "normal":
            title = "CHOICE"
            body = "Your response has been remembered."
        elif mode == "insight":
            title = "CHOICE IMPACT"
            body = _choice_effect_text(choice_id, exact=False)
        elif mode == "full":
            title = "STAT CHANGES"
            body = _choice_effect_text(choice_id, exact=True)
        else:
            title = "DEBUG CHOICE"
            tags = get_choice_tags(choice_id)
            tag_text = ", ".join(tags) if tags else "none"
            body = "{}\nID: {}\nTags: {}".format(
                _choice_effect_text(choice_id, exact=True),
                choice_id,
                tag_text,
            )

        runtime = renpy.store._lc_choice_toast_runtime
        runtime.serial += 1
        runtime.payload = {
            "serial": runtime.serial,
            "title": title,
            "body": body,
        }
        return None


    def maybe_show_status_choice_tutorial(choice_id):
        """One-time player onboarding after the first real stat-changing story choice."""
        if choice_id.startswith("dev_"):
            return None
        if not getattr(renpy.store, "phone_unlocked", False):
            return None
        if getattr(renpy.store.persistent, "status_choice_tutorial_seen", False):
            return None
        if not any(amount != 0 for _group, _stat, amount in get_choice_effects(choice_id)):
            return None

        # Persistent UI onboarding intentionally survives rollback/new saves.
        renpy.store.persistent.status_choice_tutorial_seen = True
        renpy.save_persistent()
        renpy.show_screen("status_choice_tutorial")
        return None


    def apply_choice(choice_id):
        """Apply effects, record the choice, show transient feedback and onboarding."""
        for group_name, stat_name, amount in get_choice_effects(choice_id):
            change_stat(group_name, stat_name, amount)

        renpy.store.last_choice_id = choice_id
        renpy.store.choice_history.append(choice_id)
        show_choice_feedback(choice_id)
        maybe_show_status_choice_tutorial(choice_id)
        return choice_id


    def lc_phone_current_app():
        """Read the active Phone app safely so extra app buttons only appear on Home."""
        phone = renpy.get_screen("phone_screen")
        if phone is None:
            return None
        scope = getattr(phone, "scope", None)
        if isinstance(scope, dict):
            return scope.get("phone_app", "home")
        return "home"


    def lc_phone_set_information_mode(mode):
        if mode in ("normal", "insight", "full"):
            return set_player_transparency_mode(mode)
        if mode == "developer":
            set_choice_display_mode("developer")
            return mode
        raise ValueError("Unknown information mode: {}".format(mode))


    def lc_mark_status_intro_seen():
        renpy.store.persistent.status_page_intro_seen = True
        renpy.save_persistent()
        renpy.restart_interaction()
        return None


    if "lc_phone_extra_apps" not in config.overlay_screens:
        config.overlay_screens.append("lc_phone_extra_apps")


screen choice_feedback_overlay():
    zorder 295

    $ _runtime = _lc_choice_toast_runtime
    if _runtime.payload:
        $ _choice_toast = _runtime.payload
        $ _choice_toast_serial = _choice_toast.get("serial", 0)
        $ _choice_toast_title = _choice_toast.get("title", "CHOICE")
        $ _choice_toast_body = _choice_toast.get("body", "")

        frame at gameplay_toast_appear:
            xalign 0.985
            yalign 0.045
            xmaximum 560
            background Frame("gui/phone/rounded_white.png", 24, 24)
            padding (20, 16)

            vbox:
                spacing 5
                text "[_choice_toast_title]" size 13 color "#8e8e93" bold True
                text "[_choice_toast_body]" size 17 color "#1c1c1e" line_spacing 3

        timer 3.20 action Function(clear_choice_feedback, _choice_toast_serial)


screen status_choice_tutorial():
    modal True
    zorder 410

    add Solid("#00000077")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 760
        background Frame("gui/phone/rounded_white.png", 28, 28)
        padding (32, 28)

        vbox:
            spacing 15
            xfill True

            text "YOUR CHOICES CHANGE THE RELATIONSHIP" size 19 color "#007aff" bold True xalign 0.5 text_align 0.5
            text "That choice changed one or more underlying stats." size 25 color "#1c1c1e" bold True xalign 0.5 text_align 0.5
            text "Open your Phone and tap STATUS to see how Ryan, Leia, and the relationship are developing. SETTINGS lets you choose how much of the hidden system the game reveals." size 18 color "#5f5f64" xalign 0.5 text_align 0.5 line_spacing 5

            null height 4

            hbox:
                xalign 0.5
                spacing 14

                textbutton "Open Phone":
                    xsize 220
                    ysize 54
                    background Frame("gui/phone/rounded_button_blue.png", 24, 24)
                    hover_background Frame("gui/phone/rounded_button_blue_hover.png", 24, 24)
                    text_idle_color "#ffffff"
                    text_hover_color "#ffffff"
                    text_xalign 0.5
                    text_yalign 0.5
                    action [Hide("status_choice_tutorial"), Show("phone_screen")]

                textbutton "Later":
                    xsize 150
                    ysize 54
                    background Frame("gui/phone/rounded_light.png", 24, 24)
                    hover_background Frame("gui/phone/rounded_blue.png", 24, 24)
                    text_idle_color "#3a3a3c"
                    text_hover_color "#007aff"
                    text_xalign 0.5
                    text_yalign 0.5
                    action Hide("status_choice_tutorial")


# Two extra Phone apps live in a small Home-screen dock so the main Phone file
# does not duplicate the existing Messages/Photos/Shop/Wallet/Delivery logic.
screen lc_phone_extra_apps():
    zorder 325

    if renpy.get_screen("phone_screen") and not renpy.get_screen("lc_phone_status") and not renpy.get_screen("lc_phone_settings"):
        if lc_phone_current_app() == "home":
            frame:
                xalign 0.5
                yalign 0.875
                xsize 350
                ysize 76
                background Frame("gui/phone/rounded_white.png", 24, 24)
                padding (8, 8)

                hbox:
                    spacing 8
                    xfill True
                    yfill True

                    textbutton ("STATUS  •  NEW" if not getattr(persistent, "status_page_intro_seen", False) else "STATUS"):
                        xsize 165
                        yfill True
                        background Frame("gui/phone/rounded_blue.png", 22, 22)
                        hover_background Frame("gui/phone/rounded_button_blue_hover.png", 22, 22)
                        text_idle_color "#1c1c1e"
                        text_hover_color "#ffffff"
                        text_size 15
                        text_xalign 0.5
                        text_yalign 0.5
                        action Show("lc_phone_status")

                    textbutton "SETTINGS":
                        xsize 160
                        yfill True
                        background Frame("gui/phone/rounded_light.png", 22, 22)
                        hover_background Frame("gui/phone/rounded_blue.png", 22, 22)
                        text_idle_color "#1c1c1e"
                        text_hover_color "#007aff"
                        text_size 15
                        text_xalign 0.5
                        text_yalign 0.5
                        action Show("lc_phone_settings")


screen lc_phone_status_row(row):
    vbox:
        spacing 4
        xfill True

        hbox:
            xfill True
            text row["label"] size 15 color "#1c1c1e"
            if row["detail"]:
                text row["detail"] size 13 color "#6d6d72" xalign 1.0

        bar:
            value StaticValue(row["value"], 100)
            xfill True
            ysize 11
            left_bar Solid("#cc5d91")
            right_bar Solid("#e5e5ea")

        if row["internal_key"]:
            text row["internal_key"] size 10 color "#8e8e93"


screen lc_phone_status_section(title, rows):
    frame:
        xfill True
        background Frame("gui/phone/rounded_white.png", 24, 24)
        padding (16, 14)

        vbox:
            spacing 11
            xfill True
            text title size 17 color "#1c1c1e" bold True
            for row in rows:
                use lc_phone_status_row(row)


screen lc_phone_status():
    modal True
    zorder 340

    key "K_ESCAPE" action Hide("lc_phone_status")

    $ _mode = current_choice_mode()
    $ _relationship_rows = status_relationship_rows(_mode)
    $ _leia_rows = status_leia_rows(_mode)
    $ _ryan_rows = status_ryan_rows(_mode)
    $ _route_rows = status_route_rows(_mode)

    add Solid("#00000066")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 660
        ysize 1010
        background Frame("gui/phone/rounded_shell.png", 30, 30)
        padding (14, 14)

        frame:
            xfill True
            yfill True
            background Frame("gui/phone/rounded_screen.png", 28, 28)
            padding (22, 20)

            vbox:
                spacing 12
                xfill True
                yfill True

                hbox:
                    xfill True
                    vbox:
                        spacing 2
                        text "STATUS" size 29 color "#1c1c1e" bold True
                        text "Display: [transparency_mode_label()]" size 13 color "#8e8e93"
                    vbox:
                        xalign 1.0
                        spacing 4
                        textbutton "‹ Phone":
                            background None
                            hover_background None
                            text_idle_color "#007aff"
                            text_hover_color "#5ac8fa"
                            action Hide("lc_phone_status")
                        textbutton "Settings":
                            xalign 1.0
                            background None
                            hover_background None
                            text_idle_color "#007aff"
                            text_hover_color "#5ac8fa"
                            action [Hide("lc_phone_status"), Show("lc_phone_settings")]

                viewport:
                    xfill True
                    yfill True
                    mousewheel True
                    draggable True

                    vbox:
                        spacing 12
                        xfill True

                        if not getattr(persistent, "status_page_intro_seen", False):
                            frame:
                                xfill True
                                background Frame("gui/phone/rounded_blue.png", 24, 24)
                                padding (16, 14)

                                vbox:
                                    spacing 8
                                    text "THIS IS YOUR LIVE DASHBOARD" size 14 color "#007aff" bold True
                                    text "Status tracks the relationship, Leia's developing traits, and Ryan's mindset. What you can see depends on your information setting." size 14 color "#2c2c2e" line_spacing 3
                                    textbutton "Got it":
                                        xfill True
                                        ysize 42
                                        background Frame("gui/phone/rounded_button_blue.png", 22, 22)
                                        hover_background Frame("gui/phone/rounded_button_blue_hover.png", 22, 22)
                                        text_idle_color "#ffffff"
                                        text_hover_color "#ffffff"
                                        text_xalign 0.5
                                        text_yalign 0.5
                                        action Function(lc_mark_status_intro_seen)

                        frame:
                            xfill True
                            background Frame("gui/phone/rounded_light.png", 24, 24)
                            padding (15, 13)
                            vbox:
                                spacing 6
                                text "[girlfriend_name] right now" size 17 color "#1c1c1e" bold True
                                text "[leia_overview_text()]" size 13 color "#5f5f64" line_spacing 3

                        use lc_phone_status_section("RELATIONSHIP", _relationship_rows)
                        use lc_phone_status_section(girlfriend_name.upper(), _leia_rows)
                        use lc_phone_status_section(player_name.upper(), _ryan_rows)

                        if _route_rows:
                            use lc_phone_status_section("ROUTE TENDENCIES", _route_rows)

                        text "[status_mode_note()]" size 12 color "#8e8e93" text_align 0.5 xalign 0.5
                        null height 12


screen lc_phone_settings_mode(mode_id):
    $ _selected = current_choice_mode() == mode_id
    $ _info = transparency_mode_info(mode_id)

    button:
        xfill True
        padding (15, 13)
        background (Frame("gui/phone/rounded_blue.png", 24, 24) if _selected else Frame("gui/phone/rounded_white.png", 24, 24))
        hover_background Frame("gui/phone/rounded_blue.png", 24, 24)
        action Function(lc_phone_set_information_mode, mode_id)

        vbox:
            spacing 4
            xfill True
            hbox:
                xfill True
                text _info["label"] size 17 color "#1c1c1e" bold True
                if _selected:
                    text "SELECTED" size 11 color "#007aff" bold True xalign 1.0
            text _info["tagline"] size 13 color "#5f5f64"
            text _info["description"] size 12 color "#8e8e93" line_spacing 2


screen lc_phone_settings():
    modal True
    zorder 340

    key "K_ESCAPE" action Hide("lc_phone_settings")

    add Solid("#00000066")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 660
        ysize 1010
        background Frame("gui/phone/rounded_shell.png", 30, 30)
        padding (14, 14)

        frame:
            xfill True
            yfill True
            background Frame("gui/phone/rounded_screen.png", 28, 28)
            padding (22, 20)

            vbox:
                spacing 12
                xfill True
                yfill True

                hbox:
                    xfill True
                    vbox:
                        spacing 2
                        text "SETTINGS" size 29 color "#1c1c1e" bold True
                        text "Information Visibility" size 13 color "#8e8e93"
                    vbox:
                        xalign 1.0
                        spacing 4
                        textbutton "‹ Phone":
                            background None
                            hover_background None
                            text_idle_color "#007aff"
                            text_hover_color "#5ac8fa"
                            action Hide("lc_phone_settings")
                        textbutton "Status":
                            xalign 1.0
                            background None
                            hover_background None
                            text_idle_color "#007aff"
                            text_hover_color "#5ac8fa"
                            action [Hide("lc_phone_settings"), Show("lc_phone_status")]

                frame:
                    xfill True
                    background Frame("gui/phone/rounded_light.png", 24, 24)
                    padding (14, 12)
                    text "These modes only change what the UI tells you. They never alter story outcomes, stats, or difficulty." size 13 color "#5f5f64" text_align 0.5 xalign 0.5 line_spacing 3

                viewport:
                    xfill True
                    yfill True
                    mousewheel True
                    draggable True

                    vbox:
                        spacing 10
                        xfill True

                        use lc_phone_settings_mode("normal")
                        use lc_phone_settings_mode("insight")
                        use lc_phone_settings_mode("full")
                        use lc_phone_settings_mode("developer")

                        if current_choice_mode() == "developer":
                            frame:
                                xfill True
                                background Frame("gui/phone/rounded_yellow.png", 22, 22)
                                padding (14, 12)
                                text "Developer exposes internal IDs, stat keys, route tendencies, and debug information. It is intended for testing rather than a first blind playthrough." size 12 color "#4a3a16" line_spacing 3

                        null height 12
