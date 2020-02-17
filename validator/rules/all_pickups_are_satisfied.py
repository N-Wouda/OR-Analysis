from typing import Tuple

from heuristic.classes import Item, Route, Solution
from heuristic.constants import DEPOT


# TODO deduplicate this
def all_pickups_are_satisfied(solution: Solution) -> Tuple[bool, str]:
    """
    Verifies all demands are satisfied, that is, the demanded items are loaded
    according to a feasible loading plan for each customer.
    """
    for customer in range(solution.problem.num_customers):
        route = _find_route(solution, customer)
        assert route is not None

        pickup = Item(solution.problem.pickups[customer], customer, DEPOT)

        for stacks in route.plan[route.customers.index(customer) + 1:]:
            try:
                stacks.find_stack(pickup)
            except ValueError:
                return False, f"{pickup} is not in the solution for all " \
                              f"appropriate legs of the route."

    return True, "All pick-ups are satisfied."


def _find_route(solution: Solution, customer: int) -> Route:
    for route in solution.routes:
        if customer in route:
            return route
