import os
from cffi import FFI
from .cffi_helpers import get_lib_handle


_this_path = os.path.dirname(os.path.realpath(__file__))

_build_dir = os.getenv('FLANDERS_BUILD_DIR')
if _build_dir is None:
    _build_dir = _this_path
else:
    _build_dir = os.path.join(_build_dir, 'lib')

_include_dir = _this_path

_lib = get_lib_handle(
    ['-DFLANDERS_API=', '-DCPP_INTERFACE_NOINCLUDE'],
    'flanders.h',
    'flanders',
    _build_dir,
    _include_dir
)


# outward facing API

def new_context(num_points,
                x_coordinates,
                y_coordinates):

    # cast a pointer which points to the numpy array data
    # we work with numpy because tree initialization with normal lists segfault
    # for lists longer than ca. 0.5 million points
    ffi = FFI()
    x_coordinates_p = ffi.cast("double *", x_coordinates.ctypes.data)
    y_coordinates_p = ffi.cast("double *", y_coordinates.ctypes.data)

    return _lib.new_context(num_points,
                            x_coordinates_p,
                            y_coordinates_p)


free_context = _lib.free_context


def search_neighbor(context,
                    x,
                    y,
                    view_vector=None,
                    view_angle_deg=None,
                    naive=False):
    if (view_vector is not None and view_angle_deg is not None):
        use_angles = True
    else:
        use_angles = False
        view_vector = [0.0, 0.0]
        view_angle_deg = 0.0
    return _lib.search_neighbor(context,
                                x,
                                y,
                                use_angles,
                                view_vector,
                                view_angle_deg,
                                naive)


def search_neighbor_by_index(context,
                             ref_index,
                             view_vector=None,
                             view_angle_deg=None,
                             naive=False):
    if (view_vector is not None and view_angle_deg is not None):
        use_angles = True
    else:
        use_angles = False
        view_vector = [0.0, 0.0]
        view_angle_deg = 0.0
    return _lib.search_neighbor_by_index(context,
                                         ref_index,
                                         use_angles,
                                         view_vector,
                                         view_angle_deg,
                                         naive)
