import sys
import os
from subprocess import Popen, PIPE
from cffi import FFI


def _get_library_suffix():
    if sys.platform == "darwin":
        return 'dylib'
    else:
        return 'so'


def _get_lib_handle(definitions, header, library, build_dir, include_dir):
    ffi = FFI()
    interface = Popen(['cc', '-E'] + definitions + [os.path.join(include_dir, header)],
                      stdout=PIPE).communicate()[0].decode("utf-8")
    ffi.cdef(interface)

    suffix = _get_library_suffix()
    lib = ffi.dlopen(os.path.join(build_dir, 'lib{0}.{1}'.format(library, suffix)))
    return lib


_this_path = os.path.dirname(os.path.realpath(__file__))

_build_dir = os.getenv('FLANDERS_BUILD_DIR')
if _build_dir is None:
    _build_dir = _this_path
else:
    _build_dir = os.path.join(_build_dir, 'lib')

_include_dir = _this_path

_lib = _get_lib_handle(
    ['-DCPP_INTERFACE_API=', '-DCPP_INTERFACE_NOINCLUDE'],
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
find_neighbor = _lib.find_neighbor


def find_neighbor_naive(ref_index,
                        num_points,
                        x_coordinates,
                        y_coordinates,
                        use_angles,
                        view_vector,
                        view_angle_deg):

    # cast a pointer which points to the numpy array data
    # we work with numpy because tree initialization with normal lists segfault
    # for lists longer than ca. 0.5 million points
    ffi = FFI()
    x_coordinates_p = ffi.cast("double *", x_coordinates.ctypes.data)
    y_coordinates_p = ffi.cast("double *", y_coordinates.ctypes.data)

    return _lib.find_neighbor_naive(ref_index,
                                    num_points,
                                    x_coordinates_p,
                                    y_coordinates_p,
                                    use_angles,
                                    view_vector,
                                    view_angle_deg)
