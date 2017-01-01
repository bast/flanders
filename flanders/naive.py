def get_neighbor_index_naive(ref_index,
                             points,
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
    from .distance import get_distance
    from .angle import point_within_view_angle

    use_angles = False
    if view_vector is not None:
        if view_angle is not None:
            use_angles = True

    ref_point = points[ref_index]

    d = float_info.max
    index = -1

    for i, point in enumerate(points):
        if i != ref_index:
            is_in_view = True
            if use_angles:
                is_in_view = point_within_view_angle(point=point,
                                                     view_origin=ref_point,
                                                     view_vector=view_vector,
                                                     view_angle=view_angle)
            if is_in_view:
                _d = get_distance(point, ref_point)
                if _d < d:
                    d = _d
                    index = i

    return index
