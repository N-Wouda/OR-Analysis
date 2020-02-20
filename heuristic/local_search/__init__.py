from typing import Callable, List

from numpy.random import RandomState

from heuristic.classes import Solution
from .LocalSearch import LocalSearch

L_OPERATORS: List[Callable[[Solution, RandomState], Solution]] = [
    # TODO
]
