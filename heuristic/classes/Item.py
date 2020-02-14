from __future__ import annotations


class Item:
    volume: float
    customer: int

    def __init__(self, volume: float, customer: int):
        """
        Creates an item with a set volume and destination (customer). A pickup
        will have destination 0 (a.k.a. the depot).
        """
        self.volume = volume
        self.customer = customer
