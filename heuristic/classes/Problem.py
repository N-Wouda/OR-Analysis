from __future__ import annotations
import numpy as np


class Problem:
    capacity: float
    handling_cost: float

    num_customers: int
    num_stacks: int

    distances: np.ndarray
    demands: np.ndarray
    pickups: np.ndarray

    @classmethod
    def from_file(cls, location: str, **kwargs) -> Problem:
        """
        Sets-up a problem instance from the passed-in data file location. Any
        additional arguments are passed to ``numpy.genfromtxt``.

        Parameters
        ----------
        location
            Data file location.
        kwargs
            Additional arguments.

        Returns
        -------
        Problem
            Problem instance for the data file.
        """
        data = np.genfromtxt(location, **kwargs)

        problem = cls()

        problem.capacity = data[1]
        problem.num_customers = int(data[2])
        problem.handling_cost = data[3]
        problem.num_stacks = int(data[4])

        # Distances include depot, so customers + 1
        distances = data[5:5 + (problem.num_customers + 1) ** 2]
        problem.distances = distances.reshape((problem.num_customers + 1,
                                               problem.num_customers + 1))

        demands = np.empty(problem.num_customers)
        pickups = np.empty(problem.num_customers)

        for idx in range(problem.num_customers):
            demands[idx] = data[-2 * problem.num_customers + 2 * idx]
            pickups[idx] = data[-2 * problem.num_customers + 2 * idx + 1]

        problem.demands = demands
        problem.pickups = pickups

        return problem
