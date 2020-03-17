from heuristic.classes import Problem
from heuristic.constants import M, MAX_STACK_INDEX


def demand_binary(problem: Problem, solver):
    """
    Sets the demand binary
    """
    for customer_1 in range(1, problem.num_customers):
        for customer_2 in range(1, problem.num_customers):
            for stack in range(problem.num_stacks):
                for index in range(MAX_STACK_INDEX):
                    solver.add_constraint(
                        solver.demand_volumes[customer_1,
                                              customer_2,
                                              stack,
                                              index]
                        <=
                        M * solver.demand_binary[customer_1,
                                                 customer_2,
                                                 stack,
                                                 index])
