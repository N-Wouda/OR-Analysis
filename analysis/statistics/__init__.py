from typing import Callable, List, Tuple

from heuristic.classes import Solution

from .handling import handling
from .num_routes import nr_routes
from .routing_cost import routing_cost
from .objective import objective
from .handling_cost import handling_cost
from .instance import instance
from .num_customers import num_customers


STATISTICS: List[Callable[[Solution], Tuple[str, float]]] = [
    instance,
    nr_routes,
    num_customers,
    handling,
    objective,
    handling_cost,
    routing_cost,
    # TODO
]
