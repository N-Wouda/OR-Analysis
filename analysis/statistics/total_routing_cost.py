from typing import Tuple

from heuristic.classes import Solution


def total_routing_cost(solution: Solution) -> Tuple[str, float]:
    """
    Returns instance's total routing costs.
    """
    return "total_routing_cost", sum(solution.routes[idx].routing_cost()
                                     for idx in range(len(solution.routes)))
