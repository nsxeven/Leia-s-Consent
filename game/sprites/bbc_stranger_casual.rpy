# BBC Stranger — Day One restaurant casual outfit (legacy single-state name).
#
# The production art is split into dry and wet states that share one 941x1672
# canvas (see chapters/ch01/ch01_scenes_07_13_visuals.rpy):
#   stranger_casual_dry  -> pre-spill approach
#   stranger_casual_wet  -> post-spill aftermath and exit
#
# The old Base_Casual.png / Penis_Casual.png files no longer exist, so the former
# layered rig here pointed at unloadable files. `bbc_stranger_casual` is kept only
# as an alias of the dry state for any old reference; story code should use the
# explicit dry/wet images. The later passerby is a different man and must not
# use either of them.

transform stranger_breathing_expand:
    xzoom 1.0
    xoffset 0

    block:
        parallel:
            linear 0.65 xzoom 1.04
        parallel:
            linear 0.65 xoffset -18
        pause 0.10
        parallel:
            linear 0.65 xzoom 1.0
        parallel:
            linear 0.65 xoffset 0
        pause 0.10
        repeat

image bbc_stranger_casual = "stranger_casual_dry"
