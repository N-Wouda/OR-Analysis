from ..constants import DEGREE_OF_DESTRUCTION
from ..classes import Problem
from numpy.random import RandomState


def customers_to_remove():
    return int(Problem.num_customers * DEGREE_OF_DESTRUCTION)
