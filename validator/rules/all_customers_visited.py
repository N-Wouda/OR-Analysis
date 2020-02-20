from typing import Tuple

from heuristic.classes import Problem, Solution


def all_customers_visited(solution: Solution) -> Tuple[bool, str]:
    """
    Verifies the solution visits all customers (at least once).
    """
    problem = Problem()
    customers = set()

    for route in solution.routes:
        customers.update(route.customers)

    for customer in range(problem.num_customers):
        if customer not in customers:
            return False, f"Customer {customer} is not in the solution."

    return True, "All customers are visited."
