from copy import copy, deepcopy
from itertools import product

from heuristic.classes import Heap, Problem, Solution
from heuristic.constants import DEPOT
from heuristic.functions import remove_empty_routes


@remove_empty_routes
def cross_customer_exchange(solution: Solution) -> Solution:
    """
    Tries to remove crossing links between routes.
    TODO neighbourhood size
    TODO best move? First better?

    References
    ----------
    - Savelsbergh, Martin W. P. 1992. "The Vehicle Routing Problem with Time
      Windows: Minimizing Route Duration." *ORSA Journal on Computing* 4 (2):
      146-154.
    """
    improvements = Heap()

    for idx1, route1 in enumerate(solution.routes):
        for idx2, route2 in enumerate(solution.routes[idx1 + 1:], idx1 + 1):
            for first, second in product(enumerate(route1), enumerate(route2)):
                if _gain(route1, *first, route2, *second) >= 0:
                    continue

                c_idx1, _ = first
                c_idx2, _ = second

                first_customers = route1.customers[c_idx1 + 1:]
                second_customers = route2.customers[c_idx2 + 1:]

                new_route1 = deepcopy(route1)
                new_route2 = deepcopy(route2)

                for customer in first_customers:
                    new_route1.remove_customer(customer)

                for customer in second_customers:
                    new_route2.remove_customer(customer)

                if not new_route1.attempt_append_tail(second_customers):
                    continue

                if not new_route2.attempt_append_tail(first_customers):
                    continue

                current = route1.cost() + route2.cost()
                proposed = new_route1.cost() + new_route2.cost()

                if proposed < current:
                    improvements.push(proposed,
                                      (idx1, new_route1, idx2, new_route2))

    if len(improvements) != 0:
        _, (idx1, new_route1, idx2, new_route2) = improvements.pop()

        solution = copy(solution)

        solution.routes[idx1] = new_route1
        solution.routes[idx2] = new_route2

    return solution


def _gain(route1, idx1, customer1, route2, idx2, customer2):
    next1 = DEPOT if idx1 == len(route1) - 1 else route1.customers[idx1 + 1]
    next2 = DEPOT if idx2 == len(route2) - 1 else route2.customers[idx2 + 1]

    problem = Problem()

    gain = problem.distances[customer2 + 1, next1 + 1]
    gain += problem.distances[customer1 + 1, next2 + 1]

    gain -= problem.distances[customer1 + 1, next1 + 1]
    gain -= problem.distances[customer2 + 1, next2 + 1]

    return gain
