import matplotlib.pyplot as plt


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


add_plot('test1.txt', 'ro-')
add_plot('test2.txt', 'go-')
add_plot('test3.txt', 'bo-')

plt.show()
