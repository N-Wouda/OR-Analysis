from numpy.random import RandomState

from heuristic.classes import Solution
from heuristic.functions import customers_to_remove


def random_routes(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Randomly removes a routes from the current solution. See
    ``customers_to_remove`` for the degree of destruction done - at least this
    many customers are removed, but likely more since whole routes are deleted.

    Similar to route removal in Hornstra et al. (2020).
    """
    destroyed = current.copy()
    to_remove = customers_to_remove(destroyed.problem.num_customers)

    while len(destroyed.unassigned) < to_remove:
        idx_route = rnd_state.randint(len(destroyed.routes))
        destroyed.unassigned.extend(destroyed.routes[idx_route].customers)

        del destroyed.routes[idx_route]

    return destroyed
