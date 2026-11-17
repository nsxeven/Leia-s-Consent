# Feed app

A parody social-feed app on Ryan's phone. Ryan can stumble on what happened elsewhere on
every route by reading posts; reading never changes stats. The display name is one constant,
`define LC_FEED_APP_NAME = "Instababe"` in `game/systems/feed.rpy` (placeholder until darryn
picks a name; renaming it is a one-line change and breaks nothing, because no id contains it).

| Piece | File |
|---|---|
| Rules (registry checks, release batches and gates, ordering, seen/opened records, badge, stamps, reactions, 18+ masking, scroll-to-focus maths) | `game/python-packages/lc_feed.py` |
| Store state, API, reaction runner | `game/systems/feed.rpy` |
| Feed list inside the phone, opened post | `game/screens/phone_feed.rpy` |
| Home-grid slot, badge, catch-up timer, feed scroll, Back/close (`phone_closed` hook) | `game/screens/phone_sweetheart.rpy` (`lc_sm_home_apps`, `lc_sm_app_badge`, `lc_phone_back`, `lc_phone_close`) |
| Phone HUD badge (messages + unseen posts) | `game/screens/phone_hud.rpy` |
| Banner deep link and icon | `game/systems/phone_presentation_logic.rpy` (`lc_phone_open_from_notification`), `game/screens/scrapbook_ui.rpy` (`phone_notification_banner`) |
| App icon art | `game/gui/phone/sprite_match/feed.png`, drawn by `tools/gen_sprite_match_ui.py` |
| Day Two posts | `game/chapters/ch01/day2/ch01_day2_feed.rpy` |
| Tests | `tests/test_feed.py` |

## Writing a post

1. Register it at `init 1` in the Day's feed file:

```renpy
init 1 python:
    lc_feed_register(
        "d2_feed_love_shop", "ch01_d2", "Margaret", "islandmart_marg",
        "A young lady bought the last chocolate muffins for her sweetheart today.",
        comments=[("harold_b", "You still are, Marg.")],
        likes=12,
        unlock={"ch01_d2_errand_lane": "love"},
        reaction="ch01_d2_feed_react_shop")
```

   `lc_feed_register(post_id, day, author, handle, caption, image=None, comments=(), likes=0,
   when=None, unlock=None, mature=False, reaction=None)`

   - `post_id`: stable and unique; it is saved (never rename it).
   - `day`: the review day id (`ch01_d2`).
   - `author` / `handle`: display name and @handle (no `@`). An author whose lower-cased name
     has a phone avatar (`gui/phone/sprite_match/avatar_maya.png`) gets it; anyone else gets
     an initial tile.
   - `author`, `handle`, `caption` and `comments` (0-3 `(handle, text)` pairs) write
     player-editable names as `[player_name]`, `[girlfriend_name]`, `[friend_name]`; a typed
     default name raises (handles are checked case-blind: `leia.official` raises too).
   - `image`: a Ren'Py image name (`"cg ..."`). `mature=True` follows the Gallery rule: while
     `GALLERY_MASK_MATURE_COVERS` is on, the feed card and the opened post show a dark
     "MATURE / 18+" card with **no image**; tapping it in the opened post opens the full-screen
     photo viewer, like opening a Gallery entry.
   - `when`: leave it `None` and the post is stamped with the story clock at release (set
     `lc_phone_set_story_time(...)` first, see step 2). A fixed `"14:10"` or a zero-argument
     callable (run once at release, e.g. a helper that reads the visit order) also work. With
     no story clock and no `when`, the post shows no time: the device clock never appears.
   - `unlock` (the gate, checked **once, at release**):
     - `None`: always.
     - a dict, every row must hold: `{"ch01_d2_errand_lane": "love"}` (story value equals),
       `{"ch01_d2_errand_lane": ("love", "exhibitionism")}` (any of), `{"ch01_d2_leia_told": True}`
       (set), `{"leia_did": "ch01_d2_cafe_ntr_lingered"}` / `{"leia_did_not": ...}` (Leia's recorded
       choices, `lc_leia_did`). A save that has no value for a row fails the gate.
     - a zero-argument callable for anything else.
     **Day posts that describe a scene gate on that scene's recorded outcome**, so old saves and
     paths that skipped it stay clean (no post, no banner, no app).
   - Variants (a caption that depends on a choice): register one post per variant with
     complementary gates (`"leia_did"` / `"leia_did_not"`) and release them together; only the
     matching one comes out.
   - `reaction`: Ryan's one-time reaction the first time he sees the post: a **label name**
     (preferred; it plays as normal story lines) or a zero-argument callable. It runs once, after
     the player closes the phone, then the line under the phone shows again. It never runs
     from inside the screen.

