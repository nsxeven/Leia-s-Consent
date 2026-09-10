# Core one-currency economy.
# Story and systems code should use these helpers rather than mutating money directly.

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
