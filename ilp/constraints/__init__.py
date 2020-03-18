from .demand import demand
from .demand_binary import demand_binary
from .demand_moved_1 import demand_moved_1
from .demand_moved_2 import demand_moved_2
from .demands_from_depot import demands_from_depot
from .edge_del_pick_dependence import edge_del_pick_dependence
from .is_moved import is_moved
from .handling_costs import handling_costs
from .once_from_customer import once_from_customer
from .once_to_customer import once_to_customer
from .pickup import pickup
from .pickup_binary import pickup_binary
from .pickup_moved_1 import pickup_moved_1
from .pickup_moved_2 import pickup_moved_2
from .pickups_to_depot import pickups_to_depot
from .same_number_in_vehicle import same_number_in_vehicle
from .stack_size import stack_size
from .total_items import total_items

CONSTRAINTS = [
    demand,
    demands_from_depot,
    edge_del_pick_dependence,
    is_moved,
    handling_costs,
    once_from_customer,
    once_to_customer,
    pickup,
    pickups_to_depot,
    stack_size,
    same_number_in_vehicle,
    # total_items,
    # TODO
]
