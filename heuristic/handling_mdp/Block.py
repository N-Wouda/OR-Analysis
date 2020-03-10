from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from heuristic.classes import Problem


@dataclass(eq=True, unsafe_hash=True, init=False)
class Block:
    """
    A block of customers. This groups several customers together, that are
    moved around by the MDP (as an approximation to the optimal handling
    policy, which would move each customer individually).
    """
    customers: Tuple[int]

    def __init__(self, customers):
        self.customers = tuple(customers)

    def max_capacity_used(self) -> float:
        """
        Worst-case capacity used by this block, as the maximum of each
        customer's demand and pickup item. This scenario might not occur in
        practice, but we should be able to handle it for each Block to remain
        interchangeable.
        """
        problem = Problem()

        return sum(max(problem.demands[customer].volume,
                       problem.pickups[customer].volume)
                   for customer in self.customers)

    def __iter__(self):
        yield from self.customers

    def __len__(self) -> int:
        return len(self.customers)

    def __str__(self):
        return str(self.customers)

    def __repr__(self):
        return f"Block({self})"
