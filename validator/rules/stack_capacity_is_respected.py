from typing import Tuple

from heuristic.classes import Solution


def stack_capacity_is_respected(solution: Solution) -> Tuple[bool, str]:
    """
    Verifies the stack capacities are respected for each leg in each tour of
    the solution.
    """
    for route in solution.routes:
        for stacks in route.plan:
            if any(stack.volume() > solution.problem.stack_capacity
                   for stack in stacks):
                return False, "Stack capacity is not respected."

    return True, "Stack capacity is respected."
