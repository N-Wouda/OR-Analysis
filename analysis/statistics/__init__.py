from typing import Callable, List, Tuple

from heuristic.classes import Solution

from .total_handling_cost import total_handling_cost
from .nr_routes import nr_routes
from .total_routing_cost import total_routing_cost
from .total_cost import total_cost
from .handling_cost import handling_cost
from .instance import instance
from .num_customers import num_customers


STATISTICS: List[Callable[[Solution], Tuple[str, float]]] = [
    instance,
    nr_routes,
    num_customers,
    handling_cost,
    total_cost,
    total_handling_cost,
    total_routing_cost,
    # TODO
]