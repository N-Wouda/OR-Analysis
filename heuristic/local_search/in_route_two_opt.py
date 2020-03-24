import numpy as np

from heuristic.classes import Problem, Route, Stacks
from heuristic.constants import DEPOT


def in_route_two_opt(route: Route) -> Route:
    """
    Performs the best in-route two-opt swap, based on routing costs.

    Intra 2-opt in Hornstra et al. (2020).
    """
    problem = Problem()
    dist = problem.distances

    best = np.array([DEPOT] + route.customers.to_list())
    best += 1

    for first in range(1, len(route.customers)):
        for second in range(first + 1, len(route.customers)):
            gain = dist[best[first - 1], best[second - 1]]
            gain += dist[best[first], best[second]]

            gain -= dist[best[first - 1], best[first]]
            gain -= dist[best[second - 1], best[second]]

            if gain >= 0:
                continue  # this is not a better move.

            # This is a better route than the one we have currently. Of course
            # that does not mean we can find a good handling configuration as
            # well, so we create a route for this 2-opt move first and return
            # if it is indeed better than the one we had before.
            best[first:second] = best[second - 1:first - 1:-1]
            new_route = Route([], [Stacks(problem.num_stacks)])

            for idx, customer in enumerate(best[1:] - 1):
                if not new_route.can_insert(customer, idx):
                    break  # this is an infeasible 2-opt move.

                new_route.insert_customer(customer, idx)
            else:
                if new_route.cost() < route.cost():
                    return new_route

    return route
