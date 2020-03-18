from typing import Callable, List

from heuristic.classes import Route
from .LocalSearch import LocalSearch
from .in_route_two_opt import in_route_two_opt
from .in_route_opt_reinsert import in_route_opt_reinsert

L_OPERATORS: List[Callable[[Route], Route]] = [
    # TODO we should probably also do something about handling!
    #   e.g.:
    #   - fix up later pickup insertions in front of earlier pickups
    #     e.g. by re-inserting pickups for customers?
    #   - use empty or near empty stacks more?
    #   - switch customers around if that improves handling more than it
    #     hurts in routing cost?
    in_route_opt_reinsert,
    in_route_two_opt
]
