from typing import Tuple

from heuristic.classes import Problem, Solution


def instance(solution: Solution) -> int:
    """
    Returns problem instance number.
    """
    return Problem().instance
