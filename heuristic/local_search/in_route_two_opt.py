from collections import namedtuple

from numpy.random import RandomState

from heuristic.classes import Problem, Solution
from heuristic.constants import DEPOT

best_swap = namedtuple("best_swap", ["cost", "idx_first", "idx_second"])


def in_route_two_opt(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Performs the best in-route two-opt swap, based on routing costs.

    Intra 2-opt in Hornstra et al. (2020).
    """
    problem = Problem()

    for route in current.routes:
        customers = route.customers
        best = best_swap(route.routing_cost(), 0, 0)

        for idx_first, first in enumerate(customers):
            for idx_second, second in enumerate(customers[idx_first + 1:],
                                                idx_first + 1):
                after_first = customers[idx_first + 1] \
                    if idx_first + 1 < len(customers) else DEPOT
                after_second = customers[idx_second + 1] \
                    if idx_second + 1 < len(customers) else DEPOT

                # These are the costs of the proposed edges.
                change = problem.distances[first + 1, second + 1]
                change += problem.distances[after_first + 1, after_second + 1]

                # And these will be removed (the current connecting edges).
                change -= problem.distances[first + 1, after_first + 1]
                change -= problem.distances[second + 1, after_second + 1]

                if route.routing_cost() + change < best.cost:
                    best = best_swap(route.routing_cost() + change,
                                     idx_first,
                                     idx_second)

        if best.idx_first == best.idx_second == 0:
            continue  # no-op.

        # Collect the customers between the customers that are to be swapped.
        # These customers need to be removed, and reinserted in reverse order
        # (this is the 2-opt "swap" operation).
        sub_route = customers[best.idx_first:best.idx_second + 1]

        for customer in sub_route:
            route.remove_customer(customer)

        for idx, customer in enumerate(reversed(sub_route), best.idx_first):
            route.insert_customer(customer, idx)

    return current
