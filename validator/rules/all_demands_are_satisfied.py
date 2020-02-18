from typing import Tuple

from heuristic.classes import Item, Solution
from heuristic.constants import DEPOT


def all_demands_are_satisfied(solution: Solution) -> Tuple[bool, str]:
    """
    Verifies all demands are satisfied, that is, the demanded items are loaded
    according to a feasible loading plan for each customer.
    """
    for customer in range(solution.problem.num_customers):
        route = solution.find_route(customer)
        delivery = Item(solution.problem.demands[customer], DEPOT, customer)

        for stacks in route.plan[:route.customers.index(customer) + 1]:
            try:
                # Quickly finds the stack this item is stored in, or raises
                # if no such stack exists. Just the existence is sufficient.
                stacks.find_stack(delivery)
            except LookupError:
                return False, f"{delivery} is not in the solution for all " \
                              f"appropriate legs of the route."

    return True, "All demands are satisfied."
