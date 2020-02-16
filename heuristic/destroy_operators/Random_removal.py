from ..classes import Solution
from random import randrange


def random_removal(old_solution: Solution, q: int) -> Solution:
    """
    Copies the old solution, randomly removes q customers from the solution and
    places them in the unassigned list.
    """
    solution = old_solution.copy()

    for idx in range(q):
        random_route = randrange(0, len(solution.routes))
        random_customer = randrange(0, len(solution.routes[random_route]))

        removed_customer = solution.routes[random_route].customers.\
            pop(random_customer)

        solution.unassigned.append(removed_customer)

    return solution
