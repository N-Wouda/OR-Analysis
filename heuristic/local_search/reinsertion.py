from numpy.random import RandomState

from heuristic.classes import Solution, Problem
from heuristic.repair_operators import greedy_insert


def reinsertion(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Attempts to find an improvement in the current solution by removing a
    customer and reinserting this customer at the optimal location. If an
    improvement is found the new solution is returned.
    """
    problem = Problem()

    for customer in range(problem.num_customers):
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
