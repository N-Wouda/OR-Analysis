from __future__ import annotations


class Item:
    volume: float
    customer: int

    @classmethod
    def create(cls, volume, customer) -> Item:
        """
        Creates an item with a set volume and destination (customer). A pickup
        will have destination 0 (a.k.a. the depot).
        """
        item = cls()
        item.volume = volume
        item.customer = customer

        return item

    def get_volume(self):
        return self.volume

    def get_customer(self):
        return self.customer
