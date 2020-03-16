
import numpy as np
from docplex.mp.model import Model

from heuristic.constants import M, MAX_STACK_INDEX
from heuristic.classes import Problem, Solution
from .constraints import CONSTRAINTS


def ilp(problem: Problem) -> Solution:
    """
    Solves the integer linear programming (ilp) formulation of the VRPSPD-H.
    From https://github.com/N-Wouda/PL-Heuristic/blob/master/ilp/ilp.py
    """
    with Model("VRPSPD-H") as solver:
        solver.parameters.threads = 8

        _setup_decision_variables(problem, solver)
        _setup_objective(problem, solver)

        solver.B = 1000000

        for constraint in CONSTRAINTS:
            constraint(problem, solver)

        solution = solver.solve()

        if solution is None:
            # There is not much that can be done in this case, so we raise an
            # error. Logging should pick this up, but it is nearly impossible
            # for this to happen due to the problem structure.
            raise ValueError("Infeasible!")

        # return _to_state(problem, solver)


def _setup_objective(problem: Problem, solver: Model):
    """
    Specifies the optimisation objective.
    """
    routes_cost = solver.sum(
        problem.distances[i, j] * solver.edges[i, j]
        for i in range(problem.num_customers)
        for j in range(problem.num_customers))

    handling_cost = solver.sum(solver.handling[i, k, g]
                               for i in range(1, problem.num_customers)
                               for k in range(problem.num_stacks)
                               for g in range(MAX_STACK_INDEX))

    del_cost = problem.handling_cost * sum(problem.demands)

    solver.minimize(routes_cost +
                    problem.handling_cost * handling_cost
                    - del_cost)


def _setup_decision_variables(problem: Problem, solver: Model):
    """
    Prepares and applies the decision variables to the model.
    """
    assignment_problem = [list(range(problem.num_customers)),
                          list(range(problem.num_customers)),
                          list(range(problem.num_stacks)),
                          list(range(MAX_STACK_INDEX))]

    solver.edges = solver.binary_var_matrix(
        *assignment_problem[:1], name="edge_traveled")

    solver.delivery_volumes = solver.var_multidict(solver.continuous_vartype,
                                                   assignment_problem,
                                                   name="del_volume",
                                                   lb=0)

    solver.pickup_volumes = solver.var_multidict(solver.continuous_vartype,
                                                 assignment_problem,
                                                 name="pickup_volume",
                                                 lb=0)


def _to_state(problem: Problem, solver: Model) -> Solution:
    pass
