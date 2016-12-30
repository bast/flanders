def get_points(num_points, x0, x1, y0, y1, seed):
    import random
    random.seed(seed)
    return [(random.uniform(x0, x1), random.uniform(y0, y1)) for _ in range(num_points)]


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
    from draw import draw_point, draw_arrow
    if tree is not None:
        p = tree.get_coordinates()
        index = tree.get_index()
        draw_point(p, index, ax)
        for child in tree.get_children():
            draw_tree(child, ax)
            draw_arrow(p, child.get_coordinates(), ax)


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


def get_neighbor_index(ref_point, tree, ax, plot):
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

    # for the moment we discard distance
#   return index, distance
    return index


def get_neighbor_index_naive(point, other_points):
    from sys import float_info
    from math import sqrt

    d = float_info.max
    index = None

    for i, other_point in enumerate(other_points):
        _d = sqrt((other_point[0] - point[0])**2.0 + (other_point[1] - point[1])**2.0)
        if _d < d:
            d = _d
            index = i

    return index
