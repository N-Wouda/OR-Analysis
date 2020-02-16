from typing import Callable, List, Tuple

from heuristic.classes import Solution
from .each_route_is_a_tour import each_route_is_a_tour

RULES: List[Callable[[Solution], Tuple[bool, str]]] = [
    each_route_is_a_tour,
    # TODO
]
