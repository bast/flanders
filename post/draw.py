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
