def main():
    import matplotlib.pyplot as plt
    import sys
    import time
    import random
    from kd import BinaryTree, get_neighbor_index, draw_tree
    from naive import get_neighbor_index_naive

    x0 = -1.0
    x1 = 1.0
    y0 = x0
    y1 = x1
    num_points = 250

    seed = 1
    random.seed(seed)

#   plot = True
    plot = False
    if plot:
        fig, ax = plt.subplots()
    else:
        ax = None

    points = [(random.uniform(x0, x1), random.uniform(y0, y1)) for _ in range(num_points)]
    view_vectors = [(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)) for _ in range(num_points)]
    view_angles = [random.uniform(30.0, 80.0) for _ in range(num_points)]

    tree = BinaryTree(coordinates=points[0], index=0, parent=None, split_dimension=0)
    for i, point in enumerate(points):
        if i > 0:
            tree.insert(point, i)

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
    for i, point in enumerate(points):
        index_naive = get_neighbor_index_naive(ref_index=i,
                                               points=points,
                                               view_vector=view_vectors[i],
                                               view_angle=view_angles[i])
    print('time used in naive:', time.time() - t0)

    # time tree approach
    t0 = time.time()
    for i, point in enumerate(points):
        index = get_neighbor_index(ref_index=i,
                                   points=points,
                                   tree=tree,
                                   view_vector=view_vectors[i],
                                   view_angle=view_angles[i])
    print('time used in kd-tree:', time.time() - t0)

    if plot:
        draw_tree(tree, ax)
        plt.show()


if __name__ == '__main__':
    main()
