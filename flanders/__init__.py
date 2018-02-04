import os
from cffi import FFI
from .cffi_helpers import get_lib_handle
import numpy as np


_this_path = os.path.dirname(os.path.realpath(__file__))

_library_dir = os.getenv('FLANDERS_LIBRARY_DIR')
if _library_dir is None:
    _library_dir = os.path.join(_this_path, 'lib')

_include_dir = os.getenv('FLANDERS_INCLUDE_DIR')
if _include_dir is None:
    _include_dir = os.path.join(_this_path, 'include')

_lib = get_lib_handle(
    ['-DFLANDERS_API='],
    'flanders.h',
    'flanders',
    _library_dir,
    _include_dir
)


# outward facing API

def new_context(num_points, points):

    x_coordinates, y_coordinates = zip(*points)

    # cast a pointer which points to the numpy array data
    # we work with numpy because tree initialization with normal lists segfault
    # for lists longer than ca. 0.5 million points
    ffi = FFI()

    x_coordinates_np = np.array(x_coordinates)
    x_coordinates_p = ffi.cast("double *", x_coordinates_np.ctypes.data)

    y_coordinates_np = np.array(y_coordinates)
    y_coordinates_p = ffi.cast("double *", y_coordinates_np.ctypes.data)

    return _lib.new_context(num_points,
                            x_coordinates_p,
                            y_coordinates_p)


free_context = _lib.free_context


def search_neighbors(context,
                     ref_indices=None,
                     coordinates=None,
                     view_vectors=None,
                     angles_deg=None,
                     naive=False):

    ffi = FFI()

    if ref_indices is None:
        num_indices = len(coordinates)
        x, y = zip(*coordinates)
        x_np = np.array(x)
        x_p = ffi.cast("double *", x_np.ctypes.data)
        y_np = np.array(y)
        y_p = ffi.cast("double *", y_np.ctypes.data)
    else:
        num_indices = len(ref_indices)

    indices_np = np.zeros(num_indices, dtype=np.int32)
    indices_p = ffi.cast("int *", indices_np.ctypes.data)

    if (view_vectors is None and angles_deg is None):
        use_angles = False
        vx_p = ffi.new("double *")
        vy_p = ffi.new("double *")
        angles_deg_p = ffi.new("double *")
    else:
        use_angles = True
        vx, vy = zip(*view_vectors)
        vx_np = np.array(vx)
        vx_p = ffi.cast("double *", vx_np.ctypes.data)
        vy_np = np.array(vy)
        vy_p = ffi.cast("double *", vy_np.ctypes.data)
        angles_deg_np = np.array(angles_deg)
        angles_deg_p = ffi.cast("double *", angles_deg_np.ctypes.data)

    if ref_indices is None:
        _lib.search_neighbors_by_coordinates(context,
                                             num_indices,
                                             indices_p,
                                             x_p,
                                             y_p,
                                             use_angles,
                                             vx_p,
                                             vy_p,
                                             angles_deg_p,
                                             naive)
    else:
        _lib.search_neighbor_by_indices(context,
                                        num_indices,
                                        indices_p,
                                        ref_indices,
                                        use_angles,
                                        vx_p,
                                        vy_p,
                                        angles_deg_p,
                                        naive)

    return indices_np.tolist()
