from __future__ import annotations

from functools import lru_cache

import numpy as np


class Problem:
    instance: int

    capacity: float
    handling_cost: float

    num_customers: int
    num_stacks: int

    distances: np.ndarray
    demands: np.ndarray
    pickups: np.ndarray

    @property
    def stack_capacity(self):
        return self.capacity / self.num_stacks

    @property
    @lru_cache(1)
    def inverse_distances(self):
        """
        Returns the inverse (reciprocal) of the distances matrix. This is used
        as a measure of relatedness between customers.
        """
        distances = self.distances[1:, 1:]
        return np.reciprocal(distances, where=distances > 0)

    @classmethod
    def from_file(cls, location: str, **kwargs) -> Problem:
        """
        Sets-up a problem instance from the passed-in data file location. Any
        additional arguments are passed to ``numpy.genfromtxt``. For the assumed
        file format, see the data in `/data` - in particular the text file.

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

        problem.instance = int(data[0])

        problem.capacity = data[1]
        problem.handling_cost = data[3]

        problem.num_customers = int(data[2])
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
