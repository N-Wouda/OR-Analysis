from ..classes import Solution
from numpy.random import RandomState


def random_removal(current: Solution,
                   random_state: RandomState,
                   q: int) -> Solution:
    """
    Copies the old solution, randomly places q customers in the unassigned list
    and removes them from their routes.
    """
    destroyed = current.copy()

    for idx in random_state.choice(destroyed.problem.num_customers,
                                   q,
                                   replace=False):

        destroyed.unassigned.append(idx)

        for route_number in range(len(destroyed.routes)):
            destroyed.routes[route_number].customers.remove(idx)

    return destroyed
