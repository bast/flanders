

def get_points(num_points, x0, x1, y0, y1, seed):
    import random
    random.seed(seed)
    return [(random.uniform(x0, x1), random.uniform(y0, y1)) for _ in range(num_points)]


def get_distance_naive(point, other_points):
    import sys
    import math
    d = sys.float_info.max
    for other_point in other_points:
            _d = math.sqrt((other_point[0] - point[0])**2.0 + (other_point[1] - point[1])**2.0)
            if _d < d:
                d = _d
    return d


def get_all_distances_naive(points_a, points_b):
    return [get_distance_naive(point, points_b) for point in points_a]


def get_all_distances_kd(points_a, points_b):
    from scipy import spatial
    tree = spatial.KDTree(points_b)
    distances = []
    for point in points_a:
        distance_kd, _index = tree.query(point)
        distances.append(distance_kd)
    return distances


def main():
    import time

    x0 = 0.0
    x1 = 1.0
    y0 = x0
    y1 = x1
    num_points = 2000

    points_a = get_points(num_points, x0, x1, y0, y1, 1)
    points_b = get_points(num_points, x0, x1, y0, y1, 2)

    t0 = time.time()
    distances_naive = get_all_distances_naive(points_a, points_b)
    print('time used:', time.time() - t0)

    t0 = time.time()
    distances_kd = get_all_distances_kd(points_a, points_b)
    print('time used:', time.time() - t0)


if __name__ == "__main__":
    main()
