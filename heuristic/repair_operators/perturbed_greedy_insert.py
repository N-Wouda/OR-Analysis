import heapq
from numpy.random import RandomState

from heuristic.classes import Route, Solution
from heuristic.functions import create_single_customer_route


def perturbed_greedy_insert(current: Solution,
                            rnd_state: RandomState) -> Solution:
    """
    Sequentially inserts each a random permutation of the unassigned customers
    into their y-th best, feasible route at a locally optimal leg of the tour.

    Perturbed sequential best insertion in Hornstra et al. (2020).
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
            y = min(3, len(feasible_routes))
            nsmallest = heapq.nsmallest(y, feasible_routes)
            rnd_state.shuffle(nsmallest)

            cost, insert_idx, route = nsmallest[0]
            cost_new = Route([customer], []).routing_cost()

            if cost_new > cost:
                route.insert_customer(customer, insert_idx)
                continue

        route = create_single_customer_route(customer)
        current.routes.append(route)

    return current
