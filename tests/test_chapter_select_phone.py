"""Chapter Select phone history: earlier Days' messages, Photos, reply cards and the Trip Group picture.

A Chapter Select preset starts a new game at Day N. Each Day pack's "finished" seed (its
*_chapter.rpy) replays what that Day put on the phone through chapter_select_phone*
(game/systems/chapter_select.rpy), so the phone at Day N's start looks like a normal playthrough's.

Checks:
* Drift: every seeded message id exists in the story files with the same thread, sender and text
  (the text expression is compared as code, so a name concatenation matches only the same
  concatenation; a branch-dependent text must equal one of the branches the story can deliver).
  Reply-card messages (<prompt>_ryan, <prompt>_followup_NN) are checked against the card's option.
* Completeness: every message the Prologue-Day 4 story files can deliver is seeded by some preset
  or listed in NOT_SEEDED with the reason (another branch than the presets imply).
* State: for each of the presets, the seeded phone (thread message ids in order, every count read,
  no banners, no open reply cards, Photos, Trip Group stage and Maya membership) equals EXPECTED,
  a table written from the story files; EXPECTED itself is checked against them (threads and play
  order of every id).
"""
import ast
import re
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lc_rpy_harness import load, load_blocks  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
CH = GAME / "chapters"

# Story files in play order (the order a playthrough reaches them). Only files that deliver texts
# in label code matter for the order check; the rest still feed the id/text index.
PLAY_ORDER = [
    "prologue/prologue.rpy",
    "ch01/day1/ch01_main.rpy",
    "ch01/day1/ch01_scenes_04_06.rpy",
    "ch01/day1/ch01_scenes_07_13.rpy",
    "ch01/day1/ch01_scenes_14_30.rpy",
    "ch01/day2/ch01_day2_scenes_01_15.rpy",
    "ch01/day2/ch01_day2_scenes_16_30.rpy",
    "ch01/day3/ch01_day3_scenes.rpy",
    "ch01/day4/ch01_day4_scenes_01_08.rpy",
    "ch01/day4/ch01_day4_scenes_09_16.rpy",
]
EARLIER_DAYS = ("prologue/", "ch01/day1/", "ch01/day2/", "ch01/day3/", "ch01/day4/")

CALLS = ("phone_add_message", "phone_send_player_message", "phone_offer_reply", "chapter_select_phone",
         "chapter_select_phone_reply")
CALL_RE = re.compile(r"\b(" + "|".join(CALLS) + r")\(")


# ------------------------------------------------------------------ source scanning

def _balanced(src, start):
    """Index just past the parenthesis that closes the one at src[start] (quotes respected)."""
    depth, i, q = 0, start, None
    while i < len(src):
        c = src[i]
        if q:
            if c == "\\":
                i += 2
                continue
            if c == q:
                q = None
        elif c in "\"'":
            q = c
        elif c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("unbalanced call at %d" % start)


def _calls(path):
    """[(function name, ast.Call, line, in_init_block)] for the phone calls in one .rpy file."""
    src = path.read_text(encoding="utf-8-sig")
    lines = src.split("\n")
    out = []
    for mo in CALL_RE.finditer(src):
        line_start = src.rfind("\n", 0, mo.start()) + 1
        prefix = src[line_start:mo.start()]
        if "#" in prefix or prefix.strip().startswith(("def ", "#")):
            continue
        if re.search(r"\bdef\s+$", prefix):
            continue
        end = _balanced(src, mo.end() - 1)
        try:
            call = ast.parse(src[mo.start():end], mode="eval").body
        except SyntaxError:
            continue
        line = src.count("\n", 0, mo.start()) + 1
        # Inside an `init ... python:` block (a helper run from elsewhere) or in label code?
        top = next((ln for ln in reversed(lines[:line - 1]) if ln[:1] not in ("", " ", "\t", "#")), "")
        out.append((mo.group(1), call, line, top.startswith("init")))
    return out


def _arg(call, index, name, default=None):
    for kw in call.keywords:
        if kw.arg == name:
            return kw.value
    if len(call.args) > index:
        return call.args[index]
    return default


def _const(node):
    return node.value if isinstance(node, ast.Constant) else None


