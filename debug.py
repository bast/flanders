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

    view_vectors = [(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)) for _ in range(num_points)]
    view_angles = [random.uniform(30.0, 80.0) for _ in range(num_points)]

    for i in [1, 2]:
        index = get_neighbor_index(ref_index=i,
                                   points=points,
                                   tree=tree,
                                   view_vector=view_vectors[i],
                                   view_angle=view_angles[i])
        print()
        print('vector={0} angle={1}'.format(view_vectors[i], view_angles[i]))
        print('point={0} nearest={1}'.format(i, index))

if __name__ == '__main__':
    debug()
