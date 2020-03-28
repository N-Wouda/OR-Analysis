from copy import copy, deepcopy
from itertools import product

import numpy as np

from heuristic.classes import Heap, Route, Solution
from heuristic.constants import DEPOT
from heuristic.functions import remove_empty_routes, routing_costs


@remove_empty_routes
def exchange_customer(solution: Solution) -> Solution:
    """
    TODO

    References
    ----------
    - Savelsbergh, Martin W. P. 1992. "The Vehicle Routing Problem with Time
      Windows: Minimizing Route Duration." *ORSA Journal on Computing* 4 (2):
      146-154.
    """
    improvements = Heap()
    costs = routing_costs(solution)

    for idx1, route1 in enumerate(solution.routes):
        for idx2, route2 in enumerate(solution.routes[idx1 + 1:], idx1 + 1):
            iterable = product(range(len(route1)), range(len(route2)))

            for idx_cust1, idx_cust2 in iterable:
                if _gain(costs, route1, idx_cust1, route2, idx_cust2) >= 0:
                    continue

                new_route1 = deepcopy(route1)
                new_route2 = deepcopy(route2)

                customer1 = route1.customers[idx_cust1]
                customer2 = route2.customers[idx_cust2]

                new_route1.remove_customer(customer1)
                new_route2.remove_customer(customer2)

                if not new_route1.can_insert(customer2, idx_cust1):
                    continue

                if not new_route2.can_insert(customer1, idx_cust2):
                    continue

                new_route1.insert_customer(customer2, idx_cust1)
                new_route2.insert_customer(customer1, idx_cust2)

                current = route1.cost() + route2.cost()
                proposed = new_route1.cost() + new_route2.cost()

                if proposed < current:
                    improvements.push(proposed,
                                      (idx1, new_route1, idx2, new_route2))

    if len(improvements) != 0:
        _, (idx1, new_route1, idx2, new_route2) = improvements.pop()

        solution = copy(solution)

        solution.routes[idx1] = new_route1
        solution.routes[idx2] = new_route2

    return solution


def _gain(costs: np.ndarray,
          route1: Route,
          idx1: int,
          route2: Route,
          idx2: int) -> float:
    prev1 = DEPOT if idx1 == 0 else route1.customers[idx1 - 1]
    next1 = DEPOT if idx1 == len(route1) - 1 else route1.customers[idx1 + 1]

    prev2 = DEPOT if idx1 == 0 else route2.customers[idx2 - 1]
    next2 = DEPOT if idx2 == len(route2) - 1 else route2.customers[idx2 + 1]

    # Proposed changes.
    gain = Route.distance([prev1, route2.customers[idx2], next1])
    gain += Route.distance([prev2, route1.customers[idx1], next2])

    # Current situation.
    gain -= costs[route1.customers[idx1]]
    gain -= costs[route2.customers[idx2]]

    return gain
