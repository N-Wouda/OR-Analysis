from dataclasses import dataclass
from typing import List


@dataclass
class Block:
    customers: List[int]
