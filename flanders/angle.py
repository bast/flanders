def point_within_view_angle(r, v, p, angle):
    """
    Check whether point p is in view angle.
    View angle is enclosed by two rays from point r in the direction v
    enclosing a cone of 2*angle.
    """
    from normalize import normalize
    from math import acos, pi

    vn = normalize(v, 1.0)
    vp = normalize((p[0] - r[0], p[1] - r[1]), 1.0)

    a_rad = acos(vn[0]*vp[0] + vn[1]*vp[1])
    a_deg = a_rad*180.0/pi

    return abs(a_deg) <= abs(angle)


def test_point_within_view_angle():
    r = (0.0, 0.0)
    p = (100.0, 100.0)
    v = (0.0, 1.0)
    assert point_within_view_angle(r, v, p, 45.001)
    assert not point_within_view_angle(r, v, p, 44.999)
    p = (-100.0, 100.0)
    assert point_within_view_angle(r, v, p, 45.001)
    assert not point_within_view_angle(r, v, p, 44.999)
