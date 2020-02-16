from typing import Tuple

from heuristic.classes import Solution


def all_customers_visited(solution: Solution) -> Tuple[bool, str]:
    """
    Verifies the solution visits all customers (at least once).
    """
    customers = set()

    for route in solution.routes:
        customers.update(route.customers)

    for customer in range(solution.problem.num_customers):
        if customer not in customers:
            return False, f"Customer {customer} is not in the solution."

    return True, "All customers are visited."
