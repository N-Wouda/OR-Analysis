from __future__ import annotations

from heuristic.constants import DEPOT


class Item:

    __slots__ = ['volume', 'origin', 'destination']

    volume: float
    origin: int
    destination: int

    def __init__(self, volume: float, origin: int, destination: int):
        """
        Creates an item with a volume, origin and destination. A pickup item
        will have destination DEPOT. A delivery item will have origin DEPOT.
        """
        self.volume = volume
        self.origin = origin
        self.destination = destination

    def __eq__(self, other) -> bool:
        # NW: we don't really need a type comparison, and this is a bit faster.
        return self.volume == other.volume \
               and self.origin == other.origin \
               and self.destination == other.destination

    def __hash__(self) -> int:
        return hash((self.volume, self.origin, self.destination))

    @property
    def customer(self) -> int:
        assert self.is_pickup() or self.is_delivery()
        return self.origin if self.is_pickup() else self.destination

    def is_pickup(self) -> bool:
        return self.destination == DEPOT

    def is_delivery(self) -> bool:
        return self.origin == DEPOT

    def __str__(self):
        assert self.is_pickup() or self.is_delivery()

        if self.is_pickup():
            # Pick-up item, so this came from a customer.
            return "p" + str(self.origin + 1)

        # Delivery item, so this is going to a customer.
        return "d" + str(self.destination + 1)

    def __repr__(self):
        return f"Item({self}, {self.volume:.2f})"
