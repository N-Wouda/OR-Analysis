from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def pickup_not_from_depot(problem: Problem, solver):
    """
    Ensures there are no pickups items comming from the depot.
    """
    for customer in range(problem.num_customers + 1):
        for stack in range(problem.num_stacks):
            for index in range(MAX_STACK_INDEX):
                for origin in range(problem.num_customers + 1):
                    solver.add_constraint(solver.pickup_binary[0,
                                                               customer,
                                                               stack,
                                                               index,
                                                               origin] == 0)
