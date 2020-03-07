from types import SimpleNamespace

from numpy.testing import assert_almost_equal

from heuristic.classes import Item, Stacks
from heuristic.constants import DEPOT


def get_problem(num_stacks, handling_cost):
    demands = [Item(5, DEPOT, 0), Item(4, DEPOT, 1), Item(3, DEPOT, 2)]
    pickups = [Item(2, 0, DEPOT), Item(3, 1, DEPOT), Item(0.5, 2, DEPOT)]

    return SimpleNamespace(demands=demands,
                           pickups=pickups,
                           num_stacks=num_stacks,
                           handling_cost=handling_cost)


def test_handling_costs_scale_with_parameter():
    problem = get_problem(1, 0)

    before = Stacks(problem.num_stacks)  # [d2, d1]
    before[0].stack.extend(problem.demands[:2])

    after = Stacks(problem.num_stacks)  # [p1, d2]
    after[0].stack.append(problem.demands[1])
    after[0].stack.append(problem.pickups[0])

    # No handling costs, so volume moved should not matter.
    assert_almost_equal(Stacks.cost(0, before, after, problem), 0)

    # We need to move d2 to get p1 into the front position, which costs
    # 1 * 4.
    problem.handling_cost = 1
    assert_almost_equal(Stacks.cost(0, before, after, problem), 4)

    # Same scenario, but now with a larger handling cost.
    problem.handling_cost = 4
    assert_almost_equal(Stacks.cost(0, before, after, problem), 16)


def test_moving_items_between_two_stacks():
    problem = get_problem(2, 4 / 3)

    before = Stacks(problem.num_stacks)  # [d1; d3, d2]
    before[0].stack.append(problem.demands[0])
    before[1].stack.extend(problem.demands[1:])

    after = Stacks(problem.num_stacks)  # [d2, d1; p3]
    after[0].stack.extend(problem.demands[:2])
    after[1].stack.append(problem.pickups[2])

    # We need to move d1 and d2 to get to the after configuration, which costs
    # (4 / 3) * 9 = 12.
    assert_almost_equal(Stacks.cost(2, before, after, problem), 12)


def test_after_stack_is_empty():
    problem = get_problem(2, 3)

    before = Stacks(problem.num_stacks)  # [d1; d3, d2]
    before[0].stack.append(problem.demands[0])
    before[1].stack.extend(problem.demands[1:])

    after = Stacks(problem.num_stacks)  # [d1, d2, p3; ]
    after[0].stack.append(problem.pickups[2])
    after[0].stack.append(problem.demands[1])
    after[0].stack.append(problem.demands[0])

    # We need to move d2 to get to the after configuration, which costs
    # 3 * 4 = 12.
    assert_almost_equal(Stacks.cost(2, before, after, problem), 12)

# TODO
