import numpy as np

from heuristic.classes import Problem, Solution, Stacks


def handling_costs(solution: Solution) -> np.ndarray:
    """
    Computes handling costs for each customer. This is an approximation: only
    the handling costs *at* the customer are computed, any costs made at other
    legs of the tour are not considered. O(|customers|).

    Note: this is a lower bound on the actual handling costs, as those are
    rather hard to compute. Some experimentation suggests it is e.g. not
    worthwhile to also count the costs incurred due to the delivery and pickup
    items at other legs of the route.
    """
    problem = Problem()
    costs = np.zeros(problem.num_customers)

    for route in solution.routes:
        for idx, customer in enumerate(route):
            before, after = route.plan[idx], route.plan[idx + 1]

            # This is the handling cost for just this customer, as an
            # approximation to the total handling costs.
            costs[customer] += Stacks.cost(customer, before, after)

    return costs
