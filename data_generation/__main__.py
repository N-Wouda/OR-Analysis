from scipy.spatial.distance import squareform
from numpy.random import random_sample


def main():
    instance_index = 50
    num_customers = 20
    min_distance = 0
    max_distance = 80

    vehicle_cap = 500  # small ~300, medium ~500, large ~ 800
    handling_cost = 5  # 5, 10, 15
    num_stacks = 2  # in small instances, only 1 and 2

    delivery_demand = (80 * random_sample(num_customers)).round(5)
    # random between 0 and 80, 0 and 120
    pickup_demand = (80 * random_sample(num_customers)).round(5)
    # random between 0 and 80, 0 and 120

    # number of draws needed to fill the upper triangle of a square matrix
    # minus the diagonal entries.
    num_draws = sum(x for x in range(num_customers + 1))

    distances = \
        (max_distance - min_distance) * random_sample(num_draws) + min_distance

    distance_matrix = squareform(distances).round(5)

    file = open('test_1.csv', 'w+')

    print(f"{instance_index},{vehicle_cap},{num_customers},{handling_cost},"
          f"{num_stacks},", end='', file=file)
    distance_matrix.flatten().tofile(file, sep=',')
    print(end=",", file=file)
    delivery_demand.tofile(file, sep=',')
    print(end=",", file=file)
    pickup_demand.tofile(file, sep=',')

    file.close()


if __name__ == "__main__":
    main()
