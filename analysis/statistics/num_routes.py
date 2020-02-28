from typing import Tuple

from heuristic.classes import Solution


def num_routes(solution: Solution) -> Tuple[str, float]:
    """
    Returns instance's number of routes used.
    """
    return "nr_routes", len(solution.routes)
