from typing import Callable, List


def get_names(operators: List[Callable]):
    """
    Gets the operator names from the passed-in function list.
    """
    return [func.__name__ for func in operators]
