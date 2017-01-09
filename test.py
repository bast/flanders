def test_library():
    from sys import float_info
    import time
    import random
    import cpp_interface

    x0 = -1.0
    x1 = 1.0
    y0 = x0
    y1 = x1
    num_points = 500
    do_timing = False

    # generate random but reproducible data
    seed = 10
    random.seed(seed)
    points = [(random.uniform(x0, x1), random.uniform(y0, y1)) for _ in range(num_points)]
    view_vectors = [(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)) for _ in range(num_points)]
    view_angles = [random.uniform(30.0, 80.0) for _ in range(num_points)]

    x_coordinates = [point[0] for point in points]
    y_coordinates = [point[1] for point in points]

    bounds = [
        [float_info.max, float_info.min],
        [float_info.max, float_info.min],
    ]

    for point in points:
        bounds[0][0] = min(bounds[0][0], point[0])
        bounds[0][1] = max(bounds[0][1], point[0])
        bounds[1][0] = min(bounds[1][0], point[1])
        bounds[1][1] = max(bounds[1][1], point[1])

    context = cpp_interface.new_context(num_points, bounds)
    for i, point in enumerate(points):
        _point = [point[0], point[1]]
        cpp_interface.insert(context, _point, i)

    # verify results without and with angles
    for use_angles in [False, True]:
        t0 = time.time()
        for i, point in enumerate(points):
            if not do_timing:
                index_naive = cpp_interface.find_neighbor_naive(i,
                                                                len(points),
                                                                x_coordinates,
                                                                y_coordinates,
                                                                use_angles,
                                                                [view_vectors[i][0], view_vectors[i][1]],
                                                                view_angles[i])
            index = cpp_interface.find_neighbor(context,
                                                i,
                                                use_angles,
                                                [view_vectors[i][0], view_vectors[i][1]],
                                                view_angles[i])

        if do_timing:
            print('\nuse_angles: {0}'.format(use_angles))
            print('time used: {0}'.format(time.time() - t0))
        else:
            assert index_naive == index

    cpp_interface.free_context(context)
