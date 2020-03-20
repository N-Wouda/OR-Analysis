from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def moved_lifo(problem: Problem, solver):
    """
    Ensures an item at index can only be moved if items closer to the rear are
    handled as well.
    """
    for customer in range(1, problem.num_customers + 1):
        for stack in range(problem.num_stacks):
            for idx in range(1, MAX_STACK_INDEX):
                solver.add_constraint(
                    solver.is_moved[customer, stack, idx] <=
                    solver.is_moved[customer, stack, idx - 1]
                )
