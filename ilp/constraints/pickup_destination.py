from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def pickup_destination(problem: Problem, solver):
    """
    Ensures pickup destination is depot = 0.
    """
    for customer_1 in range(problem.num_customers + 1):
        for customer_2 in range(problem.num_customers + 1):
            for stack in range(problem.num_stacks):
                for index in range(MAX_STACK_INDEX):
                    for destination in range(1, problem.num_customers + 1):
                        for origin in range(problem.num_customers):
                            solver.add_constraint(solver.pickup_binary[
                                                      customer_1,
                                                      customer_2,
                                                      stack,
                                                      index,
                                                      destination,
                                                      origin] == 0)
