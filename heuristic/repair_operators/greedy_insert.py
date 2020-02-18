import numpy as np
from numpy.random import RandomState

from heuristic.classes import Item, Route, Solution, Stacks, Stack
from heuristic.constants import DEPOT


def greedy_insert(current: Solution, rnd_state: RandomState) -> Solution:
    """
    TODO.
    """
    while len(current.unassigned) != 0:
        customer = current.unassigned.pop()
        insertion_costs = []

        # Costs inserting in an existing route
        for route in current.routes:
            full_route = np.array([DEPOT, *route.customers, DEPOT])
            full_route += 1

            insertion_costs.append([current.problem.distances
                                    [first, customer + 1]
                                    + current.problem.distances
                                    [customer + 1, second]
                                    for first, second in
                                    zip(full_route, full_route[1:])])

        # Costs new route
        insertion_costs.append([current.problem.distances
                                [DEPOT + 1, customer + 1] +
                                current.problem.distances
                                [customer + 1, DEPOT + 1]])

        # Finding the lowest cost
        min_cost = min(min(route_insertion_costs) for route_insertion_costs
                       in insertion_costs)

        # Finding its index
        indexes = [(idx, route_insertion_costs.index(min_cost))
                   for idx, route_insertion_costs in enumerate(insertion_costs)
                   if min_cost in insertion_costs[idx]]

        idx_route, idx_customer = indexes[0]

        delivery = Item(current.problem.demands[customer], DEPOT, customer)
        pickup = Item(current.problem.pickups[customer], customer, DEPOT)

        # If creating a new route is cheapest
        if idx_route == len(current.routes):
            stacks = [Stacks(current.problem.num_stacks) for _ in range(2)]

            stacks[0].shortest_stack().push_rear(delivery)
            stacks[1].shortest_stack().push_rear(pickup)

            current.routes.append(Route([customer], stacks))
        else:
            route = current.routes[idx_route]

            # insert in cheapest route
            route.customers.insert(idx_customer, customer)
            route._set.add(customer)  # TODO this is not very nice

            # insert handling plan at added customer
            stack_after_customer = Stacks.copy(route.plan[idx_customer])

            route.plan.insert(idx_customer + 1, stack_after_customer)

            # insert for delivery in all stacks before customer
            for plan in route.plan[:idx_customer + 1]:
                plan.shortest_stack().push_rear(delivery)

            # insert pickup for all stacks after customer
            for plan in route.plan[idx_customer + 1:]:
                plan.shortest_stack().push_rear(pickup)

    return current