def _assignments(path):
    """{name: [value expr]} for every `name = expr` / `$ name = expr` in a story file."""
    src = path.read_text(encoding="utf-8-sig")
    out = {}
    for mo in re.finditer(r"^[ \t]*(?:\$[ \t]*)?([A-Za-z_]\w*)[ \t]*=[ \t]*(?!=)", src, re.M):
        start = mo.end()
        end = src.find("\n", start)
        end = len(src) if end < 0 else end
        text = src[start:end]
        if text.rstrip().endswith(("(", "[", "{")):
            end = _balanced(src, start + len(text.rstrip()) - 1)
            text = src[start:end]
        try:
            out.setdefault(mo.group(1), []).append(ast.parse(text.strip(), mode="eval").body)
        except SyntaxError:
            pass
    return out


def _candidates(node, assigns, depth=0):
    """The text expressions a story argument can deliver (branches and assigned names opened)."""
    if node is None:
        return [ast.Constant("")]
    if depth > 4:
        return [node]
    if isinstance(node, ast.IfExp):
        return _candidates(node.body, assigns, depth + 1) + _candidates(node.orelse, assigns, depth + 1)
    if isinstance(node, ast.Name) and node.id in assigns:
        out = []
        for value in assigns[node.id]:
            out += _candidates(value, assigns, depth + 1)
        return out
    return [node]


def _dump(node):
    return ast.dump(node, annotate_fields=False)


def story_index():
    """{message id or regex: [entry]} for every text the story files can deliver."""
    index = {}
    prompts = {}
    for path in sorted(CH.rglob("*.rpy")):
        rel = path.relative_to(CH).as_posix()
        if rel.endswith("_chapter.rpy"):
            continue
        assigns = _assignments(path)
        order = PLAY_ORDER.index(rel) if rel in PLAY_ORDER else None
        for name, call, line, in_init in _calls(path):
            if name == "phone_offer_reply":
                prompt = _const(call.args[1])
                options = call.args[2]
                prompts[prompt] = {}
                for opt in options.elts:
                    o = {_const(k): v for k, v in zip(opt.keys, opt.values)}
                    oid = _const(o["id"])
                    leave = _const(o.get("leave_on_read", ast.Constant(False)))
                    prompts[prompt][oid] = dict(leave=bool(leave), followups=[])
                    if not leave:
                        ryan_id = _const(o["message_id"]) if "message_id" in o else prompt + "_ryan"
                        prompts[prompt][oid]["ryan"] = ryan_id
                        index.setdefault(ryan_id, []).append(dict(
                            thread=_const(call.args[0]), sender="player", rel=rel, line=line, order=None,
                            text=_candidates(o.get("send", o["text"]), assigns), attachment=None))
                    for n, pair in enumerate(o.get("followups", ast.List([])).elts, 1):
                        # A third item keeps an existing save id (darryn 2026-11-19).
                        mid = (_const(pair.elts[2]) if len(pair.elts) > 2
                               else "{}_followup_{:02d}".format(prompt, n))
                        prompts[prompt][oid]["followups"].append(mid)
                        index.setdefault(mid, []).append(dict(
                            thread=_const(call.args[0]), sender=_const(pair.elts[0]), rel=rel, line=line,
                            order=None, text=_candidates(pair.elts[1], assigns), attachment=None))
                continue
            if name not in ("phone_add_message", "phone_send_player_message"):
                continue
            mid = _arg(call, 99, "message_id")
            if name == "phone_send_player_message":
                thread, sender, text = _const(call.args[0]), "player", _arg(call, 1, "text")
                mid = _arg(call, 2, "message_id")
            else:
                thread, sender, text = _const(call.args[0]), _const(call.args[1]), _arg(call, 2, "text")
            if isinstance(mid, ast.Constant):
                key = mid.value
            elif (isinstance(mid, ast.Call) and isinstance(mid.func, ast.Attribute)
                  and mid.func.attr == "format" and isinstance(mid.func.value, ast.Constant)):
                key = re.compile("^" + re.sub(r"\\\{[^}]*\\\}", r"\\d+", re.escape(mid.func.value.value)) + "$")
            else:
                continue
            entry = dict(thread=thread, sender=sender, rel=rel, line=line, text=_candidates(text, assigns),
                         attachment=_candidates(_arg(call, 99, "attachment_id"), assigns),
                         order=None if in_init or order is None else (order, line))
            index.setdefault(key, []).append(entry)
    return index, prompts


