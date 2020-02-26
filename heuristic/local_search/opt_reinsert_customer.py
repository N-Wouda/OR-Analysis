from numpy.random import RandomState
import numpy as np

from heuristic.classes import Solution, Problem
from heuristic.repair_operators import greedy_insert


def opt_reinsert_customer(current: Solution, rnd_state: RandomState) \
        -> Solution:
    """
    Attempts to find an improvement in the current solution by removing a
    customer and reinserting this customer at the optimal location. If an
    improvement is found the new solution is returned.
    """
    problem = Problem()

    customers = np.arange(problem.num_customers)
    rnd_state.shuffle(customers)

    for customer in customers:
        destroyed = current.copy()

        route = destroyed.find_route(customer)
        route.remove_customer(customer)

        destroyed.unassigned.append(customer)

        destroyed.routes = [route for route in destroyed.routes
                            if len(route.customers) != 0]

        destroyed = greedy_insert(destroyed, rnd_state)

        if destroyed.objective() < current.objective():
            return destroyed

    return current
