from heuristic.classes import Problem, Solution
from heuristic.functions import create_single_customer_route


def initial_solution(problem: Problem) -> Solution:
    """
    Computes a dumb, initial solution to the passed-in problem instance. This
    solution assigns each customer to their own route. O(|customers|).
    """
    sol = Solution.empty(problem)

    for customer in range(problem.num_customers):
        route = create_single_customer_route(customer, problem)
        sol.routes.append(route)

    assert len(sol.routes) == problem.num_customers

    return sol
