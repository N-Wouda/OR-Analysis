from heuristic.classes import Problem
from heuristic.constants import M, MAX_STACK_INDEX


def stack_size(problem: Problem, solver):
    """
    Ensures stack size limit is not violated.
    """
    for customer_1 in range(1, problem.num_customers):
        for customer_2 in range(1, problem.num_customers):
            for stack in range(problem.num_stacks):
                demands = solver.sum(
                    solver.demand_volumes[customer_1, customer_2, stack, index]
                    for index in range(MAX_STACK_INDEX))
                pickups = solver.sum(
                    solver.pickup_volumes[customer_1, customer_2, stack, index]
                    for index in range(MAX_STACK_INDEX))

                solver.add_constraint(
                    demands + pickups <= problem.stack_capacity
                )
