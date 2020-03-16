from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def deliveries(problem: Problem, solver):
    """
    Ensures customer demands are met.
    """
    for customer_1 in range(1, problem.num_customers):
        assignments = solver.sum(
            solver.delivery_volumes[customer_2, customer_1, stack, index] -
            solver.delivery_volumes[customer_1, customer_2, stack, index]
            for customer_2 in range(problem.num_customers + 1)
            for stack in range(problem.num_stacks)
            for index in range(MAX_STACK_INDEX))
        solver.add_constraint(assignments == problem.demands[customer_1])
