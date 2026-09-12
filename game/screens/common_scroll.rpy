# Shared scrolling convention for custom Leia's Consent screens.
# Any screen body that can grow with content should use this wrapper so
# mouse wheel, drag, Page Up/Down, and a vertical scrollbar work consistently.

screen lc_scroll_body():

    viewport:
        xfill True
        yfill True
        mousewheel True
        draggable True
        pagekeys True
        scrollbars "vertical"
        side_yfill True

        transclude
