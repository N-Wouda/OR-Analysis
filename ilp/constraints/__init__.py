from .demand import demand
from .demand_inventory import demand_inventory
from .demand_origin import demand_origin
from .demand_sum_from_depot import demand_sum_from_depot
from .edge_del_pick_dependence import edge_del_pick_dependence
from .handling_costs import handling_costs
from .index_from_rear import index_from_rear
from .moved import moved
from .moved_lifo import moved_lifo
from .once_from_customer import once_from_customer
from .once_to_customer import once_to_customer
from .pickup import pickup
from .pickup_destination import pickup_destination
from .pickup_inventory import pickup_inventory
from .pickups_sum_to_depot import pickups_sum_to_depot
from .same_number_in_vehicle import same_number_in_vehicle
from .stack_size import stack_size
from .sub_tour_elimination import sub_tour_elimination
from .total_items import total_items

CONSTRAINTS = [
    demand,
    demand_inventory,
    demand_origin,
    # demand_sum_from_depot,
    edge_del_pick_dependence,
    handling_costs,
    index_from_rear,
    moved,
    moved_lifo,
    once_from_customer,
    once_to_customer,
    pickup,
    pickup_destination,
    pickup_inventory,
    # pickups_sum_to_depot,
    # same_number_in_vehicle,
    stack_size,
    sub_tour_elimination,
    total_items,
]
