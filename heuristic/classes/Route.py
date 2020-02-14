from typing import List

from .LoadingPlan import LoadingPlan
from .Problem import Problem


class Route:
    legs: List  # customers visited, in order (indices)
    plan: LoadingPlan  # loading plan detailing the mutations at each customer

    customers_visited = List
    customers_destroyed = List

    def cost(self, problem: Problem) -> float:
        """
        Computes the cost (objective) value of this route.
        """
        return self._distance_cost(problem) + self.plan.cost(problem)

    def _distance_cost(self, problem: Problem) -> float:
        from_depot = problem.distances[0, self.legs[0]]
        to_depot = problem.distances[self.legs[-1], 0]

        return from_depot + to_depot + sum(problem.distances[first, second]
                                           for first, second
                                           in zip(self.legs, self.legs[1:]))
