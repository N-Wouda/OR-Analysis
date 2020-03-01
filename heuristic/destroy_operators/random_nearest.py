from numpy.random import RandomState

from heuristic.classes import Problem, Solution
from heuristic.functions import customers_to_remove, remove_empty_routes


@remove_empty_routes
def random_nearest(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Removes customers from the solution that are near each other in distance.
    See ``customers_to_remove`` for the degree of destruction done.

    Similar to related removal in Hornstra et al. (2020).
    """
    destroyed = current.copy()

    removed_set = set()
    removed_list = list()

    def remove(candidate: int):
        removed_set.add(candidate)
        removed_list.append(candidate)

        route = destroyed.find_route(candidate)
        route.remove_customer(candidate)

    problem = Problem()

    while len(removed_set) != customers_to_remove():
        # Either chooses from the removed list, or a random customer if the
        # list is not yet populated.
        customer = rnd_state.choice(removed_list
                                    if len(removed_list) != 0
                                    else problem.num_customers)

        # Find nearest other customer that's not already removed. This should
        # be fairly fast in practice, but is at most O(n), with n the number
        # of customers.
        for other in problem.nearest_customers[customer]:
            if other not in removed_set:
                remove(other)
                break

    destroyed.unassigned = removed_list

    return destroyed
