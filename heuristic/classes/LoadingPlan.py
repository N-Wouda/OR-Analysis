from typing import List

from .Problem import Problem
from .Stacks import Stacks


class LoadingPlan:
    snapshots: List[Stacks]

    def cost(self, customers: List[int], problem: Problem) -> float:
        # Customers does not include the start depot, and the final return.
        # Both such stops incur zero cost, so we can avoid it below.
        assert len(customers) == len(self.snapshots) - 2

        return sum(snapshot.cost(customer, problem)
                   for customer, snapshot in zip(customers, self.snapshots[1:]))

    def max_capacity_used(self) -> float:
        return max(snapshot.used_capacity() for snapshot in self.snapshots)
