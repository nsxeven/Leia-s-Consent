# Leia's side

Once a day the player can play a short stretch as Leia: where she goes when Ryan isn't there,
in a few short sprite scenes with a couple of her own choices. Day Two's errand (between scene
19b and 19c) is the first instance; its content lands separately. Approved design: LC-Brain
`Plans/2026-11-17 Leia's side design.md` (Part 1).

| Part | File |
|---|---|
| Pure rules (places, cards, visit log, outcomes, cap ledger) | `game/python-packages/lc_leia_side.py` |
| Store binding, hooks, segment labels | `game/systems/leia_side.rpy` |
| Map screen | `game/screens/leia_map_screen.rpy` |
| `leia_think` speaker | `game/characters.rpy` |
| Tinted text box | `screen say` in `game/screens/scrapbook_ui.rpy` |
| Cap hook points | `game/systems/choice_engine.rpy` |
| Developer demo | `game/dev/dev_leia_side.rpy` |
| Tests | `tests/test_leia_side.py` |

## Authoring a segment

1. **Register the places** in the day's visuals or scene file, at `init 1`:

   ```renpy
   init 1 python:
       lc_leia_place("ch01_d2", "cafe", "Café", "bg ch01_d2_cafe", "Something cold for him.", mood="his drink")
       lc_leia_place("ch01_d2", "bar", "Resort bar", "bg ch01_restaurant_bar", "Cocktails and loud music.",
                     locked_reason="A bar, on my own, at four in the afternoon? Not on day two.")
   ```

   `bg` is the card's thumbnail: an existing image name (preferred, it doubles as the Moments
   strip art) or a file path. A `locked_reason` locks the card; it is Leia's own words and shows
   in every mode. A map holds at most four places (one fixed row). Place ids are save data:
   never rename one.

2. **Register her choices** so their gains share the day's cap, next to their
   `CHOICE_EFFECTS.update(...)`:

   ```renpy
       lc_leia_register_choices("ch01_d2", "ch01_d2_errand_cafe_warm", "ch01_d2_errand_cafe_plain")
   ```

   The menus themselves are ordinary story menus: `format_choice` + `apply_choice` with the same
   id, at most five options, scored under `docs/STAT_MODEL.md`.

3. **Play the segment**:

   ```renpy
       call lc_leia_segment_begin("ch01_d2") from d2_errand_begin
       scene bg ch01_villa_entry_day
       with dissolve
       "I left [player_name] dozing on the lounger..."         # her narration, first person
       leia_think "He'd never ask for any of this."             # her inner voice
       while not lc_leia_errand_done("ch01_d2"):
           $ d2_errand_place = lc_leia_map("ch01_d2")
           if d2_errand_place:
               $ lc_leia_visit("ch01_d2", d2_errand_place)
               call expression "ch01_d2_errand_" + d2_errand_place from d2_errand_stop
       call lc_leia_segment_end from d2_errand_end
   ```

   `lc_leia_segment_begin` sets the segment flag, fades to black and shows the
   "Meanwhile — [girlfriend_name]" card; the next `scene` brings her first background in.
   While the flag is set the text box is tinted (blush on day paper, lilac on night paper, pink
   tape corners). `lc_leia_segment_end` clears it; the following Ryan scene brings its own
   `scene`.

4. **Record what happened** with named outcomes (`$ lc_leia_mark("d2_cafe_told_him")`) that later
   scenes, the feed and the review read with `lc_leia_did(...)`, and the visit order with
   `lc_leia_visits("ch01_d2")`.

## The map

- One row of place cards in the scrapbook look (choice-card paper, polaroid thumbnail of the
  place's background, Handjet name, Patrick Hand hint). Heading "WHERE TO FIRST?", then
  "WHERE TO NEXT?".
- **Open** cards return their id (click, tap, Enter/A, or the number key of their slot).
  **Visited** cards are desaturated with a BEEN THERE stamp. **Locked** cards are greyed with a
  padlock and show Leia's reason in every mode; Insight, Full and Developer add
  "Opens on a later day." (no unlock rule is promised).
- Locked and visited cards take keyboard/gamepad focus like any card, so the reason can be read,
  but activating them does nothing (`NullAction`). Number keys exist only for open cards.
- No dismiss: she visits every open place, in the order the player picks. There is no invisible
  full-screen button (the dim behind the cards is a plain `Solid`), so focus always lands on a card;
  the first open card takes default keyboard focus.
- Reduced motion (screen shake or transitions off, `lc_pov_reduce_motion`) drops the staggered
  entrance and the hover lift; the hover art still cross-fades.
- `lc_leia_map` shows the screen only while an open place is left (it returns `None` otherwise),
  and never returns a closed place (developer builds raise, release ignores the pick).

## Moments strip

Every open place registers a Moments strip moment of kind `errand` (neutral Immersive label
"Her errand") with id `leia_<day>_<place>` and the place's image; `lc_leia_visit` marks it found.
Locked places are not registered, so they never count as unfound. Use the review day id
(`ch01_d2`) as the segment day so the moments land on that day's review.

## The +2 per day cap

Leia-side choices may raise her stats by **+2 in total per day** (all stats together). Losses are
never capped and never refund the allowance.

- `apply_choice` applies `lc_choice_effective_effects(id)`: the registered effects passed through
  the `choice_effects` hook filter. `systems/leia_side.rpy` cuts the gains of registered Leia-side
  choices to what is left of the day's allowance, in effect order. After the stats move,
  `choice_applied` records what really landed in the save-local ledger.
- **How a capped gain is shown (Insight/Full/Developer, cards and the toast):** the stat keeps its
  place on the card with the amount that will really apply and a "(capped)" label:
  Full `[Love (capped) +0]`, Insight `[Love (capped) →]`; a partial cut reads `[Love (capped) +1]`.
  The chip keeps the stat's colour logic (`stat_id_for_label` ignores the suffix), so a fully cut
  gain is drawn in plain ink. Immersive shows nothing, as for every choice. Nothing on a card ever
  promises a gain that won't land; the day review lists the real change because it snapshots stats.
  The Full path stamp still comes from the registered effects (it names the direction, not an
  amount). Capped-to-zero picks play no gain sound, and the post-choice toast draws a +0 chip on
  plain paper with no arrow (`screen lc_chip`), so it never reads as a loss.
- `lc_leia_applied_effects(id)` returns what a Leia-side choice really applied. A Day that makes
  her choices lane-exempt (Day Two: `CH01_D2_LANE_EXEMPT_CHOICES`) should subtract these amounts,
  not the registered ones, when it re-resolves its lane.
- The cap is pure (`lc_leia_side.cap_effects` / `record_gain`) and unit-tested.

## Saves and rollback

All state is one save-local dict, `default lc_leia_side_state = {}` (visits per day in order,
named outcomes, the cap ledger), plus `default lc_leia_segment_day = None`. The pure functions
always return a new dict, so rollback (which restores the store's reference) brings visits,
outcomes, the cap and the tint back exactly; this includes rolling back on the map between
visits. Old saves and Chapter Select starts read as "nothing happened".

## Developer demo

Developer systems menu → "Leia's side demo", or `call lc_dev_leia_side` (refuses to run without
`config.developer`). Two open places (Café `ch02_cafe`, Resort shop `ch01_conveniencestore`) and
two locked (Resort bar `ch01_bar`, Boutique `ch02_clothingstore`). Pick the warm option at both
stops to see the cap: the second card reads `Love (capped) +0` in Full.
