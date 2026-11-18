"""Source text of the split screen files, by family.

The Sweetheart phone and the scrapbook skin were split into one file per app / part (modular
backend finishing pass). Tests that check source text across a family read it here, so the next
split only edits this table.
"""
from pathlib import Path

SCREENS = Path(__file__).resolve().parents[1] / "game" / "screens"

FAMILIES = {
    # the handset first (phone_screen, styles, helpers), then one file per app
    "phone": ("phone_sweetheart.rpy", "phone_app_status.rpy", "phone_app_settings.rpy", "phone_app_photos.rpy"),
    # the stock-screen skin first, then the parts split out of it
    "scrapbook": ("scrapbook_ui.rpy", "quick_menu.rpy", "demo_end_card.rpy"),
}


def family_source(name):
    """Every file of a family, joined in the order above (main file first)."""
    return "\n".join((SCREENS / f).read_text(encoding="utf-8") for f in FAMILIES[name])
