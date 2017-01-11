import matplotlib.pyplot as plt
import glob
import math


def extract_data(file_name):
    points = []
    with open(file_name, 'r') as f:
        for i, line in enumerate(f):
            if i > 2:
                s = line.split()
                point = (float(s[0]), float(s[1]))
                points.append(point)
    return points


def normalize(vector, s):
    norm = math.sqrt(vector[0]**2.0 + vector[1]**2.0)
    return (s*vector[0]/norm, s*vector[1]/norm)


def get_normal_vectors(points):
    num_points = len(points)
    vectors = []
    for i in range(num_points):
        i_before = i - 1
        i_after = (i + 1)%num_points
        vector = (points[i_after][1] - points[i_before][1], -(points[i_after][0] - points[i_before][0]))
        vector = normalize(vector, 5000.0)
        vectors.append(vector)
    return vectors


def add_plot(file_name, style):
    points = extract_data(file_name)
    if len(points) > 3:  # for the moment cannot handle linear islands
        ax = plt.axes()
        vectors = get_normal_vectors(points)
        for i in range(len(points)):
            ax.arrow(points[i][0], points[i][1], vectors[i][0], vectors[i][1], head_width=0.1, head_length=0.1, fc='k', ec='k')
        (xs, ys) = zip(*points)
        plt.plot(xs, ys, style)


for f in glob.glob('*.txt'):
    add_plot(f, 'r-')


#axes = plt.gca()
#axes.set_xlim([-20.0, 0.0])
#axes.set_ylim([40.0, 60.0])
plt.show()
