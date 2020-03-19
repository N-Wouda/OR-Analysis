from typing import Callable, List

from heuristic.classes import Route
from .LocalSearch import LocalSearch
from .in_route_item_reinsert import in_route_item_reinsert
from .in_route_two_opt import in_route_two_opt

L_OPERATORS: List[Callable[[Route], Route]] = [
    in_route_two_opt,
    # TODO more routing options
    in_route_item_reinsert,
]
