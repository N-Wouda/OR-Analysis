from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def index_from_rear(problem: Problem, solver):
    """
    Ensures items are placed as close as possible to the rear.
    """
    for customer_1 in range(problem.num_customers + 1):
        for customer_2 in range(problem.num_customers + 1):
            for stack in range(problem.num_stacks):
                for idx in range(1, MAX_STACK_INDEX):
                    solver.add_constraint(
                        solver.sum(
                            solver.pickup_binary[customer_1,
                                                 customer_2,
                                                 stack,
                                                 idx - 1,
                                                 destination,
                                                 origin] +
                            solver.demand_binary[customer_1,
                                                 customer_2,
                                                 stack,
                                                 idx - 1,
                                                 destination,
                                                 origin]
                            for destination in range(problem.num_customers + 1)
                            for origin in range(problem.num_customers + 1))
                        <=
                        solver.sum(
                            solver.pickup_binary[customer_1,
                                                 customer_2,
                                                 stack,
                                                 idx,
                                                 destination,
                                                 origin] +
                            solver.demand_binary[customer_1,
                                                 customer_2,
                                                 stack,
                                                 idx,
                                                 destination,
                                                 origin]
                            for destination in range(problem.num_customers + 1)
                            for origin in range(problem.num_customers + 1))
                    )
