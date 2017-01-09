def test_library():
    import time
    import random
    import cpp_interface

    bounds = [-1.0, 1.0]
    num_points = 500
    do_timing = False

    # generate random but reproducible data
    seed = 10
    random.seed(seed)
    x_coordinates = [random.uniform(bounds[0], bounds[1]) for _ in range(num_points)]
    y_coordinates = [random.uniform(bounds[0], bounds[1]) for _ in range(num_points)]
    view_vectors = [(random.uniform(bounds[0], bounds[1]), random.uniform(bounds[0], bounds[1])) for _ in range(num_points)]
    view_angles = [random.uniform(30.0, 80.0) for _ in range(num_points)]

    context = cpp_interface.new_context(num_points, x_coordinates, y_coordinates)

    for i in range(num_points):
        cpp_interface.insert(context,
                             x_coordinates[i],
                             y_coordinates[i],
                             i)

    # verify results without and with angles
    for use_angles in [False, True]:
        t0 = time.time()
        for i in range(num_points):
            index = cpp_interface.find_neighbor(context,
                                                i,
                                                use_angles,
                                                [view_vectors[i][0], view_vectors[i][1]],
                                                view_angles[i])

            if not do_timing:
                index_naive = cpp_interface.find_neighbor_naive(i,
                                                                num_points,
                                                                x_coordinates,
                                                                y_coordinates,
                                                                use_angles,
                                                                [view_vectors[i][0], view_vectors[i][1]],
                                                                view_angles[i])
                assert index_naive == index

        if do_timing:
            print('\nuse_angles: {0}'.format(use_angles))
            print('time used: {0}'.format(time.time() - t0))

    cpp_interface.free_context(context)
