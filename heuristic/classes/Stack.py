from __future__ import annotations

from collections import deque
from typing import Deque, List, Set

from .Item import Item
from .Problem import Problem


class Stack:
    """
    Wrapper class for a stack of items, maintained as a deque of Items. Such
    a stack represents a single stack of a truck, from the rear (left) to the
    front (right).
    """
    stack: Deque[Item]
    _set: Set[Item]

    _index: int
    _volume: float

    def __init__(self, index: int):
        self.stack = deque()
        self._set = set()

        self._index = index
        self._volume = 0.

    def __contains__(self, item: Item) -> bool:
        """
        Tests if this stack contains the passed-in item. O(1).
        """
        return item in self._set

    @property
    def index(self):
        """
        Returns this stack's index in the truck.
        """
        return self._index

    def insert_volume(self, at: int) -> float:
        """
        Computes the volume that needs to be moved in order to insert an item at
        the given index. Does not actually change the stack lay-out. O(n), where
        n is the number of stack items.
        """
        return sum(self.stack[idx].volume
                   for idx in range(min(at, len(self.stack))))

    def remove_volume(self, item: Item) -> float:
        """
        Computes the (excess) volume that needs to be moved to remove the
        passed-in item. Does not actually change the stack lay-out. O(n), where
        n is the number of stack items.
        """
        assert item in self
        at = self.stack.index(item)

        return sum(self.stack[idx].volume for idx in range(at))

    def push_front(self, item: Item):
        """
        Places the item in the front of the truck (right). O(1).
        """
        self.stack.append(item)
        self._set.add(item)
        self._volume += item.volume

    def push_front_demands(self, item: Item):
        """
        Places an item just before the most-near-the-front demand item. This
        is useful to e.g. insert pickup items, as those are then never again
        unloaded (except at the depot).
        """
        self._set.add(item)
        self._volume += item.volume

        # Find the index of the last demand item, and insert the pickup item
        # just in front of it, so it never needs to be moved again.
        # TODO maybe check that we are not inserting items before pickups
        #  taken later in the tour (as those would incur handling costs).
        demand_idx = next((idx for idx, item in enumerate(reversed(self.stack))
                           if item.is_delivery()), len(self.stack))

        self.stack.insert(len(self.stack) - demand_idx, item)

    def push_rear(self, item: Item):
        """
        Adds item to the rear of the truck (left). O(1).
        """
        self.stack.appendleft(item)
        self._set.add(item)
        self._volume += item.volume

    def remove(self, item: Item):
        """
        Removes the passed-in item from the stack. O(n), where n is the number
        of items in the stack.
        """
        self.stack.remove(item)
        self._set.remove(item)
        self._volume -= item.volume

    def volume(self) -> float:
        """
        Returns the currently used volume by the items in this stack. O(1).
        """
        return self._volume

    @classmethod
    def from_strings(cls, idx: int, items: List[str]) -> Stack:
        """
        (Re)constructs a Stack instance from the string representation of a
        solution output.
        """
        problem = Problem()
        stack = Stack(idx)

        for str_item in items:
            if not str_item:
                continue

            typ, cust = str_item[0], str_item[1:]
            assert typ in {"d", "p"}

            customer = int(cust) - 1

            if typ == "d":
                stack.push_rear(problem.demands[customer])
            else:
                stack.push_rear(problem.pickups[customer])

        return stack

    def __str__(self):
        """
        Prints a comma-separated representation of this stack's contents, from
        front (first item) to rear (last). O(n), where n is the number of stack
        items.
        """
        return ",".join(str(item) for item in reversed(self.stack))
