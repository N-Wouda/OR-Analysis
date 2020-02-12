from typing import List

from .Problem import Problem
from .Stacks import Stacks


class LoadingPlan:
    snapshots: List[Stacks]  # a capacity plan for each leg of the tour

    def cost(self, problem: Problem) -> float:
        pass  # TODO

    def max_capacity_used(self) -> int:
        pass  # TODO
