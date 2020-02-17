import numpy as np
from numpy.random import RandomState

from heuristic.classes import Item, Route, Solution, Stacks
from heuristic.constants import DEPOT


def greedy_insert(current: Solution, rnd_state: RandomState) -> Solution:
    """
    TODO.
    """
    assigned = [customer for customer in
                list(range(current.problem.num_customers)) if customer
                not in current.unassigned]

    #  per unassigned probeer in te voegen per route op elke plek en bereken
    #  kosten, en ook kosten voor nieuwe route. Selecteer laagste en plaats daar

    while current.unassigned != 0:
        customer = next(customer for customer in current.unassigned)

        # Closest visitable node.
        nearest = np.argmin(current.problem.distances[assigned, customer])
        # Find route it is in and insert customer after closest other customer.
        if nearest == 0:
            delivery = Item(current.problem.demands[customer], DEPOT, customer)
            pickup = Item(current.problem.pickups[customer], customer, DEPOT)

            stacks = [Stacks(current.problem.num_stacks) for _ in range(2)]

            stacks[0].shortest_stack().push_rear(delivery) #0, 1 is voor 2 delige route
            stacks[1].shortest_stack().push_rear(pickup)

            current.routes.append(Route([customer], stacks))
        else:
            for route_number in range(len(current.routes)):
                if current.routes[route_number].customers.index(nearest):
                    current.routes[route_number].customers.insert(
                        current.routes[route_number].customers.index(nearest),
                        customer)

    for route in current.routes:


    return current
