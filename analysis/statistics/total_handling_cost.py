from typing import Tuple

from heuristic.classes import Problem, Solution


def total_handling_cost(solution: Solution) -> Tuple[str, float]:
    """
    Returns instance's total handling costs.
    """
    return "total_handling_cost", sum(solution.routes[idx].handling_cost()
                                      for idx in range(len(solution.routes)))