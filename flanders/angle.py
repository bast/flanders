def point_within_view_angle(point, view_origin, view_vector, view_angle):
    """
    Check whether point is in view described by view_origin, view_vector,
    and view_angle.
    """
    from normalize import normalize
    from math import acos, pi

    vn = normalize(view_vector, 1.0)
    vp = normalize((point[0] - view_origin[0], point[1] - view_origin[1]), 1.0)

    a_rad = acos(vn[0]*vp[0] + vn[1]*vp[1])
    a_deg = a_rad*180.0/pi

    return abs(a_deg) <= abs(view_angle/2.0)


def test_point_within_view_angle():

    view_origin = (0.0, 0.0)
    view_vector = (0.0, 1.0)

    point = (100.0, 100.0)
    assert point_within_view_angle(point, view_origin, view_vector, 90.001)
    assert not point_within_view_angle(point, view_origin, view_vector, 89.999)

    point = (-100.0, 100.0)
    assert point_within_view_angle(point, view_origin, view_vector, 90.001)
    assert not point_within_view_angle(point, view_origin, view_vector, 89.999)
