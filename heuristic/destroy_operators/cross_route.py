from numpy.random import RandomState

from heuristic.classes import Problem, Solution
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

    customer_set = set(range(problem.num_customers))

    removed_set = set()
    removed_list = list()

    selected_list = list()

    def select_candidate_and_neighbours(candidate: int):
        selected_list.append(candidate)

        route = destroyed.find_route(candidate)
        place_in_route = route.customers.index(candidate)

        if place_in_route > 0:
            selected_list.append(route.customers[place_in_route - 1])
        if place_in_route < len(route.customers) - 1:
            selected_list.append(route.customers[place_in_route + 1])

    def remove(candidate: int):
        removed_set.add(candidate)
        removed_list.append(candidate)

        route = destroyed.find_route(candidate)
        route.remove_customer(candidate)

        customer_set.remove(candidate)

        selected_list.remove(candidate)

    while len(removed_set) != to_remove:
        customer = rnd_state.choice(tuple(customer_set), replace=False)

        select_candidate_and_neighbours(customer)
        route = destroyed.find_route(customer)

        # Find the nearest customer that is not in the same route.
        for other in problem.nearest_customers[customer]:
            if other not in route and other not in removed_set:
                select_candidate_and_neighbours(other)
                break

        for selected in selected_list[:to_remove - len(removed_set)]:
            remove(selected)

    destroyed.unassigned = removed_list

    return destroyed
