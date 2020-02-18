from numpy.random import RandomState

from heuristic.classes import Solution


def random_route(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Randomly removes a single route from the current solution. This runs in time
    O(n), where n is the number of customers.

    Similar to route removal in Hornstra et al. (2020).
    """
    destroyed = current.copy()

    idx_route = rnd_state.randint(len(destroyed.routes))
    destroyed.unassigned.extend(destroyed.routes[idx_route].customers)

    del destroyed.routes[idx_route]

    return destroyed
