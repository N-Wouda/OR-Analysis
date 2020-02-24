import numpy as np
from numpy.random import RandomState

from heuristic.classes import Problem, Solution
from heuristic.functions import customers_to_remove, remove_empty_routes


@remove_empty_routes
def _worst(costs: np.ndarray, current: Solution,
           rnd_state: RandomState) -> Solution:
    """
    Removes the worst customers based on the passed-in costs array. TODO.

    Internal - should not be exposed outside this module.
    """
    problem = Problem()
    destroyed = current.copy()

    to_remove = -customers_to_remove(problem.num_customers)
    customers = np.argsort(costs)[-to_remove:]

    # TODO some randomness
    for customer in customers:
        destroyed.unassigned.append(customer)

        route = destroyed.find_route(customer)
        route.remove_customer(customer)

    return destroyed
