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
        solver.parameters.threads = 20
        # solver.time_limit = 50

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
        for i in range(problem.num_customers + 1)
        for j in range(problem.num_customers + 1))

    handling_cost = problem.handling_cost * solver.sum(
        solver.handling_cost[i, k, g]
        for i in range(1, problem.num_customers + 1)
        for k in range(problem.num_stacks)
        for g in range(MAX_STACK_INDEX))

    unavoidable_costs = problem.handling_cost * (np.sum(demand.volume
                                                        for demand in
                                                        problem.demands)
                                                 + np.sum(pickup.volume
                                                          for pickup in
                                                          problem.pickups))

    solver.minimize(routes_cost + handling_cost - unavoidable_costs)


def _setup_decision_variables(problem: Problem, solver: Model):
    """
    Prepares and applies the decision variables to the model.
    """
    assignment_problem = [list(range(problem.num_customers + 1)),
                          list(range(problem.num_customers + 1)),
                          list(range(problem.num_stacks)),
                          list(range(MAX_STACK_INDEX)),
                          list(range(problem.num_customers + 1)),
                          list(range(problem.num_customers + 1))]

    solver.edges = solver.binary_var_matrix(
        *assignment_problem[:2], name="edge_traveled")

    solver.sub_tour = solver.binary_var_list(assignment_problem[0],
                                             name="sub_tour")

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
    print("edges")
    for customer_1 in range(problem.num_customers + 1):
        for customer_2 in range(problem.num_customers + 1):
            print(int(solver.edges[customer_1, customer_2].solution_value),
                  ' ',
                  end='')
        print()
    print()
    print("pickup_binaries")
    for customer_1 in range(problem.num_customers + 1):
        for customer_2 in range(problem.num_customers + 1):
            print(int(sum(
                solver.pickup_binary[
                    customer_1, customer_2, stack, index, 0, origin].
                    solution_value
                for origin in range(problem.num_customers + 1)
                for stack in range(problem.num_stacks) for index in
                range(MAX_STACK_INDEX))),
                ' ',
                end='')
        print()
    print("demand_binary")
    for customer_1 in range(problem.num_customers + 1):
        for customer_2 in range(problem.num_customers + 1):
            print(int(sum(
                solver.demand_binary[
                    customer_1, customer_2, stack, index, destination, 0].
                    solution_value
                for destination in range(problem.num_customers + 1)
                for stack in range(problem.num_stacks) for index in
                range(MAX_STACK_INDEX))),
                ' ',
                end='')
        print()
    print()
    print("demand destination")
    for customer_1 in range(problem.num_customers + 1):
        for customer_2 in range(problem.num_customers + 1):
            if solver.edges[customer_1, customer_2].solution_value == 1:
                print(f"From {customer_1} to {customer_2} destinations: ",
                      end='')
                for stack in range(problem._num_stacks):
                    for index in range(MAX_STACK_INDEX):
                        for destination in range(problem.num_customers + 1):
                            if solver.demand_binary[
                                customer_1, customer_2, stack, index, destination, 0].solution_value == 1:
                                print(f"{destination} ", end='')
                print()
    print()
    print("pickup origin")
    for customer_1 in range(problem.num_customers + 1):
        for customer_2 in range(problem.num_customers + 1):
            if solver.edges[customer_1, customer_2].solution_value == 1:
                print(f"From {customer_1} to {customer_2} origins: ", end='')
                for stack in range(problem._num_stacks):
                    for index in range(MAX_STACK_INDEX):
                        for origin in range(problem.num_customers + 1):
                            if solver.pickup_binary[
                                customer_1, customer_2, stack, index, 0, origin].solution_value == 1:
                                print(f"{origin} ", end='')
                print()

    print()
    print("items index")
    for customer_1 in range(problem.num_customers + 1):
        for customer_2 in range(problem.num_customers + 1):
            if solver.edges[customer_1, customer_2].solution_value == 1:
                print(f"From {customer_1} to {customer_2}: ",
                      end='')
                for stack in range(problem._num_stacks):
                    print(f"in stack: {stack} ", end='')
                    for index in range(MAX_STACK_INDEX):
                        for destination in range(problem.num_customers + 1):
                            if solver.demand_binary[
                                customer_1, customer_2, stack, index, destination, 0].solution_value == 1:
                                print(f"index: {index} ", end='')
                                print(f"d{destination} ", end='')
                                for origin in range(1, problem.num_customers + 1):
                                    if solver.demand_binary[customer_1, customer_2, stack, index, destination, origin].solution_value == 1:
                                        print(f"error: origin {origin}")

                        for origin in range(problem.num_customers + 1):
                            if solver.pickup_binary[
                                customer_1, customer_2, stack, index, 0, origin].solution_value == 1:
                                print(f"index: {index} ", end="")
                                print(f"p{origin} ", end='')
                            for destination in range(1, problem.num_customers + 1):
                                if solver.pickup_binary[customer_1, customer_2, stack, index, destination, origin].solution_value == 1:
                                    print(f"error destination {destination} ")

                print()
    print()
    print("is moved")
    # bij 0 telt niet mee
    for customer_1 in range(problem.num_customers + 1):
        print(f"{customer_1}: ", end='')
        for stack in range(problem.num_stacks):
            print(f"stack: {stack}, indexes changed: ", end='')
            for index in range(MAX_STACK_INDEX):
                if solver.is_moved[customer_1, stack, index].solution_value == 1:
                    print(f"{index} ", end='')
            print()
    print()
    print("test wrong destinations")
    for customer_1 in range(problem.num_customers + 1):
        for customer_2 in range(problem.num_customers + 1):
            for stack in range(problem.num_stacks):
                for index in range(MAX_STACK_INDEX):
                    for destination in range(problem.num_customers + 1):
                        for origin in range(problem.num_customers + 1):
                            if origin is not 0:
                                if solver.demand_binary[customer_1, customer_2, stack, index, destination, origin].solution_value is not 0:
                                    print(customer_1, customer_2, stack, index, destination, origin)
    print()
    print("test wrong origins")
    for customer_1 in range(problem.num_customers + 1):
        for customer_2 in range(problem.num_customers + 1):
            for stack in range(problem.num_stacks):
                for index in range(MAX_STACK_INDEX):
                    for destination in range(problem.num_customers + 1):
                        for origin in range(problem.num_customers + 1):
                            if destination is not 0:
                                if solver.pickup_binary[
                                    customer_1, customer_2, stack, index, destination, origin].solution_value is not 0:
                                    print(customer_1, customer_2, stack, index,
                                          destination, origin)
    print()
    print("handling costs: ")
    for customer_1 in range(1, problem.num_customers + 1):
        print(f"{customer_1}: ", end='')
        for stack in range(problem.num_stacks):
            print(f"stack: {stack}, handling cost: ", end='')
            for index in range(MAX_STACK_INDEX):
                print(f"index {index}: {solver.handling_cost[customer_1, stack, index].solution_value} ", end='')
            print()
    print("stack_capacity: ", problem.stack_capacity)
    print("demands: ", problem._demands)
    print("pickups: ", problem._pickups)
    print("distances: ")
    for customer_1 in range(problem.num_customers + 1):
        for customer_2 in range(problem.num_customers + 1):
            print(problem.distances[customer_1, customer_2], " ", end='')
        print()
    num_routes = sum(solver.edges[0, customer].solution_value for customer in
                     range(problem.num_customers + 1))
    print(num_routes)

    def _route_append(route: List) -> List:
        for customer in range(1, problem.num_customers + 1):
            if solver.edges[route[-1], customer].solution_value == 1:
                route.append(customer)
                _route_append(route)
        return route

    routes = []
    for customer in range(problem.num_customers + 1):
        if solver.edges[0, customer].solution_value == 1:
            route = [0, customer]
            _route_append(route)
            route.append(0)
            routes.append(route)
    print(routes)
    # for route in routes:
    #     print(route)
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
