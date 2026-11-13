# Day Two breakfast: the same stable CG id remains mapped to the mature
# Gallery page. The registry owns only the opt-in cue and image scope.
init 1 python:
    lc_pov_register(
        "d2_breakfast_julian",
        image="cg ch01_d2_breakfast_julian_pov",
        source="cg ch01_d2_breakfast_02",
        position=(1660, 240),
        title="Julian's POV",
        mature=True,
    )
