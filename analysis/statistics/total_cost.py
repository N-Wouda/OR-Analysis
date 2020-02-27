from typing import Tuple

from heuristic.classes import Solution


def total_cost(solution: Solution) -> Tuple[str, float]:
    """
    Returns instance's total cost.
    """
    return "total_cost", solution.objective()
