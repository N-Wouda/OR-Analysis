import numpy as np

from analysis.parameters import PARAMETERS
from analysis.statistics import STATISTICS
from .get_names import get_names
import pandas as pd


def make_pivot_table(data: pd.DataFrame) -> pd.DataFrame:
    values = get_names(STATISTICS)

    report = data.pivot_table(index=get_names(PARAMETERS),
                              values=values,
                              margins=True,
                              margins_name='Avg',
                              aggfunc=np.mean)

    return report.reindex(values, axis=1)
