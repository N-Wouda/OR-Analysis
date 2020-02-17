from numpy.random import RandomState

from heuristic.classes import Solution
from heuristic.functions import customers_to_remove


def random_customer_removal(current: Solution,
                            random_state: RandomState) -> Solution:
    """
    Removes a number of randomly selected customers from the passed-in solution.
    See ``customers_to_remove`` for the degree of destruction done.
    """
    destroyed = current.copy()
    num_customers = destroyed.problem.num_customers

    for customer in random_state.choice(destroyed.problem.num_customers,
                                        customers_to_remove(num_customers),
                                        replace=False):
        destroyed.unassigned.append(customer)

        for route in destroyed.routes:
            if customer in route:
                route.remove_customer(customer, destroyed.problem)
            if not route.customers:
                # remove route if empty
                destroyed.routes.remove(route)

    return destroyed
