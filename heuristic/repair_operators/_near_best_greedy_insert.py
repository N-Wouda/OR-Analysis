import heapq

from numpy.random import RandomState

from heuristic.classes import Route, Solution
from heuristic.constants import DEPOT
from heuristic.functions import create_single_customer_route


def _near_best_greedy_insert(max_offset: int,
                             current: Solution,
                             rnd_state: RandomState) -> Solution:
    """
    Sequentially inserts a random permutation of the unassigned customers
    into a random feasible route which is within max_offset insertion points of
    their optimal insertion point.
    """
    rnd_state.shuffle(current.unassigned)

    while len(current.unassigned) != 0:
        customer = current.unassigned.pop()
        feasible_routes = []

        for route in current.routes:
            insert_idx, cost = route.opt_insert(customer)

            if route.can_insert(customer, insert_idx):
                heapq.heappush(feasible_routes, (cost, insert_idx, route))

        if len(feasible_routes) != 0:
            num_smallest = min(max_offset, len(feasible_routes))
            near_best = heapq.nsmallest(num_smallest, feasible_routes)

            cost, insert_idx, route = near_best[rnd_state.choice(num_smallest)]
            cost_new = Route.distance([DEPOT, customer, DEPOT])

            if cost_new > cost:
                route.insert_customer(customer, insert_idx)
                continue

        route = create_single_customer_route(customer)
        current.routes.append(route)

    return current
