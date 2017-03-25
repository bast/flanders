import random
import flanders
import numpy as np


def test_library():
    bounds = [-1.0, 1.0]
    num_points = 1000

    x_coordinates = np.zeros(num_points, dtype=np.float64)
    y_coordinates = np.zeros(num_points, dtype=np.float64)

    # generate random but reproducible data
    seed = 10
    random.seed(seed)
    for i in range(num_points):
        x_coordinates[i] = random.uniform(bounds[0], bounds[1])
        y_coordinates[i] = random.uniform(bounds[0], bounds[1])

    context = flanders.new_context(num_points, x_coordinates, y_coordinates)

    view_vectors = [(random.uniform(bounds[0], bounds[1]), random.uniform(bounds[0], bounds[1])) for _ in range(num_points)]
    view_angles = [random.uniform(10.0, 20.0) for _ in range(num_points)]

    # verify results without and with angles
    for use_angles in [False, True]:
        for i in range(num_points):
            index = flanders.find_neighbor(context,
                                           i,
                                           use_angles,
                                           [view_vectors[i][0], view_vectors[i][1]],
                                           view_angles[i])

            index_naive = flanders.search_neighbor_naive(i,
                                                       num_points,
                                                       x_coordinates,
                                                       y_coordinates,
                                                       use_angles,
                                                       [view_vectors[i][0], view_vectors[i][1]],
                                                       view_angles[i])
            assert index_naive == index

    flanders.free_context(context)
