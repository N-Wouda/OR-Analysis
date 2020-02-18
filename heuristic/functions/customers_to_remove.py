from heuristic.constants import DEGREE_OF_DESTRUCTION


def customers_to_remove(num_customers: int) -> int:
    """
    Returns the number of customers to remove from the solution.
    """
    return int(num_customers * DEGREE_OF_DESTRUCTION)
