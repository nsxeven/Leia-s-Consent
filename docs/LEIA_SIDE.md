# Leia's side

Once a day the player can play a short stretch as Leia: where she goes when Ryan isn't there,
in a few short sprite scenes with a couple of her own choices. Day Two's errand (between scene
19b and 19c) is the first instance; its content lands separately. Approved design: LC-Brain
`Plans/2026-11-17 Leia's side design.md` (Part 1).

| Part | File |
|---|---|
| Pure rules (places, cards, visit log, outcomes, cap ledger) | `game/python-packages/lc_leia_side.py` |
| Store binding, hooks, segment labels, place checks | `game/systems/leia_side.rpy` |
| Map screen | `game/screens/leia_map_screen.rpy` |
| `leia_think` speaker | `game/characters.rpy` |
| Tinted text box | `screen say` in `game/screens/scrapbook_ui.rpy` |
| Cap hook points | `game/systems/choice_engine.rpy` |
| Developer demo | `game/dev/dev_leia_side.rpy` |
| Tests | `tests/test_leia_side.py` |

## Authoring a segment

1. **Register the places** in the day's visuals or scene file, at `init 1`. Either one call per
   place:

   ```renpy
   init 1 python:
       lc_leia_place("ch01_d2", "cafe", "Café", "bg ch01_d2_cafe", "Something cold for him.",
                     mood="his drink", done="Frappuccino: got it.")
       lc_leia_place("ch01_d2", "bar", "Resort bar", "bg ch01_restaurant_bar",
                     locked_reason="A bar, on my own, at four in the afternoon? Not on day two.")
   ```

   or a list (or tuple) of dicts, registered once:

   ```renpy
   define CH01_D2_ERRAND_PLACES = [
       {"id": "cafe", "label": "Café", "bg": "bg ch01_d2_cafe",
        "hint": "Something cold for him.", "done": "Frappuccino: got it."},
       {"id": "bar", "label": "Resort bar", "bg": "bg ch01_restaurant_bar", "locked": True,
        "locked_reason": "A bar, on my own, at four in the afternoon? Not on day two."},
   ]
   init 1 python:
       lc_leia_register_places("ch01_d2", CH01_D2_ERRAND_PLACES)
   ```

   Dict keys: `id`, `label`, `bg`, `hint`, `locked_reason`, `locked`, `mood`, `done`. Any other
   key raises, `"locked": True` needs a `locked_reason`, and only open places need a `hint`.
   `done` (optional) replaces the hint on the card once she has been there.

   `bg` is the card's thumbnail and the Moments strip art: an image **name** with its tag
   (`"bg ch01_d2_cafe"`, not `"ch01_d2_cafe"`) or a file path. Images are defined at init 500, so
   every place's `bg` is checked at `init 999`: a name that is not a defined image (or a path that
   doesn't load) stops a developer build with an error naming the day, the place and the bad
   `bg`, and suggests `"bg <name>"` when you left the tag off. Text in a `bg` that can't be an
   image name (spaces in odd places, brackets such as `"x (see C3)"`) is rejected at
   registration. A `locked_reason` locks the card; it is Leia's own words and shows in every mode.
   A map holds at most four places (one fixed row). Place ids are save data: never rename one.

2. **Register her choices** so their gains share the day's cap, next to their
   `CHOICE_EFFECTS.update(...)`:

   ```renpy
       lc_leia_register_choices("ch01_d2", "ch01_d2_errand_cafe_warm", "ch01_d2_errand_cafe_plain")
   ```

   The menus themselves are ordinary story menus: `format_choice` + `apply_choice` with the same
   id, at most five options, scored under `docs/STAT_MODEL.md`. Never register Ryan's choices
   here (his confession reply included): his are never capped.

