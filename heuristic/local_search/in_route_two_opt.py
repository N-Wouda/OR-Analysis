import numpy as np

from heuristic.classes import Heap, Problem, Route, Stacks
from heuristic.constants import DEPOT


def in_route_two_opt(route: Route) -> Route:
    """
    Performs the best in-route two-opt swap, based on routing costs.

    Intra 2-opt in Hornstra et al. (2020).
    """
    problem = Problem()

    tour = np.array([DEPOT] + route.customers.to_list())

    feasible_moves = Heap()
    feasible_moves.push(route.cost(), route)

    for first in range(1, len(route)):
        for second in range(first + 1, len(route)):
            if _gain(tour, first, second) >= 0:
                continue  # this is not a better move.

            # This is a better route than the one we have currently. Of course
            # that does not mean we can find a good handling configuration as
            # well, so we attempt to create a route for this 2-opt move and skip
            # if it is infeasible.
            tour[first:second] = tour[second - 1:first - 1:-1]
            new_route = Route([], [Stacks(problem.num_stacks)])

            if new_route.attempt_append_tail(tour[1:]):
                feasible_moves.push(new_route.cost(), new_route)

    _, best_route = feasible_moves.pop()
    return best_route


def _gain(tour: np.ndarray, first: int, second: int) -> float:
    # Proposed changes.
    gain = Route.distance([tour[first - 1], tour[second - 1]])
    gain += Route.distance([tour[first], tour[second]])

    # Current situation.
    gain -= Route.distance([tour[first - 1], tour[first]])
    gain -= Route.distance([tour[second - 1], tour[second]])

    return gain
