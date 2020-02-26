from typing import Callable, List

from numpy.random import RandomState

from heuristic.classes import Solution
from .LocalSearch import LocalSearch
from .loading_order import loading_order
from .opt_reinsert_customer import opt_reinsert_customer


L_OPERATORS: List[Callable[[Solution, RandomState], Solution]] = [
    # opt_reinsert_customer,
    # loading_order,
    # TODO
]
