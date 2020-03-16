from heuristic.classes import Problem


def once_from_customer(problem: Problem, solver):
    """
    Ensures there is only one route from each customer.
    """
    for customer_1 in range(1, problem.num_customers):
        assignments = solver.sum(solver.edges[customer_1, customer_2]
                                 for customer_2 in
                                 range(problem.num_customers))
        solver.add_constraint(assignments == 1)
