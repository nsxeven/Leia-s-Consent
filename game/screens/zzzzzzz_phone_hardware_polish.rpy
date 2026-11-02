# The Sweetheart handset draws its own bezel inside phone_screen, lc_phone_status
# and lc_phone_settings. This overlay used to stamp the scrapbook case on top
# of those screens. Leave it registered so load order stays stable, but draw nothing.

init 300 python:
    if "lc_phone_hardware_overlay" not in config.overlay_screens:
        config.overlay_screens.append("lc_phone_hardware_overlay")


screen lc_phone_hardware_overlay():
    zorder 399
