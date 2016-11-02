def get_points(num_points, x0, x1, y0, y1, seed):
    import random
    random.seed(seed)
    return [(random.uniform(x0, x1), random.uniform(y0, y1)) for _ in range(num_points)]


def draw_point(point, text, ax):
    x, y = point
    ax.scatter([x], [y])
    ax.annotate(' {0}'.format(text), (x, y))


def draw_line(point1, point2, ax):
    x1, y1 = point1
    x2, y2 = point2
    u = x2 - x1
    v = y2 - y1
    x1 += 0.1*u
    y1 += 0.1*v
    u *= 0.8
    v *= 0.8
    ax.arrow(x1, y1, u, v, head_width=0.03, head_length=0.05, fc='k', ec='k')


def get_distance(p1, p2):
    import math
    return math.sqrt((p2[0] - p1[0])**2.0 + (p2[1] - p1[1])**2.0)


class BinaryTree():

    def __init__(self, coordinates, index, parent, split_dimension):
        self.children = [None, None]
        self.parent = parent
        self.coordinates = coordinates
        self.index = index
        self.split_dimension = split_dimension

    def get_coordinates(self):
        return self.coordinates

    def get_index(self):
        return self.index

    def get_children(self):
        return [child for child in self.children if child is not None]

    def get_parent(self):
        return self.parent

    def get_signed_distance_to_split(self, coordinates):
        return self.coordinates[self.split_dimension] - coordinates[self.split_dimension]

    def get_distance_to_node(self, coordinates):
        return get_distance(self.coordinates, coordinates)

    def get_position(self, coordinates):
        if self.get_signed_distance_to_split(coordinates) > 0:
            # insert "right"
            return 1
        else:
            # insert "left"
            return 0

    def insert(self, coordinates, index):
        position = self.get_position(coordinates)
        if self.children[position] is None:
            # child position is vacant, create child
            if self.split_dimension == 0:
                d = 1
            else:
                d = 0
            self.children[position] = BinaryTree(coordinates=coordinates, index=index, parent=self, split_dimension=d)
        else:
            # child position is full, pass creation on to child
            self.children[position].insert(coordinates, index)

    def guess_node(self, p):
        position = self.get_position(p)
        if self.children[position] is None:
            # child position is vacant
            return self
        else:
            # child position is full
            return self.children[position].guess_node(p)


def draw_tree(tree, ax):
    if tree is not None:
        p = tree.get_coordinates()
        index = tree.get_index()
        draw_point(p, index, ax)
        for child in tree.get_children():
            draw_tree(child, ax)
            draw_line(p, child.get_coordinates(), ax)


def traverse(node, ref_point, index, distance, indices_traversed):

    i = node.get_index()
    if i in indices_traversed:
        # in case we have already checked this node, we return
        return index, distance, indices_traversed
    else:
        indices_traversed.add(i)

    d = node.get_distance_to_node(ref_point)

    if d < distance:
        index = i
        distance = d

    ref_to_split = node.get_signed_distance_to_split(ref_point)

    for child in node.get_children():
        child_to_split = node.get_signed_distance_to_split(child.get_coordinates())
        # only consider child if radius is larger than distance to split line
        # or if it is smaller, then only consider the child on the same side as the reference point
        if (abs(ref_to_split) < distance) or (ref_to_split*child_to_split > 0.0):
            index, distance, indices_traversed = traverse(child, ref_point, index, distance, indices_traversed)

    parent = node.get_parent()
    if parent is None:
        # we have reached the root so we are done
        return index, distance, indices_traversed
    else:
        # we go one level up
        return traverse(parent, ref_point, index, distance, indices_traversed)


def find_neighbor(ref_point, tree, ax, plot):
    import sys

    node = tree.guess_node(ref_point)
    index, distance, indices_traversed = traverse(node=node,
                                                  ref_point=ref_point,
                                                  index=node.get_index(),
                                                  distance=sys.float_info.max,
                                                  indices_traversed=set())

#   print('nearest with index {0} and distance {1} after {2} steps'.format(index, distance, len(indices_traversed)))

    if plot:
        ax.scatter([ref_point[0]], [ref_point[1]], color='red')
        ax.annotate(' {0}'.format(index), ref_point)

    return index, distance


def get_distance_naive(point, other_points):
    import sys
    import math
    d = sys.float_info.max
    for other_point in other_points:
            _d = math.sqrt((other_point[0] - point[0])**2.0 + (other_point[1] - point[1])**2.0)
            if _d < d:
                d = _d
    return d


def get_all_distances_naive(points_a, points_b):
    return [get_distance_naive(point, points_b) for point in points_a]


def main():
    import matplotlib.pyplot as plt
    import sys
    import time

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
    print('time used:', time.time() - t0)

    t0 = time.time()
    distances = []
    for point in ref_points:
        index, distance = find_neighbor(point, tree, ax, plot=plot)
        distances.append(distance)
    print('time used:', time.time() - t0)

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
