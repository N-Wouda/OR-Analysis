from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def demand_origin(problem: Problem, solver):
    """
    Ensures demand origin is the depot = 0.
    """
    for customer_1 in range(problem.num_customers + 1):
        for customer_2 in range(problem.num_customers + 1):
            for stack in range(problem.num_stacks):
                for index in range(MAX_STACK_INDEX):
                    solver.add_constraint(solver.demand_binary[customer_1,
                                                               customer_2,
                                                               stack,
                                                               index,
                                                               0] == 0)
