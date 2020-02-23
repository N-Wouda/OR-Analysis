import numpy as np
from numpy.random import RandomState
from scipy.stats import geom

from heuristic.classes import Problem, Solution
from heuristic.constants import MIN_QUANTITY_SAMPLE_SHAPE
from heuristic.functions import customers_to_remove, remove_empty_routes


@remove_empty_routes
def minimum_quantity(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Removes customers based on quantity (demand + pickup). Randomly selects q
    customers based on a distribution over these quantities, favouring smaller
    over larger quantity customers.

    Similar - but not equivalent - to minimum quantity removal in Hornstra et
    al. (2020).
    """
    destroyed = current.copy()

    for customer in _customers(rnd_state):
        destroyed.unassigned.append(customer)

        route = destroyed.find_route(customer)
        route.remove_customer(customer)

    return destroyed


def _customers(rnd_state: RandomState) -> np.ndarray:
    """
    Determines a probability distribution over the customers with smallest
    quantity (sum of pickup and delivery). The distribution is geometric over
    the customers, from smallest to largest quantity, and then normalised to
    one. This ensures in general the smallest quantities are selected, *but*
    there is some randomness involved.
    """
    problem = Problem()

    to_remove = customers_to_remove(problem.num_customers)
    probabilities = geom.pmf(np.arange(1, problem.num_customers + 1),
                             MIN_QUANTITY_SAMPLE_SHAPE)

    return rnd_state.choice(problem.smallest_quantity_customers,
                            to_remove,
                            replace=False,
                            p=probabilities / np.sum(probabilities))
