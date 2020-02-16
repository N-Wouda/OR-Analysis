from __future__ import annotations

from typing import Callable, List

from .Item import Item
from .Stack import Stack


class Stacks:
    _stacks: List[Stack]

    def __init__(self, num_stacks: int):
        self._stacks = [Stack() for _ in range(num_stacks)]

    @property
    def num_stacks(self) -> int:
        return len(self._stacks)

    def smallest_stack(self) -> Stack:
        return self._first_stack(min)

    def largest_stack(self) -> Stack:
        return self._first_stack(max)

    def find(self, item: Item) -> Stack:
        """
        Finds the stack the given item is stored in. Raises a ValueError when
        the item is not in any stacks.
        """
        for stack in self._stacks:
            if item in stack:
                return stack

        raise ValueError(f"Item {item} not in any stacks.")

    def _first_stack(self, criterion: Callable[..., Stack]) -> Stack:
        return criterion(self._stacks, key=lambda stack: stack.volume())