def story_entries(index, mid):
    out = list(index.get(mid, ()))
    for key, entries in index.items():
        if not isinstance(key, str) and key.match(mid):
            out += entries
    return out


def seed_calls():
    """[(rel, name, ast.Call, line)] for the chapter_select_phone* calls in the Day packs."""
    out = []
    for path in sorted(CH.rglob("*_chapter.rpy")):
        for name, call, line, _init in _calls(path):
            if name.startswith("chapter_select_phone"):
                out.append((path.relative_to(CH).as_posix(), name, call, line))
    return out


# ------------------------------------------------------------------ the expected table

PROLOGUE_GROUP = ["prologue_julian_downstairs_01", "prologue_julian_downstairs_02"]
D1_GROUP = [
    "ch01_trip_group_trio_photo", "ch01_trip_group_pool_capture_01", "ch01_trip_group_late_pool_photo",
    "ch01_trip_group_late_photo_leia_react", "ch01_trip_group_late_photo_julian_reply",
    "ch01_trip_group_late_photo_leia_reply", "ch01_movie_photo_reply_ryan", "ch01_movie_photo_reply_followup_01",
    "ch01_trip_group_breakfast_warning", "ch01_trip_group_breakfast_leia_reply",
]
D2_GROUP = ["ch01_d2_julian_wake_up", "ch01_trip_group_maya_added", "ch01_trip_group_four_photo",
            "ch01_trip_group_maya_first_post"]
D2_MAYA = ["ch01_d2_maya_lunch_checkin", "ch01_d2_maya_lunch_reply_ryan", "ch01_d2_maya_lunch_reply_followup_01",
           "ch01_d2_maya_dm_01", "ch01_d2_maya_dm_02"]
D2_LEIA = ["ch01_d2_boutique_selfie", "ch01_d2_boutique_selfie_ask", "ch01_d2_boutique_selfie_reply",
           "ch01_d2_boutique_selfie_followup", "ch01_d2_boutique_selfie_stay"]
D4_GROUP_MORNING = ["ch01_d4_group_breakfast_julian", "ch01_d4_group_breakfast_maya", "ch01_d4_group_maya_police_growth",
                    "ch01_d4_group_julian_energy", "ch01_d4_group_maya_shoes"]
D4_GROUP_BOAT = ["ch01_d4_group_day5_announce", "ch01_d4_group_day5_maya", "ch01_d4_group_day5_julian_boat",
                 "ch01_d4_group_day5_maya_haunted"]
D4_HOOK = {"in": ["ch01_d4_player_hook_in", "ch01_d4_group_hook_reply_in"],
           "maybe": ["ch01_d4_player_hook_maybe", "ch01_d4_group_hook_reply_maybe"]}

