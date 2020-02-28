from heuristic.classes import Solution


def routes(solution: Solution) -> int:
    """
    Returns number of routes in the solution.
    """
    return len(solution.routes)
