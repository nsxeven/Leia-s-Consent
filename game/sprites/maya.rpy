# Maya — green tube top for the Day Two café sequence only.
# Her own 941x1672 Base -> animated Chest -> Expression rig uses Leia's
# animation mechanics and silhouette, but none of Leia's art. Maya's Base
# already contains her neutral face; no separate neutral or blink PNG exists.
# Do not use nude layers as public clothing or reuse this outfit after the café.
layeredimage maya_green_tube_top_layers:
    always "images/sprites/maya/CH2/Base_GreenTubeTop.png"
    always "images/sprites/maya/CH2/Chest_GreenTubeTop.png" at leia_chest_breathe

    group expression:
        # Neutral leaves the face painted on Base unobscured.
        attribute neutral null default
        attribute smile:
            "images/sprites/maya/expressions/Smile.png"
        attribute shy:
            "images/sprites/maya/expressions/Shy.png"
        attribute skeptical:
            "images/sprites/maya/expressions/Skeptical.png"
        attribute angry:
            "images/sprites/maya/expressions/Angry.png"

# Cast staging requests neutral first, including on first speech. Keep the
# plain image as the same no-overlay neutral for any external callers.
image maya_green_tube_top = Fixed(lc_sprite_silhouette("maya_green_tube_top_layers neutral"), xysize=(941, 1672))
image maya_green_tube_top neutral = Fixed(lc_sprite_silhouette("maya_green_tube_top_layers neutral"), xysize=(941, 1672))
image maya_green_tube_top smile = Fixed(lc_sprite_silhouette("maya_green_tube_top_layers smile"), xysize=(941, 1672))
image maya_green_tube_top shy = Fixed(lc_sprite_silhouette("maya_green_tube_top_layers shy"), xysize=(941, 1672))
image maya_green_tube_top skeptical = Fixed(lc_sprite_silhouette("maya_green_tube_top_layers skeptical"), xysize=(941, 1672))
image maya_green_tube_top angry = Fixed(lc_sprite_silhouette("maya_green_tube_top_layers angry"), xysize=(941, 1672))