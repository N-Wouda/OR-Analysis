from ..classes import Solution
from random import randrange


def random_repair(old_solution: Solution) -> Solution:
    """
    Makes a copy of the current solution. Randomly selects customer from the
    unassigned list and places them in a random location in a random route.
    Returns the resulting solution.
    """
    solution = old_solution.copy()

    while solution.unassigned:
        idx = randrange(0, len(solution.unassigned))
        rand_customer = solution.unassigned.pop(idx)

        random_route_idx = randrange(0, len(solution.routes))
        random_loc_idx = \
            randrange(0, len(solution.routes[random_route_idx].customers))

        solution.routes[random_route_idx].\
            customers.insert(random_loc_idx, rand_customer)

    return solution
