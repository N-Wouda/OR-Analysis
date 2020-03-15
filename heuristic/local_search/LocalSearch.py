import numpy as np
from numpy.random import RandomState

from heuristic.classes import Problem, Route, Solution, Stacks
from heuristic.constants import DEPOT
from .held_karp import held_karp


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
        # TODO check all this *very* carefully, and expand upon it where needed
        #  - we should probably also do something about handling!
        if len(route.customers) <= 15:
            # This we can solve optimally using a dynamic programming based
            # algorithm (Held-Karp) for the TSP.
            new_route = self._held_karp(route)
        else:
            # This is constructive, using the Lin-Kernighan heuristic.
            new_route = self._lin_kernighan(route)

        return new_route

    @staticmethod
    def _held_karp(route: Route) -> Route:
        if len(route.customers) == 1:
            return route  # this is already optimal (single customer route).

        problem = Problem()

        customers = np.array([DEPOT] + route.customers.to_list())
        distances = problem.distances[np.ix_(customers + 1, customers + 1)]

        candidate = Route([], [Stacks(problem.num_stacks)])

        for customer in reversed(customers[held_karp(distances)]):
            if not candidate.can_insert(customer, len(candidate.customers)):
                return route  # candidate is infeasible.

            candidate.insert_customer(customer, len(candidate.customers))

        return candidate

    @staticmethod
    def _lin_kernighan(route: Route) -> Route:
        return route