# Day Five presets (keyed by the stored Day Four end route): Day Four's leia / maya / julian threads.
D4_LEIA = {
    "love": ["ch01_d4_leia_morning_text", "ch01_d4_player_text_warm", "ch01_d4_leia_photo_candid",
             "ch01_d4_leia_photo_candid_reply", "ch01_d4_leia_dinner_toast", "ch01_d4_leia_day5_love"],
    "exhibitionism": ["ch01_d4_leia_morning_text", "ch01_d4_player_text_flirt", "ch01_d4_leia_photo_pose",
                      "ch01_d4_leia_photo_pose_reply", "ch01_d4_leia_dinner_toast", "ch01_d4_leia_day5_exhib"],
    "love_repaired": ["ch01_d4_leia_morning_ntr_1", "ch01_d4_leia_morning_ntr_2", "ch01_d4_player_ntr_join",
                      "ch01_d4_leia_morning_ntr_3", "ch01_d4_leia_photo_candid", "ch01_d4_leia_photo_candid_reply",
                      "ch01_d4_leia_dinner_toast", "ch01_d4_leia_day5_ntr_repaired"],
    "ntr_unresolved": ["ch01_d4_leia_morning_ntr_1", "ch01_d4_leia_morning_ntr_2", "ch01_d4_player_ntr_later",
                       "ch01_d4_leia_morning_ntr_3", "ch01_d4_leia_photo_candid", "ch01_d4_leia_photo_candid_reply",
                       "ch01_d4_leia_dinner_toast", "ch01_d4_leia_day5_ntr_unresolved"],
    "ntr_confirmed": ["ch01_d4_leia_morning_ntr_1", "ch01_d4_leia_morning_ntr_2", "ch01_d4_player_ntr_fine",
                      "ch01_d4_leia_morning_ntr_3"],
}
D4_MAYA = {
    "love": ["ch01_d4_maya_dress_code"], "love_repaired": ["ch01_d4_maya_dress_code"],
    "ntr_unresolved": ["ch01_d4_maya_dress_code"],
    "exhibitionism": ["ch01_d4_maya_dress_code", "ch01_d4_maya_day5_exhib"],
    "ntr_confirmed": ["ch01_d4_maya_dress_code", "ch01_d4_maya_day5_ntr_confirmed"],
}
D4_JULIAN = {"ntr_confirmed": ["ch01_d4_julian_day5_ntr_confirmed"]}
D5_HOOK = {"love": "in", "exhibitionism": "in", "love_repaired": "in", "ntr_unresolved": "maybe",
           "ntr_confirmed": "maybe"}
# Day Five preset -> the Day Two end state behind it (CH01_SELECT_DAY5_PRESETS "d2").
D5_BASE = {"love": "love", "exhibitionism": "exhibitionism", "love_repaired": "ntr_confirmed",
           "ntr_unresolved": "mixed_unresolved", "ntr_confirmed": "ntr_confirmed"}

DAY2_ROUTES = ("love", "exhibitionism", "ntr_risk")
END_ROUTES = ("love", "exhibitionism", "love_repaired", "mixed_unresolved", "ntr_confirmed")
DAY5_ROUTES = ("love", "exhibitionism", "love_repaired", "ntr_unresolved", "ntr_confirmed")

# Story texts no preset seeds: other branches than the ones the presets imply.
NOT_SEEDED = {
    "ch01_trip_group_pool_capture_02": "the presets keep the default one Capture photo (ch01_pool_capture_count unset = 1)",
    "ch01_trip_group_pool_capture_03": "same: three Captures only after the longer photoshoot",
    "ch01_pool_photo_reply_ryan": "the pool reply card is only offered with three Captures",
    "ch01_pool_photo_reply_followup_01": "same",
    "ch01_d2_maya_dm_ryan": "the late DM takes its default: left on read",
    "ch01_d2_maya_dm_followup_01": "same",
    "ch01_d4_player_text_coffee": "Love/Exhibitionism morning reply: the presets pick warm / flirt",
    "ch01_d4_leia_photo_swap_reply": "no Day Five preset takes the photo-swap branch",
    "ch01_d4_player_hook_ask": "no Day Five preset stores hook_reply ask_leia",
    "ch01_d4_group_hook_reply_ask": "same",
}


def expected(day, route):
    """{thread: [message ids]} a normal playthrough has at `day`'s start on this preset."""
    threads = {"group": PROLOGUE_GROUP + D1_GROUP}
    if day == "day2":
        return threads
    base = route if day in ("day3", "day4") else D5_BASE[route]
    threads["group"] += D2_GROUP
    threads["maya"] = list(D2_MAYA)
    threads["leia"] = list(D2_LEIA)
    if day in ("day3", "day4"):
        return threads
    threads["group"] += D4_GROUP_MORNING + D4_GROUP_BOAT + D4_HOOK[D5_HOOK[route]]
    threads["leia"] += D4_LEIA[route]
    threads["maya"] += D4_MAYA[route]
    if route in D4_JULIAN:
        threads["julian"] = list(D4_JULIAN[route])
    assert base
    return threads


def presets():
    for r in DAY2_ROUTES:
        yield "day2", r
    for day in ("day3", "day4"):
        for r in END_ROUTES:
            yield day, r
    for r in DAY5_ROUTES:
        yield "day5", r


