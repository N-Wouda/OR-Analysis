from typing import Tuple

from heuristic.classes import Problem, Solution


def handling_cost(solution: Solution) -> Tuple[str, float]:
    """
    Handling cost per volume unit.
    """
    problem = Problem()

    return "handling_cost", problem.handling_cost
