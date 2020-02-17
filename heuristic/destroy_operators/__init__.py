from typing import Callable, List

from numpy.random import RandomState

from heuristic.classes import Solution
from .random_customer_removal import random_customer_removal

D_OPERATORS: List[Callable[[Solution, RandomState], Solution]] = [
    random_customer_removal,
    # TODO
]
