import numpy as np
from numpy.random import RandomState

from heuristic.classes import Solution
from heuristic.functions import random_selection, remove_empty_routes


@remove_empty_routes
def _worst(costs: np.ndarray, current: Solution,
           rnd_state: RandomState) -> Solution:
    """
    Randomly removes the worst customers based on the passed-in costs array.
    The random distribution is skewed to favour worst-cost customers.

    Internal - should not be exposed outside this module.
    """
    destroyed = current.copy()

    # First we sort the costs to obtain the customers by increasing cost. We
    # then randomly select customers, favouring worst customers.
    customers = np.argsort(costs)
    customers = customers[-random_selection(rnd_state)]

    for customer in customers:
        destroyed.unassigned.append(customer)

        route = destroyed.find_route(customer)
        route.remove_customer(customer)

    return destroyed
