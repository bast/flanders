def draw_dividing_line(node, ax):
    if node is not None:
        if node.split_dimension == 0:
            p1 = (
                node.coordinates[0],
                node.bounds[1][0],
            )
            p2 = (
                node.coordinates[0],
                node.bounds[1][1],
            )
        else:
            p1 = (
                node.bounds[0][0],
                node.coordinates[1],
            )
            p2 = (
                node.bounds[0][1],
                node.coordinates[1],
            )
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='red')
    for child in node.get_children():
        draw_dividing_line(child, ax)


def main():
    import matplotlib.pyplot as plt
    import sys
    import time
    import random
    from kd import BinaryTree, get_neighbor_index
    from naive import get_neighbor_index_naive
    from sys import float_info
    from draw import draw_point
    from angle import rotate
    from normalize import normalize

    x0 = -1.0
    x1 = 1.0
    y0 = x0
    y1 = x1
    num_points = 400
    batch = 1

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

    # verify results without angles
    for i, point in enumerate(points):
        index_naive = get_neighbor_index_naive(i, points)
        index = get_neighbor_index(i, points, tree)
        assert index_naive == index

    # verify results with angles
    for i, point in enumerate(points):
        index_naive = get_neighbor_index_naive(ref_index=i,
                                               points=points,
                                               view_vector=view_vectors[i],
                                               view_angle=view_angles[i])
        index = get_neighbor_index(ref_index=i,
                                   points=points,
                                   tree=tree,
                                   view_vector=view_vectors[i],
                                   view_angle=view_angles[i])
        assert index_naive == index

    # time naive approach
    # there is extra overhead due to function level imports
    t0 = time.time()
    for i in range(len(points)//batch):
        index_naive = get_neighbor_index_naive(ref_index=i,
                                               points=points,
                                               view_vector=view_vectors[i],
                                               view_angle=view_angles[i])
    print('time used in naive:', batch*(time.time() - t0))

    # time tree approach
    t0 = time.time()
    for i in range(len(points)//batch):
        index = get_neighbor_index(ref_index=i,
                                   points=points,
                                   tree=tree,
                                   view_vector=view_vectors[i],
                                   view_angle=view_angles[i])
    print('time used in kd-tree:', batch*(time.time() - t0))


if __name__ == '__main__':
    main()
