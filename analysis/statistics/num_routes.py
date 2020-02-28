from typing import Tuple

from heuristic.classes import Solution


def num_routes(solution: Solution) -> Tuple[str, float]:
    """
    Returns number of routes in the solution.
    """
    return "num_routes", len(solution.routes)
