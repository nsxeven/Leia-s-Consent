# Feed app

A parody social-feed app on Ryan's phone. Ryan can stumble on what happened elsewhere on
every route by reading posts; reading never changes stats or story state. The display name
is one constant, `define LC_FEED_APP_NAME = "Instababe"` in `game/systems/feed.rpy`
(placeholder until darryn picks a name; renaming it is a one-line change and breaks nothing,
because no id contains it).

| Piece | File |
|---|---|
| Rules (registry checks, release/unlock, ordering, seen record, badge, 18+ masking) | `game/python-packages/lc_feed.py` |
| Store state and API | `game/systems/feed.rpy` |
| Feed list inside the phone, opened post | `game/screens/phone_feed.rpy` |
| Home-grid slot, badge, Back/close | `game/screens/phone_sweetheart.rpy` (`lc_sm_home_apps`, `lc_sm_app_badge`, `lc_phone_back`, `lc_phone_close`) |
| Banner deep link and icon | `game/systems/phone_presentation_logic.rpy` (`lc_phone_open_from_notification`), `game/screens/scrapbook_ui.rpy` (`phone_notification_banner`) |
| App icon art | `game/gui/phone/sprite_match/feed.png`, drawn by `tools/gen_sprite_match_ui.py` |
| Day Two posts | `game/chapters/ch01/day2/ch01_day2_feed.rpy` |
| Tests | `tests/test_feed.py` |

## Writing a post

1. Register it at `init 1` in the Day's feed file:

```renpy
init 1 python:
    lc_feed_register(
        "d2_maya_group_photo", "ch01_d2", "Maya", "maya.in.frame",
        "Three attempts because somebody blinked twice.",
        comments=[("[friend_name]", "The sun was very aggressive. I stand by it.")],
        likes=23, when="14:10")
```

   `lc_feed_register(post_id, day, author, handle, caption, image=None, comments=(), likes=0,
   when=None, unlock=None, mature=False)`

   - `post_id`: stable and unique; it is saved (never rename it).
   - `day`: the review day id (`ch01_d2`); one banner per day.
   - `author` / `handle`: display name and @handle (no `@`). An author whose lower-cased name
     has a phone avatar (`gui/phone/sprite_match/avatar_maya.png`) gets it; anyone else gets
     an initial tile.
   - `caption` and `comments` (0-3 `(handle, text)` pairs) write player-editable names as
     `[player_name]`, `[girlfriend_name]`, `[friend_name]`; a typed default name raises.
   - `image`: a Ren'Py image name (`"cg ..."`). `mature=True` blurs it with an 18+ mark on the
     feed card and the opened post; tapping it opens the full-screen photo viewer unmasked,
     like a Gallery entry the player opens.
   - `when`: the time line under the handle (`"14:10"`); `None` shows none.
   - `unlock`: `None` or a zero-argument callable (for example
     `lambda: get_story_value("d2_lane") == "love"`), checked **once, at release**.

2. Release it where it should appear:

```renpy
    $ lc_feed_install()                       # only for the intro: the app joins the home grid
    $ lc_feed_release("d2_maya_group_photo")  # appears, badges the icon, banner if first today
```

   `lc_feed_release(post_id, notify=True)`: if the unlock condition is False now, nothing
   happens (release a lane's posts side by side and only the matching one appears). Once out,
   a post stays (frozen), so a post the player read never disappears when a stat moves.
   Releasing an already-released post changes nothing.

3. Read it in a later scene: `lc_feed_seen("id")` / `lc_feed_any_seen("a", "b")` are True once
   this save **opened** the post (tapped its card). Use them for an extra choice option or an
   echo, with a neutral `else`; they never move stats.

## Behaviour

- The app is on the home grid (8th slot) once `lc_feed_install()` ran or any post is out
  (`lc_feed_app_visible()`). Before that it isn't drawn at all.
- Feed order: newest release first. A blue dot marks posts not opened yet; the icon badge counts
  them (`9+` cap). The phone HUD badge still counts unread messages only.
- The first post released on a day queues one phone banner (app name, author, caption preview,
  feed icon); tapping it opens the phone on the feed.
- Back: opened photo -> opened post -> feed -> home. Close dismisses every layer.
- No posts: an empty-state card ("No posts yet").
- Developer mode shows each post id on its card.

## Saves, rollback and old saves

- Save state (all `default`s): `lc_feed_installed`, `lc_feed_released` (ids in release order),
  `lc_feed_seen_posts`, `lc_feed_banner_days`. Every change rebinds the variable to a new
  object, so rollback restores it with the story. Opening a post calls
  `renpy.retain_after_load()`, so saving with the post open keeps it seen.
- The registry `LC_FEED_POSTS` is init-time data, never saved: caption fixes reach old saves.
  A released id that is no longer registered is skipped.
- **Old saves:** a save made past the Day Two photo walk (scene 09) in an older build never ran
  the intro, so its phone has no app and nothing is back-filled (the "didn't happen" rule for
  new systems). The app appears there the next time the story releases a post. Chapter Select
  starts at the top of a Day: a Day Two start plays the intro normally; a Day Three to Five
  start has no app until a later post is released.

## Day Two

- Scene 09 (photo walk, `ch01_day2_scene_09_photo_walk`): after Maya joins the Trip Group and
  the group picture changes, she posts the group photo, installs the app on Ryan's phone and
  follows herself; `d2_maya_group_photo` is released (text-only: the four-person group selfie
  art is still pending). No other Day Two posts yet.
