def rotate(v, angle_deg):
    from math import cos, sin, pi
    (x, y) = v
    angle_rad = angle_deg*pi/180.0
    _x = x*cos(angle_rad) - y*sin(angle_rad)
    _y = x*sin(angle_rad) + y*cos(angle_rad)
    return (_x, _y)


def normalize(v, s):
    """
    Normalize vector to length s.
    """
    from math import sqrt
    length = sqrt(v[0]**2 + v[1]**2)
    return (s*v[0]/length, s*v[1]/length)


def get_intersection_point(p1, p2, r, v):
    """
    From the reference point r there is a ray with vector v.
    This function finds the intersection point u between the ray
    and a line p1-p2. If no point is found, function returns None.
    """
    from numpy import sign

    r2 = (r[0] + v[0], r[1] + v[1])
    ray = line_coeffs_from_two_points(r, r2)

    line = line_coeffs_from_two_points(p1, p2)
    (a, b, c) = get_intersection(line, ray)

    TINY = 1.0e-20
    if abs(c) < TINY:
        return None

    u = (a/c, b/c)

    # check whether intersection is in the direction of the ray
    if sign(u[0] - r[0]) != sign(v[0]):
        return None
    if sign(u[1] - r[1]) != sign(v[1]):
        return None

    # check whether intersection is not outside line bounds
    for dim in [0, 1]:
        _min = min(p1[dim], p2[dim])
        _max = max(p1[dim], p2[dim])
        if abs(_max - _min) > TINY:
            if min(u[dim], _min) == u[dim]:
                return None
            if max(u[dim], _max) == u[dim]:
                return None

    return u


def get_intersection(u1, u2):
    """
    Return line-line intersection using homogeneous coordinates.
    """
    (a1, b1, c1) = u1
    (a2, b2, c2) = u2

    a = b1*c2 - b2*c1
    b = c1*a2 - c2*a1
    c = a1*b2 - a2*b1

    return (a, b, c)


def test_get_intersection():
    u1 = (1.0, 2.0, 3.0)
    u2 = (-3.0, -2.0, -1.0)
    a, b, c = get_intersection(u1, u2)
    assert (a, b, c) == (4.0, -8.0, 4.0)


def line_coeffs_from_two_points(p1, p2):
    """
    Find (a, b, c) in ax + bx + c = 0 from two points on that line.
    """
    (x1, y1) = p1
    (x2, y2) = p2
    a = y1 - y2
    b = x2 - x1
    c = (x1 - x2)*y1 + (y2 - y1)*x1
    return (a, b, c)


def test_line_coeffs_from_two_points():
    p1 = (1.0, 2.0)
    p2 = (3.0, -5.0)
    a, b, c = line_coeffs_from_two_points(p1, p2)
    assert (a, b, c) == (7.0, 2.0, -11.0)


def main():
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from draw import draw_point, draw_arrow
    import random

    x0 = -1.0
    x1 = 1.0
    y0 = x0
    y1 = x1

    angle = 10.0

    # dividing lines
    xd = 0.2
    yd = 0.3

    fig, ax = plt.subplots()

    # draw dividing lines
    ax.plot((x0, x1), (yd, yd), color='red')
    ax.plot((xd, xd), (y0, y1), color='red')

    # we draw the bounding box which represents
    # the simulation box
    ax.add_patch(
        patches.Rectangle(
            (x0, y0),
            x1 - x0,
            y1 - y0,
            fill=False
        )
    )

    seed = 2
    random.seed(seed)

    for i in range(20):

        r = (random.uniform(x0, x1), random.uniform(y0, y1))
        draw_point(r, 'r{0}'.format(i), ax)

        vn = (random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))
        vn = normalize(vn, 1.0)

        v1 = rotate(vn, -angle)
        v2 = rotate(vn, angle)

        for v in [v1, v2]:
            ax.plot((r[0], r[0] + v[0]), (r[1], r[1] + v[1]), color='blue')
            for (p1, p2) in [((xd, y0), (xd, y1)), ((x0, yd), (x1, yd))]:
                u = get_intersection_point(p1, p2, r, v)
                if u is not None:
                    draw_point(u, 'u{0}'.format(i), ax)

    plt.show()


if __name__ == '__main__':
    main()
