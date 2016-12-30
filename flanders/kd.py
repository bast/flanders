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
        from distance import get_distance
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
            self.children[position] = BinaryTree(coordinates=coordinates,
                                                 index=index,
                                                 parent=self,
                                                 split_dimension=d)
        else:
            # child position is full, pass creation on to child
            self.children[position].insert(coordinates, index)

    def guess_node(self, p, i):
        position = self.get_position(p)
        if self.children[position] is None:
            # child position is vacant
            return self
        else:
            # child position is full
            return self.children[position].guess_node(p, i)


def draw_tree(tree, ax):
    from draw import draw_point, draw_arrow
    if tree is not None:
        p = tree.get_coordinates()
        index = tree.get_index()
        draw_point(p, index, ax)
        for child in tree.get_children():
            draw_tree(child, ax)
            draw_arrow(p, child.get_coordinates(), ax)


def traverse(node,
             ref_index,
             ref_point,
             index,
             distance,
             indices_traversed,
             view_vector,
             view_angle):
    from angle import point_within_view_angle

    i = node.get_index()
    if i in indices_traversed:
        # in case we have already checked this node, we return
        return index, distance, indices_traversed
    else:
        indices_traversed.add(i)

    d = node.get_distance_to_node(ref_point)

    use_angles = False
    if view_vector is not None:
        if view_angle is not None:
            use_angles = True

    # we need to make sure that we skip the node which is the reference point
    if i != ref_index:
        is_in_view = True
        if use_angles:
            is_in_view = point_within_view_angle(point=node.coordinates,
                                                 view_origin=ref_point,
                                                 view_vector=view_vector,
                                                 view_angle=view_angle)
        if is_in_view:
            if d < distance:
                index = i
                distance = d

    ref_to_split = node.get_signed_distance_to_split(ref_point)

    for child in node.get_children():
        child_to_split = node.get_signed_distance_to_split(child.get_coordinates())
        # only consider child if radius is larger than distance to split line
        # or if it is smaller, then only consider the child on the same side as the reference point
        if (abs(ref_to_split) < distance) or (ref_to_split*child_to_split > 0.0):
            index, distance, indices_traversed = traverse(child,
                                                          ref_index,
                                                          ref_point,
                                                          index,
                                                          distance,
                                                          indices_traversed,
                                                          view_vector,
                                                          view_angle)

    parent = node.get_parent()
    if parent is None:
        # we have reached the root so we are done
        return index, distance, indices_traversed
    else:
        # we go one level up
        return traverse(parent,
                        ref_index,
                        ref_point,
                        index,
                        distance,
                        indices_traversed,
                        view_vector,
                        view_angle)


def get_neighbor_index(ref_index,
                       points,
                       tree,
                       view_vector=None,
                       view_angle=None):
    """
    Returns index of nearest point to points[ref_index].
    By default, only the distance counts. If angle and view vector
    are both not None, they are taken into account.
    In the latter case it is possible that nearest neighbor exists,
    and in this case the function returns -1.
    """
    from sys import float_info

    ref_point = points[ref_index]
    node = tree.guess_node(ref_point, ref_index)

    index = -1

    index, _distance, _indices_traversed = traverse(node=node,
                                                    ref_index=ref_index,
                                                    ref_point=ref_point,
                                                    index=index,
                                                    distance=float_info.max,
                                                    indices_traversed=set(),
                                                    view_vector=view_vector,
                                                    view_angle=view_angle)

#   print('nearest with index {0} and distance {1} after {2} steps'.format(index, distance, len(indices_traversed)))

    return index
