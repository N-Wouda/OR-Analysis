from __future__ import annotations

from collections import deque
from typing import Deque, List, Set

from ..constants import DEPOT
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
    _volume: float

    def __init__(self):
        self.stack = deque()
        self._set = set()
        self._volume = 0.

    def __contains__(self, item: Item) -> bool:
        """
        Tests if this stack contains the passed-in item. O(1).
        """
        return item in self._set

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

    def push_effective_front(self, item: Item):
        """
        Places the item in the front of the truck (right). If there are pickups
        in the front already, places them behind them. # TODO O(n)?.
        """
        if len(self.stack) == 0:
            self.push_front(item)

            return
        
        if self.stack[-1].destination != DEPOT:
            self.push_front(item)
        else:
            stack = list(reversed(self.stack))
            idx = next(
                (stack.index(x) for x in stack if x.destination != DEPOT), -2)
            stack.insert(idx, item)

            self.stack = deque(reversed(stack))
            self._set.add(item)
            self._volume += item.volume

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
    def from_strings(cls, items: List[str]) -> Stack:
        """
        (Re)constructs a Stack instance from the string representation of a
        solution output.
        """
        problem = Problem()
        stack = Stack()

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
