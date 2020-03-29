from copy import deepcopy

from numpy.random import Generator

from heuristic.classes import Problem, Solution
from heuristic.functions import customers_to_remove, remove_empty_routes


@remove_empty_routes
def random_customers(current: Solution, rnd_state: Generator) -> Solution:
    """
    Removes a number of randomly selected customers from the passed-in solution.
    See ``customers_to_remove`` for the degree of destruction done.

    Random removal in Hornstra et al. (2020).
    """
    destroyed = deepcopy(current)

    for customer in rnd_state.choice(Problem().num_customers,
                                     customers_to_remove(),
                                     replace=False):
        destroyed.unassigned.append(customer)

        route = destroyed.find_route(customer)
        route.remove_customer(customer)

    return destroyed
