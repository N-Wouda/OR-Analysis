import numpy as np
from docplex.mp.model import Model
from typing import List

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

        print(solver.objective_value)
        print()

        return _to_state(problem, solver)


def _setup_objective(problem: Problem, solver: Model):
    """
    Specifies the optimisation objective.
    """
    routes_cost = solver.sum(
        problem.distances[i, j] * solver.edges[i, j]
        for i in range(problem.num_customers)
        for j in range(problem.num_customers))

    handling_cost = solver.sum(solver.handling_cost[i, k, g]
                               for i in range(1, problem.num_customers)
                               for k in range(problem.num_stacks)
                               for g in range(MAX_STACK_INDEX))

    del_cost = problem.handling_cost * np.sum(demand.volume
                                              for demand in problem.demands)

    solver.minimize(
        routes_cost + problem.handling_cost * handling_cost - del_cost)


def _setup_decision_variables(problem: Problem, solver: Model):
    """
    Prepares and applies the decision variables to the model.
    """
    assignment_problem = [list(range(problem.num_customers + 1)),
                          list(range(problem.num_customers + 1)),
                          list(range(problem.num_stacks)),
                          list(range(MAX_STACK_INDEX)),
                          list(range(problem.num_customers))]

    solver.edges = solver.binary_var_matrix(
        *assignment_problem[:2], name="edge_traveled")

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
                                                      name="handling_costs")


def _to_state(problem: Problem, solver: Model) -> Solution:
    print("edges")
    for customer_1 in range(problem.num_customers):
        for customer_2 in range(problem.num_customers):
            print(solver.edges[customer_1, customer_2].solution_value,
                  ' ',
                  end='')
        print()
    print()
    print("pickup_binaries")
    for customer_1 in range(problem.num_customers):
        for customer_2 in range(problem.num_customers):
            print(round(sum(
                solver.pickup_binary[
                    customer_1, customer_2, stack, index, destination].
                    solution_value
                for destination in range(problem.num_customers)
                for stack in range(problem.num_stacks) for index in
                range(MAX_STACK_INDEX)), 2),
                ' ',
                end='')
        print()
    print()
    print("demand_binary")
    for customer_1 in range(problem.num_customers):
        for customer_2 in range(problem.num_customers):
            print(round(sum(
                solver.demand_binary[
                    customer_1, customer_2, stack, index, destination].
                    solution_value
                for destination in range(problem.num_customers)
                for stack in range(problem.num_stacks) for index in
                range(MAX_STACK_INDEX)), 2),
                ' ',
                end='')
        print()
    print()
    print("is moved")
    for customer_1 in range(problem.num_customers):
        print(round(sum(solver.is_moved[
                            customer_1, stack, index].solution_value
                        for stack in range(problem.num_stacks) for index in
                        range(MAX_STACK_INDEX)), 2),
              ' ',
              end='')
        print()
    print()
    print("stack_capacity: ", problem.stack_capacity)
    print("demands: ", problem._demands)
    print("pickups: ", problem._pickups)

    num_routes = sum(solver.edges[0, customer].solution_value for customer in
                     range(problem.num_customers))
    print(num_routes)

    def _route_append(route: List) -> List:
        for customer in range(1, problem.num_customers):
            if solver.edges[route[-1], customer].solution_value == 1:
                route.append(customer)
                _route_append(route)
        return route

    routes = []
    for customer in range(problem.num_customers):
        if solver.edges[0, customer].solution_value == 1:
            route = [0, customer]
            _route_append(route)
            route.append(0)
            routes.append(route)
    print(routes)
    # for route in routes:
    #     plan = []
    #     print(route)
    #     for customer_idx, customer in enumerate(route[:-2]):
    #         # print(customer)
    #         for stack in range(problem.num_stacks):
    #             layout = []
    #             for index in range(MAX_STACK_INDEX):
    #                 print(solver.demand_binary[customer,
    #                                            route[customer_idx + 1],
    #                                            stack,
    #                                            index].solution_value)
                # for index in range(MAX_STACK_INDEX):
                #     if solver.demand_binary[customer,
                #                             route[customer_idx + 1],
                #                             stack,
                #                             index].solution_value == 1:
                #         owner = list(problem._demands).index(round(
                #             solver.demand_volumes[customer,
                #                                   route[customer_idx + 1],
                #                                   stack,
                #                                   index].solution_value, 5))
                #
                #         layout.append(f"d{owner}")
                #
                #     if solver.pickup_binary[customer,
                #                             route[customer_idx + 1],
                #                             stack,
                #                             index].solution_value == 1:
                #         owner = list(problem._pickups).index(
                #             round(solver.pickup_volumes
                #                   [customer,
                #                    route[customer_idx + 1],
                #                    stack,
                #                    index].solution_value), 5)
                #
                #         layout.append(f"p{owner}")
                # print(layout)
        # print(plan)

    pass
