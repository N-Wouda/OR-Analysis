from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def demand_not_to_depot(problem: Problem, solver):
    """
    Ensures there are no demand items going to the depot.
    """
    for customer in range(problem.num_customers + 1):
        for stack in range(problem.num_stacks):
            for index in range(MAX_STACK_INDEX):
                for origin in range(problem.num_customers + 1):
                    solver.add_constraint(solver.demand_binary[customer,
                                                               0,
                                                               stack,
                                                               index,
                                                               origin] == 0)
