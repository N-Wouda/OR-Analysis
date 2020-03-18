from __future__ import annotations

from typing import Callable, List, Optional

from .Item import Item
from .Problem import Problem
from .Stack import Stack


class Stacks:

    __slots__ = ['stacks']

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

    @staticmethod
    def cost(customer: int,
             before: Stacks,
             after: Stacks,
             problem: Optional[Problem] = None) -> float:
        """
        Determines the cost of the mutations made between the before and after
        ``Stacks``. O(|customers|), for the customers on the route to which
        these stacks belong.
        """
        if problem is None:  # problem might be passed-in for testing.
            problem = Problem()

        # We count the total volume moved. This includes the customer demand
        # item, which is not an additional operation. We subtract this here.
        volume = -problem.demands[customer].volume
        volume += sum(Stack.moved_volume(before[idx_stack], after[idx_stack])
                      for idx_stack in range(problem.num_stacks))

        assert volume >= 0.
        return problem.handling_cost * volume

    def is_feasible(self) -> bool:
        """
        Determines if this loading plan is feasible, that is, all stack
        volumes respect the capacity constraints.
        """
        problem = Problem()

        return all(stack.volume() <= problem.stack_capacity
                   for stack in self.stacks)

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
        return f"Stacks({self})"
