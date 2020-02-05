from __future__ import annotations

from typing import Dict, List

from alns import State

from .Route import Route
from .TransportPlan import TransportPlan
from .Truck import Truck


class Solution(State):
    assignments: Dict[Truck, Route]
    routes: List[Route]
    plans: List[TransportPlan]

    def copy(self) -> Solution:
        """
        Returns a copy of the current Solution object.
        """
        return Solution()  # TODO

    def objective(self) -> float:
        """
        Evaluates the current solution.
        """
        pass  # TODO
