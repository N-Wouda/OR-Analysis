from typing import Tuple

from heuristic.classes import Problem, Solution


def all_pickups_are_satisfied(solution: Solution) -> Tuple[bool, str]:
    """
    Verifies all pickups are satisfied, that is, the pickup items are loaded
    according to a feasible loading plan for each customer.
    """
    problem = Problem()

    for customer in range(problem.num_customers):
        route = solution.find_route(customer)
        pickup = problem.pickups[customer]

        for stacks in route.plan[route.customers.index(customer) + 1:]:
            try:
                # Quickly finds the stack this item is stored in, or raises
                # if no such stack exists. Just the existence is sufficient.
                stacks.find_stack(pickup)
            except LookupError:
                return False, f"{pickup} is not in the solution for all " \
                              f"appropriate legs of the route."

    return True, "All pick-ups are satisfied."
