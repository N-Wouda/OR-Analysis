from typing import Tuple

from heuristic.classes import Solution


def vehicle_capacity_is_respected(solution: Solution) -> Tuple[bool, str]:
    """
    Verifies the vehicle capacities are respected by each tour of the solution.
    """
    for route in solution.routes:
        if any(stacks.used_capacity() > solution.problem.capacity
               for stacks in route.plan):
            return False, "Vehicle capacity is not respected."

    return True, "Vehicle capacity is respected."
