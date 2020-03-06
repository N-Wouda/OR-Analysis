from __future__ import annotations

from dataclasses import dataclass
from typing import List

from heuristic.classes import Problem
import numpy as np
import bisect


@dataclass
class Block:
    """
    A block of customers. This groups several customers together, that are
    moved around by the MDP (as an approximation to the optimal handling
    policy, which would move each customer individually).
    """
    customers: List[int]

    def max_capacity_used(self) -> float:
        """
        Worst-case capacity used by this block, as the maximum of each
        customer's demand and pickup item. This scenario might not occur in
        practice, but we should be able to handle it for each Block to remain
        interchangeable.
        """
        return Block._max_capacity_used(self.customers)

    def split(self) -> List[Block]:
        """
        Splits this block into two blocks of approximately equal capacity
        used.
        """
        def key(idx: int) -> float:
            # This returns the difference (positive) between both blocks, if
            # the current block were split at this idx.
            left = Block._max_capacity_used(self.customers[:idx])
            right = Block._max_capacity_used(self.customers[idx:])

            return abs(left - right)

        split_idx = min(range(len(self.customers)), key=key)

        return [Block(self.customers[:split_idx]),
                Block(self.customers[split_idx:])]

    @staticmethod
    def _max_capacity_used(customers) -> float:
        problem = Problem()

        return sum(max(problem.demands[customer].volume,
                       problem.pickups[customer].volume)
                   for customer in customers)

    def __iter__(self):
        yield from self.customers

    def __str__(self):
        return str(self.customers)

    def __repr__(self):
        return f"Block({self})"
