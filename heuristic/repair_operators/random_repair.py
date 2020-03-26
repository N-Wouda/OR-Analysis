from numpy.random import RandomState

from heuristic.classes import Solution
from heuristic.functions import create_single_customer_route


def random_repair(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Sequentially inserts a random customer from the unassigned pool in a random
    feasible location in the solution.

    Random repair in Hornstra et al. (2020).
    """
    rnd_state.shuffle(current.unassigned)

    while len(current.unassigned) != 0:
        customer = current.unassigned.pop()

        # Traverses a random permutation of the route indices - this ensures
        # we insert into a random route, if that's feasible.
        for idx_route in rnd_state.permutation(len(current.routes)):
            route = current.routes[idx_route]
            insert_idx = rnd_state.randint(len(route))

            if route.can_insert(customer, insert_idx):
                route.insert_customer(customer, insert_idx)
                break
        else:
            # There is no feasible route to insert into, so we create a new
            # route for just this customer.
            route = create_single_customer_route(customer)
            current.routes.append(route)

    return current
