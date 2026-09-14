# Live choice-mode refresh patch.
#
# Ren'Py evaluates menu captions before the choice screen is shown. If the
# player changes information visibility while that menu is still active, those
# already-built strings would otherwise stay stale until the menu statement is
# executed again. Keep a stable choice token in the menu caption and render the
# visible annotation at screen draw time instead.

init 110 python:

    LC_CHOICE_TOKEN_PREFIX = "<<LCCHOICE:"
    LC_CHOICE_TOKEN_SEPARATOR = ">>"


    def _lc_choice_token(choice_id, base_text):
        return "{}{}{}{}".format(
            LC_CHOICE_TOKEN_PREFIX,
            choice_id,
            LC_CHOICE_TOKEN_SEPARATOR,
            base_text,
        )


    def _lc_decode_choice_token(caption):
        if not isinstance(caption, str):
            return None
        if not caption.startswith(LC_CHOICE_TOKEN_PREFIX):
            return None

        payload = caption[len(LC_CHOICE_TOKEN_PREFIX):]
        if LC_CHOICE_TOKEN_SEPARATOR not in payload:
            return None

        choice_id, base_text = payload.split(LC_CHOICE_TOKEN_SEPARATOR, 1)
        if not choice_id:
            return None
        return choice_id, base_text


    def lc_render_choice_caption(caption, mode=None):
        """Render a tokenized menu caption using the *current* visibility mode."""
        decoded = _lc_decode_choice_token(caption)
        if decoded is None:
            # Compatibility for menus that do not use the central choice engine.
            return caption

        choice_id, base_text = decoded
        mode = mode or current_choice_mode()

        if mode == "normal":
            return base_text

        if mode == "insight":
            return "{}\n[{}]".format(
                base_text,
                _choice_effect_text(choice_id, exact=False),
            )

        if mode == "full":
            return "{}\n[{}]".format(
                base_text,
                _choice_effect_text(choice_id, exact=True),
            )

        tags = get_choice_tags(choice_id)
        tag_text = " • Tags: {}".format(", ".join(tags)) if tags else ""
        return "{}\n[{}]  [ID: {}]{}".format(
            base_text,
            _choice_effect_text(choice_id, exact=True),
            choice_id,
            tag_text,
        )


    def format_choice(choice_id, base_text):
        """Store stable menu metadata; the choice screen handles live rendering."""
        # Validate early so story typos still fail where the choice is created.
        get_choice_effects(choice_id)
        return _lc_choice_token(choice_id, base_text)


    def choice_preview_text():
        """Player-settings preview rendered directly rather than exposing a token."""
        base_text = "Encourage {}'s curiosity".format(renpy.store.girlfriend_name)
        return lc_render_choice_caption(
            _lc_choice_token("dev_encourage_curiosity", base_text)
        )


# Override the stock choice screen so captions are resolved on every redraw.
# set_choice_display_mode() already calls renpy.restart_interaction(), so an
# active menu changes immediately when the Phone Settings mode changes.
screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            $ lc_visible_caption = lc_render_choice_caption(i.caption)
            textbutton lc_visible_caption action i.action:
                text_xalign 0.5
                text_align 0.5
