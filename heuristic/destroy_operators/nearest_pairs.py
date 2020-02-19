import numpy as np
from numpy.random import RandomState

from heuristic.classes import Solution
from heuristic.functions import customers_to_remove, remove_empty_routes


@remove_empty_routes
def nearest_pairs(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Removes customers from the solution that are near each other in distance.

    Related removal in Hornstra et al. (2020).
    """
    destroyed = current.copy()

    to_remove = customers_to_remove(destroyed.problem.num_customers)
    customer = rnd_state.randint(destroyed.problem.num_customers)

    removed_set = {customer}
    removed_list = [customer]
    _remove(customer, destroyed)

    while len(removed_set) != to_remove:
        customer = rnd_state.choice(removed_list)

        for other in destroyed.problem.nearest_customers[customer]:
            if other not in removed_set:
                removed_set.add(other)
                removed_list.append(other)
                _remove(other, destroyed)

                break

    destroyed.unassigned = removed_list

    return destroyed


def _remove(customer: int, destroyed: Solution):
    route = destroyed.find_route(customer)
    route.remove_customer(customer, destroyed.problem)