2. Release it where it should appear:

```renpy
    $ lc_phone_set_story_time("21:40")       # the time the dialogue gives, before releasing
    $ lc_feed_install()                       # only for the intro: the app joins the home grid
    $ lc_feed_release("d2_feed_love_pool", "d2_feed_love_shop", "d2_feed_exhib_pool", "d2_feed_ntr_clip")
    "Somewhere on the walk my phone buzzed in my pocket."
    ...
    $ lc_phone_clear_story_time()             # at the next time skip
```

   `lc_feed_release(*post_ids, notify=True)`: each post comes out only if its gate holds now
   and it is not out yet (release a lane's posts side by side and only the matching ones
   appear). **One call = one banner** when anything came out ("Maya" + caption for one post,
   "2 new posts" for a batch); `notify=False` shows none. Once out, a post stays (frozen), so a
   post the player read never disappears when a stat moves. Releasing an already-released post
   changes nothing. Set `lc_phone_set_story_time(when)` before `lc_feed_release` whenever the
   player can open the phone on that beat, so the stamp and the phone clock agree.

3. Read it in a later scene: `lc_feed_seen("id")` / `lc_feed_any_seen("a", "b")` are True once
   Ryan **saw** the post: he opened the feed while it was out (the list shows every caption) or
   opened the post. `lc_feed_opened("id")` is the narrower "tapped it open" record if a scene
   ever needs it. Use them for an extra choice option or an echo, with a neutral `else`; they
   never move stats. To be sure every reaction already played before the scene reads them,
   `call lc_feed_reaction_runner` (it does nothing when none are pending).

## Behavior

- The app is on the home grid (8th slot) once `lc_feed_install()` ran or any post is out
  (`lc_feed_app_visible()`). Before that it isn't drawn at all.
- Feed order: newest release first. Unseen posts badge the app icon (`9+` cap) **and the phone
  HUD** (added to unread messages; the Messages icon still counts messages only). Opening the
  feed marks every listed post seen (the catch-up timer in `phone_screen`); the blue dot shows
  which posts were new on this visit.
- Each release call that brings anything out queues one phone banner (app name, title, body,
  feed icon); tapping it opens the phone on the feed.
- Keyboard and gamepad: focus walks the cards and the list scrolls so the focused card is fully
  visible with a peek of the next (`lc_feed_reveal_focus`); the mouse never triggers that
  scroll. In an opened post the arrow/page keys scroll it.
- Back: opened photo -> opened post -> feed -> home. Close dismisses every layer, then runs any
  pending reactions.
- No posts: an empty-state card ("No posts yet").
- Developer mode shows each post id on its card.

## Saves, rollback and old saves

- Save state (all `default`s): `lc_feed_installed`, `lc_feed_released` (ids in release order),
  `lc_feed_seen_posts`, `lc_feed_opened_posts`, `lc_feed_stamps` (`{id: time}` frozen at
  release), `lc_feed_reacted`, `lc_feed_reaction_queue`. Every change rebinds the variable to a
  new object, so rollback restores it with the story. Marking posts seen/opened calls
  `renpy.retain_after_load()`, so saving with the phone open keeps them.
- The registry `LC_FEED_POSTS` is init-time data, never saved: caption fixes reach old saves.
  A released id that is no longer registered is skipped.
- **Old saves:** a save made past the Day Two photo walk (scene 09) in an older build never ran
  the intro, so its phone has no app and nothing is back-filled (the "didn't happen" rule for
  new systems). Gated posts keep it that way. Chapter Select installs the app for Day Three to
  Five starts (every Day Two path installs it); a Day Two start plays the intro normally.

## Day Two

- Scene 09 (photo walk, `ch01_day2_scene_09_photo_walk`): after Maya joins the Trip Group and
  the group picture changes, she installs the app on Ryan's phone and follows herself; the
  story clock is set to 14:10 (after lunch) and `d2_maya_group_photo` is released, stamped
  14:10 (text-only: the four-person group selfie art is still pending). The clock is cleared
  before scene 10.
