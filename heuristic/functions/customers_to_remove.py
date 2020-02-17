from ..constants import DEGREE_OF_DESTRUCTION
from ..classes import Problem


def customers_to_remove(problem: Problem):
    return int(Problem.num_customers * DEGREE_OF_DESTRUCTION)
