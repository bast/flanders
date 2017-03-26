import random
from flanders import new_context, free_context, search_neighbor
import numpy as np


def test_library():
    bounds = [-1.0, 1.0]
    num_points = 1000
    num_batches = 10
    assert num_points % num_batches == 0
    batch_length = int(num_points / num_batches)

    x_coordinates = np.zeros(num_points, dtype=np.float64)
    y_coordinates = np.zeros(num_points, dtype=np.float64)

    # generate random but reproducible data
    seed = 10
    random.seed(seed)
    for i in range(num_points):
        x_coordinates[i] = random.uniform(bounds[0], bounds[1])
        y_coordinates[i] = random.uniform(bounds[0], bounds[1])

    context = new_context(num_points, x_coordinates, y_coordinates)

    vx = [random.uniform(bounds[0], bounds[1]) for _ in range(num_points)]
    vy = [random.uniform(bounds[0], bounds[1]) for _ in range(num_points)]
    angles_deg = [random.uniform(10.0, 20.0) for _ in range(num_points)]

    # verify results without angles
    for batch in range(num_batches):
        i = batch*batch_length
        j = batch*batch_length + batch_length
        ref_indices = range(i, j)
        indices_fast = search_neighbor(context,
                                       ref_indices=ref_indices)
        indices_naive = search_neighbor(context,
                                        ref_indices=ref_indices,
                                        naive=True)
        assert indices_fast == indices_naive

    # verify results with angles
    for batch in range(num_batches):
        i = batch*batch_length
        j = batch*batch_length + batch_length
        ref_indices = range(i, j)
        batch_vx = vx[i:j]
        batch_vy = vy[i:j]
        batch_angles_deg = angles_deg[i:j]
        indices_fast = search_neighbor(context,
                                       ref_indices=ref_indices,
                                       vx=batch_vx,
                                       vy=batch_vy,
                                       angles_deg=batch_angles_deg)
        indices_naive = search_neighbor(context,
                                        ref_indices=ref_indices,
                                        vx=batch_vx,
                                        vy=batch_vy,
                                        angles_deg=batch_angles_deg,
                                        naive=True)
        assert indices_fast == indices_naive

        # verify results with and free-style points
        x = [random.uniform(bounds[0], bounds[1]) for _ in range(batch_length)]
        y = [random.uniform(bounds[0], bounds[1]) for _ in range(batch_length)]

        indices_fast = search_neighbor(context,
                                       x=x,
                                       y=y,
                                       vx=batch_vx,
                                       vy=batch_vy,
                                       angles_deg=batch_angles_deg)
        indices_naive = search_neighbor(context,
                                        x=x,
                                        y=y,
                                        vx=batch_vx,
                                        vy=batch_vy,
                                        angles_deg=batch_angles_deg,
                                        naive=True)
        assert indices_fast == indices_naive

    free_context(context)