3. **Play the segment.** `lc_leia_segment_begin` and `lc_leia_segment_end` are **labels**, not
   functions: always `call` them. `$ lc_leia_segment_begin("ch01_d2")` raises a NameError, and
   `tests/test_leia_side.py` fails on that form anywhere in `game/`. Copy this:

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

   `lc_leia_map(day)` shows every place registered for the day. To show a subset or a different
   order, pass a list or tuple of ids (`["shop", "cafe"]`) or the same list of dicts you
   registered (`lc_leia_map("ch01_d2", CH01_D2_ERRAND_PLACES)`). An unregistered id, a dict that
   differs from the registered place, or anything that is not a list/tuple (a single string, one
   dict) raises a clear error in developer builds; release builds fall back to every registered
   place.

   `lc_leia_segment_begin` sets the segment flag, fades to black and shows the
   "Meanwhile — [girlfriend_name]" card; the next `scene` brings her first background in.
   While the flag is set the text box is tinted (blush on day paper, a pink-lilac lift on night
   paper, pink tape corners). `lc_leia_segment_end` clears it; the following Ryan scene brings its
   own `scene`. If a scene jumps out of her segment without the end label, the day review clears
   the flag (developer builds raise so the missing `call` gets fixed).

4. **Record what happened** with named outcomes (`$ lc_leia_mark("d2_cafe_told_him")`) that later
   scenes, the feed and the review read with `lc_leia_did(...)`.

5. **Branch on the visit order** with the helpers, never by comparing `lc_leia_visits(day)`
   with a list: it returns a **tuple** (`("shop", "cafe")`), so `== ["shop"]` is always False.
   The test suite fails on `lc_leia_visits(...) == [` / `!= [` anywhere in `game/`.

   | Helper | Returns |
   |---|---|
   | `lc_leia_first("ch01_d2")` | the first place she went to, or `None` |
   | `lc_leia_visited_first("ch01_d2", "shop")` | `True` when the shop was her first stop |
   | `lc_leia_visited_before("ch01_d2", "shop", "cafe")` | `True` when she has been to the shop and not to the café before it (café later, or not yet) |
   | `lc_leia_visits("ch01_d2")` | the full tuple, in order (`len(...)`, `in`) |

   ```renpy
       if lc_leia_visited_first("ch01_d2", "shop"):
           leia_think "Muffins, done. Frappuccino last, so the ice survives the walk home."
       else:
           leia_think "Frappuccino first was maybe a mistake."
   ```

   The two place helpers check their ids against the day's registered places (a typo raises in
   developer builds).

### Porting the PR 3 draft (`nm-c-script`)

- `$ lc_leia_segment_begin("ch01_d2")` → `call lc_leia_segment_begin("ch01_d2") from <unique id>`;
  `$ lc_leia_segment_end()` → `call lc_leia_segment_end from <unique id>`.
- `CH01_D2_ERRAND_PLACES`: give every `bg` its tag and a real image (`"bg ch01_d2_cafe"`; the shop
  needs a defined day image, not `"ch01_shop_day_or_night (see C3)"`), keep `"done"`, and register
  the list at `init 1` with `lc_leia_register_places("ch01_d2", CH01_D2_ERRAND_PLACES)`. Passing it
  to `lc_leia_map` then works.
- `lc_leia_visits("ch01_d2") == ["shop"]` → `lc_leia_visited_first("ch01_d2", "shop")`.
- Lane exemption: add every errand id **and** Ryan's three confession-reply ids to
  `CH01_D2_LANE_EXEMPT_CHOICES` and change nothing else (see the cap section below).

## The map

