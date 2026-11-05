# Title screen

Code: `game/screens/title_screen.rpy`, `game/screens/title_customiser.rpy`,
`game/systems/title_screen.rpy` (reel + Continue), `game/systems/title_customiser.rpy`
(customiser data, unlocks, title-only Leia rig). Art: `game/gui/title/`.

## What it does

- **Key art.** The chosen background drifts slowly behind Leia, with a light leak and bokeh.
  Leia is a title-only rig with the same layers as in game (base, chest, face, hair) but slower,
  in-sync breathing (`LC_TITLE_BREATH`).
- **Logo.** The one-line logo floats gently, and a sheen sweeps across the letters every ~7 s.
- **Memory reel.** Polaroids of unlocked CGs scroll along the bottom. The default shows
  `LC_TITLE_SAFE_GALLERY` only; the "Memories" chip switches to all unlocked.
- **Continue.** One click loads the newest save.
- **Customise.** Lets the player pick the background, outfit and expression, applied live.

## Unlock rules

The defaults (pool evening, lilac dress) are always available. Everything else unlocks
forever, across all saves, once it has been seen:

- **Backgrounds:** any `bg <tag>` listed for the option was shown.
- **Outfits:** the cast system showed that sprite (`lc_title_note_sprite`, called from
  `cast_staging._lc_put`), or the old seen-image record has it, or any CG listed in
  `seen_cgs` was seen. The CG rule covers players who got there before this feature.
- **18+ options** (`mature=True`: towel, soaked dress, no-bra dress, ahegao) only appear when
  the player turns on "18+ options" (`persistent.lc_title_all_memories`, the same switch as
  the reel's "Memories" chip).

## Adding an outfit

```renpy
init 1 python:
    lc_title_register_outfit(
        "black_cutout", "Black cutout mini",
        "images/sprites/leia/CH2/Base_BlackCutout.png",
        "images/sprites/leia/CH2/Chest_BlackCutout.png",
        seen_tag="leia_black_cutout",          # the in-game sprite tag
        seen_cgs=("ch01_d3_cutout_reveal",),   # optional: CGs showing it
    )
```

Base and chest PNGs must sit on the shared 941 x 1672 Leia canvas. Hair and faces are
shared across outfits.

## Patron custom outfits (Patron of the Trip)

A patron's outfit ships as a personal pack (`game/outfits/<id>/`, containing its PNGs and an
`outfit.rpy`) and is never included in the public build. Its `outfit.rpy` registers the
outfit with `always_unlocked=True` and `credit="Outfit made for <name>"`; the credit is shown
under Leia whenever that outfit is selected.

Still to decide (darryn): whether packs also carry a signed licence and/or an online
one-time redeem code.
