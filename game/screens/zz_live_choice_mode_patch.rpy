# Live choice-mode refresh patch.
#
# Ren'Py builds menu captions before the choice screen is shown. To let the
# player change information visibility from the Phone while a menu is already
# open, format_choice() stores a stable token and the choice screen resolves it
# again on every interaction redraw.
#
# IMPORTANT: keep this screen geometrically identical to the stock project
# choice screen. Only the caption is dynamic; layout remains choice_vbox /
# choice_button / choice_button_text.

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


    def _lc_caption_to_text(caption):
        """Normalize Ren'Py caption/string wrappers into ordinary text."""
        if caption is None:
            return ""

        if isinstance(caption, str):
            return caption

        # Ren'Py may wrap translatable/menu text. Try common underlying fields
        # before falling back to its textual representation.
        for attr in ("text", "value", "string"):
            value = getattr(caption, attr, None)
            if isinstance(value, str):
                return value

        try:
            return str(caption)
        except Exception:
            return ""


    def _lc_decode_choice_token(caption):
        caption_text = _lc_caption_to_text(caption)
        if not caption_text:
            return None

        # Be deliberately tolerant of Ren'Py translation wrappers adding text
        # around the original caption. The token itself is unique to our choice
        # engine, so finding it anywhere is safe.
        token_start = caption_text.find(LC_CHOICE_TOKEN_PREFIX)
        if token_start < 0:
            return None

        payload = caption_text[token_start + len(LC_CHOICE_TOKEN_PREFIX):]
        if LC_CHOICE_TOKEN_SEPARATOR not in payload:
            return None

        choice_id, base_text = payload.split(LC_CHOICE_TOKEN_SEPARATOR, 1)
        if not choice_id:
            return None

        return choice_id.strip(), base_text


    def lc_render_choice_caption(caption, mode=None):
        """Render a tokenized menu caption using the CURRENT visibility mode."""
        decoded = _lc_decode_choice_token(caption)
        if decoded is None:
            # Menus outside the central choice engine continue to work normally.
            return _lc_caption_to_text(caption)

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
        """Store stable menu metadata; visible formatting happens at draw time."""
        get_choice_effects(choice_id)
        return _lc_choice_token(choice_id, base_text)


    def choice_preview_text():
        """Settings preview uses the same renderer without leaking the token."""
        base_text = "Encourage {}'s curiosity".format(renpy.store.girlfriend_name)
        return lc_render_choice_caption(
            _lc_choice_token("dev_encourage_curiosity", base_text)
        )


# This intentionally mirrors the project's original screen choice(items).
# set_choice_display_mode() calls renpy.restart_interaction(), which causes the
# current menu to redraw and lc_render_choice_caption() to read the new mode.
screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            $ lc_visible_caption = lc_render_choice_caption(i.caption)
            textbutton lc_visible_caption action i.action
