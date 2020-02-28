from heuristic.classes import Solution


def objective(solution: Solution) -> float:
    """
    Returns solution objective.
    """
    return solution.objective()
