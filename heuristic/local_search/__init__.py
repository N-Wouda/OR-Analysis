from typing import Callable, List

from numpy.random import RandomState

from heuristic.classes import Solution
from .LocalSearch import LocalSearch
from .loading_order import loading_order


L_OPERATORS: List[Callable[[Solution, RandomState], Solution]] = [
    loading_order,
    # TODO
]
