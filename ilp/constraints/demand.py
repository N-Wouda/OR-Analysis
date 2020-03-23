from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def demand(problem: Problem, solver):
    """
    Ensures each customer's demand is met.
    """
    for customer_1 in range(1, problem.num_customers + 1):

        demand_to_customer = solver.sum(
            solver.demand_binary[
                customer_2, customer_1, stack, index, customer_1]
            for customer_2 in range(problem.num_customers + 1)
            for stack in range(problem.num_stacks)
            for index in range(MAX_STACK_INDEX))

        solver.add_constraint(demand_to_customer == 1)
