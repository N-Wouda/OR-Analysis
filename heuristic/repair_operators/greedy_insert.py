import numpy as np
from numpy.random import RandomState

from heuristic.classes import Item, Route, Solution, Stacks, Stack
from heuristic.constants import DEPOT


def greedy_insert(current: Solution, rnd_state: RandomState) -> Solution:
    """
    TODO.
    """
    print("###########################")
    while current.unassigned:# != 0:
        print("unassigned customer ", current.unassigned)
        customer = next(customer for customer in current.unassigned)

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

        route_index = indexes[0][0]
        customer_index = indexes[0][1]

        delivery = Item(current.problem.demands[customer], DEPOT,
                        customer)
        pickup = Item(current.problem.pickups[customer], customer,
                      DEPOT)

        # If creating a new route is cheapest
        if route_index == (len(current.routes)):

            stacks = [Stacks(current.problem.num_stacks) for _ in range(2)]

            stacks[0].shortest_stack().push_rear(delivery)
            stacks[1].shortest_stack().push_rear(pickup)

            current.routes.append(Route([customer], stacks))
        else:
            # insert in cheapest route
            current.routes[route_index]. \
                customers.insert(customer_index, customer)

            # insert handling plan at added customer
            stack_after_customer = Stacks.copy(current.routes[route_index].plan[
                customer_index])

            current.routes[route_index].plan.insert(customer_index + 1,
                                                    stack_after_customer)

            # insert for delivery in all stacks before customer
            for idx in range(customer_index + 1):
                current.routes[route_index].plan[idx].\
                    shortest_stack().push_rear(delivery)

            # insert pickup for all stacks after customer
            for idx in range(customer_index + 1,
                             len(current.routes[route_index].plan)):
                current.routes[route_index].plan[idx].\
                    shortest_stack().push_rear(pickup)

        current.unassigned.remove(customer)

        for idx in range(len(current.routes)):
            print(f"route {idx}:", current.routes[idx].customers)
            # for idx2 in range(len(current.routes[idx].plan)):
            #     print(f"step {idx2}")
            #     for idx3 in range(len(current.routes[idx].plan[idx2].stacks)):
            #         for idx4 in range(len(current.routes[idx].plan[idx2].stacks
            #                               [idx3].stack)):
            #             print(f"stack {idx4}:", current.routes[idx].plan[idx2].
            #                   stacks[idx3].stack[idx4])
    return current
