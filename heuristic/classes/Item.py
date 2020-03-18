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
        # NW: we don't really need a type and volume comparison, and this is a
        # bit faster.
        return self.origin == other.origin \
               and self.destination == other.destination

    def __hash__(self) -> int:
        # NW: we don't really need to hash the volume, as that is assumed not
        # to change during execution.
        return hash((self.origin, self.destination))

    @property
    def customer(self) -> int:
        return self.origin if self.is_pickup() else self.destination

    def is_pickup(self) -> bool:
        return self.destination == DEPOT

    def is_delivery(self) -> bool:
        return self.origin == DEPOT

    def __str__(self):
        item_type = "p" if self.is_pickup() else "d"
        return item_type + str(self.customer + 1)

    def __repr__(self):
        return f"Item({self}, {self.volume:.2f})"
