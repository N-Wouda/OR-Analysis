from typing import Tuple

from heuristic.classes import Problem, Solution


def handling(solution: Solution) -> Tuple[str, float]:
    """
    Returns the problem's handling cost parameter.
    """
    problem = Problem()

    return "handling", problem.handling_cost
