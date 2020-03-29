from copy import deepcopy
from typing import Set

from numpy.random import Generator

from heuristic.classes import Problem, SetList, Solution
from heuristic.functions import customers_to_remove, remove_empty_routes


@remove_empty_routes
def cross_route(current: Solution, rnd_state: Generator) -> Solution:
    """
    Selects two customers that are nearest to each other and their neighbours
    and removes them from the solution. See ``customers_to_remove`` for the
    degree of destruction done.

    Similar to cross route removal in Hornstra et al. (2020).
    """
    problem = Problem()
    destroyed = deepcopy(current)

    customers = set(range(problem.num_customers))
    removed = SetList()

    while len(removed) < customers_to_remove():
        candidate = rnd_state.choice(tuple(customers))

        route_candidate = destroyed.find_route(candidate)
        _remove(destroyed, candidate, removed, customers)

        # Find the nearest customer that is not yet removed and in a different
        # route, and remove it and its neighbours as well.
        for other in problem.nearest_customers[candidate]:
            if other not in route_candidate and other not in removed:
                _remove(destroyed, other, removed, customers)
                break

    destroyed.unassigned = removed.to_list()

    return destroyed


def _remove(destroyed: Solution,
            customer: int,
            removed: SetList,
            customers: Set):
    route = destroyed.find_route(customer)
    idx = route.customers.index(customer)

    # Selects the customer and the direct neighbours before and after the
    # customer, should those exist.
    selected = route.customers[max(idx - 1, 0):min(idx + 2, len(route))]

    for candidate in selected:
        removed.append(candidate)
        route.remove_customer(candidate)
        customers.remove(candidate)
