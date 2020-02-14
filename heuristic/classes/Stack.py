from __future__ import annotations
from collections import deque
from .Item import Item


class Stack:
    """
    List of items, the last item in the list is the item in the back of the
    truck.
    """
    _stack: deque[Item]
    max_length: float
    #  misschien niet nodig hier omdat alle stacks dezelfde capacity hebben

    @classmethod
    def create(cls, size) -> Stack:
        stack = cls()
        stack.max_length = size
        return stack

    def place_in_back(self, item):
        """
        Adds item to the stack.
        """
        self._stack.append(item)

    def take_item(self) -> Item:
        """
        Removes item from the back of the truck, returns this item.
        """
        item = self._stack[-1]
        del self._stack[-1]

        return item

    def place_in_front(self, item):
        """
        Places the item in the front of the truck.
        For this function the associated costs and further layout of the stack
        are irrelevant.
        """
        self._stack.appendleft(item)

    def length_items_to_be_moved(self) -> float:
        """
        Returns the length of items to be moved when placing an item in the
        front of the truck (Pickup items at the front are never moved). The
        costs associated with this action are computed later.
        """
        # kan dit in één loop ipv 2?
        total_length = sum(self._stack[idx].get_volume() for idx in
                           range(len(self._stack)))

        len_pickups_in_front = 0
        idx = 0
        while self._stack[idx].get_customer() == 0:
            len_pickups_in_front += self._stack[idx].get_volume()
            idx += 1

        return total_length - len_pickups_in_front
