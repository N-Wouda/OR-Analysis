from numpy.random import RandomState

from heuristic.classes import Problem, Solution
from heuristic.functions import remove_empty_routes, customers_to_remove


@remove_empty_routes
def minimum_quantity(current: Solution, rnd_state: RandomState) -> Solution:
    """
    TODO.
    """
    problem = Problem()
    destroyed = current.copy()

    # Selects the q smallest customers to remove from the solution pool, and
    # randomly shuffles the list (the customers are always the same, but the
    # order in which they are removed is not).
    # TODO make this better?
    to_remove = customers_to_remove(problem.num_customers)
    customers = problem.smallest_quantity_customers[:to_remove]
    rnd_state.shuffle(customers)

    for customer in customers:
        route = destroyed.find_route(customer)
        route.remove_customer(customer)

    destroyed.unassigned = customers.tolist()

    return destroyed
