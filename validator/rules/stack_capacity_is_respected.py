from typing import Tuple

from heuristic.classes import Solution


def stack_capacity_is_respected(solution: Solution) -> Tuple[bool, str]:
    """
    Verifies the stack capacities are respected for each leg in each tour of
    the solution.
    """
    for route in solution.routes:
        if not all(stacks.is_feasible() for stacks in route.plan):
            return False, "Stack capacity is not respected."

    return True, "Stack capacity is respected."
