from typing import Callable, List

from heuristic.classes import Solution
from .handling_cost import handling_cost
from .routes import routes
from .objective import objective
from .routing_cost import routing_cost

STATISTICS: List[Callable[[Solution], float]] = [
    routes,
    objective,
    routing_cost,
    handling_cost,
    # TODO
]
