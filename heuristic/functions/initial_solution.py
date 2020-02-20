from heuristic.classes import Problem, Solution
from heuristic.functions import create_single_customer_route


def initial_solution() -> Solution:
    """
    Computes a dumb, initial solution to the passed-in problem instance. This
    solution assigns each customer to their own route. O(|customers|).
    """
    problem = Problem()
    sol = Solution.empty()

    for customer in range(problem.num_customers):
        route = create_single_customer_route(customer)
        sol.routes.append(route)

    assert len(sol.routes) == problem.num_customers

    return sol
