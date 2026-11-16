"""The load-time hook API (game/systems/lc_hooks.rpy), run from the real source.

Systems extend each other through named hooks instead of re-defining a function
from a later file. These tests pin the API contract: registration order,
idempotent registration, exceptions not swallowed, filters chaining a value,
and the registry staying out of save data (python_dict/python_list).
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lc_rpy_model as m  # noqa: E402
from lc_rpy_harness import load  # noqa: E402

API = ["_lc_hooks", "lc_hook_add", "lc_hook_run", "lc_hook_filter"]


class NotSaved(dict):
    """Stands in for Ren'Py's python_dict (a dict rollback/saves do not track)."""


class NotSavedList(list):
    """Stands in for Ren'Py's python_list."""


class HookApiTests(unittest.TestCase):
    def setUp(self):
        self.env = load(API, dict(python_dict=NotSaved, python_list=NotSavedList))
        self.calls = []

    def hook(self, tag):
        def fn(*args, **kw):
            self.calls.append((tag, args, kw))
        return fn

    def test_run_calls_hooks_in_registration_order_with_arguments(self):
        self.env["lc_hook_add"]("ev", self.hook("a"))
        self.env["lc_hook_add"]("ev", self.hook("b"))
        self.env["lc_hook_add"]("other", self.hook("c"))
        self.assertIsNone(self.env["lc_hook_run"]("ev", 1, x=2))
        self.assertEqual(self.calls, [("a", (1,), {"x": 2}), ("b", (1,), {"x": 2})])

    def test_run_without_hooks_does_nothing(self):
        self.assertIsNone(self.env["lc_hook_run"]("nobody_listens", 1))

    def test_adding_the_same_function_twice_registers_it_once(self):
        fn = self.hook("a")
        self.env["lc_hook_add"]("ev", fn)
        self.env["lc_hook_add"]("ev", fn)
        self.env["lc_hook_run"]("ev")
        self.assertEqual(len(self.calls), 1)

    def test_add_returns_the_function(self):
        fn = self.hook("a")
        self.assertIs(self.env["lc_hook_add"]("ev", fn), fn)

    def test_exceptions_are_not_swallowed(self):
        def boom(*args):
            raise RuntimeError("hook failed")
        self.env["lc_hook_add"]("ev", boom)
        self.env["lc_hook_add"]("ev", self.hook("after"))
        with self.assertRaises(RuntimeError):
            self.env["lc_hook_run"]("ev")
        self.assertEqual(self.calls, [])

    def test_filter_passes_the_value_through_each_hook_in_order(self):
        self.env["lc_hook_add"]("f", lambda value, n: value + [n, "first"])
        self.env["lc_hook_add"]("f", lambda value, n: value + ["second"])
        self.assertEqual(self.env["lc_hook_filter"]("f", [], 7), [7, "first", "second"])

    def test_filter_without_hooks_returns_the_value_unchanged(self):
        value = ("a", "b")
        self.assertIs(self.env["lc_hook_filter"]("nobody", value), value)

    def test_registry_is_kept_out_of_save_data(self):
        self.env["lc_hook_add"]("ev", self.hook("a"))
        self.assertIsInstance(self.env["_lc_hooks"], NotSaved)
        self.assertIsInstance(self.env["_lc_hooks"]["ev"], NotSavedList)


class HookPlacementTests(unittest.TestCase):
    def test_api_is_defined_before_any_registration_runs(self):
        defs = m.effective("def")
        api_priority = max(defs[name].priority for name in API[1:])
        registrations = [d for d in m.definitions("effect") if d.body.startswith("lc_hook_add(")]
        self.assertTrue(registrations, "no lc_hook_add registrations found")
        for d in registrations:
            self.assertGreater(d.priority, api_priority, f"{d.relpath}:{d.line} registers before the API exists")


if __name__ == "__main__":
    unittest.main()
