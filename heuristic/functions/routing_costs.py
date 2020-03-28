import numpy as np

from heuristic.classes import Problem, Route, Solution
from heuristic.constants import DEPOT


def routing_costs(sol: Solution) -> np.ndarray:
    """
    Computes routing costs for each customer, as the cost made currently for
    having a customer in a route, against the alternative of not having said
    customer in the route: e.g., for customer [2] this compares the hypothetical
    route [1] -> [2] -> [3] with the alternative of [1] -> [3]. The difference
    in cost is the customer's routing cost. O(|customers|).
    """
    problem = Problem()
    costs = np.zeros(problem.num_customers)

    for route in sol.routes:
        for idx, customer in enumerate(route):
            costs[customer] = _customer_routing_cost(route, customer, idx)

    return costs


def _customer_routing_cost(route: Route, customer: int, idx: int) -> float:
    customers = route.customers
    problem = Problem()

    assert 0 <= idx < len(customers)
    assert customer in route

    # There is just one customer, which, once removed, would result in a cost
    # of zero. Hence the cost for this single customer is just the route cost.
    if len(customers) == 1:
        return route.routing_cost()

    if idx == 0:
        cost = problem.short_distances[DEPOT, customer, customers[1]]
        cost -= problem.distances[DEPOT + 1, customers[1] + 1]
        return cost

    if idx == len(route) - 1:
        cost = problem.short_distances[customers[-2], customer, DEPOT]
        cost -= problem.distances[customers[-2] + 1, DEPOT + 1]
        return cost

    cost = problem.short_distances[customers[idx - 1], customer, customers[idx + 1]]
    cost -= problem.distances[customers[idx - 1] + 1, customers[idx + 1] + 1]
    return cost
