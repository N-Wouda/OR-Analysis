from __future__ import annotations

import pickle
from typing import Callable, List

from .Item import Item
from .Problem import Problem
from .Stack import Stack


class Stacks:
    stacks: List[Stack]

    def __init__(self, num_stacks: int):
        self.stacks = [Stack(idx) for idx in range(num_stacks)]

    def __len__(self):
        return len(self.stacks)

    def __iter__(self):
        yield from self.stacks

    def __getitem__(self, idx: int):
        return self.stacks[idx]

    def __setitem__(self, idx: int, stack: Stack):
        self.stacks[idx] = stack

    def copy(self) -> Stacks:
        return pickle.loads(pickle.dumps(self, pickle.HIGHEST_PROTOCOL))

    @staticmethod
    def cost(customer: int,
             before: Stacks,
             after: Stacks,
             problem: Problem = Problem()) -> float:
        """
        Determines the cost of the mutations made between the before and after
        ``Stacks``. TODO document this beast, complexity estimate.
        """
        volume = 0.
        # print()
        # print(before, customer + 1)
        # print(after, customer + 1)
        for idx_stack in range(problem.num_stacks):
            # print(before[idx_stack].stack)
            # print(after[idx_stack].stack)
            # print(volume)

            iter_before = reversed(before[idx_stack].stack)
            iter_after = reversed(after[idx_stack].stack)

            for (idx, b_item), a_item in zip(enumerate(iter_before, 1),
                                             iter_after):
                idx = len(before[idx_stack]) - idx

                if b_item != a_item:
                    if b_item.customer == customer and b_item.is_delivery():
                        volume += before[idx_stack].insert_volume(idx)
                        break

                    if a_item.customer == customer and a_item.is_pickup():
                        volume += before[idx_stack].insert_volume(idx)
                        break

                    volume += before[idx_stack].insert_volume(idx + 1)
                    break

            if len(before[idx_stack]) > len(after[idx_stack]):
                diff = len(before[idx_stack]) - len(after[idx_stack])
                volume += before[idx_stack].insert_volume(diff)

            # print(volume)

        # TODO customer item
        return problem.handling_cost * volume

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
        for idx, stack in enumerate(self.stacks):
            if item in stack:
                return stack

        raise LookupError(f"Item {item} not in any stacks.")

    def _first_stack(self, criterion: Callable[..., Stack]) -> Stack:
        return criterion(self.stacks, key=lambda stack: stack.volume())

    def __str__(self):
        return ";".join(str(stack) for stack in self.stacks)

    def __repr__(self):
        return f"Stacks({str(self)})"
