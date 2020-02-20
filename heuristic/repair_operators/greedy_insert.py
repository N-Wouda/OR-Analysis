from numpy.random import RandomState

from heuristic.classes import Route, Solution
from heuristic.functions import create_single_customer_route


def greedy_insert(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Sequentially inserts each a random permutation of the unassigned customers
    into their best, feasible route at a locally optimal leg of the tour.

    Sequential best insertion in Hornstra et al. (2020).
    """
    rnd_state.shuffle(current.unassigned)

    while len(current.unassigned) != 0:
        customer = current.unassigned.pop()
        feasible_routes = []

        for route in current.routes:
            insert_idx, cost = route.opt_insert(customer)

            if route.can_insert(customer, insert_idx):
                feasible_routes.append((cost, insert_idx, route))

        if len(feasible_routes) != 0:
            cost, insert_idx, route = min(feasible_routes)
            cost_new = Route([customer], []).routing_cost()

            if cost_new > cost:
                route.insert_customer(customer, insert_idx)
                continue

        route = create_single_customer_route(customer)
        current.routes.append(route)

        for route in current.routes:
            route.sort_start()

    return current
