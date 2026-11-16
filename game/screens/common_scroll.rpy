# Common scroll body - one scrolling convention for custom screens
#
# Purpose: Any screen body that can grow with content uses this wrapper so the mouse wheel, drag,
#   Page Up/Down and a vertical scrollbar behave the same everywhere.
#
# Public API (call these from scenes/screens):
#   screen lc_scroll_body()                   viewport with scrollbar; put the content in its `use`
#       block
#
# Example:
#   use lc_scroll_body:
#       vbox:
#           ...
#
# Depends on: nothing
# Hooks: none
# Load order: default (screens at init -500)
# Docs: docs/ARCHITECTURE.md   Tests: none directly (lint)

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
