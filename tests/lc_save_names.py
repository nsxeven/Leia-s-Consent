"""Runtime names that saves and story code depend on.

A save stores labels it can return to, store variables, story flag/value keys,
applied choice ids, delivered phone message ids and the images it shows. The
clean-up must never drop one of these; renaming any of them breaks old saves.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lc_rpy_model as m  # noqa: E402
from lc_effective_effects import effective_effects  # noqa: E402

_STORY_KEY = re.compile(
    r"\b(?:set_story_flag|set_story_value|get_story_value|has_story_flag|get_story_flag|has_story_value|clear_story_flag)"
    r"\(\s*['\"]([\w.]+)['\"]")
_CHOICE = re.compile(r"\b(?:format_choice|apply_choice)\(\s*['\"](\w+)['\"]")
_MESSAGE = re.compile(r"\bmessage_id\s*=\s*['\"]([\w.-]+)['\"]")


def save_names():
    text = "\n".join(m.read(p) for p in m.rpy_files())
    return {
        "label": {d.name for d in m.definitions("label")},
        "store": {d.name for d in m.definitions("define") + m.definitions("default")},
        "story_key": set(_STORY_KEY.findall(text)),
        "choice_id": set(_CHOICE.findall(text)) | set(effective_effects()),
        "message_id": set(_MESSAGE.findall(text)),
        "image": {d.name for d in m.definitions("image") + m.definitions("layeredimage")},
        "screen": {d.name.split("@")[0] for d in m.definitions("screen")},
    }
