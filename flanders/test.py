def main():
    import matplotlib.pyplot as plt
    import sys
    import time
    from kd import get_points, BinaryTree, get_all_distances_naive, find_neighbor, draw_tree

    x0 = -1.0
    x1 = 1.0
    y0 = x0
    y1 = x1
    num_points = 50
    seed = 1
    plot = True

    points = get_points(num_points, x0, x1, y0, y1, seed)

    tree = BinaryTree(coordinates=points[0], index=0, parent=None, split_dimension=0)
    for i, point in enumerate(points):
        if i > 0:
            tree.insert(point, i)

    if plot:
        fig, ax = plt.subplots()
    else:
        ax = None

    ref_points = get_points(num_points, x0, x1, y0, y1, seed + 1)

    t0 = time.time()
    distances_naive = get_all_distances_naive(ref_points, points)
    print('time used in naive:', time.time() - t0)

    t0 = time.time()
    distances = []
    for point in ref_points:
        index, distance = find_neighbor(point, tree, ax, plot=plot)
        distances.append(distance)
    print('time used in kd-tree:', time.time() - t0)

    for i, distance in enumerate(distances):
        if abs(distance - distances_naive[i]) > 1.0e-7:
            sys.stderr.write('ERROR\n')
            sys.exit(1)

    print('all fine')

    if plot:
        draw_tree(tree, ax)
        plt.show()


if __name__ == '__main__':
    main()
