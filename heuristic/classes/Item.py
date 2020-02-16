from __future__ import annotations

from heuristic.constants import DEPOT


class Item:
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

    def __eq__(self, other: Item) -> bool:
        return isinstance(other, Item) \
               and self.volume == other.volume \
               and self.origin == other.origin \
               and self.destination == other.destination

    def __hash__(self) -> int:
        return hash((self.volume, self.origin, self.destination))

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
