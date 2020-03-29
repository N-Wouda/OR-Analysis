from copy import deepcopy

from numpy.random import Generator

from heuristic.classes import Problem, SetList, Solution
from heuristic.functions import customers_to_remove, remove_empty_routes


@remove_empty_routes
def random_nearest(current: Solution, rnd_state: Generator) -> Solution:
    """
    Removes customers from the solution that are near each other in distance.
    See ``customers_to_remove`` for the degree of destruction done.

    Similar to related removal in Hornstra et al. (2020).
    """
    destroyed = deepcopy(current)
    problem = Problem()

    removed = SetList()

    while len(removed) != customers_to_remove():
        # Either chooses from the removed list, or a random customer if the
        # list is not yet populated.
        customer = rnd_state.choice(removed
                                    if len(removed) != 0
                                    else problem.num_customers)

        # Find nearest other customer that's not already removed. This should
        # be fairly fast in practice, but is at most O(n), with n the number
        # of customers.
        for other in problem.nearest_customers[customer]:
            if other not in removed:
                removed.append(other)

                route = destroyed.find_route(other)
                route.remove_customer(other)
                break

    destroyed.unassigned = removed.to_list()

    return destroyed
