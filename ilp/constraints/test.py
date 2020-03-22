from heuristic.classes import Problem


def test(problem: Problem, solver):
    """
    Sets the maximum number of routes.
    """
    sum_routes_from = solver.sum(solver.edges[0, customer_2]
                                 for customer_2 in
                                 range(problem.num_customers + 1))
    solver.add_constraint(sum_routes_from <= 2)
