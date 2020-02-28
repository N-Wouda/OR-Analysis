from typing import Tuple

from heuristic.classes import Problem, Solution


def instance(solution: Solution) -> Tuple[str, float]:
    """
    Returns problem instance number.
    """
    problem = Problem()

    return "instance", problem.instance
