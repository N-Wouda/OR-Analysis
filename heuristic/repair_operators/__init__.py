from typing import Callable, List

from numpy.random import RandomState

from heuristic.classes import Solution
from .greedy_insert import greedy_insert
from .random_repair import random_repair

R_OPERATORS: List[Callable[[Solution, RandomState], Solution]] = [
    greedy_insert,
    random_repair
    # TODO
]
