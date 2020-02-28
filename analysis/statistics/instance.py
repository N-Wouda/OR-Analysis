from typing import Tuple

from heuristic.classes import Problem, Solution


def instance(solution: Solution) -> Tuple[str, float]:
    """
    Returns instance's number.
    """
    problem = Problem()

    return "instance", problem.instance
