from typing import Callable, List

from numpy.random import RandomState

from heuristic.classes import Solution
from .random_customers import random_customers
from .random_route import random_route

D_OPERATORS: List[Callable[[Solution, RandomState], Solution]] = [
    random_customers,
    random_route,
    # TODO
]
