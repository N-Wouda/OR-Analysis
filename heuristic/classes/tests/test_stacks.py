from types import SimpleNamespace

from numpy.testing import assert_almost_equal

from heuristic.classes import Item, Stacks
from heuristic.constants import DEPOT


def test_stacks_handling_costs_scales_with_parameter():
    problem = SimpleNamespace(demands=[Item(5, DEPOT, 0), Item(4, DEPOT, 1)],
                              pickups=[Item(2, 0, DEPOT), Item(3, 1, DEPOT)],
                              num_stacks=1,
                              handling_cost=0)

    before = Stacks(problem.num_stacks)  # [d2, d1]
    before[0].stack.extend(problem.demands)

    after = Stacks(problem.num_stacks)  # [p1, d2]
    after[0].stack.append(problem.demands[1])
    after[0].stack.append(problem.pickups[0])

    # No handling costs, so volume moved should not matter
    assert_almost_equal(Stacks.cost(0, before, after, problem), 0)

    # We need to move d2 to get p1 into the front position, which costs
    # 1 * 4.
    problem.handling_cost = 1
    assert_almost_equal(Stacks.cost(0, before, after, problem), 4)

    # TODO
