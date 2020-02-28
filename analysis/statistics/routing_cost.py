from typing import Tuple

from heuristic.classes import Solution


def routing_cost(solution: Solution) -> Tuple[str, float]:
    """
    Returns instance's routing costs.
    """
    return ("routing_cost",
            sum(route.routing_cost() for route in solution.routes))
