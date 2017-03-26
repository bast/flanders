import os
from cffi import FFI
from .cffi_helpers import get_lib_handle
import numpy as np


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
                    ref_indices=None,
                    x=None,
                    y=None,
                    vx=None,
                    vy=None,
                    angles_deg=None,
                    naive=False):

    ffi = FFI()

    if ref_indices is None:
        num_indices = len(x)
        x_np = np.array(x)
        x_p = ffi.cast("double *", x_np.ctypes.data)
        y_np = np.array(y)
        y_p = ffi.cast("double *", y_np.ctypes.data)
    else:
        num_indices = len(ref_indices)
        ref_indices_np = np.array(ref_indices)
        ref_indices_p = ffi.cast("int *", ref_indices_np.ctypes.data)

    indices_np = np.zeros(num_indices, dtype=np.int32)
    indices_p = ffi.cast("int *", indices_np.ctypes.data)

    if (vx is None and vy is None and angles_deg is None):
        use_angles = False
        vx_p = ffi.new("double *")
        vy_p = ffi.new("double *")
        angles_deg_p = ffi.new("double *")
    else:
        use_angles = True
        vx_np = np.array(vx)
        vx_p = ffi.cast("double *", vx_np.ctypes.data)
        vy_np = np.array(vy)
        vy_p = ffi.cast("double *", vy_np.ctypes.data)
        angles_deg_np = np.array(angles_deg)
        angles_deg_p = ffi.cast("double *", angles_deg_np.ctypes.data)

    if ref_indices is None:
        _lib.search_neighbor_xy(context,
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
        _lib.search_neighbor_index(context,
                                   num_indices,
                                   indices_p,
                                   ref_indices_p,
                                   use_angles,
                                   vx_p,
                                   vy_p,
                                   angles_deg_p,
                                   naive)

    return indices_np.tolist()
