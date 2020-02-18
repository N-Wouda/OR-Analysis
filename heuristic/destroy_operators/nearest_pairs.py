import numpy as np
from numpy.random import RandomState

from heuristic.classes import Solution
from heuristic.functions import customers_to_remove, remove_empty_routes


@remove_empty_routes
def nearest_pairs(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Removes customers from the solution that are near each other in distance.
    # TODO verify and think a bit more about this

    Related removal in Hornstra et al. (2020).
    """
    destroyed = current.copy()
    num_customers = current.problem.num_customers

    closest = np.argmax(current.problem.inverse_distances, axis=1)
    relatedness = current.problem.inverse_distances[np.arange(num_customers),
                                                    closest]

    customers = np.argsort(relatedness)

    for idx in range(customers_to_remove(num_customers)):
        customer = customers[-idx - 1]
        destroyed.unassigned.append(customer)

        route = destroyed.find_route(customer)
        route.remove_customer(customer, destroyed.problem)

    return destroyed
