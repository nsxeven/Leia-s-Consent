# Full Transparency path stamps on choice cards (darryn 2026-11-08, stat model v2).
#
# In Full Transparency only, each choice card gets a small ink stamp after its
# stat line naming the path the choice leads (or may lead) to:
#   -> LOVE, -> LOVE+EXHIB, -> NTS, -> NTR, MAY LEAD TO NTR, LOCKS NTR,
#   NTR STAYS OPEN, REPAIR, REPAIR, NTR STAYS OPEN. Neutral choices get no stamp.
# The tag is lc_choice_route_tag(choice_id) -> lc_stat_model.choice_route_tag, the
# same function Developer mode, the route simulation and the tests use, so the
# stamp can never disagree with the stats. Colours are the stat-delta meanings
# (LC_REVIEW_DELTA_INK, the darker inks that read on paper): green = Love family
# and Repair, red = toward NTR, pink = Love+Exhib, purple = NTS.
#
# How the card knows the choice id: in Full mode format_choice() (and the gate
# formatters below) put an invisible Ren'Py comment tag {#lcpath=<id>} in the
# caption. Captions without one (literal test captions) fall back to the stat
# line, scored by the same lc_stat_model.route_tag().

define LC_PATH_STAMP_ARROW = "{font=DejaVuSans.ttf}\u2192{/font}"
define LC_PATH_STAMP_PAPER = "#fbf4e6"

transform lc_path_stamp_tilt:
    rotate -2
    rotate_pad False
    transform_anchor True

init 6 python:
    import lc_stat_model
    import lc_ui_logic

    def lc_choice_path_stamp(caption):
        """(label markup, ink) for a choice card's Full Transparency stamp, or None.

        None outside Full mode and for Neutral choices, so no other mode changes.
        """
        if current_choice_mode() != "full":
            return None
        choice_id, text = lc_ui_logic.split_choice_mark(lc_choice_caption(caption))
        tag = None
        if choice_id:
            if choice_id in CHOICE_EFFECTS:
                tag = lc_choice_route_tag(choice_id)
        else:
            _line, chips = lc_ui_logic.parse_choice_caption(text)
            effects = lc_stat_model.effects_from_chips(chips) if chips else None
            if effects:
                tag = lc_stat_model.route_tag(effects)
        stamp = lc_stat_model.path_stamp(tag)
        if not stamp:
            return None
        label, kind = stamp
        label = label.upper().replace("->", LC_PATH_STAMP_ARROW)
        return label, LC_REVIEW_DELTA_INK[kind]

    def _lc_path_gate_formatter(original):
        """Wrap a Day 2/4/5 gate formatter (their files are Scriptwriter-owned or story).

        - A gate option that does not lean toward NTR (the Repair / reconnect answer)
          is formatted like any other choice: no red warning diamond, so it no
          longer looks the same as the NTR options in its menu.
        - The diamond is drawn in DejaVuSans: Patrick Hand has no glyph for it.
        - Full mode gets the {#lcpath=<id>} marker for the path stamp.
        Developer mode is unchanged.
        """
        def formatter(choice_id, base_text, *args, **kwargs):
            mode = current_choice_mode()
            if mode in ("insight", "full") and lc_choice_route_tag(choice_id) not in lc_stat_model.NTR_TAGS:
                return format_choice(choice_id, base_text)
            text = original(choice_id, base_text, *args, **kwargs)
            if mode in ("insight", "full"):
                text = text.replace("\u25c6", "{font=DejaVuSans.ttf}\u25c6{/font}")
            if mode == "full":
                text = lc_ui_logic.choice_mark(choice_id) + text
            return text
        formatter.lc_wrapped = original
        return formatter

    for _lc_name in ("format_day2_risk_choice", "format_day4_gate_choice", "format_day5_gate_choice"):
        if _lc_name in globals() and not hasattr(globals()[_lc_name], "lc_wrapped"):
            globals()[_lc_name] = _lc_path_gate_formatter(globals()[_lc_name])
