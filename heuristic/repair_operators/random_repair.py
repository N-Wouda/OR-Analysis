from numpy.random import RandomState
import numpy as np

from heuristic.classes import Solution
from heuristic.functions import create_single_customer_route


def random_repair(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Sequentially inserts a random customer from the unassigned pool in a random
    feasible location in the Solution.

    Random repair in Hornstra et al. (2020).

    Tries inserting in one location per route, if it is non feasible for every
    route, creates a new route.
    """
    rnd_state.shuffle(current.unassigned)

    while len(current.unassigned) != 0:
        customer = current.unassigned.pop()

        indices_routes = np.arange(len(current.routes))
        rnd_state.shuffle(indices_routes)

        inserted = False

        for idx_route in indices_routes:
            route = current.routes[idx_route]

            insert_idx = rnd_state.randint(
                len(current.routes[idx_route].customers))

            if route.can_insert(customer, insert_idx, current.problem):
                route.insert_customer(customer, insert_idx, current.problem)
                inserted = True
                break

        if not inserted:
            route = create_single_customer_route(customer, current.problem)
            current.routes.append(route)

    return current
