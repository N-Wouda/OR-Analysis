from __future__ import annotations

from collections import deque
from copy import copy
from functools import partial
from itertools import islice
from typing import Deque, Set

from .Item import Item


class Stack:
    """
    Wrapper class for a stack of items, maintained as a deque of Items. Such
    a stack represents a single stack of a truck, from the rear (left) to the
    front (right).
    """

    __slots__ = ['stack', '_set', '_index', '_volume']

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

    def __deepcopy__(self, memodict={}):
        new = Stack(self.index)

        # We don't need deep copies of these items, as the *items* themselves
        # never change. Just a shallow copy of their containers suffices.
        new.stack = copy(self.stack)
        new._set = copy(self._set)
        new._volume = copy(self._volume)

        return new

    def __iter__(self):
        yield from self.stack

    def __reversed__(self):
        yield from reversed(self.stack)

    def __getitem__(self, idx: int):
        return self.stack[idx]

    def __len__(self):
        return len(self.stack)

    @property
    def index(self):
        """
        Returns this stack's index in the truck.
        """
        return self._index

    @staticmethod
    def moved_volume(before: Stack, after: Stack) -> float:
        """
        Computes the total volume that has been moved to go from the before
        stack to the after stack. For each stack, we look from the front to the
        rear and compare if anything has changed. If it has, that implies all
        subsequent  items have been moved, and we can return the total volume of
        such an action. Only removals are counted - insertions are not, as those
        must have been removed from some other stack (we do not want to count
        twice).
        """
        it_before = reversed(before)
        it_after = reversed(after)

        for (idx, b_item), a_item in zip(enumerate(it_before, 1), it_after):
            idx = len(before) - idx

            if b_item != a_item:
                # This implies all items up to this point must have been
                # moved out of the truck, which is exactly the volume that
                # must be moved to insert an item at this index.
                return before.insert_volume(idx + 1)
        else:
            if len(before) > len(after):
                # This implies some items have been moved out of the stack,
                # and we should count those.
                return before.insert_volume(len(before) - len(after))

        return 0.

    def deliveries_in_stack(self) -> int:
        """
        Number of deliverable items in this stack.
        """
        return len([item for item in self.stack if item.is_delivery()])

    def pickups_in_stack(self) -> int:
        """
        Number of pickup items in this stack.
        """
        return len(self.stack) - self.deliveries_in_stack()

    def insert_volume(self, at: int) -> float:
        """
        Computes the volume that needs to be moved in order to insert an item at
        the given index. Does not actually change the stack lay-out. O(n), where
        n is the number of stack items.
        """
        return sum(item.volume for item in islice(self.stack, at))

    def remove_volume(self, item: Item) -> float:
        """
        Computes the (excess) volume that needs to be moved to remove the
        passed-in item. Does not actually change the stack lay-out. O(n), where
        n is the number of stack items.
        """
        assert item in self
        return self.insert_volume(self.stack.index(item))

    def push_front(self, item: Item):
        """
        Places the item in the front of the truck (right). O(1).
        """
        self._append(self.stack.append, item)

    def push_rear(self, item: Item):
        """
        Adds item to the rear of the truck (left). O(1).
        """
        self._append(self.stack.appendleft, item)

    def push(self, idx: int, item: Item):
        """
        Generalised push, pushes an item at index idx (from the rear).
        """
        self._append(partial(self.stack.insert, idx), item)

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

    def _append(self, func, item: Item):
        func(item)
        self._set.add(item)
        self._volume += item.volume

    def __str__(self):
        """
        Prints a comma-separated representation of this stack's contents, from
        front (first item) to rear (last). O(n), where n is the number of stack
        items.
        """
        # TODO this might not be correct for the output file. Look into it once
        #  we have the output check with dr. Bakir.
        return ",".join(str(item) for item in reversed(self.stack))
