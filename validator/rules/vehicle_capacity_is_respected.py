from typing import Tuple

from heuristic.classes import Problem, Solution


def vehicle_capacity_is_respected(solution: Solution) -> Tuple[bool, str]:
    """
    Verifies the vehicle capacities are respected by each tour of the solution.
    """
    problem = Problem()

    for route in solution.routes:
        if any(stacks.used_capacity() > problem.capacity
               for stacks in route.plan):
            return False, "Vehicle capacity is not respected."

    return True, "Vehicle capacity is respected."
