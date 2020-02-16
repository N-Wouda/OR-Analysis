from __future__ import annotations

from heuristic.constants import DEPOT


class Item:
    volume: float
    customer: int
    destination: int

    def __init__(self, volume: float, customer: int, destination: int):
        """
        Creates a customer item with a volume and destination. A pickup item
        will have destination DEPOT. Customer is assumed to be an index - this
        will be offset in the string representation.
        """
        self.volume = volume
        self.customer = customer
        self.destination = destination

    def __eq__(self, other: Item) -> bool:
        return isinstance(other, Item) \
               and self.volume == other.volume \
               and self.destination == other.destination

    def __hash__(self) -> int:
        return hash((self.destination, self.volume))

    def is_pickup(self) -> bool:
        return self.destination == DEPOT

    def is_delivery(self) -> bool:
        return not self.is_pickup()

    def __str__(self):
        assert self.is_pickup() or self.is_delivery()

        if self.is_pickup():
            return "p" + str(self.customer + 1)

        return "d" + str(self.customer + 1)
