import numpy as np
from docplex.mp.model import Model
from typing import List

from heuristic.constants import DEPOT, MAX_STACK_INDEX
from heuristic.classes import Problem, Route, Solution, Stacks
from .constraints import CONSTRAINTS


def ilp(problem: Problem) -> Solution:
    """
    Solves the integer linear programming (ilp) formulation of the VRPSPD-H.
    Inspired by https://github.com/N-Wouda/PL-Heuristic/blob/master/ilp/ilp.py
    """
    with Model("VRPSPD-H") as solver:
        solver.parameters.threads = 8
        solver.time_limit = 172000 # slightly less than 2 days.

        problem.distances[problem.distances == 0] = np.inf

        _setup_decision_variables(problem, solver)
        _setup_objective(problem, solver)

        for constraint in CONSTRAINTS:
            constraint(problem, solver)

        solution = solver.solve()

        print(solver.solve_details)
        print(solver.solve_details.status_code)
        print(solution.solve_status)

        if solution is None:
            # There is not much that can be done in this case, so we raise an
            # error. Logging should pick this up, but it is nearly impossible
            # for this to happen due to the problem structure.
            raise ValueError("Infeasible!")

        return _to_state(problem, solver)


def _setup_objective(problem: Problem, solver: Model):
    """
    Specifies the optimisation objective.
    """
    routes_cost = solver.sum(
        problem.distances[i, j] * solver.edges[i, j]
        for i in range(problem.num_customers + 1)
        for j in range(problem.num_customers + 1))

    handling_cost = problem.handling_cost * solver.sum(
        solver.handling_cost[i, k, g]
        for i in range(1, problem.num_customers + 1)
        for k in range(problem.num_stacks)
        for g in range(MAX_STACK_INDEX))

    solver.minimize(routes_cost + handling_cost)


def _setup_decision_variables(problem: Problem, solver: Model):
    """
    Prepares and applies the decision variables to the model.
    """
    assignment_problem = [list(range(problem.num_customers + 1)),
                          list(range(problem.num_customers + 1)),
                          list(range(problem.num_stacks)),
                          list(range(MAX_STACK_INDEX)),
                          list(range(problem.num_customers + 1))]

    solver.edges = solver.binary_var_matrix(
        *assignment_problem[:2], name="edge_traveled")

    solver.sub_tour = solver.integer_var_list(assignment_problem[0],
                                              name="sub_tour",
                                              ub=problem.num_customers)

    solver.demand_binary = solver.var_multidict(solver.binary_vartype,
                                                assignment_problem,
                                                name="del_binary",
                                                lb=0,
                                                ub=1)

    solver.pickup_binary = solver.var_multidict(solver.binary_vartype,
                                                assignment_problem,
                                                name="pickup_binary",
                                                lb=0,
                                                ub=1)

    solver.is_moved = solver.binary_var_cube(*assignment_problem[1:4],
                                             name="is_moved")

    solver.handling_cost = solver.continuous_var_cube(*assignment_problem[1:4],
                                                      name="handling_costs",
                                                      lb=0)


def _to_state(problem: Problem, solver: Model) -> Solution:
    """"
    Converts ILP solution to solution type
    """
    def _route_append(route: List) -> List:
        for customer in range(1, problem.num_customers + 1):
            if solver.edges[route[-1], customer].solution_value == 1:
                route.append(customer)
                _route_append(route)
        return route

    ilp_routes = []
    for customer in range(problem.num_customers + 1):
        if solver.edges[0, customer].solution_value == 1:
            route = [customer]
            _route_append(route)
            route = [it - 1 for it in route]
            ilp_routes.append(route)

    routes = [Route(ilp_route, []) for ilp_route in ilp_routes]

    for route in routes:
        full_route = [DEPOT] + route.customers.to_list() + [DEPOT]
        full_route = [it + 1 for it in full_route]

        for idx_customer, customer in enumerate(full_route[:-1]):
            route.plan.append(Stacks(problem.num_stacks))
            for idx_stack in range(problem.num_stacks):
                stack = route.plan[-1][idx_stack]
                for index in range(MAX_STACK_INDEX):
                    for target in range(problem.num_customers + 1):
                        if solver.demand_binary[customer,
                                                full_route[idx_customer + 1],
                                                idx_stack,
                                                index,
                                                target].solution_value == 1:
                            stack.push_front(
                                problem.demands[target - 1])

                        if solver.pickup_binary[customer,
                                                full_route[idx_customer + 1],
                                                idx_stack,
                                                index,
                                                target].solution_value == 1:
                            stack.push_front(problem.pickups[target - 1])

    return Solution(routes, [])
