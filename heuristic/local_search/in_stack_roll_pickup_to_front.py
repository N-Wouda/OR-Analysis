from copy import deepcopy

from heuristic.classes import Item, Problem, Route


def in_stack_roll_pickup_to_front(route: Route) -> Route:
    """
    TODO.
    """
    problem = Problem()

    for idx_customer, customer in enumerate(route.customers, 1):
        pickup = problem.pickups[customer]
        idx_stack = route.plan[idx_customer].find_stack(pickup).index

        for plan_offset in range(idx_customer, len(route.customers) + 1):
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
