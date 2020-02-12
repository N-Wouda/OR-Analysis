from typing import List

from .LoadingPlan import LoadingPlan


class Route:
    legs: List
    plan: LoadingPlan

    def cost(self) -> float:
        # TODO determine legs cost (from data?)
        return sum(self.legs) + self.plan.cost()
