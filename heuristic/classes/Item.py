from __future__ import annotations


class Item:
    volume: float
    destination: int

    def __init__(self, volume: float, destination: int):
        """
        Creates an item with a volume and (customer) destination. A pickup
        will have destination 0 (i.e., the depot).
        """
        self.volume = volume
        self.destination = destination

    def __eq__(self, other: Item) -> bool:
        return isinstance(other, Item) \
               and self.volume == other.volume \
               and self.destination == other.destination

    def __hash__(self) -> int:
        return hash((self.destination, self.volume))

    def is_pickup(self) -> bool:
        return self.destination == 0

    def is_delivery(self) -> bool:
        return not self.is_pickup()

    def __str__(self):
        assert self.is_pickup() or self.is_delivery()

        if self.is_pickup():
            return "p" + str(self.destination)

        return "d" + str(self.destination)
