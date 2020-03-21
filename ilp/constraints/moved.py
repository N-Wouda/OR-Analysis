from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def moved(problem: Problem, solver):
    """
    If an item in at an index is not the same before and after visiting a
    customer, it has been moved.
    """
    for customer_1 in range(problem.num_customers + 1):
        for stack in range(problem.num_stacks):
            for idx in range(MAX_STACK_INDEX):
                for destination in range(problem.num_customers + 1):
                    for origin in range(problem.num_customers + 1):
                        before_demand = solver.sum(solver.demand_binary[
                                                       customer_2, customer_1, stack, idx, destination, origin]
                                                   for customer_2 in range(problem.num_customers + 1))
                        after_demand = solver.sum(solver.demand_binary[
                                                      customer_1, customer_2, stack, idx, destination, origin]
                                                  for customer_2 in range(problem.num_customers + 1))
                        if before_demand is not after_demand:
                            solver.add_constraint(
                                solver.is_moved[customer_1, stack, idx] == 1)

                        before_pickup = solver.sum(solver.pickup_binary[
                                                       customer_2, customer_1, stack, idx, destination, origin]
                                                   for customer_2 in range(problem.num_customers + 1))
                        after_pickup = solver.sum(solver.pickup_binary[
                                                      customer_1, customer_2, stack, idx, destination, origin]
                                                  for customer_2 in range(problem.num_customers + 1))
                        if before_pickup is not after_pickup:
                            solver.add_constraint(
                                solver.is_moved[customer_1, stack, idx] == 1)
