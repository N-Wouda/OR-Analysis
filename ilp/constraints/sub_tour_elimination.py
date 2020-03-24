from heuristic.classes import Problem
#

def sub_tour_elimination(problem: Problem, solver):
    """
    Ensures all routes start and end at the depot.
    """
    for customer_1 in range(1, problem.num_customers + 1):
        for customer_2 in range(1, problem.num_customers + 1):
            if customer_1 is not customer_2:
                solver.add_constraint(
                    solver.sub_tour[customer_1] -
                    solver.sub_tour[customer_2] +
                    (problem.num_customers + 1) *
                    solver.edges[customer_1, customer_2] <=
                    problem.num_customers)
