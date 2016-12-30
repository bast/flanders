def point_within_view_angle(point, view_origin, view_vector, view_angle):
    """
    Check whether point is in view described by view_origin, view_vector,
    and view_angle.
    """
    from normalize import normalize
    from math import acos, pi

    vn = normalize(view_vector, 1.0)
    vp = normalize((point[0] - view_origin[0], point[1] - view_origin[1]), 1.0)

    angle_rad = acos(vn[0]*vp[0] + vn[1]*vp[1])
    angle_deg = angle_rad*180.0/pi

    return abs(angle_deg) <= abs(view_angle/2.0)


def test_point_within_view_angle():

    view_origin = (0.0, 0.0)
    view_vector = (1.0, 1.0)

    point = (10.0, 0.0)
    assert point_within_view_angle(point, view_origin, view_vector, 90.001)
    assert not point_within_view_angle(point, view_origin, view_vector, 89.999)

    point = (10.0, -0.1)
    assert not point_within_view_angle(point, view_origin, view_vector, 90.0)


def rotate(v, angle_deg):
    """
    Rotate vector v by angle_deg.
    """
    from math import cos, sin, pi

    (x, y) = v

    angle_rad = angle_deg*pi/180.0

    _x = x*cos(angle_rad) - y*sin(angle_rad)
    _y = x*sin(angle_rad) + y*cos(angle_rad)

    return (_x, _y)
