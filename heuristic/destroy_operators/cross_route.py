from numpy.random import RandomState

from heuristic.classes import Problem, Route, Solution
from heuristic.functions import customers_to_remove, remove_empty_routes


@remove_empty_routes
def cross_route(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Selects two customers that are nearest to each other and their neighbours
    and removes them from the solution.
    See ``customers_to_remove`` for the degree of destruction done.

    Similar to cross route removal in Hornstra et al. (2020).
    """
    problem = Problem()
    destroyed = current.copy()

    to_remove = customers_to_remove(problem.num_customers)

    customers = set(range(problem.num_customers))
    removed = set()

    while len(removed) < to_remove:
        candidate = rnd_state.choice(tuple(customers))

        route_candidate = destroyed.find_route(candidate)
        selected_1 = \
            _select_candidate_and_neighbours(route_candidate, candidate)
        route_other = []
        selected_2 = []

        # Find the nearest customer that is not in the same route.
        for other in problem.nearest_customers[candidate]:
            if other not in route_candidate and other not in removed:
                route_other = destroyed.find_route(other)
                selected_2 = \
                    _select_candidate_and_neighbours(route_other, other)
                break

        _remove(route_candidate, removed, customers, selected_1)
        _remove(route_other, removed, customers, selected_2)

    destroyed.unassigned = list(removed)

    return destroyed


def _select_candidate_and_neighbours(route: Route, candidate: int) -> list:
    idx = route.customers.index(candidate)
    selected = []

    for customer in route.customers[max(idx - 1, 0):
                                    min(idx + 2, len(route.customers))]:
        selected.append(customer)

    return selected


def _remove(route: Route, removed_set: set, customers: set, selected: list):
    for candidate in selected:
        removed_set.add(candidate)
        route.remove_customer(candidate)
        customers.remove(candidate)
