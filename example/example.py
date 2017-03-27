import flanders

points = [(60.4, 51.3), (173.9, 143.8), (132.9, 124.9), (19.5, 108.9), (196.5, 9.9), (143.3, 53.3)]

num_points = len(points)

context = flanders.new_context(num_points, points)

indices = flanders.search_neighbor(context,
                                   coordinates=[(119.2, 59.7), (155.2, 30.2)],
                                   view_vectors=[(0.0, 1.0), (-1.0, -1.0)],
                                   angles_deg=[90.0, 90.0])

assert indices == [2, -1]

indices = flanders.search_neighbor(context,
                                   ref_indices=range(num_points),
                                   view_vectors=[(1.0, 1.0) for _ in xrange(num_points)],
                                   angles_deg=[90.0 for _ in xrange(num_points)])

assert indices == [2, 2, -1, 2, 1, 2]

flanders.free_context(context)
