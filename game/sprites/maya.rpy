# Maya — green tube top for the Day Two café sequence only.
# Her own 941x1672 Base -> animated Chest -> Expression rig uses Leia's
# animation mechanics and silhouette, but none of Leia's art. Maya currently
# has no neutral or blink frames: Smile is the intentional default, not neutral.
# Do not use nude layers as public clothing or reuse this outfit after the café.
layeredimage maya_green_tube_top_layers:
    always "images/sprites/maya/CH2/Base_GreenTubeTop.png"
    always "images/sprites/maya/CH2/Chest_GreenTubeTop.png" at leia_chest_breathe

    group expression:
        attribute smile default:
            "images/sprites/maya/expressions/Smile.png"
        attribute shy:
            "images/sprites/maya/expressions/Shy.png"
        attribute skeptical:
            "images/sprites/maya/expressions/Skeptical.png"
        attribute angry:
            "images/sprites/maya/expressions/Angry.png"

# Cast staging prefers an explicit neutral image, then the plain image. The
# latter resolves to Smile so missing faces never masquerade as neutral art.
image maya_green_tube_top = Fixed(lc_sprite_silhouette("maya_green_tube_top_layers smile"), xysize=(941, 1672))
image maya_green_tube_top smile = Fixed(lc_sprite_silhouette("maya_green_tube_top_layers smile"), xysize=(941, 1672))
image maya_green_tube_top shy = Fixed(lc_sprite_silhouette("maya_green_tube_top_layers shy"), xysize=(941, 1672))
image maya_green_tube_top skeptical = Fixed(lc_sprite_silhouette("maya_green_tube_top_layers skeptical"), xysize=(941, 1672))
image maya_green_tube_top angry = Fixed(lc_sprite_silhouette("maya_green_tube_top_layers angry"), xysize=(941, 1672))