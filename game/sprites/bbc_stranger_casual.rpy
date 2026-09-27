# BBC Stranger — Day One restaurant casual outfit.
 # Fixed-coordinate production layers: Base -> Penis -> Chest.
 # Penis uses the same synchronized breathing expansion as Chest.

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

layeredimage bbc_stranger_casual_layers:
    always "images/sprites/bbc stranger/Base_Casual.png"
    always "images/sprites/bbc stranger/Penis_Casual.png" at stranger_breathing_expand
    always "images/sprites/bbc stranger/Chest_Casual.png" at stranger_breathing_expand

image bbc_stranger_casual = Fixed(lc_sprite_silhouette("bbc_stranger_casual_layers"), xysize=(941, 1672))
