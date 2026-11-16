# Phone Home presentation patch.
# Replaces the temporary Status/Settings dock with two standalone app tiles.
# Final icon art can replace the placeholder rounded tiles later without changing
# any Status/Settings logic.
#
# Final art swap points:
# - Status placeholder tile -> gui/phone/icons/status.png
# - Settings placeholder tile -> gui/phone/icons/settings.png

init 95 python:

    def lc_phone_hovered_app():
        phone = renpy.get_screen("phone_screen")
        if phone is None:
            return None
        scope = getattr(phone, "scope", None)
        if isinstance(scope, dict):
            return scope.get("hovered_app")
        return None

