# Economy - the one in-game currency
#
# Purpose: Owns earning, checking and spending money (store.money, default in game/defaults.rpy);
#   money never goes below zero. Prices and purchases live in systems/wardrobe_logic.rpy.
#
# Public API (call these from scenes/screens):
#   earn_money(amount, reason=None)           add a non-negative amount; returns the new balance
#   can_afford(amount) -> bool                True when the player has at least amount
#   spend_money(amount, reason=None) -> bool  spend if affordable; True on success
#
# Example:
#   "Buy the black mini for her." if can_afford(get_outfit("boutique_cutout_mini")["cost"]):
#
# Depends on: game/defaults.rpy (money)
# Hooks: none
# Load order: default (init 0)
# Docs: docs/ARCHITECTURE.md   Tests: tests/test_shop_coming_soon.py

init python:

    def earn_money(amount, reason=None):
        """Add non-negative currency to the current playthrough."""
        amount = int(amount)
        if amount < 0:
            raise ValueError("earn_money() requires a non-negative amount")

        renpy.store.money += amount
        renpy.store.last_money_change = amount
        renpy.store.last_money_reason = reason or "Income"
        return renpy.store.money


    def can_afford(amount):
        """Return True when the player has enough currency for amount."""
        amount = int(amount)
        if amount < 0:
            return False
        return renpy.store.money >= amount


    def spend_money(amount, reason=None):
        """Spend currency if affordable. Money can never fall below zero."""
        amount = int(amount)
        if amount < 0:
            raise ValueError("spend_money() requires a non-negative amount")

        if not can_afford(amount):
            return False

        renpy.store.money -= amount
        renpy.store.last_money_change = -amount
        renpy.store.last_money_reason = reason or "Purchase"
        return True
