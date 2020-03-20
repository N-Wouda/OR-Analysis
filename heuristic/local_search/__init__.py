from typing import Callable, List

from heuristic.classes import Route
from .LocalSearch import LocalSearch
from .in_route_item_reinsert import in_route_item_reinsert
from .in_stack_roll_delivery_to_rear import in_stack_roll_delivery_to_rear
from .in_stack_roll_pickup_to_front import in_stack_roll_pickup_to_front
from .two_opt import two_opt

L_OPERATORS: List[Callable[[Route], Route]] = [
    two_opt,
    # TODO more routing options
    in_route_item_reinsert,
    in_stack_roll_delivery_to_rear,
    in_stack_roll_pickup_to_front,
]
