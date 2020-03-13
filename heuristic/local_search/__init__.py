from typing import Callable, List

from numpy.random import RandomState

from heuristic.classes import Solution
from .LocalSearch import LocalSearch
from .in_route_two_opt import in_route_two_opt

L_OPERATORS: List[Callable[[Solution, RandomState], Solution]] = [
    # in_route_two_opt,
    # TODO
]
