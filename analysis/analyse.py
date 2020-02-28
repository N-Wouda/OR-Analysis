import glob
from datetime import datetime
from pathlib import Path

import pandas as pd

from heuristic.classes import Problem, Solution
from .functions import make_pivot_table
from .parameters import PARAMETERS
from .statistics import STATISTICS


def analyse(in_files: str, out_file: str):
    """
    Creates a summary file for the passed-in in-files, at the out-file
    location. This file summarises all passed-in instances.
    """
    file = Path(out_file)

    if file.exists():
        last_modified = file.lstat().st_mtime
        timestamp = datetime.fromtimestamp(last_modified)

        print(f"Printing {out_file} (last modified {timestamp})")
        instances = pd.read_csv(out_file, skipfooter=1, engine="python")
    else:
        instances = pd.DataFrame()

        for location in glob.iglob(in_files):
            problem = Problem.from_file(location, delimiter=',')
            sol = Solution.from_file(f"solutions/oracs_{problem.instance}.csv")

            instance = dict([(func.__name__, func(sol))
                             for func in PARAMETERS + STATISTICS])

            instances = instances.append(instance, ignore_index=True)

    report = make_pivot_table(instances)

    if not file.exists():
        report.to_csv(out_file)

    print(report)
