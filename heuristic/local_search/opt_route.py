import numpy as np
from ortools.constraint_solver import pywrapcp

from heuristic.classes import Problem, Route, Stacks
from heuristic.constants import DEPOT


def opt_route(route: Route) -> Route:
    """
    Determines a good (often optimal) solution to the routing problem for the
    passed-in route. This uses Google's solver.
    """
    problem = Problem()

    customers = np.array([DEPOT] + route.customers.to_list())

    # OR-Tools assumes the distance matrix is integral, so we scale it here to
    # ensure this is indeed the case.
    distances = 1000 * problem.distances[np.ix_(customers + 1, customers + 1)]

    # This part is more or less a direct copy of the TSP tutorial here:
    # https://developers.google.com/optimization/routing/tsp.
    manager = pywrapcp.RoutingIndexManager(len(distances), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        return distances[from_index, to_index]

    transit_callback = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.time_limit.seconds = 2

    solution = routing.SolveWithParameters(search_parameters)

    if not solution:
        return route

    # Reconstruct a candidate route from the solution output.
    index = routing.Start(0)
    path = [index]

    while not routing.IsEnd(index):
        index = solution.Value(routing.NextVar(index))
        path.append(index)

    candidate = Route([], [Stacks(problem.num_stacks)])

    for customer in customers[path[1:-1]]:  # skip over the depot.
        if not candidate.can_insert(customer, len(candidate.customers)):
            return route  # TODO candidate is infeasible - is this OK?

        candidate.insert_customer(customer, len(candidate.customers))

    c_cost = candidate.routing_cost()
    r_cost = route.routing_cost()

    assert c_cost <= r_cost or np.isclose(c_cost, r_cost)
    return candidate
