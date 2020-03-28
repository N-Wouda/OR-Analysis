from copy import deepcopy

import numpy as np

from heuristic.classes import Problem, Route


def pickup_push_to_front(route: Route) -> Route:
    """
    Pushes pickup items to the front, at various legs of the route. This is
    somewhat preferred, as these items cannot get in the way if they are
    positioned at the front.
    """
    if np.isclose(route.handling_cost(), 0.):
        return route

    problem = Problem()

    for idx_customer, customer in enumerate(route, 1):
        pickup = problem.pickups[customer]
        idx_stack = route.plan[idx_customer].find_stack(pickup).index

        # This skips the last offset, as that would not be interesting anyway
        # (that is the leg towards the depot, where we have only pickups and
        # handling can no longer be improved).
        for plan_offset in range(idx_customer, len(route)):
            new_route = deepcopy(route)

            for stacks in new_route.plan[plan_offset:]:
                stack = stacks[idx_stack]

                idx_current = stack.item_index(pickup)
                stack.remove(pickup)

                stack.push(idx_current + 1, pickup)

            new_route.invalidate_handling_cache()

            if new_route.handling_cost() < route.handling_cost():
                return new_route

    return route
