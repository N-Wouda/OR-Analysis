from typing import List

from .LoadingPlan import LoadingPlan
from .Truck import Truck


class Route:
    legs: List
    plan: LoadingPlan
    truck: Truck

    def cost(self) -> float:
        assert self.plan.max_capacity_used() <= self.truck.capacity

        # TODO determine legs cost (from data?)
        return sum(self.legs) + self.plan.cost()
