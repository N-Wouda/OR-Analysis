from typing import Callable, List

from heuristic.classes import Route
from .LocalSearch import LocalSearch
from .item_reinsert import item_reinsert
from .in_stack_roll_delivery_to_rear import in_stack_roll_delivery_to_rear
from .pickup_push_to_front import pickup_push_to_front
from .in_route_two_opt import in_route_two_opt

L_OPERATORS: List[Callable[[Route], Route]] = [
    in_route_two_opt,
    # TODO more routing options
    item_reinsert,
    in_stack_roll_delivery_to_rear,
    pickup_push_to_front,
]
