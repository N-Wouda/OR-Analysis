import numpy as np
from numpy.random import RandomState

from heuristic.classes import Item, Route, Solution, Stacks
from heuristic.constants import DEPOT, M


def greedy_insert(current: Solution, rnd_state: RandomState) -> Solution:
    """
    TODO.
    """

    while len(current.unassigned) != 0:
        customer = current.unassigned.pop()
        insertion_costs = []
        # insertion_costs = np.full((len(current.routes),
        #                            current.problem.num_customers), M)

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

            # for first, second in zip(full_route, full_route[1:]):
            #     print(first, second)
            #     insertion_costs[route, first] = \
            #         current.problem.distances[first, customer + 1]\
            #         + current.problem.distances[customer + 1, second]

        # Costs new route
        insertion_costs.append([current.problem.distances
                                [DEPOT + 1, customer + 1] +
                                current.problem.distances
                                [customer + 1, DEPOT + 1]])

        # insertion_costs[-1, 0] = \
        #     current.problem.distances[DEPOT + 1, customer + 1] + \
        #     current.problem.distances[customer + 1, DEPOT + 1]

        # Finding a feasible entry
        feasible = False
        while not feasible:
            # Finding the lowest cost
            min_cost = min(min(route_insertion_costs) for route_insertion_costs
                           in insertion_costs)
            # min_cost = min(insertion_costs)

            # Finding its index
            indexes = [(idx, route_insertion_costs.index(min_cost))
                       for idx, route_insertion_costs in enumerate(insertion_costs)
                       if min_cost in insertion_costs[idx]]

            idx_route, idx_customer = indexes[0]

            # idx_route, idx_customer = insertion_costs.argmin()

            # Checking if feasible
            # New route always feasible so
            if idx_route == len(current.routes):
                feasible = True
            else:
                route = current.routes[idx_route]
                demand = current.problem.demands[customer]
                pickup_size = current.problem.pickups[customer]
                stack_capacity = current.problem.capacity

                for plan in route.plan[:idx_customer + 1]:
                    if plan.shortest_stack().volume() + demand > stack_capacity:
                        # insertion_costs[idx_route][idx_customer] += M
                        insertion_costs[idx_route, idx_customer] = M

                for plan in route.plan[idx_customer + 1:]:
                    if plan.shortest_stack().volume() + pickup_size\
                            > stack_capacity:
                        # insertion_costs[idx_route][idx_customer] += M
                        insertion_costs[idx_route, idx_customer] = M

                if insertion_costs[idx_route][idx_customer] < M:
                    feasible = True

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
