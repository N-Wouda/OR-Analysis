from copy import deepcopy

import numpy as np

from heuristic.classes import Item, Problem, Route


def item_reinsert(route: Route) -> Route:
    """
    Reinserts customer demands and pickups item in the optimal stack and
    position. Stops once an improving move has been found.
    """
    if np.isclose(route.handling_cost(), 0.):
        return route

    problem = Problem()

    for idx, customer in enumerate(route.customers, 1):
        delivery = problem.demands[customer]
        pickup = problem.pickups[customer]

        new_route = deepcopy(route)

        for stacks in new_route.plan[:idx]:
            stacks.find_stack(delivery).remove(delivery)

        for stacks in new_route.plan[idx:]:
            stacks.find_stack(pickup).remove(pickup)

        next_route = _insert_item(new_route, delivery)
        next_route = _insert_item(next_route, pickup)

        if next_route.handling_cost() < route.handling_cost():
            return next_route

    return route


def _insert_item(route: Route, item: Item) -> Route:
    """
    Inserts the given item into the least-cost feasible position on this route.
    """
    idx_customer = route.indices[item.customer] + 1

    if item.is_delivery():
        stacks = route.plan[0]
    else:
        stacks = route.plan[idx_customer]

    copies = []

    for idx_stack, stack in enumerate(stacks):
        for idx_item in range(len(stack) + 1):
            copy = deepcopy(route)

            if item.is_delivery():
                plan = copy.plan[:idx_customer]
            else:
                plan = copy.plan[idx_customer:]

            for stacks in plan:
                stacks[idx_stack].push(idx_item, item)

            if not all(stacks.is_feasible() for stacks in plan):
                continue

            copy.invalidate_handling_cache()
            copies.append(copy)

    assert len(copies) > 0
    return min(copies, key=lambda copy: copy.handling_cost())
