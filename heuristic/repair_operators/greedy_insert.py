from heapq import heapify, heappop

from numpy.random import RandomState

from heuristic.classes import Item, Route, Solution, Stacks
from heuristic.constants import DEPOT


def greedy_insert(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Sequentially inserts each a random permutation of the unassigned customers
    into their best, feasible route at a locally optimal leg of the tour.

    Sequential best insertion in Hornstra et al. (2020).
    """
    rnd_state.shuffle(current.unassigned)

    while len(current.unassigned) != 0:
        customer = current.unassigned.pop()
        routes = []

        for route in current.routes:
            idx, cost = route.opt_insert(customer, current.problem)

            if route.can_insert(customer, idx, current.problem):
                routes.append((cost, idx, route))

        heapify(routes)

        cost, insert_idx, route = heappop(routes)
        cost_new = Route([DEPOT, customer], []).routing_cost(current.problem)

        if cost_new < cost:  # a new route is the cheapest action
            stacks = [Stacks(current.problem.num_stacks) for _ in range(2)]

            delivery = Item(current.problem.demands[customer], DEPOT, customer)
            pickup = Item(current.problem.pickups[customer], customer, DEPOT)

            stacks[0].shortest_stack().push_rear(delivery)
            stacks[1].shortest_stack().push_rear(pickup)

            current.routes.append(Route([customer], stacks))
        else:  # insert into lowest-cost, feasible route
            delivery = Item(current.problem.demands[customer], DEPOT, customer)
            pickup = Item(current.problem.pickups[customer], customer, DEPOT)

            route.customers.insert(insert_idx, customer)
            route._set.add(customer)  # TODO this is not very nice

            # insert handling plan at added customer
            stack_after_customer = Stacks.copy(route.plan[insert_idx])
            route.plan.insert(insert_idx + 1, stack_after_customer)

            # insert for delivery in all stacks before customer
            for plan in route.plan[:insert_idx + 1]:
                plan.shortest_stack().push_rear(delivery)

            # insert pickup for all stacks after customer
            for plan in route.plan[insert_idx + 1:]:
                plan.shortest_stack().push_rear(pickup)

    return current