- One row of place cards in the scrapbook look (choice-card paper, polaroid thumbnail of the
  place's background, Handjet name, Patrick Hand hint). Heading "WHERE TO FIRST?", then
  "WHERE TO NEXT?".
- **Open** cards return their id (click, tap, Enter/A, or the number key of their slot).
  **Visited** cards are desaturated with a BEEN THERE stamp and show the place's `done` line when
  it has one (its hint otherwise). **Locked** cards are greyed with a padlock and show Leia's
  reason in every mode; Insight, Full and Developer add "Opens on a later day." (no unlock rule is
  promised).
- Locked and visited cards take keyboard/gamepad focus like any card, so the reason can be read,
  but activating them does nothing (`NullAction`). Number keys exist only for open cards.
- No dismiss: she visits every open place, in the order the player picks. There is no invisible
  full-screen button (the dim behind the cards is a plain `Solid`), so focus always lands on a card;
  the first open card takes default keyboard focus.
- The map sits at zorder 90, under the quick menu (100) like the choice menu, so Back, Log, Save
  and Prefs stay clickable while it is up.
- Reduced motion (screen shake or transitions off, `lc_pov_reduce_motion`) drops the staggered
  entrance and the hover lift; the hover art still cross-fades.
- `lc_leia_map` shows the screen only while an open place is left (it returns `None` otherwise),
  and never returns a closed place (developer builds raise, release ignores the pick).

## Moments strip

Every open place registers a Moments strip moment of kind `errand` (neutral Immersive label
"Her errand") with id `leia_<day>_<place>` and the place's image; `lc_leia_visit` marks it found.
Locked places are not registered, so they never count as unfound. Use the review day id
(`ch01_d2`) as the segment day so the moments land on that day's review. A save with no visit on
that day (for example an old save already past the errand) shows no errand tiles at all (the
`discovery_strip` filter), so a missed errand never reads as a failure.

## The +2 per day cap

Leia-side choices may raise her stats by **+2 in total per day** (all stats together). Losses are
never capped and never refund the allowance.

- `apply_choice` applies `lc_choice_effective_effects(id)`: the registered effects passed through
  the `choice_effects` hook filter. `systems/leia_side.rpy` cuts the gains of registered Leia-side
  choices to what is left of the day's allowance, in effect order. After the stats move,
  `choice_applied` records what really landed in the save-local ledger.
- **How a capped gain is shown (Insight/Full/Developer, cards and the toast):** the stat keeps its
  place on the card with the amount that will really apply and a "(capped)" label
  (`lc_stat_model.CAPPED_SUFFIX`): Full `[Love (capped) +0]`, Insight `[Love (capped) →]`; a
  partial cut reads `[Love (capped) +1]`. The chip keeps the stat's colour logic
  (`stat_id_for_label` ignores the suffix), so a fully cut gain is drawn in plain ink. Immersive
  shows nothing, as for every choice. Nothing on a card ever promises a gain that won't land; the
  day review lists the real change because it snapshots stats. The Full path stamp still comes
  from the registered effects (it names the direction, not an amount). Capped-to-zero picks play
  no gain sound, and the post-choice toast draws a +0 chip on plain paper with no arrow
  (`screen lc_chip`), so it never reads as a loss.
- **Lane exemption (Day Two and later days):** the design keeps her side and Ryan's confession
  reply from changing tonight's lane. Add their ids to the day's exempt tuple
  (`CH01_D2_LANE_EXEMPT_CHOICES`); nothing else. The lane loop subtracts
  `lc_choice_applied_effects(id)` and `lc_exhib_gained(prefix)` adds the same values, so the two
  always agree:
  - a Leia-side id gives what her cap really let through (her ledger), counted once;
  - every other id, Ryan's confession reply included, gives its registered effects (his choices
    are never capped, so registered = applied).
  Don't call `lc_leia_applied_effects` for this: it returns `[]` for any id that is not hers, so
  Ryan's reply would silently stop being subtracted.
- The cap is pure (`lc_leia_side.cap_effects` / `record_gain`) and unit-tested.

## Saves and rollback

All state is one save-local dict, `default lc_leia_side_state = {}` (visits per day in order,
named outcomes, the cap ledger), plus `default lc_leia_segment_day = None`. The pure functions
always return a new dict, so rollback (which restores the store's reference) brings visits,
outcomes, the cap and the tint back exactly; this includes rolling back on the map between
visits. Old saves and Chapter Select starts read as "nothing happened".

## Developer demo

Developer systems menu → "Leia's side demo", or `call lc_dev_leia_side` (refuses to run without
`config.developer`). Two open places (Café `bg ch01_d2_cafe`, Resort shop `bg ch01_shop_night`,
both with a `done` line) and two locked (Resort bar `bg ch01_restaurant_bar`, Boutique
`bg ch01_d2_boutique`). Each run forgets only the demo's own record (`lc_leia_side.reset_day`),
never a story day's. Pick the warm option at both stops to see the cap: café first, the shop card
then reads `[Love (capped) +0]` in Full; shop first, the café card reads
`[Love +1 • Trust (capped) +0]`.

## Not done

- History entries during her segment look like Ryan's (no "Leia" marker). Changing how the
  History screen labels entries is a UI call for darryn; nothing here depends on it.
