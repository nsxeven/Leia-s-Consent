# Day Two breakfast: the same stable CG id remains mapped to the mature
# Gallery page. The registry owns only the opt-in cue and image scope.
init 1 python:
    lc_pov_register(
        "d2_breakfast_julian",
        image="cg ch01_d2_breakfast_julian_pov",
        source="cg ch01_d2_breakfast_02",
        # Sparkle centre; same spot as the old 64x64 slot at (1660, 240).
        center=(1692, 272),
        title="Julian's POV",
        mature=True,
    )


# Old-save compatibility (builds from 2026-11-10 to 11-14 used a blocking
# `call screen lc_breakfast_julian_pov`). A save made while that screen was up
# still names it in its screen stack, so the screen must exist. This stub draws
# nothing, takes no input and immediately returns None (= "keep reading"), so
# the story carries on with the shared Hidden POV cue. Do not use it for new
# content.
screen lc_breakfast_julian_pov(*args, **kwargs):
    zorder 0
    timer 0.01 action Return(None)