# ------------------------------------------------------------------ harness run of the presets

def run_preset(day, route):
    store = SimpleNamespace(
        phone_messages={"leia": [], "julian": [], "group": []}, phone_photos=[], phone_reply_prompts={},
        phone_reply_delivery={}, lc_phone_story_time=None, lc_phone_read_receipts={},
        phone_group_avatar_stage=None, phone_group_maya_member=False, story_flags={}, story_values={},
        owned_outfits=["casual_default"], equipped_outfit="casual_default",
        player_name="Ryan", girlfriend_name="Leia", friend_name="Julian",
    )
    banners = []
    env = dict(
        renpy=SimpleNamespace(store=store, restart_interaction=lambda: None, loadable=lambda p: False),
        store=store, persistent=SimpleNamespace(),
        player_name="Ryan", girlfriend_name="Leia", friend_name="Julian",
        set_story_flag=lambda k, v=True: store.story_flags.__setitem__(k, bool(v)),
        has_story_flag=lambda k: bool(store.story_flags.get(k)),
        set_story_value=lambda k, v: store.story_values.__setitem__(k, v),
        get_story_value=lambda k, d=None: store.story_values.get(k, d),
        has_story_value=lambda k: k in store.story_values,
        lc_review_reset=lambda: None, set_phone_unlocked=lambda v=True: None,
        set_phone_hud_enabled=lambda v=True: None, lc_feed_install=lambda: None,
        grant_story_outfit=lambda oid, equip=False: store.owned_outfits.append(oid),
        owns_outfit=lambda oid: oid in store.owned_outfits,
        phone_show_notification=lambda *a, **kw: banners.append(a),
    )
    load_blocks(["phone_store_message", "chapter_select_apply"], env)
    load(["phone_group_stage", "phone_group_members"], env)
    entry = env["chapter_select_apply"](day, route)
    return env, store, banners, entry


class SeedTextsMatchTheStory(unittest.TestCase):
    """Every seeded message is the story's message: id, thread, sender, text and attachment."""

    @classmethod
    def setUpClass(cls):
        cls.index, cls.prompts = story_index()
        cls.seeds = seed_calls()

    def test_seed_calls_are_found(self):
        self.assertGreater(len([s for s in self.seeds if s[1] == "chapter_select_phone"]), 60)

    def test_every_seeded_message_matches_a_story_delivery(self):
        problems = []
        for rel, name, call, line in self.seeds:
            if name != "chapter_select_phone":
                continue
            thread, sender, mid = (_const(a) for a in call.args[:3])
            text = _arg(call, 3, "text", ast.Constant(""))
            attachment = _arg(call, 99, "attachment_id")
            where = f"{rel}:{line} {mid}"
            entries = [e for e in story_entries(self.index, mid) if e["thread"] == thread and e["sender"] == sender]
            if not entries:
                problems.append(f"{where}: no story delivery with thread {thread!r} and sender {sender!r}")
                continue
            if not any(_dump(text) in {_dump(t) for t in e["text"]} for e in entries):
                problems.append(f"{where}: text {ast.unparse(text)} is not a text the story delivers")
            computed = all(not isinstance(a, ast.Constant) for e in entries for a in (e["attachment"] or ()))
            if attachment is not None and computed:
                # The story computes it (the pool Captures loop): PresetPhoneState checks it against
                # the story's own function.
                continue
            if attachment is not None and not any(
                    _dump(attachment) in {_dump(a) for a in (e["attachment"] or ())} for e in entries):
                problems.append(f"{where}: attachment {ast.unparse(attachment)} differs from the story")
        self.assertEqual(problems, [], "\n" + "\n".join(problems))

    def test_resolved_reply_cards_post_what_their_option_posts(self):
        problems = []
        seeded = {_const(c.args[2]) for _r, n, c, _l in self.seeds if n == "chapter_select_phone"}
        for rel, name, call, line in self.seeds:
            if name != "chapter_select_phone_reply":
                continue
            prompt, option = _const(call.args[0]), _const(call.args[1])
            spec = self.prompts.get(prompt, {}).get(option)
            if spec is None:
                problems.append(f"{rel}:{line}: {prompt} has no option {option!r} in the story")
                continue
            left = _arg(call, 2, "left_on_read")
            if spec["leave"] != (left is not None):
                problems.append(f"{rel}:{line}: {prompt}/{option} left_on_read must match the option")
            posted = ([] if spec["leave"] else [spec.get("ryan", prompt + "_ryan")]) + spec["followups"]
            missing = [m for m in posted if m not in seeded]
            if missing:
                problems.append(f"{rel}:{line}: {prompt}/{option} posts {missing} but they are not seeded")
        self.assertEqual(problems, [], "\n" + "\n".join(problems))

    def test_every_earlier_day_message_is_seeded_or_explained(self):
        seeded = set()
        for day, route in presets():
            for ids in expected(day, route).values():
                seeded.update(ids)
        story = set()
        for key, entries in self.index.items():
            if not any(e["rel"].startswith(EARLIER_DAYS) for e in entries):
                continue
            if isinstance(key, str):
                story.add(key)
            else:
                story.update(m for m in ("ch01_trip_group_pool_capture_%02d" % n for n in (1, 2, 3)) if key.match(m))
        unexplained = sorted(story - seeded - set(NOT_SEEDED))
        self.assertEqual(unexplained, [], "add these to a Day pack's phone seed or to NOT_SEEDED")
        stale = sorted(k for k in NOT_SEEDED if k in seeded or k not in story)
        self.assertEqual(stale, [], "NOT_SEEDED lists ids that are seeded or gone")


