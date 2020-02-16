from heuristic.constants import DEPOT
from .classes import Item, LoadingPlan, Problem, Route, Solution, Stacks


def initial_solution(problem: Problem) -> Solution:
    sol = Solution.empty(problem)

    for customer in range(problem.num_customers):
        delivery = Item(problem.demands[customer], customer, customer)
        pickup = Item(problem.pickups[customer], customer, DEPOT)

        # After depot, and after customer: two configurations in total.
        stacks = [Stacks(problem.num_stacks) for _ in range(2)]

        stacks[0].shortest_stack().push_rear(delivery)
        stacks[1].shortest_stack().push_rear(pickup)

        sol.routes.append(Route([customer], LoadingPlan(stacks)))

    return sol
