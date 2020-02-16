from __future__ import annotations

from typing import Callable, List

from .Item import Item
from .Stack import Stack
from .Problem import Problem


class Stacks:
    _stacks: List[Stack]

    def __init__(self, num_stacks: int):
        self._stacks = [Stack() for _ in range(num_stacks)]

    @property
    def num_stacks(self) -> int:
        return len(self._stacks)

    def cost(self, customer: int, problem: Problem) -> float:
        # Pick-up cost (item goes to depot)
        item = Item(problem.pickups[customer], 0)
        stack = self.find_stack(item)

        # TODO Policy?
        cost = stack.insert_volume(0)

        # Delivery cost (item goes to customer)
        item = Item(problem.demands[customer], customer)
        stack = self.find_stack(item)

        return problem.handling_cost * (cost + stack.remove_volume(item))

    def smallest_stack(self) -> Stack:
        return self._first_stack(min)

    def largest_stack(self) -> Stack:
        return self._first_stack(max)

    def used_capacity(self) -> float:
        return sum(stack.volume() for stack in self._stacks)

    def find_stack(self, item: Item) -> Stack:
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
