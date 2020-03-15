import numpy as np
from numpy.random import RandomState

from heuristic.classes import Problem, Route, Solution, Stacks
from heuristic.constants import DEPOT
from .held_karp import held_karp


class LocalSearch:

    def __call__(self, current: Solution, rnd_state: RandomState) -> Solution:
        improved = current.copy()

        for idx, route in enumerate(improved.routes):
            improved.routes[idx] = self._improve_route(route)

        assert improved.objective() <= current.objective()
        return improved

    def _improve_route(self, route: Route):
        return route
        # TODO check all this *very* carefully, and expand upon it where needed
        #  - we should probably also do something about handling!
        self._opt_tour(route)

        return route

    @staticmethod
    def _opt_tour(route: Route):
        if len(route.customers) == 1 or len(route.customers) > 15:
            return  # this is either too small a route, or too large.

        problem = Problem()

        customers = np.array([DEPOT] + route.customers.to_list())
        distances = problem.distances[np.ix_(customers + 1, customers + 1)]

        candidate = Route([], [Stacks(problem.num_stacks)])

        for customer in reversed(customers[held_karp(distances)]):
            if not candidate.can_insert(customer, len(candidate.customers)):
                return  # infeasible route.

            candidate.insert_customer(customer, len(candidate.customers))

        if route.cost() < candidate.cost():
            # This can happen when the handling costs balloon - the routing is
            # weakly better, but that does not say much about the handling.
            return

        route.customers = candidate.customers
        route.invalidate_routing_cache()

        route.plan = candidate.plan
        route.invalidate_handling_cache()
