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


def draw_dividing_line(node, ax):
    if node is not None:
        if node.split_dimension == 0:
            p1 = (
                node.coordinates[0],
                node.bounds[1][0],
            )
            p2 = (
                node.coordinates[0],
                node.bounds[1][1],
            )
        else:
            p1 = (
                node.bounds[0][0],
                node.coordinates[1],
            )
            p2 = (
                node.bounds[0][1],
                node.coordinates[1],
            )
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='red')
    for child in node.get_children():
        draw_dividing_line(child, ax)
