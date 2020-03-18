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
                    problem.demands[destination].volume *
                    solver.demand_binary[
                        customer_1, customer_2, stack, index, destination]
                    for destination in
                    range(problem.num_customers)
                    for index in range(MAX_STACK_INDEX))
                pickups = solver.sum(
                    problem.pickups[destination].volume *
                    solver.pickup_binary[
                        customer_1, customer_2, stack, index, destination]
                    for destination in
                    range(problem.num_customers)
                    for index in range(MAX_STACK_INDEX))

                solver.add_constraint(
                    demands + pickups <= problem.stack_capacity
                )
