def test_library():
    import time
    import random
    import cpp_interface
    import numpy as np
    from cffi import FFI

    bounds = [-1.0, 1.0]
    num_points = 1000
    do_timing = False

    x_coordinates = np.zeros(num_points, dtype=np.float64)
    y_coordinates = np.zeros(num_points, dtype=np.float64)

    # generate random but reproducible data
    seed = 10
    random.seed(seed)
    for i in range(num_points):
        x_coordinates[i] = random.uniform(bounds[0], bounds[1])
        y_coordinates[i] = random.uniform(bounds[0], bounds[1])

    # cast a pointer which points to the numpy array data
    # we work with numpy because tree initialization with normal lists segfault
    # for lists longer than ca. 0.5 million points
    ffi = FFI()
    x_coordinates_p = ffi.cast("double *", x_coordinates.ctypes.data)
    y_coordinates_p = ffi.cast("double *", y_coordinates.ctypes.data)

    t0 = time.time()
    context = cpp_interface.new_context(num_points, x_coordinates_p, y_coordinates_p)
    if do_timing:
        print('\ntime used building tree: {0}'.format(time.time() - t0))

    view_vectors = [(random.uniform(bounds[0], bounds[1]), random.uniform(bounds[0], bounds[1])) for _ in range(num_points)]
    view_angles = [random.uniform(30.0, 80.0) for _ in range(num_points)]

    # verify results without and with angles
    for use_angles in [False, True]:
        t0 = time.time()
        for i in range(num_points):
            index = cpp_interface.find_neighbor(context,
                                                i,
                                                use_angles,
                                                [view_vectors[i][0], view_vectors[i][1]],
                                                view_angles[i])

            if not do_timing:
                index_naive = cpp_interface.find_neighbor_naive(i,
                                                                num_points,
                                                                x_coordinates_p,
                                                                y_coordinates_p,
                                                                use_angles,
                                                                [view_vectors[i][0], view_vectors[i][1]],
                                                                view_angles[i])
                assert index_naive == index

        if do_timing:
            print('\nuse_angles: {0}'.format(use_angles))
            print('time used in search: {0}'.format(time.time() - t0))

    cpp_interface.free_context(context)
