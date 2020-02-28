import glob
import sys

import pandas as pd
import numpy as np

from heuristic.classes import Problem, Solution
from .statistics import STATISTICS

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('precision', 2)


def main():
    """
    Prints several statistics of each instance and descriptive
    statistics of the instances overall to a file.
    """
    if len(sys.argv) < 2:
        raise ValueError(f"{sys.argv[0]}: expected file location.")

    instances = pd.DataFrame()

    for file in glob.glob(sys.argv[1]):
        problem = Problem.from_file(file, delimiter=',')
        solution = Solution.from_file(f"solutions/oracs_{problem.instance}.csv")

        instance = dict([statistic(solution) for statistic in STATISTICS])
        instances = instances.append(instance, ignore_index=True)

    instances.set_index('instance', inplace=True)
    instances.sort_index(inplace=True)

    instances = pd.pivot_table(instances, index=['instance'])
    pivoted_instances = pd.pivot_table(instances,
                                       margins=True,
                                       margins_name='average',
                                       index=['num_customers', 'handling'],
                                       values=list(instances),
                                       aggfunc=[np.mean, min, max])

    instances.to_csv("statistics/summary.csv", sep='\t')
    pivoted_instances.to_csv("statistics/summary.csv", mode='a', sep='\t')

    print(instances)
    print(pivoted_instances)


if __name__ == "__main__":
    main()
