# Sprite staging — how to slot sprites in

Everything lives in `game/systems/cast_staging.rpy`. Writers never place sprites
per line; they say **who is in the scene** and **what they wear**, and the
dialogue decides who stands where.

## The rules (darryn, 2026-11-05)

| Situation | What happens |
|---|---|
| Scene opens | Nobody on screen. A sprite appears on that character's **first line**, then stays. |
| Leia speaks | Leia on the **right**, always. |
| Ryan speaks | Ryan on the **left**. |
| Julian / stranger / Maya / anyone else speaks | They take the **left** slot (Ryan steps out). They **stay** through narration and Leia's lines until Ryan or another guest speaks. No flicker. |
| Leia is **not** in the cast (car while she sleeps, villa arrival) | Ryan left, the guest on the **right**. |
| Leia joins mid-scene while a guest is on the right | The guest steps out; they come back on the left when they next speak. |
| CG / cinematic mode up | No sprites. They come back on the next spoken line after the CG. |

## Writing a scene

```renpy
label ch02_scene_03_breakfast:
    scene bg ch01_villa_kitchen_day
    with dissolve
    $ cast(ryan="casual", leia="casual", julian="lounge")

    "Narration — nobody on screen yet."
    friend "Morning."            # Julian appears on the left
    gf "You look awful."         # Leia appears on the right; Julian stays
    "He did look awful."         # both stay
    mc "Coffee?"                 # Ryan replaces Julian on the left
```

| Call | Use |
|---|---|
| `$ cast(ryan="casual", leia="casual", julian="lounge")` | After every `scene bg …`. Replaces the previous cast. `$ cast()` = nobody. |
| `$ face("leia", "smile")` | Change an expression. Applies now if on screen, otherwise on entry. Outfit comes from the cast. |
| `$ cast_add(leia="towel")` | Someone joins, or an outfit change mid-scene. |
| `$ cast_remove("julian")` | Someone leaves mid-scene (fades out). **Not needed before `scene`**: the scene dissolve takes everyone. |
| `$ cast_hold()` … `$ cast_resume(leia="<tag>")` | Hand-choreographed moments (dinner collision). Between them, plain `show`/`hide` lines are yours; `cast_resume` can adopt a hand-placed sprite into its slot without a blink. |

Expressions: `neutral` (default), `smile`, `shy`, `pout`, `flustered`,
`skeptical`, `angry`, `ahegao` — whichever the outfit image defines. Missing
expressions fall back to `neutral`, then to the plain image.

## Adding new art

1. Define the image as `image <who>_<outfit>` (optionally `image <who>_<outfit> smile`, …)
   on the 941×1672 canvas, e.g. `image julian_beach = Fixed(lc_sprite_silhouette("julian_beach_layers"), xysize=(941, 1672))`.
2. Use the outfit name in `cast(julian="beach")`. Done.

New character: add `("<who>", "<Character variable>")` to `LC_CAST_SPEAKERS`
in `cast_staging.rpy` (e.g. `("maya", "maya")` is already there) and define
`image <who>_<outfit>`.

## Leia before the pool reveal

Leave her **out of the cast** until she should be seen (e.g. before she walks
out in her swimsuit); her off-screen lines then show no sprite.
