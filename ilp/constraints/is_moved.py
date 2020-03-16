from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def is_moved(problem: Problem, solver):
    """
    Ensures an item at index can only be moved if items closer to the rear are
    handled as well.
    """
    for customer_1 in range(1, problem.num_customers):
        for stack in range(problem.num_stacks):
            for idx in range(MAX_STACK_INDEX):
                solver.add_constraint(
                    solver.is_moved[customer_1, stack, idx] <=
                    solver.is_moved[customer_1, stack, idx - 1]
                )
