from __future__ import annotations

from collections import deque
from typing import Set

from .Item import Item


class Stack:
    """
    List of items, the last item in the list is the item in the back of the
    truck.
    """
    stack: deque[Item]
    _set: Set[Item]

    def __init__(self):
        self.stack = deque()
        self._set = set()

    def place_in_back(self, item: Item):
        """
        Adds item to the stack.
        """
        self.stack.append(item)
        self._set.add(item)

    def take_item(self) -> Item:
        """
        Removes item from the back of the truck, returns this item.
        """
        item = self.stack.pop()
        self._set.remove(item)

        return item

    def place_in_front(self, item: Item):
        """
        Places the item in the front of the truck.
        For this function the associated costs and further layout of the stack
        are irrelevant.
        """
        self._set.add(item)
        self.stack.appendleft(item)

    def __contains__(self, item):
        return item in self._set

    def volume(self) -> float:
        return sum(self.stack[idx].volume
                   for idx in range(len(self.stack)))

    def length_items_to_be_moved(self) -> float:
        """
        Returns the length of items to be moved when placing an item in the
        front of the truck (Pickup items at the front are never moved). The
        costs associated with this action are computed later.
        """
        # TODO O(1) or O(log n)?
        total_length = sum(self.stack[idx].volume for idx in
                           range(len(self.stack)))

        len_pickups_in_front = 0
        idx = 0
        while self.stack[idx].destination == 0:
            len_pickups_in_front += self.stack[idx].volume
            idx += 1

        return total_length - len_pickups_in_front
