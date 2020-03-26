from functools import wraps
from typing import Callable

from heuristic.classes import Solution


def remove_empty_routes(operator: Callable[..., Solution]):
    """
    Wrapper function that removes empty routes from the returned solution
    instance. These routes may come into existence because all customers have
    been removed by e.g. a destroy operator.
    """
    @wraps(operator)
    def decorator(*args, **kwargs):
        destroyed = operator(*args, **kwargs)
        destroyed.routes = [route for route in destroyed.routes
                            if len(route) != 0]

        return destroyed

    return decorator
