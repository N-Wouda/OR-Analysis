from heuristic.classes import Solution


def handling_cost(solution: Solution) -> float:
    """
    Returns the solution handling cost.
    """
    return sum(route.handling_cost() for route in solution.routes)
