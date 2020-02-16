from typing import List

from .Problem import Problem
from .Stacks import Stacks


class LoadingPlan:
    snapshots: List[Stacks]

    def __init__(self, snapshots: List[Stacks]):
        self.snapshots = snapshots

    def cost(self, customers: List[int], problem: Problem) -> float:
        assert len(customers) + 1 == len(self.snapshots)

        cost = 0.

        for idx, customer in enumerate(customers):
            before = self.snapshots[idx]
            after = self.snapshots[idx + 1]

            cost += Stacks.cost(customer, problem, before, after)

        return cost

    def max_capacity_used(self) -> float:
        return max(snapshot.used_capacity() for snapshot in self.snapshots)
