from copy import deepcopy

import numpy as np

from heuristic.classes import Item, Problem, Route


# TODO make all this cleaner.

def in_route_item_reinsert(route: Route) -> Route:
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

        next_route = _insert_item(new_route, delivery, idx)
        next_route = _insert_item(next_route, pickup, idx)

        if next_route.handling_cost() < route.handling_cost():
            return next_route

    return route


def _insert_item(route: Route,
                 item: Item,
                 idx_customer: int) -> Route:
    copies = []

    if item.is_delivery():
        for idx_stack, stack in enumerate(route.plan[0].stacks):
            for idx_item in range(len(stack) + 1):
                copy = _play_forward(route,
                                     item,
                                     idx_customer,
                                     idx_stack,
                                     idx_item)

                if copy:
                    copies.append(copy)
    else:
        for idx_stack, stack in enumerate(route.plan[idx_customer].stacks):
            for idx_item in range(len(stack) + 1):
                copy = _play_forward(route,
                                     item,
                                     idx_customer,
                                     idx_stack,
                                     idx_item)

                if copy:
                    copies.append(copy)

    return min(copies, key=lambda copy: copy.handling_cost())


def _play_forward(route: Route,
                  item: Item,
                  idx_customer: int,
                  idx_stack: int,
                  idx_item: int):
    copy = deepcopy(route)
    problem = Problem()

    if item.is_delivery():
        for stacks in copy.plan[:idx_customer]:
            stacks[idx_stack].push(idx_item, item)

            if stacks[idx_stack].volume() > problem.stack_capacity:
                return False
    else:
        for stacks in copy.plan[idx_customer:]:
            stacks[idx_stack].push(idx_item, item)

            if stacks[idx_stack].volume() > problem.stack_capacity:
                return False

    copy.invalidate_handling_cache()
    return copy
