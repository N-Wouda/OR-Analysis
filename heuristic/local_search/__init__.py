from typing import Callable, List

from numpy.random import RandomState

from heuristic.classes import Solution
from .LocalSearch import LocalSearch
from .loading_order import loading_order
from .reinsertion import reinsertion


L_OPERATORS: List[Callable[[Solution, RandomState], Solution]] = [
    reinsertion,
    # loading_order,
    # TODO
]
