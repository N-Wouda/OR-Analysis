from __future__ import annotations

import copy
from typing import Callable, List, Union

from .Item import Item
from .Problem import Problem
from .Stack import Stack


class Stacks:
    stacks: List[Stack]

    def __init__(self, num_stacks: int):
        self.stacks = [Stack() for _ in range(num_stacks)]

    def __len__(self):
        return len(self.stacks)

    def __iter__(self):
        yield from self.stacks

    def __getitem__(self, idx: int):
        return self.stacks[idx]

    def copy(self) -> Stacks:
        return copy.deepcopy(self)

    @staticmethod
    def cost(customer: int, before: Stacks, after: Stacks) -> float:
        """
        Determines the cost of the mutations made between the before and after
        ``Stacks``. This is in O(n), where n is the number of items in a stack.
        """
        problem = Problem()

        delivery = problem.demands[customer]
        pickup = problem.pickups[customer]

        d_stack_idx = before.find_stack_index(delivery)
        p_stack_idx = after.find_stack_index(pickup)

        d_volume = before[d_stack_idx].remove_volume(delivery)
        p_volume = after[p_stack_idx].remove_volume(pickup)

        if d_stack_idx != p_stack_idx:
            # The delivery and pickup items are stored in different stacks. We
            # pay for both delivery removal, and pickup insertion.
            return problem.handling_cost * (d_volume + p_volume)
        else:
            # But now we have some synergy: those items removed to access the
            # delivery item do not need to be removed *again* - only any excess
            # volume must. This implies we only pay for the maximum volume
            # actually removed from the stack.
            return problem.handling_cost * max(d_volume, p_volume)

    def shortest_stack(self) -> Stack:
        """
        Returns the shortest stack, that is, the stack that has the smallest
        capacity in use. O(1).
        """
        return self._first_stack(min)

    def longest_stack(self) -> Stack:
        """
        Returns the shortest stack, that is, the stack that has the largest
        capacity in use. O(1).
        """
        return self._first_stack(max)

    def used_capacity(self) -> float:
        """
        Total volume used by all stacks. O(1).
        """
        return sum(stack.volume() for stack in self.stacks)

    def find_stack(self, item: Item) -> Stack:
        """
        Finds the stack the given item is stored in. Raises a LookupError when
        the item is not in any stacks. O(1).
        """
        return self._find_stack(item, False)

    def find_stack_index(self, item: Item) -> int:
        """
        Finds the stack index the given item is stored in. Raises a LookupError
        when the item is not in any stacks. O(1).
        """
        return self._find_stack(item, True)

    def _first_stack(self, criterion: Callable[..., Stack]) -> Stack:
        return criterion(self.stacks, key=lambda stack: stack.volume())

    def _find_stack(self, item: Item, return_idx: bool) -> Union[Stack, int]:
        for idx, stack in enumerate(self.stacks):
            if item in stack:
                return idx if return_idx else stack

        raise LookupError(f"Item {item} not in any stacks.")
