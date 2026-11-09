"""Story motion must respect the SCREEN SHAKE setting."""
from pathlib import Path
import re
import unittest

GAME = Path(__file__).resolve().parents[1] / "game"
STORY = [GAME / "chapters" / "prologue.rpy"]
STORY += sorted((GAME / "chapters" / "ch01").glob("ch01_*.rpy"))
STORY = [p for p in STORY if not re.search(r"day[345]", p.name)]
RAW = re.compile(r"\b(?:hpunch|vpunch)\b", re.IGNORECASE)


class ShakeConsistencyTests(unittest.TestCase):
    def test_no_raw_punch_in_prologue_day_one_or_day_two(self):
        offenders = []
        for path in STORY:
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                code = line.split("#", 1)[0]
                if RAW.search(code):
                    offenders.append(f"{path.relative_to(GAME)}:{line_number}: {code.strip()}")
        self.assertFalse(offenders, "Raw punches bypass lc_fx:\n" + "\n".join(offenders))
