from heuristic.constants import DEPOT
from .classes import Item, Problem, Route, Solution, Stacks


def initial_solution(problem: Problem) -> Solution:
    """
    Computes a dumb, initial solution to the passed-in problem instance. This
    solution assigns each customer to their own route, as ``[DEPOT, customer,
    DEPOT]``.
    """
    sol = Solution.empty(problem)

    for customer in range(problem.num_customers):
        delivery = Item(problem.demands[customer], DEPOT, customer)
        pickup = Item(problem.pickups[customer], customer, DEPOT)

        # After depot, and after customer: two configurations in total.
        stacks = [Stacks(problem.num_stacks) for _ in range(2)]

        # We place the deliveries and pickups in the shortest stack - this
        # does not really matter much, as each stack is empty at this point
        # anyway.
        stacks[0].shortest_stack().push_rear(delivery)
        stacks[1].shortest_stack().push_rear(pickup)

        sol.routes.append(Route([customer], stacks))

    assert len(sol.routes) == problem.num_customers

    return sol
