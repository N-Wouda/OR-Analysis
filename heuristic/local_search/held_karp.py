from functools import lru_cache
from itertools import islice
from typing import FrozenSet, List

from heuristic.classes import Problem, Route, Stacks
from heuristic.constants import DEPOT


def held_karp(route: Route) -> Route:
    """
    The Held-Karp shortest tour of this set of customers. For each customer C,
    find the shortest segment from DEPOT (the start) to C. Out of all these
    shortest segments, pick the one that is the shortest tour.

    O(2^n n^2), with n the number of customers.
    """
    customers = frozenset(route.customers.to_set())
    tour = min((shortest_segment(DEPOT,
                                 customers - {customer},
                                 customer) + [DEPOT]
                for customer in customers if customer != DEPOT),
               key=Route.distance)

    route = Route([], [Stacks(Problem().num_stacks)])

    # This slices off the DEPOT from the start and end, as that's not an actual
    # customer.
    for customer in islice(tour, 1, len(tour) - 1):
        route.insert_customer(customer, len(route.customers))

    return route


@lru_cache(None)
def shortest_segment(start: int,
                     between: FrozenSet[int],
                     end: int) -> List[int]:
    """
    Returns the shortest segment starting at start, going through between, and
    ending at end.
    """
    if len(between) == 0:
        return [start, end]

    return min((shortest_segment(start, between - {customer}, customer) + [end]
                for customer in between),
               key=Route.distance)
