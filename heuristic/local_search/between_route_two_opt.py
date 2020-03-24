from copy import deepcopy
from typing import Tuple

from heuristic.classes import Problem, Route, Solution


def between_route_two_opt(solution: Solution) -> Solution:
    """
    Performs the best between-route two-opt swap, based on routing costs.

    Inter 2-opt in Hornstra et al. (2020).
    """
    problem = Problem()
    dist = problem.distances

    # TODO https://imada.sdu.dk/~marco/Teaching/Fall2008/DM87/Slides/dm87-lec19-2x2.pdf
    for idx1, route1 in enumerate(solution.routes):
        for idx2, route2 in enumerate(solution.routes[idx1 + 1:], idx1 + 1):
            # k-opt moves are somewhat opaque. Draw an example route, including
            # directed edges, to understand what's happening here.
            for idx_first in range(1, len(route1.customers)):
                for idx_second in range(1, len(route2.customers)):
                    gain = dist[route1.customers[idx_first - 1] + 1,
                                route2.customers[idx_second - 1] + 1]

                    gain += dist[route1.customers[idx_first] + 1,
                                 route2.customers[idx_second] + 1]

                    gain -= dist[route1.customers[idx_first - 1] + 1,
                                 route1.customers[idx_first] + 1]

                    gain -= dist[route2.customers[idx_second - 1] + 1,
                                 route2.customers[idx_second] + 1]

                    if gain >= 0:
                        continue  # this is not a better move.

                    new_route1 = deepcopy(route1)
                    new_route2 = deepcopy(route2)

                    customer1 = route1.customers[idx_first]
                    new_route1.remove_customer(route1.customers[idx_first])

                    customer2 = route2.customers[idx_second]
                    new_route2.remove_customer(route2.customers[idx_second])

                    if not new_route2.can_insert(customer1, idx_second) \
                            or not new_route1.can_insert(customer2, idx_first):
                        continue

                    new_route1.insert_customer(customer2, idx_first)
                    new_route2.insert_customer(customer1, idx_second)

                    new = new_route1.routing_cost() + new_route2.routing_cost()
                    old = route1.routing_cost() + route2.routing_cost()

                    print(new, old)

                    if new > old:
                        continue

                    solution.routes[idx1] = new_route1
                    solution.routes[idx2] = new_route2

                    return solution

    return solution

