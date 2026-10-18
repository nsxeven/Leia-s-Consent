# Menu-safe transparency/settings actions.
#
# Ren'Py Function(...) actions can resolve the current interaction if the
# called helper returns a non-None value. If Settings is opened while a story
# `menu:` is active, returning "full" / "developer" / etc. is interpreted by
# the menu AST as the selected choice index, causing:
#   TypeError: list indices must be integers or slices, not str
#
# All player-facing mode setters therefore deliberately return None.

init 200 python:

    def set_player_transparency_mode(mode):
        """Set player-facing information visibility without resolving a story menu."""
        if mode not in PLAYER_TRANSPARENCY_MODES:
            raise ValueError("Unknown player transparency mode: {}".format(mode))

        first_full_selection = (
            mode == "full"
            and not getattr(renpy.store.persistent, "full_transparency_notice_seen", False)
        )

        if first_full_selection:
            renpy.store.persistent.full_transparency_notice_seen = True

        set_choice_display_mode(mode)

        if first_full_selection:
            renpy.notify("Full Transparency may reveal relationship trends before the story makes them obvious.")

        # CRITICAL: Function(...) actions over an active Ren'Py menu must not
        # return a mode string or any other non-None interaction result.
        return None


    def lc_phone_set_information_mode(mode):
        """Phone Settings wrapper that is safe to use while choices are visible."""
        if mode in ("normal", "insight", "full"):
            set_player_transparency_mode(mode)
            return None

        if mode == "developer":
            set_choice_display_mode("developer")
            return None

        raise ValueError("Unknown information mode: {}".format(mode))
