def debug():
    from sys import float_info
    import random
    from flanders.kd import BinaryTree, get_neighbor_index
    from flanders.angle import rotate
    from flanders.normalize import normalize

    x0 = -1.0
    x1 = 1.0
    y0 = x0
    y1 = x1
    num_points = 5

    seed = 10
    random.seed(seed)

    points = [(random.uniform(x0, x1), random.uniform(y0, y1)) for _ in range(num_points)]

    bounds = [
        [float_info.max, float_info.min],
        [float_info.max, float_info.min],
    ]

    for point in points:
        bounds[0][0] = min(bounds[0][0], point[0])
        bounds[0][1] = max(bounds[0][1], point[0])
        bounds[1][0] = min(bounds[1][0], point[1])
        bounds[1][1] = max(bounds[1][1], point[1])

    print('bounds', bounds)
    print('root', points[0])

    tree = BinaryTree(coordinates=points[0],
                      index=0,
                      parent=None,
                      split_dimension=0,
                      bounds=bounds)

    for i, point in enumerate(points):
        if i > 0:
            tree.insert(point, i, debug=True)

    node = tree.guess_node((0.3, -0.8))
    print('guess:', node.index)


if __name__ == '__main__':
    debug()
