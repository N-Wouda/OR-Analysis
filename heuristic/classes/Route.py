from typing import List

from .LoadingPlan import LoadingPlan
from .Problem import Problem


class Route:
    customers: List[int]  # customers visited, in order (indices)
    plan: LoadingPlan  # loading plan detailing the mutations at each customer

    def cost(self, problem: Problem) -> float:
        """
        Computes the cost (objective) value of this route.
        """
        return self._distance_cost(problem) \
               + self.plan.cost(self.customers, problem)

    def _distance_cost(self, problem: Problem) -> float:
        from_depot = problem.distances[0, self.customers[0]]
        to_depot = problem.distances[self.customers[-1], 0]

        tour = sum(problem.distances[first, second]
                   for first, second in zip(self.customers, self.customers[1:]))

        return from_depot + to_depot + tour
