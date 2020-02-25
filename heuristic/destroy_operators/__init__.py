from typing import Callable, List

from numpy.random import RandomState

from heuristic.classes import Solution
from .minimum_quantity import minimum_quantity
from .random_customers import random_customers
from .random_nearest import random_nearest
from .random_routes import random_routes
from .worst_cost import worst_cost
from .worst_distance import worst_distance
from .worst_handling import worst_handling

D_OPERATORS: List[Callable[[Solution, RandomState], Solution]] = [
    minimum_quantity,
    random_customers,
    random_nearest,
    random_routes,
    worst_cost,
    worst_distance,
    worst_handling,
    # TODO
]
