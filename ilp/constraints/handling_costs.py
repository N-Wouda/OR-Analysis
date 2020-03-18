from heuristic.classes import Problem
from heuristic.constants import M, MAX_STACK_INDEX


def handling_costs(problem: Problem, solver):
    """
    Sets handling costs.
    """
    for customer_1 in range(1, problem.num_customers):
        for stack in range(problem.num_stacks):
            for index in range(MAX_STACK_INDEX):
                demand_cost = \
                    solver.sum(problem.demands[destination].volume *
                               solver.demand_binary[customer_1,
                                                    customer_2,
                                                    stack,
                                                    index,
                                                    destination]
                               for destination in range(problem.num_customers)
                               for customer_2 in range(problem.num_customers))

                pickup_cost = \
                    solver.sum(problem.pickups[destination].volume *
                               solver.pickup_binary[customer_1,
                                                    customer_2,
                                                    stack,
                                                    index,
                                                    destination]
                               for destination in range(problem.num_customers)
                               for customer_2 in range(problem.num_customers))

                not_moved_reduction = M * (
                        1 - solver.is_moved[customer_1, stack, index])

                handling_value = solver.max(demand_cost +
                                            pickup_cost - not_moved_reduction,
                                            0)

                solver.add_constraint(
                    solver.handling_cost[customer_1, stack, index]
                    >= handling_value)
