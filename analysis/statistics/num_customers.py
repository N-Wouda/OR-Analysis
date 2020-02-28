from typing import Tuple

from heuristic.classes import Problem, Solution


def num_customers(solution: Solution) -> Tuple[str, float]:
    """
    Returns the number of customers in the problem instance.
    """
    problem = Problem()

    return "num_customers", problem.num_customers
