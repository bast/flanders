import random
from flanders import new_context, free_context, search_neighbors


def test_library():
    bounds = [-1.0, 1.0]
    num_points = 1000
    num_batches = 10
    assert num_points % num_batches == 0
    batch_length = int(num_points / num_batches)

    # generate random but reproducible data
    seed = 10
    random.seed(seed)

    points = [(random.uniform(bounds[0], bounds[1]), random.uniform(bounds[0], bounds[1])) for _ in range(num_points)]
    view_vectors = [(random.uniform(bounds[0], bounds[1]), random.uniform(bounds[0], bounds[1])) for _ in range(num_points)]
    angles_deg = [random.uniform(10.0, 20.0) for _ in range(num_points)]
    coordinates = [(random.uniform(bounds[0], bounds[1]), random.uniform(bounds[0], bounds[1])) for _ in range(num_points)]

    context = new_context(num_points=num_points, points=points)

    # verify results without angles
    for batch in range(num_batches):
        i = batch*batch_length
        j = batch*batch_length + batch_length
        ref_indices = list(range(i, j))
        indices_fast = search_neighbors(context=context,
                                        ref_indices=ref_indices)
        indices_naive = search_neighbors(context=context,
                                         ref_indices=ref_indices,
                                         naive=True)
        assert indices_fast == indices_naive

    # compare pointwise vs. batched
    for batch in range(num_batches):
        i = batch*batch_length
        j = batch*batch_length + batch_length
        ref_indices = list(range(i, j))
        indices_batch = search_neighbors(context=context,
                                         ref_indices=ref_indices)
        indices_pointwise = [search_neighbors(context=context, ref_indices=[i])[0] for i in ref_indices]
        assert indices_batch == indices_pointwise

    # verify results with angles
    for batch in range(num_batches):
        i = batch*batch_length
        j = batch*batch_length + batch_length
        ref_indices = list(range(i, j))
        indices_fast = search_neighbors(context=context,
                                        ref_indices=ref_indices,
                                        view_vectors=view_vectors[i:j],
                                        angles_deg=angles_deg[i:j])
        indices_naive = search_neighbors(context=context,
                                         ref_indices=ref_indices,
                                         view_vectors=view_vectors[i:j],
                                         angles_deg=angles_deg[i:j],
                                         naive=True)
        assert indices_fast == indices_naive

        # verify results with free-style coordinates
        indices_fast = search_neighbor(context,
                                       coordinates=coordinates[i:j],
                                       view_vectors=view_vectors[i:j],
                                       angles_deg=angles_deg[i:j])
        indices_naive = search_neighbor(context,
                                        coordinates=coordinates[i:j],
                                        view_vectors=view_vectors[i:j],
                                        angles_deg=angles_deg[i:j],
                                        naive=True)
        assert indices_fast == indices_naive

    free_context(context)
