from typing import Tuple

from heuristic.classes import Problem, Solution


def handling(solution: Solution) -> Tuple[str, float]:
    """
    Returns instance's handling.
    """
    problem = Problem()

    return "handling", problem.handling_cost
