from heuristic.classes import Problem
from heuristic.constants import M, MAX_STACK_INDEX


def demand_moved_2(problem: Problem, solver):
    """
    Ensures the moved variable is 1 if the delivery volume is higher after
    visiting a customer for every index in every stack.
    """
    for customer_1 in range(1, problem.num_customers):
        for stack in range(problem.num_stacks):
            for index in range(MAX_STACK_INDEX):
                before = solver.sum(
                    solver.demand_volumes[customer_1,
                                          customer_2,
                                          stack,
                                          index]
                    for customer_2 in range(problem.num_customers))

                after = solver.sum(
                    solver.demand_volumes[customer_2,
                                          customer_1,
                                          stack,
                                          index]
                    for customer_2 in range(problem.num_customers))

                solver.add_constraint(after - before <= M * solver.is_moved[
                    customer_1, stack, index])
