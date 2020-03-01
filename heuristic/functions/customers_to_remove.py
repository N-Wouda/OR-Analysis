from functools import lru_cache

from heuristic.classes import Problem
from heuristic.constants import DEGREE_OF_DESTRUCTION


@lru_cache(1)
def customers_to_remove() -> int:
    """
    Returns the number of customers to remove from the solution.
    """
    return int(Problem().num_customers * DEGREE_OF_DESTRUCTION)
