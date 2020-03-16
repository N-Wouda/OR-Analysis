from heuristic.classes import Problem


def once_to_customer(problem: Problem, solver):
    """
    Ensures there is only one route to each customer.
    """
    for customer_1 in range(1, problem.num_customers):
        assignments = solver.sum(solver.edges[customer_2, customer_1]
                                 for customer_2 in
                                 range(problem.num_customers))
        solver.add_constraint(assignments == 1)
