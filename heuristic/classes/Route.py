from typing import List

from .LoadingPlan import LoadingPlan
from .Problem import Problem


class Route:
    customers: List[int]  # customers visited, in order (indices)
    plan: LoadingPlan  # loading plan detailing the mutations at each customer

    def __init__(self, customers: List[int], plan: LoadingPlan):
        self.customers = customers
        self.plan = plan

    def cost(self, problem: Problem) -> float:
        """
        Computes the cost (objective) value of this route.
        """
        return self._distance_cost(problem) \
               + self.plan.cost(self.customers, problem)

    def _distance_cost(self, problem: Problem) -> float:
        # +1 everywhere, since the first row/column is depot
        from_depot = problem.distances[0, self.customers[0] + 1]
        to_depot = problem.distances[self.customers[-1] + 1, 0]

        tour = sum(problem.distances[first + 1, second + 1]
                   for first, second in zip(self.customers, self.customers[1:]))

        return from_depot + to_depot + tour
