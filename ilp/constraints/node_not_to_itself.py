from heuristic.classes import Problem
#

def node_not_to_itself(problem: Problem, solver):
    """
    Shouldn't be needed since the cost of a route to itself is set to inf but
    might cause faster computation speed in the case of the feasible solution.
    """
    for customer in range(problem.num_customers + 1):
        solver.add_constraint(solver.edges[customer, customer] == 0)
