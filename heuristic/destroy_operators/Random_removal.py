from ..classes import Solution
from ..functions import customers_to_remove

from numpy.random import RandomState


def random_removal(current: Solution, random_state: RandomState) -> Solution:
    """
    Copies the old solution, randomly places q customers in the unassigned list
    and removes them from the solution.
    """
    destroyed = current.copy()
    number_to_remove = customers_to_remove(current.problem)

    for customer in random_state.choice(destroyed.problem.num_customers,
                                        number_to_remove,
                                        replace=False):
        destroyed.unassigned.append(customer)
        customer_demand = current.problem.demands[customer]

        for route_number in range(len(destroyed.routes)):
            destroyed.routes[route_number].\
                remove_customer(customer, customer_demand)

    return destroyed
