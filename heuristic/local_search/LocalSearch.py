from copy import deepcopy

from numpy.random import RandomState

from heuristic.classes import Solution


class LocalSearch:

    def __init__(self):
        self._solution_operators = []
        self._route_operators = []

    def add_route_operator(self, operator):
        self._route_operators.append(operator)

    def add_solution_operator(self, operator):
        self._solution_operators.append(operator)

    def __call__(self, current: Solution, rnd_state: RandomState) -> Solution:
        improved = deepcopy(current)
        improved = self._improve(improved, self._solution_operators)

        for idx, route in enumerate(improved.routes):
            improved.routes[idx] = self._improve(route, self._route_operators)

        assert improved.objective() <= current.objective()
        return improved

    @staticmethod
    def _improve(entity, operators):
        """
        Generic local search procedure. Improves the passed-in entity using
        the given routes.
        """
        while True:
            for operator in operators:
                new_entity = operator(entity)

                if new_entity.cost() < entity.cost():
                    entity = new_entity
                    break
            else:
                return entity
