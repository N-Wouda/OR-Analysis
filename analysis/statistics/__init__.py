from typing import Callable, List, Tuple

from heuristic.classes import Solution
from .handling import handling
from .handling_cost import handling_cost
from .instance import instance
from .num_customers import num_customers
from .num_routes import num_routes
from .objective import objective
from .routing_cost import routing_cost

STATISTICS: List[Callable[[Solution], Tuple[str, float]]] = [
    instance,
    num_routes,
    num_customers,
    handling,
    objective,
    handling_cost,
    routing_cost,
    # TODO
]
