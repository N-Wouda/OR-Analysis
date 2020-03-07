from numpy.random import RandomState

from heuristic.classes import Problem, Solution
from heuristic.functions import random_selection, remove_empty_routes


@remove_empty_routes
def minimum_quantity(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Removes customers based on quantity (demand + pickup). Randomly selects q
    customers based on a distribution over these quantities, favouring smaller
    over larger quantity customers.

    Similar - but not equivalent - to minimum quantity removal in Hornstra et
    al. (2020).
    """
    problem = Problem()
    destroyed = current.copy()

    indices = random_selection(rnd_state)
    customers = problem.smallest_quantity_customers[indices]

    for customer in customers:
        destroyed.unassigned.append(customer)

        route = destroyed.find_route(customer)
        route.remove_customer(customer)

    return destroyed
