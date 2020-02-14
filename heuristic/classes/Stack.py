from __future__ import annotations
from collections import deque
from .Item import Item


class Stack:
    """
    List of items, the last item in the list is the item in the back of the
    truck.
    """
    stack: deque[Item]

    def place_in_back(self, item):
        """
        Adds item to the stack.
        """
        self.stack.append(item)

    def take_item(self) -> Item:
        """
        Removes item from the back of the truck, returns this item.
        """
        return self.stack.pop()

    def place_in_front(self, item):
        """
        Places the item in the front of the truck.
        For this function the associated costs and further layout of the stack
        are irrelevant.
        """
        self.stack.appendleft(item)

    def length_items_to_be_moved(self) -> float:
        """
        Returns the length of items to be moved when placing an item in the
        front of the truck (Pickup items at the front are never moved). The
        costs associated with this action are computed later.
        """
        total_length = sum(self.stack[idx].volume for idx in
                           range(len(self.stack)))

        len_pickups_in_front = 0
        idx = 0
        while self.stack[idx].customer == 0:
            len_pickups_in_front += self.stack[idx].volume
            idx += 1

        return total_length - len_pickups_in_front
