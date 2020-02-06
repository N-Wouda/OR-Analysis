from typing import List

from .TransportPlan import TransportPlan
from .Truck import Truck


class Route:
    legs: List
    plan: TransportPlan
    truck: Truck

    def cost(self) -> float:
        assert self.plan.max_capacity_used() <= self.truck.capacity

        # TODO determine legs cost (from data?)
        return sum(self.legs) + self.plan.cost()
