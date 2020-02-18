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
            idx = route.opt_insert(current.problem, customer)
            cost = route.insert_cost(current.problem, idx, customer)

            if route.is_feasible(current.problem, idx):
                routes.append((cost, idx, route))

        heapify(routes)

        cost_new = current.problem.distances[DEPOT + 1, customer + 1] \
                   + current.problem.distances[customer + 1, DEPOT + 1]

        cost, idx_customer, route = heappop(routes)

        delivery = Item(current.problem.demands[customer], DEPOT, customer)
        pickup = Item(current.problem.pickups[customer], customer, DEPOT)

        if cost_new < cost:  # a new route is the cheapest action
            stacks = [Stacks(current.problem.num_stacks) for _ in range(2)]

            stacks[0].shortest_stack().push_rear(delivery)
            stacks[1].shortest_stack().push_rear(pickup)

            current.routes.append(Route([customer], stacks))
        else:  # insert into lowest-cost, feasible route
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
