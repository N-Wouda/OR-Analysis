import glob
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from heuristic.classes import Problem, Solution
from .parameters import PARAMETERS
from .statistics import STATISTICS

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('precision', 2)


def main():
    if len(sys.argv) < 3:
        raise ValueError(f"{sys.argv[0]}: expected in- and output files.")

    file = Path(sys.argv[2])

    if file.exists():
        last_modified = file.lstat().st_mtime
        timestamp = datetime.fromtimestamp(last_modified)

        print(f"Printing {sys.argv[2]} (last modified {timestamp})")
        instances = pd.read_csv(sys.argv[2])
    else:
        instances = pd.DataFrame()

        for location in glob.iglob(sys.argv[1]):
            problem = Problem.from_file(location, delimiter=',')
            sol = Solution.from_file(f"solutions/oracs_{problem.instance}.csv")

            instance = dict([(func.__name__, func(sol))
                             for func in PARAMETERS + STATISTICS])

            instances = instances.append(instance, ignore_index=True)

    values = [func.__name__ for func in STATISTICS]
    indices = [func.__name__ for func in PARAMETERS]

    report = instances.pivot_table(index=indices,
                                   values=values,
                                   margins=True,
                                   margins_name='Avg',
                                   aggfunc=np.mean)
    report = report.reindex(values, axis=1)

    if not file.exists():
        report.to_csv(sys.argv[2])

    print(report)


if __name__ == "__main__":
    main()
