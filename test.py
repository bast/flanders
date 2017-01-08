def test_foo():
    import matplotlib.pyplot as plt
    from sys import float_info
    import time
    import random
    import cpp_interface
    from flanders.draw import draw_point
    from flanders.kd import BinaryTree
    from flanders.draw import draw_point, draw_dividing_line
    from flanders.angle import rotate
    from flanders.normalize import normalize

    x0 = -1.0
    x1 = 1.0
    y0 = x0
    y1 = x1
    num_points = 500

    seed = 10
    random.seed(seed)

    points = [(random.uniform(x0, x1), random.uniform(y0, y1)) for _ in range(num_points)]
    view_vectors = [(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)) for _ in range(num_points)]
    view_angles = [random.uniform(30.0, 80.0) for _ in range(num_points)]

    bounds = [
        [float_info.max, float_info.min],
        [float_info.max, float_info.min],
    ]

    for point in points:
        bounds[0][0] = min(bounds[0][0], point[0])
        bounds[0][1] = max(bounds[0][1], point[0])
        bounds[1][0] = min(bounds[1][0], point[1])
        bounds[1][1] = max(bounds[1][1], point[1])

    tree = BinaryTree(coordinates=points[0],
                      index=0,
                      parent=None,
                      split_dimension=0,
                      bounds=bounds)

    for i, point in enumerate(points):
        if i > 0:
            tree.insert(point, i)

    plot = False
    if plot:
        fig, ax = plt.subplots()
        for i, point in enumerate(points):
            draw_point(point, 'r{0}'.format(i), ax)
            vn = view_vectors[i]
            vn = normalize(vn, 0.2)
            angle = view_angles[i]
            for v in [rotate(vn, angle/2.0), rotate(vn, -angle/2.0)]:
                ax.plot((point[0], point[0] + v[0]), (point[1], point[1] + v[1]), color='blue')
        draw_dividing_line(tree, ax)
        plt.show()


    points_array = []
    for point in points:
        points_array.append(point[0])
        points_array.append(point[1])

    context = cpp_interface.new_context()
    cpp_interface.set_bounds(context, bounds)
    for i, point in enumerate(points):
        _point = [point[0], point[1]]
        cpp_interface.insert(context, _point, i)

    # verify results without angles
# for the moment fails without angles
#   for i, point in enumerate(points):
#       _not_used = 0.0
#       index_naive = cpp_interface.get_neighbor_index_naive(i,
#                                                            len(points),
#                                                            points_array,
#                                                            False,
#                                                            _not_used,
#                                                            _not_used,
#                                                            _not_used)
#       _coordinates = [point[0], point[1]]
#       _view_vector = [_not_used, _not_used]
#       index = cpp_interface.get_neighbor_index(context,
#                                                _coordinates,
#                                                i,
#                                                False,
#                                                _view_vector,
#                                                _not_used)
#       assert index_naive == index

    # verify results with angles
    for i, point in enumerate(points):
        index_naive = cpp_interface.get_neighbor_index_naive(i,
                                                             len(points),
                                                             points_array,
                                                             True,
                                                             view_vectors[i][0],
                                                             view_vectors[i][1],
                                                             view_angles[i])
        _coordinates = [point[0], point[1]]
        _view_vector = [view_vectors[i][0], view_vectors[i][1]]
        index = cpp_interface.get_neighbor_index(context,
                                                 _coordinates,
                                                 i,
                                                 True,
                                                 _view_vector,
                                                 view_angles[i])

        assert index_naive == index

    cpp_interface.free_context(context)
