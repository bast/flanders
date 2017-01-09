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

    seed = 10
    random.seed(seed)

    points = [(random.uniform(x0, x1), random.uniform(y0, y1)) for _ in range(num_points)]

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

    context = cpp_interface.new_context()
    cpp_interface.set_bounds(context, bounds)
    for i, point in enumerate(points):
        _point = [point[0], point[1]]
        cpp_interface.insert(context, _point, i)

    # verify results without angles
    for i, point in enumerate(points):
        _not_used = 0.0
        index_naive = cpp_interface.find_neighbor_naive(i,
                                                             len(points),
                                                             x_coordinates,
                                                             y_coordinates,
                                                             False,
                                                             [_not_used, _not_used],
                                                             _not_used)
        index = cpp_interface.find_neighbor(context,
                                                 [point[0], point[1]],
                                                 i,
                                                 False,
                                                 [_not_used, _not_used],
                                                 _not_used)
        assert index_naive == index

    view_vectors = [(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)) for _ in range(num_points)]
    view_angles = [random.uniform(30.0, 80.0) for _ in range(num_points)]

    # verify results with angles
    for i, point in enumerate(points):
        index_naive = cpp_interface.find_neighbor_naive(i,
                                                             len(points),
                                                             x_coordinates,
                                                             y_coordinates,
                                                             True,
                                                             [view_vectors[i][0], view_vectors[i][1]],
                                                             view_angles[i])
        index = cpp_interface.find_neighbor(context,
                                                 [point[0], point[1]],
                                                 i,
                                                 True,
                                                 [view_vectors[i][0], view_vectors[i][1]],
                                                 view_angles[i])

        assert index_naive == index

    cpp_interface.free_context(context)
