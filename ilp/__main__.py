import sys

from heuristic.classes import Problem, Solution
from .ilp import ilp

problem = Problem.from_file(sys.argv[1], delimiter=',')

solution = ilp(problem)

# write_result(result, MethodType.ILP, sys.argv[1], sys.argv[2])
solution.to_file(f"solutions/ILP_{problem.instance}.csv")
