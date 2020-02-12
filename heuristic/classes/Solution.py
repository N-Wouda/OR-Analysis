from __future__ import annotations

from copy import deepcopy
from typing import List

import matplotlib.pyplot as plt
from alns import State

from .Route import Route


class Solution(State):
    routes: List[Route]

    def copy(self) -> Solution:
        """
        Returns a copy of the current Solution object.
        """
        solution = Solution()
        solution.routes = deepcopy(self.routes)

        return solution

    def objective(self) -> float:
        """
        Evaluates the current solution.
        """
        return sum(route.cost() for route in self.routes)

    def plot(self):
        """
        Plots the current solution state.
        """
        # TODO
        plt.draw_if_interactive()

    @classmethod
    def from_file(cls, location: str) -> Solution:
        pass

    def to_file(self, location: str):
        pass
