from heuristic.classes import Problem
from heuristic.constants import M, MAX_STACK_INDEX


def edge_del_pick_dependence(problem: Problem, solver):
    """
    Ensures an edge to a customer has to be traveled if a pickup or delivery
    will take place at the customer. And that only there can only be 1 item
    at each index in each stack.
    """
    for customer_1 in range(problem.num_customers + 1):
        for customer_2 in range(problem.num_customers + 1):
            for stack in range(problem.num_stacks):
                for index in range(MAX_STACK_INDEX):
                    solver.add_constraint(
                        solver.sum(
                            solver.demand_binary[customer_1,
                                                 customer_2,
                                                 stack,
                                                 index,
                                                 destination,
                                                 0] for destination in
                            range(problem.num_customers + 1))
                        +
                        solver.sum(
                            solver.pickup_binary[customer_1,
                                                 customer_2,
                                                 stack,
                                                 index,
                                                 0,
                                                 origin] for origin in
                            range(problem.num_customers + 1))
                        <=
                        solver.edges[customer_1, customer_2]
                    )
