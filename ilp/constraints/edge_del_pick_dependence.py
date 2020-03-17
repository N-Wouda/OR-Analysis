from heuristic.classes import Problem
from heuristic.constants import M, MAX_STACK_INDEX


def edge_del_pick_dependence(problem: Problem, solver):
    """
    Ensures an edge to a customer has to be traveled if a pickup or delivery
    will take place at the customer.
    """
    for customer_1 in range(problem.num_customers):
        for customer_2 in range(problem.num_customers):
            for stack in range(problem.num_stacks):
                for index in range(MAX_STACK_INDEX):
                    solver.add_constraint(
                        solver.demand_binary[customer_1,
                                             customer_2,
                                             stack,
                                             index]
                        +
                        solver.pickup_binary[customer_1,
                                             customer_2,
                                             stack,
                                             index]
                        <=
                        solver.edges[customer_1, customer_2]
                    )
