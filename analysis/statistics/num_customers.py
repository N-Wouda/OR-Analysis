from typing import Tuple

from heuristic.classes import Problem, Solution


def num_customers(solution: Solution) -> Tuple[str, float]:
    """
    Returns instance's number of customers.
    """
    problem = Problem()

    return "num_customers", problem.num_customers
