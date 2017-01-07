class BinaryTree():

    def __init__(self,
                 coordinates,
                 index,
                 parent,
                 split_dimension,
                 bounds):
        self.children = [None, None]
        self.parent = parent
        self.coordinates = coordinates
        self.index = index
        self.split_dimension = split_dimension
        self.bounds = bounds

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
        from .distance import get_distance
        return get_distance(self.coordinates, coordinates)

    def get_position(self, coordinates):
        if self.get_signed_distance_to_split(coordinates) > 0.0:
            # insert "left"
            return 0
        else:
            # insert "right"
            return 1

    def insert(self, coordinates, index, debug=False):
        from copy import copy
        position = self.get_position(coordinates)
        if self.children[position] is None:
            # child position is vacant, create child
            if self.split_dimension == 0:
                d = 1
            else:
                d = 0

            new_bounds = [
                [self.bounds[0][0], self.bounds[0][1]],
                [self.bounds[1][0], self.bounds[1][1]],
            ]

            if position == 0:
                new_bounds[self.split_dimension][1] = self.coordinates[self.split_dimension]
            else:
                new_bounds[self.split_dimension][0] = self.coordinates[self.split_dimension]

            if debug:
                print('creating child coordinates={0}, index={1}, parent={2}, bounds={3}'.format(coordinates, index, self.index, new_bounds))

            self.children[position] = BinaryTree(coordinates=coordinates,
                                                 index=index,
                                                 parent=self,
                                                 split_dimension=d,
                                                 bounds=new_bounds)
        else:
            # child position is full, pass creation on to child
            self.children[position].insert(coordinates, index, debug)

    def guess_node(self, p):
        position = self.get_position(p)
        if self.children[position] is None:
            # child position is vacant
            return self
        else:
            # child position is full
            return self.children[position].guess_node(p)


def traverse(node,
             ref_index,
             ref_point,
             index,
             distance,
             indices_traversed,
             view_vector,
             view_angle):
    from .angle import point_within_view_angle
    from .intersections import get_num_intersections

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
        consider_child = False
        if (ref_to_split*child_to_split > 0.0):
            # child is on the same side as the reference point
            consider_child = True
        else:
            # child is on the other side
            if (abs(ref_to_split) < distance):
                # radius is larger than distance to split line
                if not use_angles:
                    consider_child = True
                else:
                    if i == ref_index:
                        # reference point is the node
                        # for simplicity we will consider both children
                        # TODO here a shortcut is possible
                        # for this check the sign of the vector component perpendicular to
                        # the dividing split, if both ray vector components have same sign and opposite
                        # sign that the child, then one could skip the child
                        consider_child = True
                    else:
                        # if at least one ray intersects the bounds, we consider the child
                        for (p1, p2) in [((node.bounds[0][0], node.bounds[1][0]), (node.bounds[0][1], node.bounds[1][0])),
                                         ((node.bounds[0][1], node.bounds[1][0]), (node.bounds[0][1], node.bounds[1][1])),
                                         ((node.bounds[0][1], node.bounds[1][1]), (node.bounds[0][0], node.bounds[1][1])),
                                         ((node.bounds[0][0], node.bounds[1][1]), (node.bounds[0][0], node.bounds[1][0]))]:
                            if not consider_child:
                                num_intersections = get_num_intersections(p1,
                                                                          p2,
                                                                          view_origin=ref_point,
                                                                          view_vector=view_vector,
                                                                          view_angle=view_angle)
                            if num_intersections > 0:
                                consider_child = True

                        # if there is no intersection, it is possible that the ray covers entire
                        # area, in this case all boundary points are in the view cone and
                        # it is enough to check whether one of the boundary points is in view
                        if not consider_child:
                            if point_within_view_angle((node.bounds[0][0], node.bounds[1][0]), ref_point, view_vector, view_angle):
                                consider_child = True
        if consider_child:
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
    In the latter case it is possible that no nearest neighbor exists,
    and in this case the function returns -1.
    """
    from sys import float_info

    ref_point = points[ref_index]
    node = tree.guess_node(ref_point)

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