class ExpectedTableMatchesTheStory(unittest.TestCase):
    """EXPECTED (above) against the story files: thread of every id and the play order per thread."""

    @classmethod
    def setUpClass(cls):
        cls.index, _prompts = story_index()

    def test_every_expected_id_is_delivered_by_the_story_on_that_thread(self):
        problems = []
        for day, route in presets():
            for thread, ids in expected(day, route).items():
                for mid in ids:
                    if not any(e["thread"] == thread for e in story_entries(self.index, mid)):
                        problems.append(f"{day}:{route} {thread}: {mid} is not a story message of that thread")
        self.assertEqual(sorted(set(problems)), [], "\n" + "\n".join(sorted(set(problems))))

    def test_expected_order_follows_the_play_order(self):
        problems = []
        for day, route in presets():
            for thread, ids in expected(day, route).items():
                # An id delivered from several branches (ch01_d4_leia_morning_ntr_3) takes the first
                # of its call sites that comes after the previous message.
                last, last_id = (-1, -1), None
                for mid in ids:
                    sites = sorted(e["order"] for e in story_entries(self.index, mid) if e["order"])
                    if not sites:
                        continue
                    later = [s for s in sites if s > last]
                    if not later:
                        problems.append(f"{day}:{route} {thread}: {mid} plays before {last_id}")
                        continue
                    last, last_id = later[0], mid
        self.assertEqual(sorted(set(problems)), [], "\n" + "\n".join(sorted(set(problems))))


