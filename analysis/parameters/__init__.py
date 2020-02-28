from typing import Callable, List

from heuristic.classes import Solution
from .handling import handling
from .instance import instance
from .customers import customers
from .stacks import stacks

PARAMETERS: List[Callable[[Solution], float]] = [
    instance,
    customers,
    handling,
    stacks,
]
