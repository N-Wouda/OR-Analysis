from typing import Tuple

from heuristic.classes import Solution


def handling_cost(solution: Solution) -> Tuple[str, float]:
    """
    Returns instance's handling costs.
    """
    return ("handling_cost",
            sum(route.handling_cost() for route in solution.routes))
