# Julian — sprites. Staging is handled game-wide by systems/cast_staging.rpy:
# put him in the scene with  $ cast(..., julian="<outfit>")  and he appears
# when he speaks.
#
# Outfit art (941x1672 canvas, same envelope as Ryan and Leia):
#   party   -> black button-up + khaki shorts (stand-in until party art exists;
#              darryn, 2026-11-04). Swap the file in julian_party_layers later.
#   travel  -> cream shirt + olive shorts
#   pool    -> swim shorts
#   evening -> black button-up + khaki shorts
#   lounge  -> black tee + grey shorts

init 1:
    # init 1: lc_sprite_silhouette is defined at init 0 in leia_prologue_party.rpy,
    # which loads after this file.
    layeredimage julian_party_layers:
        always "images/sprites/julian/BASE_BlackShirt.png"

    layeredimage julian_travel_layers:
        always "images/sprites/julian/BASE_CreamShirt.png"

    layeredimage julian_pool_layers:
        always "images/sprites/julian/BASE_SwimShorts.png"

    layeredimage julian_evening_layers:
        always "images/sprites/julian/BASE_BlackShirt.png"

    layeredimage julian_lounge_layers:
        always "images/sprites/julian/BASE_BlackTeeGreyShorts.png"

    image julian_party = Fixed(lc_sprite_silhouette("julian_party_layers"), xysize=(941, 1672))
    image julian_travel = Fixed(lc_sprite_silhouette("julian_travel_layers"), xysize=(941, 1672))
    image julian_pool = Fixed(lc_sprite_silhouette("julian_pool_layers"), xysize=(941, 1672))
    image julian_evening = Fixed(lc_sprite_silhouette("julian_evening_layers"), xysize=(941, 1672))
    image julian_lounge = Fixed(lc_sprite_silhouette("julian_lounge_layers"), xysize=(941, 1672))
