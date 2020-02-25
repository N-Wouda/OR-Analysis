import numpy as np

from heuristic.classes import Problem, Route, Solution
from heuristic.constants import DEPOT


def customer_routing_costs(sol: Solution) -> np.ndarray:
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
        for idx, customer in enumerate(route.customers):
            costs[customer] = _customer_route_cost(route, customer, idx)

    return costs


def _customer_route_cost(route: Route, customer: int, idx: int) -> float:
    assert 0 <= idx < len(route.customers)
    customers = route.customers

    # There is just one customer, which, once removed, would result in a cost
    # of zero. Hence the cost for this single customer is just the route cost.
    if len(customers) == 1:
        return route.routing_cost()

    if idx == 0:
        cost = _leg_cost(DEPOT, customer, customers[1])
        cost -= _leg_cost(DEPOT, customers[1])
    elif idx == len(route.customers) - 1:
        cost = _leg_cost(customers[-2], customer, DEPOT)
        cost -= _leg_cost(customers[-2], DEPOT)
    else:
        cost = _leg_cost(customers[idx - 1], customer, customers[idx + 1])
        cost -= _leg_cost(customers[idx - 1], customers[idx + 1])

    return cost


def _leg_cost(*customers: int) -> float:
    customers = np.array(customers) + 1
    return Problem().distances[np.roll(customers, 1), customers].sum()
