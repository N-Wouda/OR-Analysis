from heuristic.classes import Problem
from heuristic.constants import M, MAX_STACK_INDEX


def stack_size(problem: Problem, solver):
    """
    Ensures stack size limit is not violated.
    """
    for customer_1 in range(1, problem.num_customers + 1):
        for customer_2 in range(1, problem.num_customers + 1):
            for stack in range(problem.num_stacks):
                demands = solver.sum(
                    problem.demands[destination - 1].volume *
                    solver.demand_binary[
                        customer_1, customer_2, stack, index, destination, 0]
                    for index in range(MAX_STACK_INDEX)
                    for destination in range(problem.num_customers + 1))
                pickups = solver.sum(
                    problem.pickups[origin - 1].volume *
                    solver.pickup_binary[
                        customer_1, customer_2, stack, index, 0, origin]
                    for index in range(MAX_STACK_INDEX)
                    for origin in range(problem.num_customers + 1))

                solver.add_constraint(
                    demands + pickups <= problem.stack_capacity
                )