class PresetPhoneState(unittest.TestCase):
    """Every Chapter Select preset seeds the phone a normal playthrough has at that Day's start."""

    def test_every_registered_preset_is_covered(self):
        env, _store, _b, _e = run_preset("day2", "love")
        registered = [(day, rid) for day, p in env["CHAPTER_SELECT_PRESETS"].items() for rid, _l in p["routes"]]
        self.assertEqual(sorted(registered), sorted(presets()))

    def test_seeded_threads_equal_the_expected_table(self):
        for day, route in presets():
            with self.subTest(preset=f"{day}:{route}"):
                env, store, banners, entry = run_preset(day, route)
                self.assertEqual(entry, {"day2": "ch01_day2_start", "day3": "ch01_day3_start",
                                         "day4": "ch01_day4_start", "day5": "ch01_day5_start"}[day])
                got = {t: [m["id"] for m in msgs] for t, msgs in store.phone_messages.items() if msgs}
                self.assertEqual(got, expected(day, route))

    def test_everything_is_read_quiet_and_answered(self):
        for day, route in presets():
            with self.subTest(preset=f"{day}:{route}"):
                env, store, banners, _entry = run_preset(day, route)
                for thread in store.phone_messages:
                    self.assertEqual(env["phone_thread_unread_count"](thread), 0, thread)
                self.assertEqual(banners, [])
                self.assertEqual(store.phone_reply_prompts, {})
                self.assertEqual(store.phone_reply_delivery, {})
                answered = {k: v for k, v in store.story_values.items() if k.endswith("_reply") or k == "ch01_d2_maya_dm"}
                self.assertEqual(answered.get("ch01_movie_photo_reply"), "nice")
                if day != "day2":
                    self.assertEqual(answered.get("ch01_d2_maya_lunch_reply"), "alive")
                    self.assertEqual(answered.get("ch01_d2_maya_dm"), "read")
                    receipt = store.lc_phone_read_receipts["maya"]
                    self.assertEqual((receipt["prompt"], receipt["message_id"], receipt["time"]),
                                     ("ch01_d2_maya_dm", "ch01_d2_maya_dm_02", "23:52"))
                    self.assertFalse(receipt.get("unopened"))

    def test_trip_group_picture_and_maya(self):
        for day, route in presets():
            with self.subTest(preset=f"{day}:{route}"):
                env, store, _b, _e = run_preset(day, route)
                if day == "day2":
                    self.assertEqual(env["phone_group_stage"](), "trio")
                    self.assertEqual(env["phone_group_members"](), ("player", "leia", "julian"))
                else:
                    self.assertEqual(env["phone_group_stage"](), "four")
                    self.assertEqual(env["phone_group_members"](), ("player", "leia", "julian", "maya"))

    def test_attachments_are_in_photos_and_times_match_the_story_clock(self):
        env, store, _b, _e = run_preset("day5", "love")
        photos = [p["id"] for p in store.phone_photos]
        attached = ["message:" + m["id"] for t in ("group", "leia", "maya")
                    for m in store.phone_messages.get(t, ()) if m.get("attachment_id")]
        self.assertEqual(sorted(photos), sorted(attached))
        self.assertIn("message:ch01_trip_group_pool_capture_01", photos)
        self.assertIn("message:ch01_d4_leia_photo_candid", photos)
        stamps = {m["id"]: m["display_time"] for msgs in store.phone_messages.values() for m in msgs}
        self.assertEqual(stamps["ch01_d2_julian_wake_up"], "11:00")
        self.assertEqual(stamps["ch01_d2_maya_dm_01"], "23:52")
        self.assertEqual(stamps["ch01_d2_maya_dm_02"], "23:52")
        self.assertEqual(sum(1 for v in stamps.values() if v), 3)
        texts = {m["id"]: m["text"] for msgs in store.phone_messages.values() for m in msgs}
        self.assertEqual(texts["ch01_trip_group_trio_photo"], "Leia changed the group picture.")
        self.assertEqual(texts["ch01_d4_group_breakfast_maya"], "Julian does not cook. Julian supervised a chef named Teodoro.")

    def test_pool_capture_is_the_story_default(self):
        """The Capture the story's own helper sends when no pool values are stored."""
        env, store, _b, _e = run_preset("day2", "love")
        store.story_values.clear()
        load(["ch01_pool_capture_assets"], env)
        assets = env["ch01_pool_capture_assets"]()
        msg = next(m for m in store.phone_messages["group"] if m["id"] == "ch01_trip_group_pool_capture_01")
        self.assertEqual(assets, [msg["attachment_id"]])
        self.assertEqual(msg["attachment_label"], "{} pool photo {:02d}".format("Leia", 1))

    def test_route_dependent_replies(self):
        cases = {("day3", "love"): "You look incredible.", ("day3", "exhibitionism"): "Didn't know you had that in you.",
                 ("day3", "mixed_unresolved"): "Maya really did this to you?", ("day3", "ntr_confirmed"): "It's... nice.",
                 ("day5", "love_repaired"): "It's... nice."}
        for (day, route), text in cases.items():
            with self.subTest(preset=f"{day}:{route}"):
                _env, store, _b, _e = run_preset(day, route)
                sent = {m["id"]: m["text"] for m in store.phone_messages["leia"]}
                self.assertEqual(sent["ch01_d2_boutique_selfie_reply"], text)


if __name__ == "__main__":
    unittest.main()
