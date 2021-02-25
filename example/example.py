import flanders


# as a first step we build the search tree
# we can later reuse the search tree many times

points = [
    (60.4, 51.3),
    (173.9, 143.8),
    (132.9, 124.9),
    (19.5, 108.9),
    (196.5, 9.9),
    (143.3, 53.3),
]

tree = flanders.build_search_tree(points)


# now we will search the indices of nearest neighbor points
# for two observer points

observer_coordinates = [(119.2, 59.7), (155.2, 30.2)]
view_vectors = [(0.0, 1.0), (-1.0, -1.0)]
view_angles_deg = [90.0, 90.0]

indices = flanders.nearest_indices_from_coordinates(
    tree, observer_coordinates, view_vectors, view_angles_deg
)

assert indices == [2, -1]


# instead of using observer coordinates, also the original
# points themselves can be observers and we can select them
# by their index

observer_indices = [0, 1, 2, 3, 4, 5]
view_vectors = [(1.0, 1.0) for _ in observer_indices]
view_angles_deg = [90.0 for _ in observer_indices]

indices = flanders.nearest_indices_from_indices(
    tree, observer_indices, view_vectors, view_angles_deg
)

assert indices == [5, -1, 1, 2, -1, 1]
