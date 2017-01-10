import matplotlib.pyplot as plt
import glob


def extract_data(file_name):
    xs = []
    ys = []
    with open(file_name, 'r') as f:
        for i, line in enumerate(f):
            if i > 2:
                s = line.split()
                xs.append(float(s[0]))
                ys.append(float(s[1]))
    return xs, ys


def add_plot(file_name, style):
    xs, ys = extract_data(file_name)
    plt.plot(xs, ys, style)


for f in glob.glob('data/*.txt'):
    add_plot(f, 'r-')

plt.show()
