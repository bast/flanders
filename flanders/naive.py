def get_neighbor_index_naive(ref_index, points):
    """
    Returns index of nearest point to points[ref_index].
    """
    from sys import float_info
    from distance import get_distance

    d = float_info.max
    index = None

    ref_point = points[ref_index]

    for i, point in enumerate(points):
        if i != ref_index:
            _d = get_distance(point, ref_point)
            if _d < d:
                d = _d
                index = i

    return index
