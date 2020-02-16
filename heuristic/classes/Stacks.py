from __future__ import annotations

from typing import Callable, List

from heuristic.constants import DEPOT
from .Item import Item
from .Problem import Problem
from .Stack import Stack


class Stacks:
    _stacks: List[Stack]

    def __init__(self, num_stacks: int):
        self._stacks = [Stack() for _ in range(num_stacks)]

    def __len__(self):
        return len(self._stacks)

    def __iter__(self):
        yield from self._stacks

    @staticmethod
    def cost(customer: int,
             problem: Problem,
             before: Stacks,
             after: Stacks) -> float:
        """
        Determines the cost of the mutations made between the before and after
        ``Stacks``. This is in O(|num_stacks| * n), where n is the number of
        items in a stack.
        """
        delivery = Item(problem.demands[customer], customer, customer)
        pickup = Item(problem.pickups[customer], customer, DEPOT)

        volume = before.find_stack(delivery).remove_volume(delivery)
        volume += after.find_stack(pickup).remove_volume(pickup)

        return problem.handling_cost * volume

    def shortest_stack(self) -> Stack:
        """
        Returns the shortest stack, that is, the stack that has the smallest
        capacity in use. O(|num_stacks|).
        """
        return self._first_stack(min)

    def longest_stack(self) -> Stack:
        """
        Returns the shortest stack, that is, the stack that has the largest
        capacity in use. O(|num_stacks|).
        """
        return self._first_stack(max)

    def used_capacity(self) -> float:
        """
        Total volume used by all stacks. O(|num_stacks|).
        """
        return sum(stack.volume() for stack in self._stacks)

    def find_stack(self, item: Item) -> Stack:
        """
        Finds the stack the given item is stored in. Raises a ValueError when
        the item is not in any stacks. O(|num_stacks|).
        """
        for stack in self._stacks:
            if item in stack:
                return stack

        raise ValueError(f"Item {item} not in any stacks.")

    def _first_stack(self, criterion: Callable[..., Stack]) -> Stack:
        return criterion(self._stacks, key=lambda stack: stack.volume())
