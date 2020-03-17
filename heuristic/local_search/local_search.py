from numpy.random import RandomState

from heuristic.classes import Route, Solution
from heuristic.constants import MAX_OPT_ROUTE_LENGTH
from .opt_route import opt_route


def local_search(current: Solution, rnd_state: RandomState) -> Solution:
    improved = current.copy()

    for idx, route in enumerate(improved.routes):
        new_route = _improve_route(route)

        if new_route.cost() < route.cost():
            improved.routes[idx] = new_route

    assert improved.objective() <= current.objective()
    return improved


def _improve_route(route: Route):
    # TODO should we really do routing optimally? This might hurt handling,
    #   although that does not appear to be a problem in practice.
    if len(route.customers) <= MAX_OPT_ROUTE_LENGTH:
        # This we can solve optimally (limiting routing cost).
        new_route = opt_route(route)
    else:
        # This should be *rare*, so there's no real problem skipping routing
        # optimisation here.
        new_route = route

    # TODO we should probably also do something about handling!
    #   e.g.:
    #   - fix up later pickup insertions in front of earlier pickups
    #     e.g. by re-inserting pickups for customers?
    #   - use empty or near empty stacks more?

    return new_route
