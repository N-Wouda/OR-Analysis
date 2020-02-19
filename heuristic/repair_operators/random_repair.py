from numpy.random import RandomState

from heuristic.classes import Solution
from heuristic.functions import create_single_customer_route


def random_repair(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Sequentially inserts a random customer from the unassigned pool in a random
    feasible location in the Solution.

    Random repair in Hornstra et al. (2020).
    """
    rnd_state.shuffle(current.unassigned)

    while len(current.unassigned) != 0:
        customer = current.unassigned.pop()

        while True:
            idx_route = rnd_state.randint(len(current.routes) + 1)

            if idx_route < len(current.routes):
                route = current.routes[idx_route]
                insert_idx = rnd_state.randint(len(route.customers))

                if route.can_insert(customer, insert_idx, current.problem):
                    route.insert_customer(customer, insert_idx, current.problem)

                    return current

            else:
                route = create_single_customer_route(customer, current.problem)
                current.routes.append(route)

                return current
