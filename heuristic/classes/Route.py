from typing import List

from .TransportPlan import TransportPlan
from .Truck import Truck


class Route:
    legs: List
    plan: TransportPlan
    truck: Truck
