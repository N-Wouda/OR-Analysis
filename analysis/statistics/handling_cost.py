from typing import Tuple

from heuristic.classes import Solution


def handling_cost(solution: Solution) -> Tuple[str, float]:
    """
    Returns the solution handling cost.
    """
    return ("handling_cost",
            sum(route.handling_cost() for route in solution.routes))
