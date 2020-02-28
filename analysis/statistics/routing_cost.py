from heuristic.classes import Solution


def routing_cost(solution: Solution) -> float:
    """
    Returns solution routing costs.
    """
    return sum(route.routing_cost() for route in solution.routes)
