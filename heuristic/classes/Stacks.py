from __future__ import annotations

import pickle
from typing import Callable, List, Optional

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
             problem: Optional[Problem] = None) -> float:
        """
        Determines the cost of the mutations made between the before and after
        ``Stacks``. O(|customers|), for the customers on the route to which
        these stacks belong.
        """
        if problem is None:  # problem might be passed-in for testing.
            problem = Problem()

        volume = 0.

        for idx_stack in range(problem.num_stacks):
            # For each stack, we look from the front to the back and compare
            # if anything has changed. If it has, that implies all subsequent
            # items have been moved, and we can add the total cost of such an
            # action. Only removals are counted - insertions are not, as those
            # must have been removed from some other stack (we do not want to
            # count twice).
            it_before = reversed(before[idx_stack])
            it_after = reversed(after[idx_stack])

            # We reason from the front to the rear, and determine the volume
            # cost for the first index that is different between the before and
            # after stack.
            for (idx, b_item), a_item in zip(enumerate(it_before, 1), it_after):
                idx = len(before[idx_stack]) - idx

                if b_item != a_item:
                    # This implies all items up to this point must have been
                    # moved out of the truck, which is exactly the volume that
                    # must be moved to insert an item at this index.
                    volume += before[idx_stack].insert_volume(idx + 1)
                    break
            else:
                if len(before[idx_stack]) > len(after[idx_stack]):
                    # This implies some items have been moved out of the stack,
                    # and we should count those.
                    num_moved = len(before[idx_stack]) - len(after[idx_stack])
                    volume += before[idx_stack].insert_volume(num_moved)

        # Above we count the total volume moved, but this includes the customer
        # demand item, which is not an additional operation. We compensate for
        # this here.
        volume -= problem.demands[customer].volume
        assert volume >= 0.

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
        return f"Stacks({self})"
