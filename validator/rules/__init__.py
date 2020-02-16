from typing import Callable, List, Tuple

from heuristic.classes import Solution
from .all_customers_visited import all_customers_visited
from .stack_capacity_is_respected import stack_capacity_is_respected
from .vehicle_capacity_is_respected import vehicle_capacity_is_respected

RULES: List[Callable[[Solution], Tuple[bool, str]]] = [
    all_customers_visited,
    stack_capacity_is_respected,
    vehicle_capacity_is_respected,
    # TODO
]
