from heuristic.classes import Route


def in_route_opt_reinsert(route: Route) -> Route:
    """
    Performs the best in-route reinsertion of a customer. Approximates both
    routing and handling costs.

    Similar to reinsertion in Hornstra et al. (2020), but significantly less
    global.
    """
    for customer in route.customers:
        pass

    return route
