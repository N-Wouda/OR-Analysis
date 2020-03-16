from numpy.random import RandomState

from heuristic.classes import Route, Solution
from heuristic.constants import MAX_OPT_ROUTE_LENGTH
from .opt_route import opt_route


class LocalSearch:

    def __call__(self, current: Solution, rnd_state: RandomState) -> Solution:
        improved = current.copy()

        for idx, route in enumerate(improved.routes):
            new_route = self._improve_route(route)

            if new_route.cost() < route.cost():
                improved.routes[idx] = new_route

        assert improved.objective() <= current.objective()
        return improved

    def _improve_route(self, route: Route):
        if len(route.customers) <= MAX_OPT_ROUTE_LENGTH:
            # This we can solve optimally (limiting routing cost). Very few
            # solutions have longer routes than the maximum route length, so
            # this is used in almost all cases.
            return opt_route(route)

        # TODO we should probably also do something about handling!

        return route
