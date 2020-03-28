import numpy as np
from numpy.random import RandomState

from heuristic.classes import Heap, Problem, Solution
from heuristic.constants import DEPOT
from heuristic.functions import create_single_customer_route


def _near_best_insert(nearness: int,
                      current: Solution,
                      rnd_state: RandomState) -> Solution:
    """
    Sequentially inserts a random permutation of the unassigned customers
    into a near-best feasible route. The distance is controlled by the nearness
    parameter: the feasible route is within nearness steps from the best
    insertion point.

    Note: nearness == 1 implies a full greedy insert.
    """
    rnd_state.shuffle(current.unassigned)
    problem = Problem()

    while len(current.unassigned) != 0:
        customer = current.unassigned.pop()
        feasible_routes = Heap()

        for route in current.routes:
            insert_idx, cost = route.opt_insert(customer)

            if route.can_insert(customer, insert_idx):
                feasible_routes.push(cost, (insert_idx, route))

        if len(feasible_routes) != 0:
            num_smallest = min(nearness, len(feasible_routes))
            routes = feasible_routes.nsmallest(num_smallest)

            cost, (insert_idx, route) = routes[rnd_state.choice(num_smallest)]
            cost_new = problem.short_distances[DEPOT, customer, DEPOT]

            if cost_new > cost:
                route.insert_customer(customer, insert_idx)
                continue

        route = create_single_customer_route(customer)
        current.routes.append(route)

    return current
