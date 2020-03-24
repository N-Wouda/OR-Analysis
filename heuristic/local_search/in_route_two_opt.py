import numpy as np

from heuristic.classes import Heap, Problem, Route, Stacks
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

    feasible_routes = Heap()
    feasible_routes.push(route.cost(), route)

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
            # well, so we attempt to create a route for this 2-opt move and skip
            # if it is infeasible.
            best[first:second] = best[second - 1:first - 1:-1]
            new_route = Route([], [Stacks(problem.num_stacks)])

            for idx, customer in enumerate(best[1:] - 1):
                if not new_route.can_insert(customer, idx):
                    break  # this is an infeasible 2-opt move.

                new_route.insert_customer(customer, idx)
            else:
                # Feasible 2-opt move, so we store this new route for evaluation
                # below.
                feasible_routes.push(new_route.cost(), new_route)

    _, best_route = feasible_routes.pop()
    return best_route
