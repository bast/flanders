from flanders import new_context, free_context, search_neighbor
import numpy as np

x_coordinates = [60.4, 173.9, 132.9, 19.5, 196.5, 143.3]
y_coordinates = [51.3, 143.8, 124.9, 108.9, 9.9, 53.3]

num_points = len(x_coordinates)

context = new_context(num_points, np.array(x_coordinates), np.array(y_coordinates))

x = [119.2, 155.2]
y = [59.7, 30.2]
vx = [0.0, -1.0]
vy = [1.0, -1.0]
angles_deg = [90.0, 90.0]

indices_fast = search_neighbor(context,
                               x=x,
                               y=y,
                               vx=vx,
                               vy=vy,
                               angles_deg=angles_deg)

assert indices_fast == [2, -1]

free_context(context)
