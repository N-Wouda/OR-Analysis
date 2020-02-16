from __future__ import annotations

from collections import deque
from typing import Set

from .Item import Item


class Stack:
    """
    Wrapper class for a stack of items, maintained as a deque of Items. Such
    a stack represents a single stack of a truck, from the rear (left) to the
    front (right).
    """
    stack: deque[Item]
    _set: Set[Item]

    def __init__(self):
        self.stack = deque()
        self._set = set()

    def pop_rear(self) -> Item:
        item = self.stack.popleft()
        self._set.remove(item)

        return item

    def index(self, item: Item):
        return self.stack.index(item)

    def remove_volume(self, item: Item) -> float:
        """
        Computes the (excess) volume that needs to be moved to remove the
        passed-in item.
        """
        assert item in self
        at = self.index(item)

        return sum(self.stack[idx].volume for idx in range(at))

    def insert_volume(self, at: int) -> float:
        """
        Computes the volume that needs to be moved in order to insert an item at
        the given index.
        """
        return sum(self.stack[idx].volume
                   for idx in range(min(at, len(self.stack))))

    def push_front(self, item: Item):
        """
        Places the item in the front of the truck (right).
        """
        self._set.add(item)
        self.stack.append(item)

    def push_rear(self, item: Item):
        """
        Adds item to the rear of the truck (left).
        """
        self.stack.appendleft(item)
        self._set.add(item)

    def __contains__(self, item: Item) -> bool:
        return item in self._set

    def volume(self) -> float:
        return sum(self.stack[idx].volume
                   for idx in range(len(self.stack)))
