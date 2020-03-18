from copy import deepcopy

from numpy.random import RandomState

from heuristic.classes import Route, Solution


class LocalSearch:

    def __init__(self):
        self._operators = []

    def add_operator(self, operator):
        self._operators.append(operator)

    def __call__(self, current: Solution, rnd_state: RandomState) -> Solution:
        improved = deepcopy(current)

        for idx, route in enumerate(improved.routes):
            improved.routes[idx] = self._improve_route(route)

        assert improved.objective() <= current.objective()
        return improved

    def _improve_route(self, route: Route):
        while True:
            for operator in self._operators:
                new_route = operator(route)

                if new_route.cost() < route.cost():
                    route = new_route
                    break
            else:
                return route
