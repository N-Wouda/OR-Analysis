from typing import Callable, List

from numpy.random import RandomState

from heuristic.classes import Solution
from .random_customers import random_customers
from .random_nearest import random_nearest
from .random_routes import random_routes

D_OPERATORS: List[Callable[[Solution, RandomState], Solution]] = [
    random_customers,
    random_nearest,
    random_routes,
    # TODO
]
