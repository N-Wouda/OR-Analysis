from typing import Callable, List

from heuristic.classes import Route, Solution
from .LocalSearch import LocalSearch
from .in_route_two_opt import in_route_two_opt
from .item_reinsert import item_reinsert
from .pickup_push_to_front import pickup_push_to_front
from .relocate_customer import relocate_customer

SOLUTION_OPERATORS: List[Callable[[Solution], Solution]] = [
    relocate_customer,
    # TODO more routing options
]

ROUTE_OPERATORS: List[Callable[[Route], Route]] = [
    in_route_two_opt,
    item_reinsert,
    pickup_push_to_front,
]
