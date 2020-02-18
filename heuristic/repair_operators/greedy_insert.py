import numpy as np
from numpy.random import RandomState
import heapq


from heuristic.classes import Item, Route, Solution, Stacks
from heuristic.constants import DEPOT


def greedy_insert(current: Solution, rnd_state: RandomState) -> Solution:
    """
    TODO.
    """

    while len(current.unassigned) != 0:
        customer = current.unassigned.pop()
        insertion_heap = []

        for idx_route, route in enumerate(current.routes):
            idx = route.opt_insert(current.problem, customer)
            cost = route.insert_cost(current.problem, idx, customer)

            if route.is_feasible(current.problem, idx):
                heapq.heappush(insertion_heap, (cost, idx, idx_route))

        # Costs new route
        cost_new_route = ([current.problem.distances[DEPOT + 1, customer + 1] +
                           current.problem.distances[customer + 1, DEPOT + 1]])
        heapq.heappush(insertion_heap, (cost_new_route, 0, len(current.routes)))

        cost, idx_customer, idx_route = heapq.heappop(insertion_heap)

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
