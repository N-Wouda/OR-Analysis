import numpy as np

from heuristic.classes import Problem, Solution, Stacks


def customer_handling_costs(sol: Solution) -> np.ndarray:
    """
    Computes handling costs for each customer. This is an approximation: only
    the handling costs *at* the customer are computed, any costs made at other
    legs of the tour are not considered. O(|customers|).
    """
    problem = Problem()
    costs = np.zeros(problem.num_customers)

    for route in sol.routes:
        for idx, customer in enumerate(route.customers):
            costs[customer] = Stacks.cost(customer, *route.plan[idx:idx + 2])

    return costs
