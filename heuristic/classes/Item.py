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

    def is_pickup(self) -> bool:
        return self.destination == 0

    def is_delivery(self) -> bool:
        return not self.is_pickup()

    def __str__(self):
        assert self.is_pickup() or self.is_delivery()

        if self.is_pickup():
            return "p" + str(self.destination)

        return "d" + str(self.destination)
