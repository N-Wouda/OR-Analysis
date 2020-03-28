from typing import Callable, List, Tuple

from heuristic.classes import Solution
from .all_customers_visited import all_customers_visited
from .all_demands_are_satisfied import all_demands_are_satisfied
from .all_pickups_are_satisfied import all_pickups_are_satisfied
from .stack_capacity_is_respected import stack_capacity_is_respected
from .vehicle_capacity_is_respected import vehicle_capacity_is_respected

RULES: List[Callable[[Solution], Tuple[bool, str]]] = [
    all_customers_visited,
    all_demands_are_satisfied,
    all_pickups_are_satisfied,
    stack_capacity_is_respected,
    vehicle_capacity_is_respected,
]
