import numpy as np
from numpy.random import RandomState

from heuristic.classes import Problem, Solution, Stacks
from heuristic.constants import DEPOT
from heuristic.functions import customers_to_remove, remove_empty_routes


@remove_empty_routes
def worst_removal(current: Solution, rnd_state: RandomState) -> Solution:
    """
    TODO split this into route and handling costs (two separate operators using
        that backend), and then a joint operator for worst in general.
    """
    problem = Problem()
    destroyed = current.copy()

    costs = np.zeros(problem.num_customers)

    for route in destroyed.routes:
        for idx, customer in enumerate(route.customers):
            # TODO this only accounts for handling *at* this customer, but its
            #   delivery and pickup items incur costs elsewhere as well. Should
            #   we also take those into account?
            handling_cost = Stacks.cost(customer, *route.plan[idx:idx + 2])

            # TODO Clean this routing cost stuff up, move it somewhere else
            if idx == 0:
                if len(route.customers) > 1:
                    route_with = [DEPOT, route.customers[0], route.customers[1]]
                    route_without = [DEPOT, route.customers[1]]
                else:
                    route_with = [DEPOT, route.customers[0]]
                    route_without = [DEPOT]
            elif idx == len(route.customers) - 1:
                if len(route.customers) > 1:
                    route_with = [route.customers[-2], route.customers[-1],
                                  DEPOT]
                    route_without = [route.customers[-2], DEPOT]
                else:
                    route_with = [route.customers[-1], DEPOT]
                    route_without = [DEPOT]
            else:
                route_with = [route.customers[idx - 1], route.customers[idx],
                              route.customers[idx + 1]]
                route_without = [route.customers[idx - 1],
                                 route.customers[idx + 1]]

            route_cost = problem.distances[np.roll(route_with, 1), route_with].sum() \
                         - problem.distances[np.roll(route_without, 1), route_without].sum()

            costs[customer] = handling_cost + route_cost

    customers = np.argsort(costs)[-customers_to_remove(problem.num_customers):]

    # TODO some randomness
    for customer in customers:
        destroyed.unassigned.append(customer)

        route = destroyed.find_route(customer)
        route.remove_customer(customer)

    return destroyed
