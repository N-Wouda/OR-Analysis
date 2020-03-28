from copy import copy, deepcopy

import numpy as np

from heuristic.classes import Heap, Route, Solution
from heuristic.constants import DEPOT
from heuristic.functions import remove_empty_routes, routing_costs


@remove_empty_routes
def relocate_customer(solution: Solution) -> Solution:
    """
    Performs the best customer relocation move, based on routing costs. Of all
    such moves, the best is performed and the updated solution is returned.
    O(n^2), where n is the number of customers.

    Similar to reinsertion in Hornstra et al. (2020).

    References
    ----------
    - Savelsbergh, Martin W. P. 1992. "The Vehicle Routing Problem with Time
      Windows: Minimizing Route Duration." *ORSA Journal on Computing* 4 (2):
      146-154.
    """
    improvements = Heap()
    costs = routing_costs(solution)

    for idx_route, curr_route in enumerate(solution.routes):
        for customer in curr_route:
            for route in solution.routes[idx_route:]:
                for idx in range(len(route) + 1):
                    gain = _gain(costs, route, idx, customer)

                    if gain >= 0 or not route.can_insert(customer, idx):
                        # This is either infeasible, or not an improving move.
                        continue

                    # The following performs the proposed move on a copy of the
                    # two routes involved. If the move is an improvement, it is
                    # added to the pool of improving moves.
                    old_route = deepcopy(curr_route)
                    new_route = deepcopy(route)

                    old_route.remove_customer(customer)
                    new_route.insert_customer(customer, idx)

                    current = route.cost() + curr_route.cost()
                    proposed = old_route.cost() + new_route.cost()

                    if proposed < current:
                        improvements.push(proposed, (customer, idx, route))

    if len(improvements) != 0:
        _, (customer, insert_idx, next_route) = improvements.pop()

        solution = copy(solution)
        route = solution.find_route(customer)

        if route is next_route and route.customers.index(customer) < insert_idx:
            # We re-insert into the same route, and the insert location will
            # shift once we remove the customer. This accounts for that.
            insert_idx -= 1

        route.remove_customer(customer)
        next_route.insert_customer(customer, insert_idx)

    return solution


def _gain(costs: np.ndarray, route: Route, idx: int, customer: int) -> float:
    pred = DEPOT if idx == 0 else route.customers[idx - 1]
    succ = DEPOT if idx == len(route) else route.customers[idx]

    return Route.distance([pred, customer, succ]) - costs[customer]
