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


def draw_point(point, text, ax):
    x, y = point
    ax.scatter([x], [y])
    ax.annotate(' {0}'.format(text), (x, y))


def draw_arrow(point1, point2, ax):
    x1, y1 = point1
    x2, y2 = point2
    u = x2 - x1
    v = y2 - y1
    x1 += 0.1*u
    y1 += 0.1*v
    u *= 0.8
    v *= 0.8
    ax.arrow(x1, y1, u, v, head_width=0.03, head_length=0.05, fc='k', ec='k')


def main():
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    x0 = -1.0
    x1 = 1.0
    y0 = x0
    y1 = x1

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

    import random
    seed = 2
    random.seed(seed)

    for i in range(20):

        r = (random.uniform(x0, x1), random.uniform(y0, y1))
        draw_point(r, 'r{0}'.format(i), ax)

        v = (random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))
        v = normalize(v, 0.1)
        draw_arrow(r, (r[0] + v[0], r[1] + v[1]), ax)

        u = get_intersection_point(p1=(xd, y0), p2=(xd, y1), r=r, v=v)
        if u is not None:
            draw_point(u, 'u{0}'.format(i), ax)

        u = get_intersection_point(p1=(x0, yd), p2=(x1, yd), r=r, v=v)
        if u is not None:
            draw_point(u, 'u{0}'.format(i), ax)

    plt.show()


if __name__ == '__main__':
    main()
