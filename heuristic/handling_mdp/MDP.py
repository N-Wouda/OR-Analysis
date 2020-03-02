from dataclasses import dataclass
from typing import List, Tuple

from heuristic.classes import Route
from heuristic.constants import NUM_BLOCKS
from .Block import Block

State = Tuple[Block]  # type alias


@dataclass
class MDP:
    states: List[State]
    route: Route

    def cost(self, from_state: State, to_state: State) -> float:
        assert len(from_state) == len(to_state) == NUM_BLOCKS

        return 0.
