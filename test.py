import random
from flanders import new_context, free_context, search_neighbor_by_index, search_neighbor
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

    context = new_context(num_points, x_coordinates, y_coordinates)

    view_vectors = [(random.uniform(bounds[0], bounds[1]), random.uniform(bounds[0], bounds[1])) for _ in range(num_points)]
    view_angles = [random.uniform(10.0, 20.0) for _ in range(num_points)]

    # verify results without angles
    for i in range(num_points):
        i_f = search_neighbor_by_index(context,
                                       ref_index=i)
        i_n = search_neighbor_by_index(context,
                                       ref_index=i,
                                       naive=True)
        assert i_f == i_n

    # verify results with angles
    for i in range(num_points):
        i_f = search_neighbor_by_index(context,
                                       ref_index=i,
                                       view_vector=[view_vectors[i][0], view_vectors[i][1]],
                                       view_angle_deg=view_angles[i])
        i_n = search_neighbor_by_index(context,
                                       ref_index=i,
                                       view_vector=[view_vectors[i][0], view_vectors[i][1]],
                                       view_angle_deg=view_angles[i],
                                       naive=True)
        assert i_f == i_n

    # verify results with and free-style points
    for i in range(num_points):
        x = random.uniform(bounds[0], bounds[1])
        y = random.uniform(bounds[0], bounds[1])
        i_f = search_neighbor(context,
                              x=x,
                              y=y,
                              view_vector=[view_vectors[i][0], view_vectors[i][1]],
                              view_angle_deg=view_angles[i])
        i_n = search_neighbor(context,
                              x=x,
                              y=y,
                              view_vector=[view_vectors[i][0], view_vectors[i][1]],
                              view_angle_deg=view_angles[i],
                              naive=True)
        assert i_f == i_n

    free_context(context)
