from numpy.random import RandomState

from heuristic.classes import Solution
from heuristic.functions import customers_to_remove


def random_customers(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Removes a number of randomly selected customers from the passed-in solution.
    See ``customers_to_remove`` for the degree of destruction done.
    """
    destroyed = current.copy()
    num_customers = destroyed.problem.num_customers

    for customer in rnd_state.choice(destroyed.problem.num_customers,
                                     customers_to_remove(num_customers),
                                     replace=False):
        destroyed.unassigned.append(customer)

        route = destroyed.find_route(customer)
        route.remove_customer(customer, destroyed.problem)

    # Some routes may now be empty, after removing all their customers. This
    # clean-up ensures they are removed from the solution.
    destroyed.routes = [route for route in destroyed.routes
                        if len(route.customers) != 0]

    return destroyed
