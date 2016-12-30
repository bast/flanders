def main():
    import matplotlib.pyplot as plt
    import sys
    import time
    from kd import get_points, BinaryTree, get_neighbor_index_naive, get_neighbor_index, draw_tree

    x0 = -1.0
    x1 = 1.0
    y0 = x0
    y1 = x1
    num_points = 50
    seed = 1

#   plot = True
    plot = False
    if plot:
        fig, ax = plt.subplots()
    else:
        ax = None

    points = get_points(num_points, x0, x1, y0, y1, seed)

    tree = BinaryTree(coordinates=points[0], index=0, parent=None, split_dimension=0)
    for i, point in enumerate(points):
        if i > 0:
            tree.insert(point, i)

    ref_points = get_points(num_points, x0, x1, y0, y1, seed + 1)

    # first we verify results
    for ref_point in ref_points:
        index_naive = get_neighbor_index_naive(ref_point, points)
        index = get_neighbor_index(ref_point, tree, ax, plot=plot)
        assert index_naive == index

    # then we run timings
    t0 = time.time()
    for ref_point in ref_points:
        index_naive = get_neighbor_index_naive(ref_point, points)
    print('time used in naive:', time.time() - t0)

    t0 = time.time()
    for ref_point in ref_points:
        index = get_neighbor_index(ref_point, tree, ax, plot=plot)
    print('time used in kd-tree:', time.time() - t0)

    if plot:
        draw_tree(tree, ax)
        plt.show()


if __name__ == '__main__':
    main()
